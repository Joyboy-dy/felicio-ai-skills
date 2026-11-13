# Version notes

Checked against the official docs and npm on 2026-11-13: `@tanstack/react-start` 1.169.5 (latest). **1.169.0 is the first stable release.** Re-check `https://tanstack.com/start/latest/docs/framework/react/migrate-from-release-candidate` when the installed version is newer than these notes.

## Changed in 1.169 (do not use the old form on 1.169+)

| Old (RC and earlier)                                            | Current                                                                                   |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `.inputValidator()` on server functions and middleware          | `.validator()`, same argument                                                             |
| `useSession` from `@tanstack/react-start/server`                | Removed. Use a session library (the docs use `iron-session` with `getCookie`/`setCookie`) |
| Vite 7                                                          | Vite 8 (or Rsbuild 2 with `@tanstack/react-start/plugin/rsbuild`)                         |
| `@tanstack/nitro-v2-vite-plugin`                                | `nitro()` from `nitro/vite`                                                               |
| `createStartHandler` swallowing errors in a custom server entry | It rethrows: catch in `createServerEntry` and `return handleStartError(error)`            |
| Returning `Location` from a server function                     | Dropped from serialized replies: `throw redirect(...)`                                    |
| `sendContext` defaulting to `{}`                                | `undefined` when nothing is sent                                                          |
| `vite-tsconfig-paths` plugin                                    | `resolve: { tsconfigPaths: true }` (native in Vite 8)                                     |

Other behavior to know on 1.169: response helpers (`setResponseHeader`, `setResponseStatus`) override the `Response` you return; `setResponseStatus` ignores codes outside 200–599; `getRequestHeader` returns `''` for a present but empty header; malformed percent-encoding in a path returns 400.

## Older generations

- **Vinxi era** (`app.config.ts`, `app/` directory, `vinxi dev`): gone. Current apps use `src/`, a Vite or Rsbuild plugin and the bundler's own CLI. Migrating means moving to `vite.config.ts` with `tanstackStart()`, `src/router.tsx` exporting `getRouter()`, and re-checking every API below.
- **`registerGlobalMiddleware`**: replaced by `createStart(() => ({ requestMiddleware, functionMiddleware }))` in `src/start.ts`.
- **`createAPIFileRoute` / `createServerFileRoute`**: replaced by `createFileRoute(path)({ server: { handlers } })`.

## TanStack Query (5.102+)

The Start Query guide uses `queryClient.query(options)` (Query 5.102+). `ensureQueryData` still works and appears in official examples; keep whichever the repo uses, and use `ensureQueryData` on older Query versions.

## Validation adapters

Zod v4, Valibot 1 and ArkType implement Standard Schema: pass the schema directly to `validateSearch` and `.validator()`. `@tanstack/zod-adapter` (`zodValidator`, `fallback`) is only needed for Zod v3.

## Experimental or unstable (avoid in production unless the user opts in)

React Server Components (`rsc: { enabled: true }`, `@tanstack/react-start-rsc`), static server functions (`staticFunctionMiddleware`), `serverFns.generateFunctionId`, CSS inlining, `transformAssets`, Early Hints, deferred hydration, OpenTelemetry. Nitro v3 is still beta. `@tanstack/vue-start` is published but has no docs.

## Where to check the current API

- `https://tanstack.com/start/latest/llms.txt` and `https://tanstack.com/router/latest/llms.txt`
- `npx @tanstack/cli search-docs "server functions" --library start --json`
- the public docs MCP server `https://tanstack.com/mcp`
- the official skills shipped in the installed packages (`npx @tanstack/intent@latest list`)
