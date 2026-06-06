---
name: codebase-architecture-guardian
description: >
  Use this skill whenever the user wants to create, audit, refactor, reorganize,
  or maintain a clean long-term codebase architecture, especially for Next.js,
  TypeScript, full-stack apps, SaaS dashboards, marketplaces, admin panels,
  or projects with messy folders like components, lib, hooks, utils, server,
  API routes, middleware, proxies, database access, and shared UI. Trigger
  strongly when the user mentions project structure, folder structure, codebase
  architecture, maintainability, scalability, technical debt, refactoring,
  "where should I put this file?", shadcn/ui conflicts, feature-based
  architecture, App Router, Server Actions, Route Handlers, services,
  repositories, or architecture cleanup. Also trigger when creating a new
  project from scratch and the user wants a solid foundation, or when the user
  asks about import conventions, dependency direction, barrel exports, or
  colocation rules.
compatibility: "Designed for Claude Code / ChatGPT-style coding assistants. No required runtime dependencies."
---

# Codebase Architecture Guardian

Use this skill to help the user design, audit, or refactor a codebase into a clean, understandable, maintainable, and scalable structure.

The default target is a modern **Next.js App Router full-stack project without a `src/` directory**, using TypeScript, Tailwind CSS, shadcn-style UI primitives, custom reusable components, server logic, route handlers, server actions, middlewares/proxy files, and database access.

## Core objective

Produce architecture decisions that reduce chaos, avoid "folder dumping", and keep code easy to navigate for both senior and junior developers.

Prioritize:

1. Clear ownership of each file.
2. Predictable folder rules.
3. Low coupling between domains.
4. Strong colocation where useful.
5. Clean separation between routing, UI primitives, feature logic, and backend logic.
6. Incremental refactoring that does not break the existing app.

## Default assumptions

Unless the user says otherwise:

- The project uses **Next.js App Router**.
- The project does **not** use a `src/` directory.
- TypeScript is mandatory.
- `app/` is primarily for routing, layouts, pages, route handlers, loading/error files, and route-local colocation.
- `components/ui/` is reserved for generated or library-level UI primitives, especially shadcn/ui.
- User-created reusable UI components should not be mixed into `components/ui/`.
- Use the alias `@/` when it improves readability for cross-domain imports, but keep relative imports for nearby files.
- Prefer incremental migration over "rewrite everything".

## Reference architecture

For a full-stack Next.js project without `src/`, recommend this baseline:

```txt
/
├── app/
│   ├── (marketing)/
│   ├── (auth)/
│   ├── (dashboard)/
│   ├── api/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── loading.tsx
│   ├── error.tsx
│   └── not-found.tsx
│
├── features/
│   ├── auth/
│   ├── billing/
│   ├── users/
│   ├── teams/
│   ├── notifications/
│   └── [domain]/
│
├── components/
│   ├── ui/
│   ├── base/
│   ├── layouts/
│   ├── providers/
│   └── [specialized-system]/
│
├── server/
│   ├── db/
│   ├── repositories/
│   ├── services/
│   ├── auth/
│   ├── mail/
│   ├── storage/
│   ├── cache/
│   └── integrations/
│
├── lib/
│   ├── utils.ts
│   └── [small-cross-cutting-utils].ts
│
├── config/
├── constants/
├── hooks/
├── types/
├── public/
├── prisma/
├── middleware.ts
├── proxy.ts
├── instrumentation.ts
├── next.config.ts
├── package.json
└── tsconfig.json
```

Adapt the structure to the project size. Do not create empty architecture theater. Add a directory only when there is a real responsibility to isolate.

> For detailed folder responsibilities, read `references/folder-responsibilities.md`.
> For the full refactoring playbook, read `references/refactoring-playbook.md`.

## Component placement decision tree

When placing a component, walk through these questions in order:

1. **Is it generated or copied from shadcn/ui?** → `components/ui/`
2. **Is it a generic reusable visual primitive?** → `components/base/`
3. **Is it a layout shell, navbar, sidebar, or app frame?** → `components/layouts/`
4. **Is it a provider?** → `components/providers/`
5. **Is it only used by one route?** → `app/[route]/_components/`
6. **Is it tied to one business domain and reused by several screens?** → `features/[domain]/components/`
7. **Is it tied to a specialized editor or isolated subsystem?** → `components/[system]/` or `features/[domain]/[system]/`, depending on whether it is generic or domain-specific.

## Colocation rule

```txt
If it is used only by one route → colocate it inside that route.
If it is reused by multiple routes of one domain → move it to features/[domain].
If it is reused across unrelated domains → move it to components/base, lib, hooks, or server.
```

## Server Actions vs Route Handlers

| Need | Placement |
|---|---|
| Mutation used by a form inside the app | `features/[domain]/actions/` or route-local `_actions/` |
| Endpoint consumed by an external system, webhook, mobile app, or public client | `app/api/[resource]/route.ts` |
| Page data fetching | Server Component, calling a service/query when logic is non-trivial |
| Complex business mutation | Server Action → service → repository |
| Database access | repository or server query layer |

Keep `route.ts` thin:

```ts
export async function POST(request: Request) {
  const payload = await request.json();
  const result = await userService.create(payload);
  return Response.json(result);
}
```

Keep Server Actions thin:

```ts
"use server";

export async function createLinkAction(input: CreateLinkInput) {
  return linkService.create(input);
}
```

## Import rules

Use `@/` for imports crossing major folders:

```ts
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { PageHeader } from "@/components/base/page-header";
import { createLinkAction } from "@/features/links/actions/create-link";
```

Use relative imports for nearby files:

```ts
import { LinkCard } from "./link-card";
import { linkSchema } from "../schemas/link-schema";
```

Avoid deep imports into another feature's internals:

```ts
// Avoid
import { tokenStorage } from "@/features/auth/lib/token-storage";

// Prefer
import { getSession } from "@/features/auth";
```

## Dependency direction

Prefer this direction (top = most generic, bottom = most specific):

```txt
components/ui
  ↓
components/base + lib + hooks + config
  ↓
server + features
  ↓
app
```

Never let generic layers depend on business layers:

- `components/ui` must not import from `features`.
- `components/base` should not import from `features`.
- `lib` should not import from `features`.
- `features` should avoid importing private files from other features.

## Default final recommendation

When in doubt, recommend:

```txt
Route           → app/
Domain          → features/
Reusable UI     → components/base/
Library UI      → components/ui/
Layout shells   → components/layouts/
Providers       → components/providers/
Backend logic   → server/
Small helpers   → lib/
Global config   → config/
Global types    → types/
```

## Anti-patterns to flag

Flag these immediately when detected:

- `components/my-components/` or `components/custom/` with no clear meaning
- Custom components inside `components/ui/`
- Huge flat `lib/` (10+ unrelated files)
- Huge flat `hooks/`
- `services/` at root with mixed frontend/backend logic
- All actions in one root `actions/` folder
- Feature code scattered across `components`, `hooks`, `lib`, and `app`
- Route handlers with direct complex Prisma/database logic
- Client components importing server-only modules
- Barrel exports that expose private internals
- Duplicate component systems with conflicting button/card/input primitives

> For the complete anti-patterns catalog with examples, read `references/anti-patterns.md`.

## Output modes

Choose the mode that matches the user request. Read `references/output-templates.md` for the full templates.

| User intent | Mode |
|---|---|
| Asks what architecture to adopt | Architecture recommendation |
| Shares a folder tree or files | Existing project audit |
| Asks where to put a file | File placement answer |
| Wants instructions for a coding agent | Agent instruction prompt |
| Wants a downloadable doc | Downloadable skill/document |

## Architecture quality checklist

Before finalizing any recommendation, verify:

- [ ] `app/` is not overloaded with global logic
- [ ] `components/ui/` remains library-primitives only
- [ ] Custom reusable components have a separate home
- [ ] Feature-specific logic is not dumped in `lib/`
- [ ] Server-only code is isolated
- [ ] API routes and actions are thin
- [ ] Naming is predictable
- [ ] The structure works without `src/` when the user prefers no `src/`
- [ ] The solution is understandable for juniors
- [ ] The migration can be done incrementally

## Tone

Be direct, practical, and implementation-oriented. Prefer clear rules over abstract explanations. When the user is frustrated by chaos, respond with a concrete cleanup plan instead of theory.

## Reference files

Read these files from the `references/` directory when you need deeper guidance:

- `references/folder-responsibilities.md` — Detailed rules for each folder (`app/`, `features/`, `components/`, `server/`, `lib/`, `hooks/`, `types/`, `config/`)
- `references/refactoring-playbook.md` — Step-by-step process for auditing and migrating messy projects
- `references/output-templates.md` — Exact output formats for each output mode
- `references/anti-patterns.md` — Full catalog of anti-patterns with examples and fixes
