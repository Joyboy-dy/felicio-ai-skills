# Skill usage guide

This guide answers three questions for an agent: **which skill should activate, what is it responsible for, and which other skill should take over at a boundary?**

## Activation matrix

| User intent or repository signal                                          | Primary skill                       | Common companion                                    |
| ------------------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------- |
| “Choose/fix our colors”, token pairing, dark mode contrast                | `chromatic-design`                  | `ux-ui-audit` when auditing an existing UI          |
| “Understand this codebase”, “where should this live?”, architecture drift | `codebase-architecture-guardian`    | Domain implementation skill                         |
| Dockerfile, Compose, image build, GHCR, container CI                      | `container-compose-ghcr-deployment` | `codebase-architecture-guardian` for repository fit |
| Form validation, unsaved changes, error messages, submit flow             | `form-ux-validation`                | `senior-frontend-engineering` for implementation    |
| “Make this UI feel better/premium/coherent”                               | `frontend-aesthetics`               | `chromatic-design` for palette work                 |
| Next.js App/Pages Router, route groups, server/client boundaries          | `nextjs-architecture-pattern`       | `senior-frontend-engineering`                       |
| Responsive breakpoints, overflow, collisions, viewport/zoom validation    | `responsive-interface-guardian`     | `ux-ui-audit` for broader interface findings        |
| Frontend feature/refactor with state, API, components, tests              | `senior-frontend-engineering`       | Framework-specific skill if present                 |
| Modern CSS capabilities, progressive enhancement, newer UI primitives     | `ui-modern-2026`                    | `frontend-aesthetics`                               |
| “Audit this interface”, accessibility/state/responsive review             | `ux-ui-audit`                       | `frontend-aesthetics` after findings                |

## Composition rules

1. **Audit before redesign when the task starts from an existing interface.** `ux-ui-audit` records evidence and severity; it should not silently turn into a redesign.
2. **Architecture before broad refactor.** `codebase-architecture-guardian` discovers ownership and dependencies; implementation skills then make the change.
3. **Domain-specific beats generic.** On a Next.js architecture question, `nextjs-architecture-pattern` owns routing and rendering boundaries while `senior-frontend-engineering` owns broader frontend implementation quality.
4. **Color is its own system.** `chromatic-design` owns palette/tokens/contrast; `frontend-aesthetics` may consume those decisions but should not invent an unrelated color system.
5. **Containers are optional infrastructure.** `container-compose-ghcr-deployment` activates because the task involves containers, not because every project should adopt them.
6. **Detect before prescribing.** Every skill must inspect the current project before naming libraries, folder structures, package managers, test runners, CI providers, or deployment targets.
7. **Responsive robustness is a dedicated concern.** `responsive-interface-guardian` owns content-driven breakpoints, overflow/collision fixes, viewport/zoom validation, and responsive regression checks; `ux-ui-audit` remains responsible for broader evidence-based interface audits and accessibility/state findings.

## Project-neutrality policy

“Project-neutral” does not mean “vague.” A skill may be highly specific to a technology or problem domain, but it must not assume one private product, company, repository layout, language, package manager, hosting provider, design system, or database unless that is the skill's explicit domain.

Agents should preserve existing conventions unless the task explicitly requests a migration. Examples in references are illustrative, not hidden requirements.

## Optional external companions

Felicio skills must remain fully usable without external skills. If the current repository clearly uses a technology covered by a complementary maintainer-owned skill, an agent may recommend that skill as an optional addition. It must not auto-install it, make it a prerequisite, or silently change the task to match the companion.

Use [`COMPANION_SKILLS.md`](COMPANION_SKILLS.md) as the maintained recommendation catalog. In particular:

- recommend the official `shadcn/ui` skill only when the project actually uses shadcn/ui;
- consider Vercel's `vercel-react-best-practices` for React/Next.js performance work;
- consider Vercel's `web-design-guidelines` as an additional implementation checklist for interface reviews;
- consider Supabase's skills only when the project actually uses Supabase/Postgres and the task reaches that layer;
- label community companions explicitly and prefer maintainer-backed sources when scopes overlap.

When a companion and a Felicio skill overlap, avoid duplicate output. The narrower domain expert supplies its specialty while the Felicio skill keeps ownership of the workflow documented in its own `SKILL.md`.

## Bundled script index

Scripts are optional accelerators. Agents should read `--help` first when arguments are unclear, prefer read-only/default modes, and treat static scans as evidence to investigate rather than proof of correctness.

| Skill                               | Script                               | Purpose                                                                     |
| ----------------------------------- | ------------------------------------ | --------------------------------------------------------------------------- |
| `chromatic-design`                  | `scripts/color_tools.py`             | Calculate contrast and scan color literals/tokens                           |
| `codebase-architecture-guardian`    | `scripts/inventory_codebase.py`      | Produce a compact repository inventory and framework hints                  |
| `container-compose-ghcr-deployment` | `scripts/container_preflight.py`     | Inspect container/Compose/GitHub workflow files without building by default |
| `form-ux-validation`                | `scripts/scan_form_ux.py`            | Find form patterns, validation, error, dirty-state and submit signals       |
| `form-ux-validation`                | `scripts/scan_validation_libs.py`    | Detect validation libraries/patterns without prescribing one                |
| `form-ux-validation`                | `scripts/scan_notification_usage.py` | Locate toast/notification usage around form flows                           |
| `form-ux-validation`                | `scripts/compare_schema_fields.py`   | Compare two explicit field lists/schema-like JSON objects                   |
| `frontend-aesthetics`               | `scripts/scan_visual_smells.py`      | Locate repeated raw styling values and visual inconsistency candidates      |
| `nextjs-architecture-pattern`       | `scripts/scan_nextjs_app.py`         | Detect router mode, Next.js version, route files and client boundaries      |
| `responsive-interface-guardian`     | `scripts/audit-viewports.mjs`        | Run the responsive viewport matrix with Playwright when already available   |
| `senior-frontend-engineering`       | `scripts/frontend_health.py`         | Inventory frontend scale/ownership smells and test/config signals           |
| `ui-modern-2026`                    | `scripts/scan_modern_css.py`         | Locate modern CSS features and fallback/support signals                     |
| `ux-ui-audit`                       | `scripts/scan_a11y_static.py`        | Static accessibility triage for common markup/JSX issues                    |

## Expected agent output

Unless the user asks for another format, a skill should produce: the discovered context and assumptions; prioritized findings or plan; exact files/areas affected; implementation or recommendations; validation performed; and remaining uncertainty. It must distinguish **observed facts**, **inferences**, and **recommendations**.
