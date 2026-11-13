# Embedded API: Elysia inside TanStack Start

Use this when the app mounts an Elysia server (or another fetch-based API framework such as Hono) inside Start: one process, one origin, the API under `/api/*`, typed calls through Eden. Checked on 2026-11-13 with Elysia 1.4 (`latest`; 2.0 is in RC) and Start 1.169. For Elysia's own API (plugins, `t` schemas, lifecycle), use the official `elysiajs/skills` skill or `https://elysiajs.com/llms.txt`, and check the installed major version first: the official skill targets Elysia 2.

## Choose one API surface per feature

| Surface                          | Use for                                                                                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Elysia routes (`/api/*`)         | The application's API: everything the UI reads or writes, plus external callers (webhooks, public API, OpenAPI, MCP, auth library routes) |
| Start server functions           | SSR glue only: reading request context for the root, cookies, redirects tied to rendering                                                 |
| Start server routes (non-`/api`) | Files outside the API: `sitemap[.]xml`, `robots[.]txt`, `[.]well-known/…`                                                                 |

Do not implement the same operation as both a server function and an Elysia route. When Elysia is present, new data features go through Elysia and Eden unless there is a stated reason.

## Layout

```
packages/api/        (or src/server/api/ in a single-package app)
  src/app.ts         new Elysia({ prefix: '/api' }) composing feature modules; export type App = typeof app
  src/modules/<domain>/  routes, service, schemas (Elysia t / TypeBox or the repo's validator)
apps/web/            (or src/)
  src/routes/api/$.ts    catch-all server route mounting the Elysia app
  src/lib/api.ts         isomorphic Eden client
  server.ts              optional production entry (Bun.serve) serving static files + Start + API
```

In a single-package app, keep the Elysia app in import-protected server files (`*.server.ts` or a `server/` folder added to the import-protection rules). Only `import type { App }` reaches client code.

## Mount: catch-all server route

```ts
// src/routes/api/$.ts
import { createFileRoute } from "@tanstack/react-router";
import { app } from "~/server/api/app.server";

const handle = ({ request }: { request: Request }) => app.handle(request); // app.fetch(request) also works

export const Route = createFileRoute("/api/$")({
  server: {
    handlers: {
      GET: handle,
      HEAD: handle,
      POST: handle,
      PUT: handle,
      PATCH: handle,
      DELETE: handle,
      OPTIONS: handle,
    },
  },
});
```

- Register every HTTP method the API uses (including `HEAD` and `OPTIONS` for CORS preflight): requests with an unregistered method never reach Elysia.
- Set `prefix: '/api'` on the Elysia app so its paths match the mount.
- With pnpm, Elysia 1.x peers may need explicit install (`@sinclair/typebox`, `openapi-types`).
- If the app needs async startup (DB pool, migrations check), await a ready promise inside `handle`, not at module scope.

## Isomorphic Eden client

```ts
// src/lib/api.ts
import { treaty } from "@elysia/eden"; // older installs: '@elysiajs/eden'
import type { App } from "~/server/api/app.server";
import { createIsomorphicFn } from "@tanstack/react-start";

type Api = ReturnType<typeof treaty<App>>["api"];

export const getApi = createIsomorphicFn()
  .server(async (): Promise<{ api: Api }> => {
    const [{ app }, { getRequest }] = await Promise.all([
      import("~/server/api/app.server"),
      import("@tanstack/react-start/server"),
    ]);
    const incoming = getRequest();
    const headers: Record<string, string> = {};
    for (const name of ["cookie", "authorization", "accept-language", "user-agent"]) {
      const value = incoming.headers.get(name);
      if (value) headers[name] = value;
    }
    return { api: treaty(app, { headers }).api as Api }; // in-memory call, no HTTP
  })
  .client(async (): Promise<{ api: Api }> => ({
    api: treaty<App>(window.location.origin, { fetch: { credentials: "same-origin" } }).api,
  }));
```

Usage in a loader or `queryFn`: `const { api } = await getApi(); const { data, error } = await api.projects({ id }).get()`.

Rules this example encodes:

- **Server side calls the app in memory** (`treaty(app)`), so SSR has no HTTP round trip. That call does not see the browser's cookies by itself: forward the auth-relevant headers of the current request, or every SSR read runs as signed out.
- **Client side uses the page origin** (`window.location.origin`), never a hard-coded `localhost:3000`.
- **Wrap the Eden proxy in an object** before returning it from an async function. The proxy exposes a `then` property, so returning it directly makes `await` treat it as a promise that never settles.
- **Server-only imports live inside `.server()`** (dynamic `import()` is fine here; this is not a server-function module). The compiler drops the `.server()` body and its imports from the client build; `import type { App }` is erased.
- **Dates**: Eden's `parseDate` (on by default) turns any date-looking string into a `Date`, including inside free text. Use `parseDate: false` for content where strings must stay strings, and convert known date fields explicitly.
- **Errors**: Eden returns `{ data, error }`; it does not throw. Convert `error.status === 404` into `throw notFound()` and 401/403 into a redirect in loaders, or throw in `queryFn` so Query and error boundaries see the failure.

With TanStack Query, put the Eden call in `queryOptions` (`queryFn: async () => { const { api } = await getApi(); ... }`) exactly as in `references/data-and-validation.md`; loaders call `context.queryClient.query(...)`.

## Contracts and validation

- The API layer is the security boundary: validate bodies, params and queries in Elysia (`t` / TypeBox, or Standard Schema when the installed Elysia supports it). Eden types flow from these schemas.
- Keep one schema library per contract. If the API uses TypeBox and the UI uses Zod for forms and search params, keep the UI schema a client-side mirror and test the overlap; do not validate the same body with two libraries on the server.
- Authorize in the Elysia route or service, deriving tenant/owner identity from the session and the parent resource, never from the request body. Route guards in Start (`beforeLoad`) stay UX only.

## Auth, CSRF and headers

- Mount the auth library's handler inside Elysia (for example Better Auth under `/api/auth/*`), so sessions and API share one origin and cookie.
- Start's automatic CSRF middleware covers **server functions only**. Elysia routes need their own protection for cookie-authenticated writes: `SameSite=Lax`/`Strict` cookies plus an `Origin`/`Sec-Fetch-Site` check on non-GET requests (auth libraries often provide one for their own routes only).
- Do not trust forwarding headers (`x-forwarded-for`, custom client-IP headers) unless the request came through your own entry server or proxy; strip them otherwise.
- Personalized API responses: `Cache-Control: private, no-store`.

## Running it

- Dev: `bun --bun vite dev` runs Vite, Start and Elysia on Bun, so Bun APIs (`Bun.file`, `Bun.password`) work in the API during development.
- Production without an adapter: `vite build` outputs `dist/client` and a fetch handler in `dist/server/server.js`. A small entry (`Bun.serve`) can serve `dist/client` with long cache for hashed `/assets/*`, then pass other requests to that handler (which reaches Elysia through `/api/$`). With Nitro, use its Bun preset instead.
- If the API uses Bun-only APIs, the runtime must be Bun (not Node, not an edge worker); state it in the hosting decision.
- Container image: see `container-compose-ghcr-deployment` (Bun projects).
