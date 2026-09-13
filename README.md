# felicio-ai-skills

[![skills.sh](https://skills.sh/b/Joyboy-dy/felicio-ai-skills)](https://skills.sh/Joyboy-dy/felicio-ai-skills)

A project-neutral collection of reusable Agent Skills for frontend engineering, interface quality, codebase architecture, forms, color systems, Next.js architecture, and container delivery.

Every skill is self-contained under `skills/<skill-name>/` and follows the Agent Skills directory convention: a required `SKILL.md`, with optional `scripts/`, `references/`, `assets/`, and `evals/` resources loaded only when useful.

## Installation

Install the complete collection with pnpm:

```bash
pnpm dlx skills add Joyboy-dy/felicio-ai-skills
```

Or with npm:

```bash
npx skills add Joyboy-dy/felicio-ai-skills
```

Install one skill:

```bash
pnpm dlx skills add Joyboy-dy/felicio-ai-skills --skill ux-ui-audit
```

Replace `ux-ui-audit` with any skill name from the catalog below.

## Optional companion skills

Felicio AI Skills does not require any external skill. When a project's stack makes another maintainer's expertise useful, the repository documents optional companions instead of bundling or auto-installing them.

Common examples:

```bash
# Official shadcn/ui project context and CLI conventions
pnpm dlx skills add shadcn/ui

# React/Next.js performance guidance from Vercel Engineering
pnpm dlx skills add vercel-labs/agent-skills --skill vercel-react-best-practices

# Additional web interface implementation guidelines from Vercel
pnpm dlx skills add vercel-labs/agent-skills --skill web-design-guidelines
```

These are recommendations, not dependencies. Install them only when the project and task match their domain. See [`docs/COMPANION_SKILLS.md`](docs/COMPANION_SKILLS.md) for the pairing matrix, Supabase/Postgres recommendations, community options, and recommendation policy.

## Skills

| Skill                               | Use it for                                                                             | Do not use it as                                        |
| ----------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `chromatic-design`                  | Color tokens, palette construction, dark/light pairing, contrast                       | A general visual redesign skill                         |
| `codebase-architecture-guardian`    | Repository archaeology, boundaries, dependency direction, safe refactors               | A framework-specific implementation guide               |
| `container-compose-ghcr-deployment` | Docker/Compose/GHCR packaging, CI image delivery, runtime separation                   | A requirement to use containers locally                 |
| `form-ux-validation`                | Form behavior, dirty state, validation, errors, navigation guards, accessibility       | A mandate for a particular form or schema library       |
| `frontend-aesthetics`               | Art direction, visual hierarchy, spacing, typography, polish                           | A structural architecture review                        |
| `nextjs-architecture-pattern`       | Next.js routing, server/client boundaries, data flow, route structure                  | Generic frontend architecture outside Next.js           |
| `responsive-interface-guardian`     | Responsive layout audits, content-driven breakpoints, overflow and viewport validation | A greenfield visual redesign skill                      |
| `senior-frontend-engineering`       | Implementation quality, ownership, state, contracts, maintainability                   | A visual-only audit                                     |
| `ui-modern-2026`                    | Progressive use of modern CSS/UI capabilities and graceful fallbacks                   | A requirement to chase novelty or one component library |
| `ux-ui-audit`                       | Evidence-based audit of an existing interface, states, responsiveness, accessibility   | Greenfield art direction                                |

## How agents should use this repository

Agents should activate the smallest skill whose trigger matches the task. Skills may compose, but their responsibilities should remain separate: for example, `ux-ui-audit` identifies interface problems, `frontend-aesthetics` proposes visual direction, and `senior-frontend-engineering` implements robust code changes.

Read [`docs/SKILLS_GUIDE.md`](docs/SKILLS_GUIDE.md) for the activation matrix, overlap rules, and bundled script index. Read [`docs/COMPANION_SKILLS.md`](docs/COMPANION_SKILLS.md) for optional external skill recommendations. Read [`docs/AUTHORING.md`](docs/AUTHORING.md) before adding or changing a skill.

## Development

Install repository tooling:

```bash
pnpm install
```

Format the repository:

```bash
pnpm format
```

Run all repository checks:

```bash
pnpm check
```

List the catalog and bundled resources:

```bash
pnpm catalog
```

The local validator enforces the repository's portability policy, resource references, maximum `SKILL.md` length, evaluation fixtures, and Python helper syntax.

When `skills-ref` is available, also run the reference validator against each skill:

```bash
for skill in skills/*; do skills-ref validate "$skill"; done
```

## Versioning

The repository follows semantic versioning for repository releases. The fresh public collection starts at `1.0.0`.

Before tagging a release, make sure the working tree is clean and run:

```bash
pnpm check
git tag -a v1.0.0 -m "felicio-ai-skills v1.0.0"
git push origin v1.0.0
```

Future releases should increment the version in `package.json` and use matching Git tags.

## License

MIT. See [`LICENSE`](LICENSE).
