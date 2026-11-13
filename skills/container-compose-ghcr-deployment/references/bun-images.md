# Bun projects

Use when the repository declares Bun (`bun.lock`, `bunfig.toml`, `"packageManager": "bun@…"`, `Bun.*` APIs, or a `bun` start script).

## Base image and install

- Use the official `oven/bun` image at the version declared in `packageManager` (or `.bun-version`), pinned by tag and, for production, by digest. Alpine variants are smaller; switch to Debian (`oven/bun:<v>-slim`) when native modules need glibc.
- Install with the lockfile: `bun install --frozen-lockfile`. Add `--ignore-scripts` when lifecycle scripts only set up local tooling (git hooks), and run required build steps explicitly.
- Workspaces: a frozen install needs every workspace `package.json` the lockfile references. In a dependency-only stage, copy the root manifests and each workspace manifest, not only the target app's.
- Production dependencies only in the runtime stage: `bun install --frozen-lockfile --production`. If the app is bundled into one file, copy only the native modules the bundle cannot include (for example `sharp` and its platform packages).

## Runtime stage

- Run with the image's `bun` user (`USER bun`), and give it ownership of writable volumes only.
- Start the real production entry (`bun server.js`, `bun run start`), never `bun --bun vite dev` or another dev server.
- A cheap build-time guard: execute the entry without configuration and expect the app's own "invalid environment" message. It proves every module evaluates in the image before it ships.
- `HEALTHCHECK` against an endpoint the app already exposes; Bun images include `bun`, so a short `bun -e "fetch(...)"` works without curl.

## Standalone Bun services

For an API that runs alone (Elysia without a frontend), `bun build --compile --minify-whitespace --minify-syntax --outfile server src/index.ts` produces one binary that can run on a minimal base such as `gcr.io/distroless/base`. This does not apply to a TanStack Start or other SSR app, whose server build reads its client assets from disk.

## Frameworks inside the image

For TanStack Start served by Bun, copy `dist/client` and the server entry or bundle; the image does not need `node_modules` for code the build already bundled. See the `tanstack-start-architecture` skill for the entry server and the embedded API.
