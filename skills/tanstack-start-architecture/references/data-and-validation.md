# Data, validation and auth

## Loader lifecycle

`beforeLoad` (guards, context; runs serially parent → child) → `loader({ params, deps, context, abortController })` (children in parallel). Both run on the server for the first request and **in the browser on client navigation**.

- Declare the search values a loader depends on with `loaderDeps: ({ search }) => ({ page: search.page })`; only those trigger a reload, and they belong in the cache key.
- Router defaults: `staleTime` 0, `preloadStaleTime` 30 s, `gcTime` 5 min, stale-while-revalidate reloads, `defaultPreload: false` (set `'intent'` on the router for hover preloading).
- Await what decides the page: main content, `head` title/description, redirects, existence (`throw notFound()`). Return a non-awaited promise for secondary data and render it with `<Await promise fallback>` or React 19 `use()`.
- Errors: `errorComponent` per route or `defaultErrorComponent` on the router; `notFoundComponent` / `defaultNotFoundComponent`. Root route can use `shellComponent` for the `<html>` document and `component` for the app.

## Loaders only, or TanStack Query

Loaders alone are enough when data is page-scoped and refreshed by navigation or `router.invalidate()`. Add TanStack Query when data is shared across routes, refreshed in the background, or driven by mutations with fine-grained invalidation. Do not cache the same data in both.

With Query (`@tanstack/react-query` 5.102+ and `@tanstack/react-router-ssr-query`):

```tsx
// src/router.tsx
export function getRouter() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { staleTime: 30_000 } } });
  const router = createRouter({
    routeTree,
    context: { queryClient },
    defaultPreload: "intent",
    defaultPreloadStaleTime: 0, // let Query decide freshness
  });
  setupRouterSsrQueryIntegration({ router, queryClient });
  return router;
}
```

```ts
// features/projects/projects.queries.ts (client-safe)
export const projectQuery = (projectId: string) =>
  queryOptions({
    queryKey: ["project", projectId],
    queryFn: () => getProject({ data: { projectId } }),
  });
```

```tsx
// routes/_authed/projects.$projectId.tsx
export const Route = createFileRoute("/_authed/projects/$projectId")({
  loader: ({ context, params }) => context.queryClient.query(projectQuery(params.projectId)),
  component: ProjectPage,
});
function ProjectPage() {
  const { projectId } = Route.useParams();
  const { data } = useSuspenseQuery(projectQuery(projectId));
  // ...
}
```

- `queryClient.query()` needs Query 5.102+; `ensureQueryData` is the older equivalent.
- `QueryClient` per router, created in `getRouter()`. A module-scope client can put one user's data in another user's HTML.
- Declare `queryClient` in `createRootRouteWithContext<{ queryClient: QueryClient }>()`.
- The integration provides `QueryClientProvider` and dehydration; do not add a second provider or dehydrate by hand (`wrapQueryClient: false` if you own the provider).
- Same `queryOptions` in loader and component. Keys include every input (ids, validated search values); never secrets.
- `void context.queryClient.query(...)` streams secondary data; handle its rejection.
- On sign-out or account switch, remove the previous account's private queries and `router.invalidate()`.

## Mutations

```tsx
const save = useServerFn(saveProject);
const queryClient = useQueryClient();
const mutation = useMutation({
  mutationFn: (input: UpdateProject) => save({ data: input }),
  // return the promise so the mutation stays pending until the refetch ends
  onSuccess: (_result, input) => queryClient.invalidateQueries({ queryKey: ["project", input.id] }),
});
```

Invalidate the actual owner: `queryClient.invalidateQueries` for Query data, `router.invalidate()` for loader data and route context (both after login/logout). Optimistic updates need cancel, rollback and reconciliation; prefer confirmed write + invalidation unless latency matters.

Without Query: call the server function, then `await router.invalidate()` (or `router.navigate` to the result).

## Search params

```ts
const ProjectsSearch = z.object({
  page: z.number().int().min(1).catch(1),
  status: z.enum(["active", "archived"]).catch("active"),
  q: z.string().optional(),
});

export const Route = createFileRoute("/_authed/projects/")({
  validateSearch: ProjectsSearch, // Zod v4 / Valibot / ArkType: no adapter
  search: { middlewares: [stripSearchParams({ page: 1, status: "active" })] },
  loaderDeps: ({ search }) => search,
  loader: ({ context, deps }) => context.queryClient.query(projectsQuery(deps)),
});
```

- Search params are typed, validated state. Use `.catch()` (or `fallback()` from `@tanstack/zod-adapter` with Zod v3) so a bad URL degrades instead of erroring.
- Read with `Route.useSearch()`; write with `<Link search={(prev) => ({ ...prev, page: 2 })}>` or `navigate({ search })`.
- `retainSearchParams(['q'])` keeps params across links; `stripSearchParams(defaults)` keeps URLs short.
- Path params: `params: { parse, stringify }` to type and validate (`parse` returning `false` falls through to the next matching route).

## Schemas

- One schema file per feature (`*.schemas.ts`), client-safe, exporting schemas and `z.infer` types. Use the same schema for `validateSearch`/forms on the client and `.validator()` on the server when the contract is the same.
- When the server needs more (ownership, uniqueness, normalization), extend the shared schema server-side; do not loosen it.
- Keep the repo's validation library; do not add Zod to a Valibot project.

## Forms

- Plain approach: a form calls a POST server function via `useServerFn`, shows pending/error state, then invalidates. A no-JS fallback can post to the server function's `.url` with `method="post"`.
- TanStack Form + Start: `@tanstack/react-form-start` provides `formOptions`, `createServerValidate` / `ServerValidateError` (inside a POST server function validating `FormData`), `getFormData()` (GET server function read by the loader) and `useTransform` + `mergeForm` on the client. See `https://tanstack.com/start/latest/docs/framework/react/guide/tanstack-form`.
- Form UX (dirty state, error display, navigation guards) belongs to `form-ux-validation`.

## Auth

- Start has no session API. Use the provider's SDK (Clerk, WorkOS, Better Auth, Supabase, Auth.js) or a cookie session library (`iron-session` with `getCookie`/`setCookie`) in a server-only file.
- Root `beforeLoad: async () => ({ user: await getCurrentUserFn() })` with `headers: () => ({ 'Cache-Control': 'private, no-store' })`. Read it with `Route.useRouteContext()`.
- Pathless `_authed.tsx`: `beforeLoad` throws `redirect({ to: '/login', search: { redirect: location.href } })` when there is no user.
- Every private server function and server route authorizes again (function middleware that puts `user` in context, plus a resource-level check in the handler). Guards only shape the UI.
- After login or logout: `await router.invalidate()`.
