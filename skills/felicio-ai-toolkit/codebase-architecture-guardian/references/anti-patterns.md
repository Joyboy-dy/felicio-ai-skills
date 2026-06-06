# Anti-Patterns Catalog

Full catalog of architecture anti-patterns to detect and fix. Each entry includes the problem, why it matters, and the recommended fix.

---

## 1. `components/my-components/` or `components/custom/`

**Problem**: Ambiguous umbrella folder that becomes a dumping ground for everything that isn't shadcn/ui.

**Why it matters**: "my-components" conveys no architectural intent. It grows unbounded because there's no rule about what does or doesn't belong. New contributors add files here by default because the name suggests "this is where my stuff goes."

**Fix**: Split into purpose-driven folders:
- Generic reusable → `components/base/`
- Domain-specific → `features/[domain]/components/`
- Layout shells → `components/layouts/`
- Providers → `components/providers/`

---

## 2. Custom components inside `components/ui/`

**Problem**: Product-specific components mixed with auto-generated shadcn/ui primitives.

**Why it matters**: When you run `npx shadcn@latest add`, it overwrites or conflicts with files in `components/ui/`. Custom components in this folder risk being accidentally deleted or corrupted. It also makes it impossible to tell which files are library primitives and which are custom.

**Examples to flag**:
```txt
components/ui/dashboard-card.tsx    ← domain-specific
components/ui/base-button.tsx       ← custom wrapper
components/ui/billing-panel.tsx     ← feature component
components/ui/custom-navbar.tsx     ← layout component
```

**Fix**: Move custom components to `components/base/`, `components/layouts/`, or `features/[domain]/components/` depending on their nature.

---

## 3. Huge flat `lib/`

**Problem**: `lib/` becomes a catch-all for everything that doesn't have an obvious home — auth, billing, database, email, analytics, storage, API clients, and actual utilities all mixed together.

**Why it matters**: When everything is in `lib/`, nothing has clear ownership. Developers can't find things, imports become tangled, and server-only code leaks into client bundles. A 25-file `lib/` with mixed concerns is a sign that the project lacks architectural boundaries.

**Threshold**: If `lib/` has more than 10-15 unrelated files, it needs an audit.

**Fix**:
- Auth logic → `server/auth/` or `features/auth/`
- Database → `server/db/`
- Business services → `server/services/`
- Email → `server/mail/`
- Storage → `server/storage/`
- External APIs → `server/integrations/`
- Feature-specific logic → `features/[domain]/`
- Keep only tiny stateless helpers in `lib/` (cn, formatDate, slugify)

---

## 4. Huge flat `hooks/`

**Problem**: All hooks dumped in one root folder regardless of domain.

**Why it matters**: `hooks/use-subscription.ts` next to `hooks/use-debounce.ts` obscures the boundary between generic utilities and domain-specific logic. When the hooks folder grows to 20+ files, it becomes hard to find what you need.

**Fix**:
- Keep generic hooks in root `hooks/`: `use-debounce`, `use-media-query`, `use-mounted`
- Move domain hooks to their feature: `features/billing/hooks/use-subscription.ts`

---

## 5. `services/` at root with mixed frontend/backend logic

**Problem**: A root-level `services/` folder that contains both client-side API calls and server-side business logic.

**Why it matters**: This violates the server/client boundary. Client components importing server-side services will cause runtime errors or bloat the client bundle. It also makes it unclear which files are safe to import where.

**Fix**:
- Server-side services → `server/services/`
- Client-side API calls → `features/[domain]/queries.ts` or `features/[domain]/api.ts`

---

## 6. All actions in one root `actions/` folder

**Problem**: Every Server Action in the entire app lives in one flat `actions/` folder at the root.

**Why it matters**: Actions are tightly coupled to their domain. A `createLink` action belongs with link logic, a `cancelSubscription` action belongs with billing logic. Putting them all in one folder breaks colocation and makes it hard to understand the scope of each action.

**Fix**:
- Route-specific actions → `app/[route]/_actions/`
- Domain actions → `features/[domain]/actions/`

---

## 7. Feature code scattered everywhere

**Problem**: Auth logic lives in `lib/auth.ts`, auth components in `components/auth/`, auth hooks in `hooks/use-auth.ts`, auth types in `types/auth.ts`, and auth actions in `actions/auth-actions.ts`.

**Why it matters**: To understand the auth feature, you need to look in 5 different folders. To modify it, you touch 5 different places. To delete it, you need to hunt across the entire codebase. This is the #1 sign that feature-based architecture would help.

**Fix**: Consolidate everything into `features/auth/`:
```txt
features/auth/
├── components/
├── actions/
├── hooks/
├── schemas/
├── types.ts
├── constants.ts
└── index.ts
```

---

## 8. Route handlers with direct complex database logic

**Problem**: A `route.ts` file that directly contains 50+ lines of Prisma queries, data transformation, and business rules.

**Why it matters**: Route handlers should be thin orchestration layers. Complex logic in route handlers is hard to test, impossible to reuse, and makes the API surface tightly coupled to database schema.

**Fix**: Extract to the service/repository pattern:
```ts
// app/api/users/route.ts — THIN
export async function POST(request: Request) {
  const payload = await request.json();
  const result = await userService.create(payload);
  return Response.json(result);
}
```

---

## 9. Client components importing server-only modules

**Problem**: A `"use client"` component that imports from `server/`, uses `prisma`, or calls a function that requires Node.js APIs.

**Why it matters**: This will crash at runtime in the browser. Next.js might catch it at build time, but not always, especially with transitive dependencies.

**Fix**: Use Server Components for data fetching, pass data as props to client components. Or use Server Actions for mutations.

---

## 10. Barrel exports that expose private internals

**Problem**: A feature's `index.ts` re-exports everything, including internal implementation details.

```ts
// features/auth/index.ts — BAD
export * from "./lib/token-storage";
export * from "./lib/password-hash";
export * from "./hooks/use-auth-internal";
export * from "./components/auth-form";
```

**Why it matters**: This defeats the purpose of having features with boundaries. Other features will depend on internal implementation details, making refactoring impossible without breaking changes.

**Fix**: Export only the public API:
```ts
// features/auth/index.ts — GOOD
export { getSession, signIn, signOut } from "./actions/auth-actions";
export { AuthGuard } from "./components/auth-guard";
export type { Session, User } from "./types";
```

---

## 11. Duplicate component systems

**Problem**: Multiple folders containing variations of the same component: `components/ui/button.tsx`, `components/base/button.tsx`, `components/my-components/custom-button.tsx`.

**Why it matters**: Developers don't know which button to use. Styling becomes inconsistent. Bundle size grows with duplicate code.

**Fix**: Establish one source of truth per component type:
- Library primitive → `components/ui/button.tsx`
- Custom wrapper with extended props → `components/base/icon-button.tsx` (wraps the shadcn button)
- Domain-specific button → `features/[domain]/components/` (wraps base or ui)
