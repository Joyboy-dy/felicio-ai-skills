# Optional companion skills

Felicio AI Skills is designed to work on its own. The skills listed here are **optional companions**, not dependencies, prerequisites, or hidden requirements.

Install a companion only when its domain matches the project you are working on. Do not install every recommendation by default, and do not let an external skill override the repository's existing conventions without a reason tied to the task.

> Last reviewed: 2026-11-13. External repositories and skill names can change. Re-check the maintainer's current documentation before publishing a release that changes these recommendations.

## Recommendation policy

A companion belongs in this guide only when it adds knowledge that Felicio intentionally does not duplicate.

- Prefer maintainer-owned or official skills when one exists.
- Label community skills explicitly.
- Keep every recommendation optional and contextual.
- Never make a Felicio skill fail because a companion is absent.
- Do not auto-install companions from a Felicio script.
- Prefer the project's current stack over introducing a tool just because a companion supports it.
- When two skills overlap, use the narrower domain expert for its specialty and keep Felicio responsible for its documented scope.

## Maintainer-backed companions

### shadcn/ui

**Source:** shadcn/ui maintainers  
**Install:**

```bash
pnpm dlx skills add shadcn/ui
```

Use it when the project actually uses shadcn/ui or contains `components.json`.

It complements Felicio by providing project-aware shadcn/ui knowledge: installed components, aliases, Tailwind version, base primitive library, icon library, registry usage, theming conventions, and current CLI workflows.

Good pairings:

- `chromatic-design` — Felicio owns palette logic, semantic color relationships, and contrast analysis; the shadcn skill owns shadcn-specific theme and component conventions.
- `form-ux-validation` — Felicio owns validation UX, dirty state, submit behavior, error presentation, and navigation safety; the shadcn skill owns shadcn-specific form/component composition.
- `frontend-aesthetics` — Felicio owns art direction and polish; the shadcn skill helps implement that direction using the project's actual component system.
- `ui-modern-2026` — Felicio owns progressive enhancement and modern platform capabilities; the shadcn skill provides current component-library context.
- `ux-ui-audit` — Felicio owns evidence-based audit methodology; the shadcn skill helps distinguish project conventions from accidental drift.

Do **not** recommend it merely because the task is frontend work. A non-shadcn project does not benefit from installing it.

Official documentation: <https://ui.shadcn.com/docs/skills>

### Vercel React Best Practices

**Source:** Vercel Engineering (`vercel-labs/agent-skills`)  
**Install:**

```bash
pnpm dlx skills add vercel-labs/agent-skills --skill vercel-react-best-practices
```

Use it for React or Next.js work where performance, data-fetching waterfalls, bundle size, rendering, server behavior, or re-render cost matter.

Good pairings:

- `nextjs-architecture-pattern` — Felicio owns routing, rendering boundaries, project structure, and architecture fit; Vercel's skill adds performance-specific React/Next.js guidance.
- `senior-frontend-engineering` — Felicio owns maintainability, contracts, ownership, state, and implementation quality; Vercel's skill adds specialized performance review rules.
- `codebase-architecture-guardian` — useful only after the repository is known to be React/Next.js and performance is part of the requested refactor.

Repository: <https://github.com/vercel-labs/agent-skills>

### Vercel Web Design Guidelines

**Source:** Vercel (`vercel-labs/agent-skills`)  
**Install:**

```bash
pnpm dlx skills add vercel-labs/agent-skills --skill web-design-guidelines
```

Use it as a complementary, current checklist for web interface implementation details such as accessibility, focus states, forms, animation, typography, images, navigation state, theming, touch interaction, and internationalization.

Good pairings:

- `ux-ui-audit` — Felicio supplies the audit process, severity model, evidence, responsive/state review, and prioritization; the Vercel skill can supply an additional rule set.
- `form-ux-validation` — useful for implementation-level form and accessibility checks after the form workflow is understood.
- `frontend-aesthetics` — useful as a guardrail after visual direction has been defined, not as a replacement for art direction.

Because the scopes overlap, avoid producing duplicate findings. Consolidate repeated issues and cite the source of the stricter or more specific rule.

Repository: <https://github.com/vercel-labs/agent-skills>

### Supabase Agent Skills

**Source:** Supabase (`supabase/agent-skills`)  
**Install all Supabase skills:**

```bash
pnpm dlx skills add supabase/agent-skills
```

**Install only Postgres best practices:**

```bash
pnpm dlx skills add supabase/agent-skills --skill supabase-postgres-best-practices
```

Recommend this only when the project actually uses Supabase or PostgreSQL and the task reaches database design, SQL performance, connection management, locking, RLS, or schema concerns.

This is deliberately outside Felicio's core frontend/UI scope. It can complement `codebase-architecture-guardian` when architecture work crosses into a Supabase/Postgres data layer, but it should not be suggested for ordinary frontend tasks.

Repository: <https://github.com/supabase/agent-skills>

### TanStack Start and Router (TanStack Intent)

**Source:** TanStack maintainers (`TanStack/router`, skills shipped inside the npm packages)  
**Install (recommended, version-matched to the installed packages):**

```bash
npx @tanstack/intent@latest install
```

**Or through skills.sh:**

```bash
pnpm dlx skills add tanstack/router --skill start-core
pnpm dlx skills add tanstack/router --skill react-start
pnpm dlx skills add tanstack/router --skill router-core
```

Use it when the project depends on `@tanstack/react-start`, `@tanstack/solid-start` or `@tanstack/react-router`. TanStack Intent reads the installed package versions, so the API guidance matches the project. `@tanstack/intent` is labelled alpha.

It complements `tanstack-start-architecture`: the official skills own exact API usage (server functions, middleware, server routes, search params, code splitting, Next.js migration); Felicio owns project layout, execution-boundary decisions, data ownership and validation workflow. When both apply, follow the official skill for API details and Felicio for where code lives.

Current API lookups without installing anything: `https://tanstack.com/start/latest/llms.txt`, the public docs MCP server `https://tanstack.com/mcp`, or `npx @tanstack/cli search-docs "<topic>" --library start --json`.

Repository: <https://github.com/TanStack/router> · Intent: <https://tanstack.com/intent/latest>

### Elysia

**Source:** Elysia maintainers (`elysiajs/skills`)  
**Install:**

```bash
bunx skills add elysiajs/skills
```

Use it only when the project uses Elysia. The skill targets **Elysia 2** (release candidate as of the review date); for an Elysia 1.x project it mainly offers migration guidance, so check the installed version first and fall back to `https://elysiajs.com/llms.txt`.

Repository: <https://github.com/elysiajs/skills>

### Bun

Bun has no official skill for application developers (the skills in `oven-sh/bun` are for contributors to Bun itself). For current Bun APIs, point agents to `https://bun.com/llms.txt` or the official docs MCP server `https://bun.com/docs/mcp`.

## Community companions

Community skills can be useful, but they are not treated as authoritative merely because they are listed here. Review their repository, recent activity, permissions, scripts, and installation behavior before use.

### mattbx/shadcn-skills

This community repository currently exposes focused shadcn companions such as component discovery and component review.

Component discovery:

```bash
pnpm dlx skills add mattbx/shadcn-skills --skill shadcn-component-discovery
```

Component review:

```bash
pnpm dlx skills add mattbx/shadcn-skills --skill shadcn-component-review
```

Potential pairings:

- `frontend-aesthetics` + `shadcn-component-discovery` when you want to search the wider shadcn-compatible registry ecosystem before building a custom component.
- `ux-ui-audit` or `chromatic-design` + `shadcn-component-review` when reviewing shadcn-specific composition, semantic tokens, or hardcoded styling after implementation.

Prefer the official `shadcn/ui` skill for authoritative shadcn project context and CLI behavior. Treat these community skills as narrower additions, not replacements.

Repository: <https://github.com/mattbx/shadcn-skills>

## Pairing matrix

| Felicio skill                       | Recommended companions when relevant                                                                                                                       |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chromatic-design`                  | shadcn/ui for shadcn theme conventions; Vercel Web Design Guidelines for additional UI checks; community shadcn component review after implementation      |
| `codebase-architecture-guardian`    | Vercel React Best Practices for React/Next.js performance refactors; Supabase/Postgres skill when the architecture task crosses into that data layer       |
| `container-compose-ghcr-deployment` | No default companion. Add infrastructure-specific expertise only when the target platform requires it                                                      |
| `form-ux-validation`                | shadcn/ui for shadcn component composition; Vercel Web Design Guidelines for implementation-level form/accessibility checks                                |
| `frontend-aesthetics`               | shadcn/ui for shadcn implementation; Vercel Web Design Guidelines as a quality guardrail; community shadcn discovery for registry exploration              |
| `nextjs-architecture-pattern`       | Vercel React Best Practices; shadcn/ui only when the UI layer actually uses shadcn                                                                         |
| `senior-frontend-engineering`       | Vercel React Best Practices; Vercel Web Design Guidelines when the task includes interface implementation quality                                          |
| `tanstack-start-architecture`       | Official TanStack Start/Router skills via TanStack Intent; Elysia skill when Start talks to an Elysia backend; Vercel React Best Practices for performance |
| `ui-modern-2026`                    | Vercel Web Design Guidelines; shadcn/ui when modern capabilities are being integrated into a shadcn project                                                |
| `ux-ui-audit`                       | Vercel Web Design Guidelines as a second rule set; shadcn/ui or community shadcn review only for shadcn projects                                           |

## How to recommend a companion to a user

Keep the recommendation short and contextual. State three things: **why it fits this project, what it adds, and that it is optional**.

Example:

> This project uses shadcn/ui, so the official `shadcn/ui` skill is a useful optional companion. It gives the agent project-aware shadcn component, registry, and theming context. Felicio's `chromatic-design` still owns palette and contrast decisions; the companion is not required for it to work.

Avoid generic prompts such as “install these five skills for the best experience.” A recommendation without a concrete project signal is noise.
