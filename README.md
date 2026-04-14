# Felicio AI Skills Toolkit 🚀

A complete ecosystem for distributing and installing Claude Code skills via NPX and GitHub Packages.

## 🛠 Installation (Recommended)

Install once on your machine and share across all projects:

```bash
# 1. Install global storage
npx @joyboy-dy/felicio-ai-skills init --global

# 2. Link to any project (default to .claude/skills)
npx @joyboy-dy/felicio-ai-skills link
```

*Note: You can specify a custom directory with `link --dir .agents/skills`.*

## 📜 Available Commands

| Command | Description |
| :--- | :--- |
| `init` | Installs skills locally in `.claude/skills/` |
| `init --global` | Installs skills globally in `~/.felicio-ai-skills/` |
| `link` | Links global skills to current project |
| `link --dir <path>` | Links global skills to a specific directory |
| `unlink` | Removes the link from current project |
| `list` | Displays the list of all available skills |
| `add <name>` | Installs a specific skill locally |

## 🌟 Included Skills

### Felicio AI Toolkit
- **frontend-aesthetics**: Design system patterns and modern aesthetics.
- **nextjs-architecture-pattern**: Next.js best practices and architecture patterns.
- **ui-modern-2026**: Premium UI components and design references for 2026.
- **ux-ui-audit**: Comprehensive UX/UI audit checklist.

### Core Skills
- **accessibility-compliance**: Web accessibility and WCAG compliance guide.
- **code-review-excellence**: Professional code review guidelines.
- **codebase-cleanup-refactor-clean**: Refactoring and cleanup strategies.
- **design-system-patterns**: Modular design system architecture.
- **responsive-design**: Modern adaptive design principles.
- **tailwind-design-system**: Advanced Tailwind CSS patterns and configurations.
- **ui-ux-pro-max**: The ultimate guide for premium interface design.

## 🚀 Publishing (GitHub Packages)

The package is automatically published to GitHub Packages via GitHub Actions upon every push to the `main` branch.

---
*Maintained by [Joyboy-dy](https://github.com/Joyboy-dy)*
