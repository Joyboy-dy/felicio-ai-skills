# Server boundaries

APIs below are for 1.169+. Imports come from `@tanstack/react-start` unless noted (`/server` = `@tanstack/react-start/server`; Solid uses `@tanstack/solid-start`).

## Server functions

```ts
// features/projects/projects.functions.ts
import { createServerFn } from "@tanstack/react-start";
import { notFound } from "@tanstack/react-router";
import { authMiddleware } from "~/middleware/auth";
import { ProjectIdSchema, UpdateProjectSchema } from "./projects.schemas";
import { findProject, updateProject } from "./projects.server";

export const getProject = createServerFn({ method: "GET" })
  .middleware([authMiddleware])
  .validator(ProjectIdSchema) // Standard Schema, a function, or FormData (POST)
  .handler(async ({ data, context }) => {
    const project = await findProject(data.projectId, context.user.id); // scoped to the user
    if (!project) throw notFound();
    return project;
  });

export const saveProject = createServerFn({ method: "POST" })
  .middleware([authMiddleware])
  .validator(UpdateProjectSchema)
  .handler(async ({ data, context }) => updateProject(data, context.user.id));
```

- Chain order: `createServerFn({ method })` → `.middleware()` → `.validator()` → `.handler()`. Default method is GET; use POST for writes and for any data that should not appear in a URL.
- Call it as `fn({ data })` from loaders, `beforeLoad`, other server functions, and components via `useServerFn(fn)` (needed for thrown `redirect`/`notFound` to take effect in components).
- Inputs and return values must be serializable; TypeScript checks it (`strict` mode, on by default; `FormData` input allowed for POST, `Response` output allowed). Return plain data, not ORM entities, DB handles or class instances. Register custom types with `createStart(() => ({ serializationAdapters }))` and `createSerializationAdapter`.
- Return or throw a `Response` for full control; return a `ReadableStream` or an `async function*` to stream.
- Disable `strict` (`strict: false`, or `{ input: false }` / `{ output: false }`) only with a stated reason.
- The validator checks shape; the handler must still check that the caller may touch this resource.

## Execution helpers

| API                                                                 | Runs                                 | Use for                                    |
| ------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------ |
| `createServerFn`                                                    | server, callable from anywhere (RPC) | anything with secrets, DB, private data    |
| `createServerOnlyFn(fn)`                                            | server only, throws on client        | helpers called from other server code only |
| `createClientOnlyFn(fn)`                                            | client only, throws on server        | `localStorage`, browser APIs               |
| `createIsomorphicFn().server().client()`                            | both, each side tree-shaken          | logging, storage, analytics with two impls |
| `<ClientOnly fallback>`, `useHydrated()` (`@tanstack/react-router`) | render after hydration               | widgets that differ server vs client       |

`createServerOnlyFn` in a loader throws on client navigation. Loaders call `createServerFn`.

## Import protection

On by default inside `srcDirectory`. Client environment denies `**/*.server.*` files and the `@tanstack/react-start/server` specifier; server environment denies `**/*.client.*`. Dev mocks the import and warns; build fails.

- Marker imports: `import '@tanstack/react-start/server-only'` or `'@tanstack/react-start/client-only'` at the top of a file.
- Type-only imports are ignored.
- Extend rules: `tanstackStart({ importProtection: { client: { files: ['**/*.server.*', '**/server/**'], specifiers: ['drizzle-orm', 'stripe'] } } })`.
- A server-only import used only inside a `createServerFn` handler is removed from the client build with the handler. The same import used anywhere else in that file stays.

Treat an import-protection warning in dev as a bug, not noise.

## Middleware

```ts
// middleware/auth.ts
import { createMiddleware } from "@tanstack/react-start";
import { getSessionUser } from "~/server/auth.server";

export const authMiddleware = createMiddleware({ type: "function" }).server(async ({ next }) => {
  const user = await getSessionUser();
  if (!user) throw new Error("Unauthorized"); // the route guard handles the redirect UX
  return next({ context: { user } });
});
```

- `createMiddleware()` (request middleware) runs for SSR, server routes and server functions: `.middleware([...])`, `.server(({ request, next, context }) => next())`. Use it for request-wide concerns (logging, headers, CSRF, locale).
- `createMiddleware({ type: 'function' })` runs for server functions: `.middleware()` → `.validator()` → `.client()` → `.server()`, in that order.
- `next({ context })` passes typed context downstream. `sendContext` moves context client→server (untrusted: validate and re-authorize) or server→client.
- Global registration in `src/start.ts`; global middleware runs before route- or function-level middleware.

## `src/start.ts` and CSRF

Without `src/start.ts`, Start installs CSRF protection for server functions automatically. **Creating `src/start.ts` removes that default**, so add it back:

```ts
import { createStart, createCsrfMiddleware } from "@tanstack/react-start";

export const startInstance = createStart(() => ({
  requestMiddleware: [createCsrfMiddleware({ filter: (ctx) => ctx.handlerType === "serverFn" })],
  functionMiddleware: [],
  // defaultSsr: true,
}));
```

The CSRF check rejects requests that cannot be proven same-origin (`Sec-Fetch-Site`, `Origin`, `Referer`). Use `createCsrfMiddleware({ origin })` behind a proxy whose public origin differs.

## Server routes

```ts
// routes/api/webhooks.stripe.ts
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/api/webhooks/stripe")({
  server: {
    handlers: {
      POST: async ({ request }) => {
        // verify the signature, parse and validate the body, then act
        return new Response(null, { status: 204 });
      },
    },
  },
});
```

- For callers outside the app. Validate bodies and authenticate by hand: no `.validator()` here.
- `server.middleware` applies to all methods; `handlers: ({ createHandlers }) => createHandlers({ POST: { middleware, handler } })` per method.
- A route file can hold both `server` and `component` for the same path.

## Request and response helpers (`/server`)

`getRequest`, `getRequestHeader(s)`, `getCookie`, `setCookie`, `deleteCookie`, `setResponseHeader(s)`, `appendResponseHeader`, `setResponseStatus`. Use `setCookie` for cookies: `setResponseHeader('set-cookie', ...)` replaces all cookies already set.

## Environment variables

- Server: `process.env.NAME`, read **inside** a server function, middleware or `createServerOnlyFn`, never at module scope (edge runtimes have no env at module load, and module code may be bundled for the client).
- Client: only `import.meta.env.VITE_*` (`PUBLIC_*` with Rsbuild). Anything there is public.
- Type both in `src/env.d.ts` (`interface ImportMetaEnv`, `namespace NodeJS { interface ProcessEnv }`) and parse server env with a schema in a server-only function.

```ts
// server/env.server.ts
import { z } from "zod";
const ServerEnv = z.object({ DATABASE_URL: z.url(), SESSION_SECRET: z.string().min(32) });
export const getServerEnv = () => ServerEnv.parse(process.env);
```
