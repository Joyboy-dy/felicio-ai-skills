# Felicio AI Skills Toolkit 🚀

Un écosystème complet pour distribuer et installer mes skills Claude Code optimisés pour le développement moderne via NPX.

## 🛠 Installation

Vous avez deux façons d'utiliser ce toolkit selon vos besoins.

### 1. Installation Globale (Recommandée)
Idéal si vous travaillez sur plusieurs projets. Installez une seule fois et partagez les skills.

```bash
# Installe les skills dans un dossier global (~/.felicio-ai-skills/)
npx @joyboy-dy/felicio-ai-skills init --global

# Liez le dossier global à votre projet actuel (crée un lien symbolique vers .agents/skills)
npx @joyboy-dy/felicio-ai-skills link
```

### 2. Installation Individuelle (Par Projet)
Si vous ne voulez que certains skills spécifiques dans un projet donné :

```bash
# Installer TOUS les skills localement dans le projet (Variante de 'init')
npx @joyboy-dy/felicio-ai-skills add --all

# Installer UN skill spécifique localement
npx @joyboy-dy/felicio-ai-skills add <nom-du-skill>
```

---

## 📜 Commandes Disponibles

| Commande | Argument | Description |
| :--- | :--- | :--- |
| `list` | - | Affiche la liste de tous les skills disponibles |
| `init` | `--global` / `-g` | Installe les skills globalement ou localement |
| `add` | `<name>` / `--all` | Installe un ou tous les skills localement dans `.agents/skills/` |
| `link` | `--dir <path>` | Relie les skills globaux au projet (défaut: `.agents/skills`) |
| `unlink` | `--dir <path>` | Supprime le lien symbolique du projet |

---

## 🌟 Skills Inclus & Installation Directe

Voici la liste des skills disponibles avec leurs commandes d'installation individuelle :

### 🎨 Felicio AI Toolkit (Premium)
| Skill | Description | Commande d'installation |
| :--- | :--- | :--- |
| `frontend-aesthetics` | Design system patterns & modern aesthetics | `npx @joyboy-dy/felicio-ai-skills add frontend-aesthetics` |
| `nextjs-architecture-pattern` | Next.js best practices & folder structure | `npx @joyboy-dy/felicio-ai-skills add nextjs-architecture-pattern` |
| `ui-modern-2026` | Premium UI components & references for 2026 | `npx @joyboy-dy/felicio-ai-skills add ui-modern-2026` |
| `ux-ui-audit` | Comprehensive UX/UI audit checklist | `npx @joyboy-dy/felicio-ai-skills add ux-ui-audit` |

### 🧠 Core Skills
| Skill | Description | Commande d'installation |
| :--- | :--- | :--- |
| `supabase-postgres-best-practices` | Expert guidelines for Postgres & Supabase | `npx @joyboy-dy/felicio-ai-skills add supabase-postgres-best-practices` |
| `accessibility-compliance` | Web accessibility & WCAG compliance guide | `npx @joyboy-dy/felicio-ai-skills add accessibility-compliance` |
| `code-review-excellence` | Professional code review guidelines | `npx @joyboy-dy/felicio-ai-skills add code-review-excellence` |
| `codebase-cleanup-refactor-clean` | Refactoring & cleanup strategies | `npx @joyboy-dy/felicio-ai-skills add codebase-cleanup-refactor-clean` |
| `design-system-patterns` | Modular design system architecture | `npx @joyboy-dy/felicio-ai-skills add design-system-patterns` |
| `responsive-design` | Modern adaptive design principles | `npx @joyboy-dy/felicio-ai-skills add responsive-design` |
| `tailwind-design-system` | Advanced Tailwind CSS patterns | `npx @joyboy-dy/felicio-ai-skills add tailwind-design-system` |
| `ui-ux-pro-max` | Ultimate guide for premium interface design | `npx @joyboy-dy/felicio-ai-skills add ui-ux-pro-max` |

---

## 🚀 Publication (GitHub Packages)

Le package est automatiquement publié sur GitHub Packages via GitHub Actions à chaque push sur la branche `main`. Vous devez être authentifié avec votre token GitHub pour l'installer.

---
*Maintenu par [Joyboy-dy](https://github.com/Joyboy-dy)*

