# Authoring and maintenance policy

Use this document when adding or revising a skill in this repository.

## 1. Scope one reusable capability

A skill should encode a coherent procedure that applies across many repositories in its domain. Preserve hard-earned edge cases and workflows, but remove private product names, one-off paths, organization-specific assumptions, and conclusions that only make sense for the original source project.

A technology-specific skill is acceptable. A Next.js skill can be Next.js-specific; a GHCR skill can be GHCR-specific. The problem is hidden coupling, not domain specificity.

## 2. Frontmatter

Every `skills/<name>/SKILL.md` must start with `name` and `description`. The `name` must exactly match the folder. Keep descriptions concrete: say what the skill does and include trigger phrases or task keywords that make activation predictable.

Do not put compatibility claims in `description`. Use optional compatibility metadata only when a real runtime dependency exists.

## 3. Progressive disclosure

Keep the main workflow in `SKILL.md` and keep it below 500 lines. Move detailed tables, examples, formulae, framework branches, and long checklists into `references/`. Mention each reference from `SKILL.md` at the point where an agent would know it needs that file.

References should be one level below the skill root. Avoid chains where one reference requires another reference to understand it.

## 4. Scripts

Bundle a script when agents would otherwise repeatedly reimplement deterministic discovery, parsing, validation, or reporting logic. Scripts in this repository should:

- be non-interactive;
- be read-only by default unless mutation is the explicit purpose;
- expose `--help`;
- return non-zero on invalid input or execution failure;
- write machine-readable JSON when structured results are useful;
- keep diagnostics distinct from primary output where practical;
- use safe defaults and bounded scans;
- document external dependencies; prefer the Python standard library for small repository scanners;
- never read secrets by default.

A static scanner is a triage tool, not a replacement for runtime testing, accessibility tooling, compilation, or human judgment.

## 5. Detect before prescribing

Before recommending a library or pattern, inspect the repository for the existing stack and conventions. Do not silently migrate package managers, validation libraries, form libraries, routing models, state libraries, CSS systems, component libraries, deployment providers, databases, or test runners.

If the repository already has a sound convention, integrate with it. If several options are valid, prefer the existing one unless the user's goal requires change.

## 6. Evaluations

Each skill includes `evals/evals.json` with at least two representative tasks. Include a positive/normal case and a boundary or negative case that verifies the skill does not over-trigger or overreach. Prefer objective expectations that can be checked from an output or repository diff.

When materially changing a skill, compare behavior on the same eval cases before and after the edit where possible.

## 7. Overlap control

State “use when” and “do not use when” boundaries in the skill. If another skill owns an adjacent concern, name the handoff. This prevents multiple broad skills from giving contradictory instructions.

## 8. Validation before publishing

From the repository root:

```bash
python scripts/validate_skills.py
python -m compileall -q scripts skills
```

Then, when the official reference validator is installed:

```bash
for skill in skills/*; do skills-ref validate "$skill"; done
```

Finally inspect the repository for secrets, absolute local paths, stale project names, unreferenced helper files, and generated artifacts before publishing.
