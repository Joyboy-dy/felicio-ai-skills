# Refactoring Playbook

Step-by-step process for auditing and migrating a messy codebase into a clean architecture.

## Table of Contents

1. [Step 1: Diagnose](#step-1-diagnose)
2. [Step 2: Classify files](#step-2-classify-files)
3. [Step 3: Propose target structure](#step-3-propose-target-structure)
4. [Step 4: Plan migration safely](#step-4-plan-migration-safely)
5. [Step 5: Add guardrails](#step-5-add-guardrails)

---

## Step 1: Diagnose

When the user provides an existing chaotic tree, identify:

- **Oversized folders** — any folder with 20+ files without subcategories
- **Duplicate concepts** — two folders doing the same job (e.g., `utils/` and `lib/`)
- **Ambiguous folder names** — `helpers/`, `shared/`, `common/`, `misc/`
- **Mixed server/client code** — server imports in client components or vice versa
- **Library primitives mixed with custom components** — shadcn files next to product components
- **Feature logic hidden in `lib/`** — auth, billing, email buried in utilities
- **Route-specific files placed globally** — one-off components in `components/`
- **Global components that are actually domain-specific** — `SubscriptionCard` in `components/`
- **Deep imports that bypass public APIs** — reaching into `features/auth/lib/internal/`

### Diagnostic output format

```markdown
## Diagnostic

### Oversized folders
- `lib/` contains 23 files with mixed responsibilities (auth, billing, db, utils)
- `components/my-components/` has 28 files with no subdomain organization

### Mixed concerns
- `lib/auth.ts` contains server-only logic but is imported in client components
- `lib/billing-actions.ts` is a Server Action hidden in utilities

### Misplaced files
- `components/ui/dashboard-card.tsx` is domain-specific, should be in features/
- `hooks/useSubscription.ts` is billing-specific, should be in features/billing/hooks/

### Missing boundaries
- No feature modules: all domain logic is scattered across lib, hooks, and components
- No server/ directory: backend logic mixed with frontend utilities
```

---

## Step 2: Classify files

Classify each file into one of these buckets:

| Bucket | Description |
|---|---|
| `routing` | page.tsx, layout.tsx, route.ts, loading.tsx, error.tsx |
| `route-local-ui` | Components used only by one route |
| `domain-feature` | Business logic tied to a domain (auth, billing, etc.) |
| `shared-ui-primitive` | Generic reusable components (buttons, tables, badges) |
| `shared-layout` | Navbars, sidebars, app shells |
| `provider` | React context providers |
| `server-db` | Database client and connection |
| `server-service` | Business rules and orchestration |
| `server-repository` | Data access layer |
| `server-integration` | External API clients |
| `generic-utility` | cn(), formatDate(), slugify() |
| `global-type` | Types shared across unrelated domains |
| `config` | Environment, feature flags, site metadata |
| `asset` | Images, fonts, static files |
| `deprecated-or-duplicate` | Dead code, unused files, duplicated systems |

---

## Step 3: Propose target structure

Give a clear before/after plan. Use this format:

```markdown
## Proposed moves

Move:
- `components/my-components/auth/login-form.tsx`
  → `features/auth/components/login-form.tsx`
  Reason: domain-specific auth component reused outside one route.

- `components/ui/base-button.tsx`
  → `components/base/button.tsx`
  Reason: custom wrapper must not live inside shadcn/ui.

- `lib/billing-actions.ts`
  → `features/billing/actions/billing.ts`
  Reason: billing actions belong in the billing feature module.

- `lib/prisma.ts`
  → `server/db/prisma.ts`
  Reason: database client is backend-only infrastructure.

- `lib/email.ts`
  → `server/mail/email.ts`
  Reason: email sending is backend-only server logic.

- `hooks/useSubscription.ts`
  → `features/billing/hooks/use-subscription.ts`
  Reason: subscription hook is billing-domain-specific.

Keep:
- `lib/utils.ts` — small generic utility, correct placement.
- `components/ui/button.tsx` — shadcn primitive, correct placement.
```

---

## Step 4: Plan migration safely

Prefer phased migration over big-bang rewrites. Each phase should be independently mergeable and should not break the running app.

### Recommended phases

```txt
Phase 1: Freeze conventions
  - Document naming rules
  - Add AGENTS.md or ARCHITECTURE.md
  - Agree on folder structure

Phase 2: Move obvious UI conflicts
  - Extract custom components from components/ui/ to components/base/
  - Move layout components to components/layouts/
  - Move providers to components/providers/

Phase 3: Extract features one domain at a time
  - Start with the most isolated domain
  - Move components, actions, hooks, types, schemas together
  - Update imports across the codebase
  - Run tests/build after each domain

Phase 4: Move backend logic from lib to server
  - Create server/db/, server/services/, server/repositories/
  - Move database client
  - Move business logic
  - Move integrations (email, storage, etc.)

Phase 5: Clean imports and remove dead files
  - Update all import paths to @/ aliases
  - Remove barrel exports that leak internals
  - Delete empty or deprecated files
  - Run typecheck and lint

Phase 6: Add architecture guardrails
  - ESLint import/no-restricted-paths rules
  - Folder README files for complex domains
  - CI checks (typecheck, lint, build)
```

### Safety rules

- Never move more than one domain per PR if possible.
- Always run `tsc --noEmit`, `eslint`, and `next build` after each phase.
- Keep a migration notes file to track what moved and why.
- If something breaks mid-migration, revert that phase — don't push forward.
- Test the running app after each phase, not just at the end.

---

## Step 5: Add guardrails

After migration, recommend guardrails to prevent regression:

### AGENTS.md / ARCHITECTURE.md

Write a brief architecture document at the project root that tells any contributor (human or AI) where things go:

```markdown
# Architecture Rules

- `components/ui/` = shadcn primitives ONLY. Never put custom components here.
- `components/base/` = reusable generic components.
- `features/[domain]/` = all domain-specific code (components, actions, hooks, types).
- `server/` = backend-only code. Never import in client components.
- `lib/` = tiny stateless utilities only. Max 15 files.
- Barrel exports in features expose public API only.
```

### ESLint boundaries

Recommend rules like `import/no-restricted-paths` to enforce dependency direction:

```js
// Prevent components/ui from importing features
{
  "zones": [
    {
      "target": "./components/ui/**",
      "from": "./features/**",
      "message": "UI primitives must not import from features."
    }
  ]
}
```

### Naming conventions

- Files: `kebab-case.tsx`
- Hooks: `use-kebab-case.ts`
- Types files: `types.ts` inside feature, or `kebab-case.ts` in `types/`
- Actions: `kebab-case.ts` with `"use server"` directive
- Repositories: `entity.repository.ts`
- Services: `entity.service.ts`

### CI checks

Always recommend:

```bash
# Minimum CI pipeline
tsc --noEmit          # Type safety
eslint .              # Code quality
next build            # Build integrity
```
