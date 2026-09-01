---
name: nextjs-architecture-pattern
description: "Use when designing, reviewing, or refactoring a Next.js application: App Router or Pages Router structure, server/client boundaries, route organization, data fetching, caching, mutations, metadata, loading/error boundaries, or Next.js-specific architecture."
---

# Next.js Architecture Pattern

Apply Next.js architecture according to the **installed version and router actually used by the repository**.

## Use when

Activate for Next.js routing/rendering architecture, App Router/Pages Router decisions, Server vs Client Components, route handlers/API routes, data fetching/caching/revalidation, layouts, loading/error/not-found boundaries, metadata, or route-group organization.

Do not force App Router migration on a Pages Router project unless requested. Do not hard-code patterns from one Next.js major version without checking the installed version and project configuration.

## Detect first

Run:

```bash
python scripts/scan_nextjs_app.py <project-root> --json
```

Then inspect `package.json`, Next config, TypeScript config, root route directories, middleware/proxy files, representative layouts/pages, and existing data-access/mutation patterns.

Record:

- installed Next.js version;
- `app/`, `pages/`, or hybrid routing;
- source root (`src/` or repository root);
- server/client boundary conventions;
- styling/component system;
- authentication/data layer only if present;
- test/build scripts.

## App Router workflow

When `app/` is used:

1. Keep route files focused on composition and route-specific orchestration.
2. Prefer Server Components by default when they do not need browser-only APIs, local interactive state, effects, or event handlers.
3. Place `'use client'` at the smallest useful interactive boundary. Do not convert a whole route tree to client rendering to satisfy one widget.
4. Keep serializable props crossing server→client boundaries. Avoid passing server-only resources or functions except framework-supported server actions/patterns for the detected version.
5. Use route segments, layouts, loading/error/not-found boundaries according to user-visible behavior, not as folder decoration.
6. Keep domain/data-access code outside route files when it is reusable or needs independent testing.
7. Treat caching/revalidation as correctness behavior. Never copy caching advice from a different Next.js version without verification.

Read `references/app-router-boundaries.md` for boundary reasoning.

## Pages Router workflow

When `pages/` is used, preserve its routing/data-fetching model. Use the repository's established API routes, SSR/SSG/client-fetching strategy, `_app`/`_document` patterns, and router APIs. Do not introduce App Router-only files or hooks unless migrating deliberately.

## Data fetching and mutations

Start from the data source and freshness requirement:

- who is allowed to read/write;
- where credentials/server-only SDKs can execute;
- whether data is request-specific, cached, revalidated, or static;
- what mutation invalidates or refreshes;
- what error/pending state the user sees.

Keep secret-bearing data access server-side. Do not assume a specific database, auth provider, RPC layer, query library, or ORM.

Read `references/implementation-patterns.md` when deciding data/mutation placement.

## Route organization

Organize by user-facing route/feature first, then extract reusable domain/components where ownership is clear. Route groups and private folders should clarify URL/layout ownership, not create a universal folder template.

Avoid duplicating the same business rule in a page, route handler, and client hook.

## Runtime boundaries

Verify whether code targets Node.js, Edge, or browser runtime before using APIs or packages. A package that works in Node may not work in Edge/browser bundles. Keep server-only modules out of client import graphs.

## Validation

After changes, run the repository's real checks and inspect relevant routes. Common validation targets include:

- TypeScript/lint;
- Next.js production build;
- route behavior and status handling;
- loading/error/not-found states;
- client bundle boundary warnings;
- hydration/runtime console errors;
- auth/data authorization at the server boundary;
- cache/revalidation behavior when changed.

Do not claim a rendering/caching issue fixed from static code inspection alone when runtime verification is available.

## Common failure modes

- Assuming every Next.js project uses the newest App Router conventions.
- Marking broad component trees `'use client'` unnecessarily.
- Importing server-only modules into client code.
- Fetching protected data client-side only because it is convenient.
- Treating route folder structure as domain architecture.
- Hard-coding one database/auth vendor into a general Next.js pattern.
- Applying stale caching APIs from a different installed version.
- Adding loading/error boundaries without deciding what the user should experience.
- Hiding an architecture problem behind dynamic imports.

## Output

State the detected Next.js version/router, relevant route/runtime boundaries, architectural decision, exact files affected, version-sensitive assumptions, validations performed, and any runtime behavior still unverified.
