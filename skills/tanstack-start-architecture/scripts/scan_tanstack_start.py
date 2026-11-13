#!/usr/bin/env python3
"""Read-only triage of a TanStack Start project.

Reports installed versions, bundler and hosting signals, required files,
route and server-function inventory, and heuristic findings (pre-1.169 APIs,
module-scope QueryClient or env reads, CSRF gap in src/start.ts, plugin order).
Findings are leads to verify in the code, not proof of a bug.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".output", "dist", "build", ".nitro", ".tanstack",
    ".vinxi", ".wrangler", ".netlify", ".vercel", "coverage", ".cache",
}
SOURCE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mts", ".mjs"}

TRACKED_PACKAGES = [
    "@tanstack/react-start", "@tanstack/solid-start", "@tanstack/vue-start", "@tanstack/start",
    "@tanstack/react-router", "@tanstack/react-query", "@tanstack/react-router-ssr-query",
    "@tanstack/react-form", "@tanstack/react-form-start", "@tanstack/zod-adapter",
    "zod", "valibot", "arktype", "vite", "@rsbuild/core", "nitro", "@cloudflare/vite-plugin",
    "@netlify/vite-plugin-tanstack-start", "iron-session", "better-auth", "@clerk/tanstack-react-start",
    "vinxi", "react", "typescript", "elysia", "@elysia/eden", "@elysiajs/eden", "hono",
]

# (id, regex, severity, message)
LEGACY_PATTERNS = [
    ("input-validator", re.compile(r"\.inputValidator\s*\("), "error",
     ".inputValidator() was renamed .validator() in 1.169"),
    ("use-session", re.compile(r"\buseSession\b"), "error",
     "useSession was removed in 1.169; use a session library"),
    ("register-global-middleware", re.compile(r"\bregisterGlobalMiddleware\b"), "error",
     "registerGlobalMiddleware is gone; use createStart() in src/start.ts"),
    ("legacy-api-route", re.compile(r"\bcreate(?:API|Server)FileRoute\b"), "error",
     "legacy API route helper; use createFileRoute(path)({ server: { handlers } })"),
    ("vinxi", re.compile(r"from\s+['\"]vinxi"), "error",
     "Vinxi-era import; current Start builds with the Vite or Rsbuild plugin"),
    ("old-start-package", re.compile(r"from\s+['\"]@tanstack/start['\"/]"), "error",
     "old @tanstack/start package; use @tanstack/react-start"),
    ("nitro-v2-plugin", re.compile(r"@tanstack/nitro-v2-vite-plugin"), "error",
     "Nitro v2 plugin removed; use nitro() from nitro/vite"),
]
VERSION_RE = re.compile(r"(\d+)\.(\d+)")
SET_COOKIE_HEADER = re.compile(r"setResponseHeaders?\s*\(\s*['\"]set-cookie", re.I)
MODULE_QUERY_CLIENT = re.compile(r"^(?:export\s+)?(?:const|let|var)\s+\w+\s*=\s*new\s+QueryClient\s*\(")
MODULE_ENV_READ = re.compile(r"^(?:export\s+)?(?:const|let|var)\s+[^=]+=.*\bprocess\.env\b")
SERVER_FN = re.compile(r"\bcreateServerFn\s*\(")
SERVER_ONLY_FN = re.compile(r"\bcreateServerOnlyFn\s*\(")
SERVER_HANDLERS = re.compile(r"\bserver\s*:\s*\{[\s\S]{0,400}?\bhandlers\b")
PROCESS_ENV = re.compile(r"\bprocess\.env\b")
EDEN_LOCALHOST = re.compile(r"treaty\s*<[^>]*>\s*\(\s*['\"`](?:https?://)?(?:localhost|127\.0\.0\.1)")
API_MOUNT = re.compile(r"\.(?:handle|fetch)\s*\(\s*\w*[rR]equest\b")
HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def load_package(root: Path) -> dict:
    try:
        data = json.loads(read_text(root / "package.json") or "{}")
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def find_catalog(root: Path) -> dict[str, str]:
    """Default dependency catalog of the enclosing workspace (Bun package.json or pnpm-workspace.yaml)."""
    for folder in [root, *list(root.parents)[:4]]:
        data = load_package(folder)
        workspaces = data.get("workspaces")
        for holder in (data, workspaces if isinstance(workspaces, dict) else {}):
            if isinstance(holder.get("catalog"), dict):
                return {k: str(v) for k, v in holder["catalog"].items()}
        pnpm = read_text(folder / "pnpm-workspace.yaml")
        block = re.search(r"(?m)^catalog:\s*\n((?:[ \t]+.+\n?)+)", pnpm)
        if block:
            pairs = re.findall(r"^[ \t]+['\"]?([^'\":]+)['\"]?\s*:\s*['\"]?([^'\"\s#]+)", block.group(1), re.M)
            return dict(pairs)
    return {}


def first_existing(root: Path, names: list[str]) -> Path | None:
    for name in names:
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def iter_sources(src: Path, limit: int):
    count = 0
    for path in src.rglob("*"):
        if count >= limit:
            return
        if any(part in SKIP_DIRS for part in path.relative_to(src).parts):
            continue
        if path.is_file() and path.suffix in SOURCE_SUFFIXES and not path.name.endswith(".gen.ts"):
            count += 1
            yield path


def scan(root: Path, src_dir: str, max_files: int) -> dict:
    pkg = load_package(root)
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    if any(str(spec) == "catalog:" for spec in deps.values()):
        catalog = find_catalog(root)
        deps = {name: catalog.get(name, spec) if str(spec) == "catalog:" else spec for name, spec in deps.items()}
    versions ={name: deps[name] for name in TRACKED_PACKAGES if name in deps}
    is_start = any(name in deps for name in ("@tanstack/react-start", "@tanstack/solid-start", "@tanstack/vue-start", "@tanstack/start"))

    findings: list[dict] = []

    def add(fid: str, severity: str, message: str, file: str | None = None, line: int | None = None):
        findings.append({k: v for k, v in {"id": fid, "severity": severity, "message": message, "file": file, "line": line}.items() if v is not None})

    start_spec = next((deps[n] for n in ("@tanstack/react-start", "@tanstack/solid-start") if n in deps), "")
    match = VERSION_RE.search(start_spec)
    if match and (int(match.group(1)), int(match.group(2))) < (1, 169):
        add("pre-stable-version", "warn", f"Start {start_spec} predates the 1.169 stable release; check references/version-notes.md before using current APIs", "package.json")

    src = root / src_dir
    vite_cfg = first_existing(root, ["vite.config.ts", "vite.config.mts", "vite.config.js", "vite.config.mjs"])
    rsbuild_cfg = first_existing(root, ["rsbuild.config.ts", "rsbuild.config.mjs", "rsbuild.config.js"])
    legacy_cfg = first_existing(root, ["app.config.ts", "app.config.js"])
    bundler = "vite" if vite_cfg else "rsbuild" if rsbuild_cfg else None

    hosting = []
    cfg_text = read_text(vite_cfg) if vite_cfg else read_text(rsbuild_cfg) if rsbuild_cfg else ""
    for marker, label in (("nitro(", "nitro"), ("cloudflare(", "cloudflare"), ("netlify(", "netlify")):
        if marker in cfg_text:
            hosting.append(label)
    if (root / "wrangler.jsonc").is_file() or (root / "wrangler.toml").is_file():
        hosting.append("wrangler-config")

    if vite_cfg:
        start_at = cfg_text.find("tanstackStart(")
        react_at = min((i for i in (cfg_text.find("viteReact("), cfg_text.find("react(")) if i >= 0), default=-1)
        if start_at < 0:
            add("plugin-missing", "warn", "tanstackStart() not found in the Vite config", vite_cfg.name)
        elif 0 <= react_at < start_at:
            add("plugin-order", "warn", "React plugin appears before tanstackStart(); the docs require it after", vite_cfg.name)
    if legacy_cfg:
        add("legacy-app-config", "error", "app.config.* is the Vinxi-era config; current Start uses vite.config with tanstackStart()", legacy_cfg.name)

    router_file = first_existing(src, ["router.tsx", "router.ts"]) if src.is_dir() else None
    root_route = first_existing(src / "routes", ["__root.tsx", "__root.ts", "__root.jsx"]) if (src / "routes").is_dir() else None
    start_file = first_existing(src, ["start.ts", "start.tsx"]) if src.is_dir() else None

    if is_start and not router_file:
        add("router-missing", "warn", f"{src_dir}/router.tsx not found")
    elif router_file and "getRouter" not in read_text(router_file):
        add("get-router", "warn", "router file does not export getRouter()", router_file.relative_to(root).as_posix())
    if root_route:
        text = read_text(root_route)
        for needed in ("HeadContent", "Scripts"):
            if needed not in text:
                add("root-shell", "warn", f"<{needed} /> not found in the root route", root_route.relative_to(root).as_posix())
    if start_file:
        text = read_text(start_file)
        if "createStart" in text and "createCsrfMiddleware" not in text:
            add("csrf-missing", "error", "src/start.ts exists without createCsrfMiddleware: server functions lose the default CSRF protection", start_file.relative_to(root).as_posix())

    tsconfig = read_text(root / "tsconfig.json")
    if re.search(r"\"verbatimModuleSyntax\"\s*:\s*true", tsconfig):
        add("verbatim-module-syntax", "warn", "verbatimModuleSyntax is on; the docs warn it can leak server code into the client bundle", "tsconfig.json")

    routes, server_fn_files, server_route_files, server_only_files = [], [], [], []
    api_mounts: list[str] = []
    scanned = 0
    if src.is_dir():
        for path in iter_sources(src, max_files):
            scanned += 1
            rel = path.relative_to(root).as_posix().replace("\\", "/")
            text = read_text(path)
            in_routes = f"{src_dir}/routes/" in rel and "/-" not in rel
            is_server_file = ".server." in path.name
            if in_routes:
                routes.append(rel)
            if SERVER_FN.search(text):
                server_fn_files.append(rel)
            if in_routes and SERVER_HANDLERS.search(text):
                server_route_files.append(rel)
                if path.stem.endswith("$") and API_MOUNT.search(text):
                    api_mounts.append(rel)
                    missing = [m for m in HTTP_METHODS if not re.search(rf"\b{m}\s*:", text)]
                    if missing:
                        add("api-mount-methods", "info", f"catch-all API mount does not register {', '.join(missing)}; requests with those methods never reach the API", rel)
            if is_server_file or "@tanstack/react-start/server-only" in text:
                server_only_files.append(rel)

            for lineno, line in enumerate(text.splitlines(), start=1):
                for fid, pattern, severity, message in LEGACY_PATTERNS:
                    if pattern.search(line):
                        add(fid, severity, message, rel, lineno)
                if SET_COOKIE_HEADER.search(line):
                    add("set-cookie-header", "warn", "setResponseHeader('set-cookie') replaces every cookie; use setCookie", rel, lineno)
                if EDEN_LOCALHOST.search(line):
                    add("eden-localhost", "warn", "Eden client with a hard-coded localhost origin; use window.location.origin in the browser and treaty(app) on the server", rel, lineno)
                if MODULE_QUERY_CLIENT.match(line):
                    add("module-query-client", "error", "QueryClient created at module scope; create it inside getRouter() per request", rel, lineno)
                if not is_server_file and MODULE_ENV_READ.match(line):
                    add("module-env-read", "warn", "process.env read at module scope in a non-.server file; read it inside a server function", rel, lineno)
            server_only_route = rel in server_route_files and not re.search(r"\b(?:loader|beforeLoad|component)\s*:", text)
            if in_routes and PROCESS_ENV.search(text) and not is_server_file and not server_only_route:
                add("env-in-route", "warn", "process.env in a route file: loaders run in the browser too; confirm it is inside a server function or server handler", rel)
            if in_routes and SERVER_ONLY_FN.search(text):
                add("server-only-fn-in-route", "info", "createServerOnlyFn in a route file throws if a loader calls it during client navigation", rel)

    return {
        "root": str(root),
        "is_tanstack_start": is_start,
        "versions": versions,
        "bundler": bundler,
        "hosting_signals": hosting,
        "files": {
            "vite_config": vite_cfg.name if vite_cfg else None,
            "rsbuild_config": rsbuild_cfg.name if rsbuild_cfg else None,
            "router": router_file.relative_to(root).as_posix() if router_file else None,
            "root_route": root_route.relative_to(root).as_posix() if root_route else None,
            "start": start_file.relative_to(root).as_posix() if start_file else None,
            "route_tree_generated": (src / "routeTree.gen.ts").is_file(),
        },
        "embedded_api": {
            "framework": next((n for n in ("elysia", "hono") if n in deps), None),
            "eden": next((n for n in ("@elysia/eden", "@elysiajs/eden") if n in deps), None),
            "mount_routes": api_mounts,
        },
        "counts": {
            "files_scanned": scanned,
            "routes": len(routes),
            "server_function_files": len(server_fn_files),
            "server_route_files": len(server_route_files),
            "server_only_files": len(server_only_files),
        },
        "routes": routes[:300],
        "server_function_files": server_fn_files[:300],
        "server_route_files": server_route_files[:300],
        "server_only_files": server_only_files[:300],
        "findings": findings[:500],
    }


def print_text(result: dict) -> None:
    print(f"TanStack Start: {'yes' if result['is_tanstack_start'] else 'not detected'}")
    for name, version in result["versions"].items():
        print(f"  {name}: {version}")
    print(f"Bundler: {result['bundler'] or 'unknown'}; hosting signals: {', '.join(result['hosting_signals']) or 'none'}")
    for key, value in result["files"].items():
        print(f"  {key}: {value}")
    api = result["embedded_api"]
    if api["framework"] or api["mount_routes"]:
        print(f"Embedded API: {api['framework'] or 'unknown'}; eden: {api['eden'] or 'none'}; mounted at: {', '.join(api['mount_routes']) or 'not found'}")
    print("Counts: " + ", ".join(f"{k}={v}" for k, v in result["counts"].items()))
    if not result["findings"]:
        print("No findings.")
    for f in result["findings"]:
        where = f.get("file", "")
        if "line" in f:
            where += f":{f['line']}"
        print(f"[{f['severity']}] {f['id']}: {f['message']}" + (f" ({where})" if where else ""))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", type=Path, help="project root (folder containing package.json)")
    parser.add_argument("--src", default="src", help="Start srcDirectory (default: src)")
    parser.add_argument("--max-files", type=int, default=5000, help="maximum source files to read")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    result = scan(root, args.src.strip("/\\"), args.max_files)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text(result)
    if not result["is_tanstack_start"]:
        print("note: no @tanstack/*-start dependency found; this skill may not apply", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
