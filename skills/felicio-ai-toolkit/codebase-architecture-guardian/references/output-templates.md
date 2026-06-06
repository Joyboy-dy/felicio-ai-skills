# Output Templates

Exact output formats for each mode the skill supports. Use the template that matches the user's request.

---

## Architecture Recommendation

Use when the user asks what architecture to adopt for a new or existing project.

```markdown
## Architecture recommandée

[Brief explanation of the approach and why it fits the project]

```txt
[Target tree — only show folders/files relevant to the project size]
```

## Règles de placement

[Clear, numbered rules for where different types of code go]

1. ...
2. ...
3. ...

## À éviter

[Specific anti-patterns to watch out for in this context]

- ...
- ...
```

---

## Existing Project Audit

Use when the user shares a folder tree, file listing, or asks you to review their project structure.

```markdown
## Diagnostic

[Direct findings — state facts about what you observe]

## Problèmes prioritaires

[Ranked list of issues by severity/impact]

1. **Critique** — [issue]
2. **Important** — [issue]
3. **Mineur** — [issue]

## Structure cible

```txt
[Target tree for this specific project]
```

## Plan de migration

[Phased plan with clear boundaries]

### Phase 1 : [Name]
- ...

### Phase 2 : [Name]
- ...

## Déplacements recommandés

[Concrete move list]

Move:
- `[source path]`
  → `[target path]`
  Raison : [short reason]

Keep:
- `[path]` — [why it's correct]
```

---

## File Placement Answer

Use when the user asks "where should I put this file?" or "where does X go?"

```markdown
Place-le ici :

```txt
[exact target path]
```

Raison : [short, clear reason based on the placement decision tree]

Imports recommandés :

```ts
[example import statements for this file]
```
```

Keep file placement answers short and direct. The user wants a quick answer, not a lecture.

---

## Agent Instruction Prompt

Use when the user wants instructions they can give to a coding agent (Claude, Cursor, Copilot, etc.) to execute a specific refactoring or architectural change.

The prompt should be strict, self-contained, and executable:

```markdown
## Instruction de refactoring

### Objectif
[One sentence describing the goal]

### Contraintes
- Ne modifie PAS [what to preserve]
- Ne touche PAS [what to leave alone]
- Préserve le comportement existant
- Exécute `tsc --noEmit` et `next build` après chaque changement

### Changements à effectuer

1. Créer `[path]` avec [description]
2. Déplacer `[source]` → `[target]`
3. Mettre à jour les imports dans [affected files]
4. ...

### Règles d'imports
- Utilise `@/` pour les imports inter-dossiers
- Utilise les imports relatifs pour les fichiers proches
- Ne fais jamais d'import profond dans un autre feature

### Critères d'acceptation
- [ ] `tsc --noEmit` passe sans erreur
- [ ] `next build` réussit
- [ ] Aucun import circulaire
- [ ] Les tests existants passent
```

---

## Downloadable Skill / Document

Use when the user asks to create a file they can download, save, or share.

Produce the file with proper formatting and provide a clear path. If the user asks for an AGENTS.md, ARCHITECTURE.md, or similar document, generate it with project-specific rules based on the conversation context.
