# Rendering, caching, hosting and migration

## Rendering modes

| Need                                             | Setting                                                                                                                      |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Default: server-rendered, hydrated               | nothing (`ssr: true`)                                                                                                        |
| Page uses browser-only libraries                 | route `ssr: false` (loader and component run in the browser)                                                                 |
| Server data, but component only works in browser | `ssr: 'data-only'`                                                                                                           |
| Decide per request                               | `ssr: ({ params, search }) => ...`                                                                                           |
| App-wide default                                 | `createStart(() => ({ defaultSsr: false }))` in `src/start.ts`                                                               |
| One widget only                                  | `<ClientOnly fallback>` instead of disabling SSR for the route                                                               |
| Static shell, no SSR server                      | `tanstackStart({ spa: { enabled: true } })` + host rewrites (`/_serverFn/*`, `/api/*` to the server; `/*` to `/_shell.html`) |
| Static pages at build time                       | `tanstackStart({ prerender: { enabled: true, crawlLinks: true }, pages: [...], sitemap: { enabled: true, host } })`          |

A child route can only be more restrictive than its parent. Prefer the narrowest change: `ClientOnly` < `ssr: 'data-only'` < `ssr: false` < SPA.

## HTTP caching (ISR)

Start has no framework cache layer; use HTTP headers and the CDN.

- Public, shared content: route `headers: () => ({ 'Cache-Control': 'public, max-age=60, s-maxage=600, stale-while-revalidate=86400' })`, or `setResponseHeaders` in a server function.
- Anything that depends on a cookie, session or user: `private, no-store` (and `Vary` where relevant). Set it on the root route when the root loads the user.
- Verify the final headers through the real host and CDN.

## Hosting

| Target                             | Setup                                                                                                                                                                         |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Node, Docker, Railway, Vercel, Bun | Nitro: `plugins: [tanstackStart(), nitro(), viteReact()]` (`import { nitro } from 'nitro/vite'`); Node runs `node .output/server/index.mjs`                                   |
| Cloudflare Workers                 | `@cloudflare/vite-plugin`: `cloudflare({ viteEnvironment: { name: 'ssr' } })` first; `wrangler.jsonc` with `"main": "@tanstack/react-start/server-entry"` and `nodejs_compat` |
| Bun, no adapter                    | `vite build` gives `dist/client` + a fetch handler in `dist/server/server.js`; serve both from a small `Bun.serve` entry (see `references/embedded-api-elysia.md`)            |
| Netlify                            | `@netlify/vite-plugin-tanstack-start`                                                                                                                                         |
| Rsbuild build                      | output `dist/client` + `dist/server/index.js` (a fetch handler), served e.g. with `srvx`                                                                                      |

- Bun as the runtime requires React 19. Check the official hosting guide for the adapter's current options: `https://tanstack.com/start/latest/docs/framework/react/guide/hosting`.
- Edge runtimes: no Node built-ins unless enabled, no env at module load, no long-lived module state per user.
- Custom server entry (`src/server.ts`): `createServerEntry({ fetch(request, opts) { return handler.fetch(request, opts) } })` with `handler` from `@tanstack/react-start/server-entry`; catch errors and `return handleStartError(error)`.
- With a separate backend (Elysia, Hono…) keep it the system of record: Start server functions call it with server-side credentials; the browser does not hold its secrets. Pick one place for auth decisions and document it.

## Migrating from Next.js

| Next.js                              | TanStack Start                                                                         |
| ------------------------------------ | -------------------------------------------------------------------------------------- |
| `app/layout.tsx`                     | `src/routes/__root.tsx` (`shellComponent` + `<HeadContent />`, `<Scripts />`)          |
| `app/page.tsx`, `posts/page.tsx`     | `index.tsx`, `posts.index.tsx`                                                         |
| `[slug]`, `[...parts]`, `(group)`    | `$slug`, `$` (splat), `(group)`                                                        |
| `app/api/x/route.ts`                 | `routes/api/x.ts` with `server.handlers`                                               |
| async Server Component data          | `createServerFn` called from the loader (the loader also runs in the browser)          |
| Server Actions + `revalidatePath`    | POST server function + `useServerFn`, then `router.invalidate()` or Query invalidation |
| `'use client'`                       | not needed; use `ClientOnly` / `ssr: false` for browser-only code                      |
| `searchParams` prop                  | `validateSearch` + `Route.useSearch()` + `loaderDeps`                                  |
| `cookies()`, `headers()`             | `getCookie`/`setCookie`, `getRequestHeader` from `@tanstack/react-start/server`        |
| `metadata`, `generateMetadata`       | route `head: ({ loaderData }) => ({ meta, links })`                                    |
| `middleware.ts`                      | request middleware in `src/start.ts`, or `beforeLoad` for route gating                 |
| `next/link`, `useRouter`             | `Link` with typed `to`/`params`/`search`, `useNavigate`, `useRouter`                   |
| `sitemap.ts`, `robots.ts`            | server routes `sitemap[.]xml.ts`, `robots[.]txt.ts`, or `sitemap` plugin option        |
| `generateStaticParams`, `revalidate` | `prerender` options, ISR headers                                                       |
| `next/image`, `next/font`            | no built-in equivalent: plain `<img>` with sizes or an image CDN; self-hosted fonts    |

Migrate route by route, keep URLs identical, and compare each migrated page on direct load and client navigation. Official guide: `https://tanstack.com/start/latest/docs/framework/react/migrate-from-next-js` (example app `examples/react/start-next-migration` in the TanStack/router repo). `@tanstack/react-start` also ships a `migrate-from-nextjs` skill through TanStack Intent.
