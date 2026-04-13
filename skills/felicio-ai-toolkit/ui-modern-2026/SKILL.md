---
name: ui-modern-2026
description: >
  Design modern, distinctive, and non-generic user interfaces in 2026.
  Use this skill whenever the user asks to create, improve, style, or rethink
  an interface, component, web page, dashboard, landing page, SaaS application,
  design system, or any visual frontend element — even if they don't explicitly
  mention "UI" or "design". Also triggers when the user gives Shadcn installation
  commands (`npx shadcn@latest add ...`), mentions Tailwind v4, OKLCH, or
  asks for something "original", "premium", "non-generic", "cinematic",
  or "unique". This skill replaces the generic frontend-design skill for any
  context requiring a high level of craft and intentionality.
---

# UI Modern 2026 — Non-Generic Design Skill

Design interfaces that breathe intentionality, craft, and brand singularity.
This skill guides every design and implementation decision to avoid **template fatigue**
and produce memorable, human, and premium experiences.

---

## Workflow — Where to Start

Before writing a single line of code, follow this workflow in order:

**1. Read the Context**
- What is the product, the target audience, the expected tone?
- Are there Shadcn components to integrate? (see "Component Integration" section)
- Is there an existing brand palette, typography, or token?

**2. Choose a Sharp Aesthetic Direction** (no lukewarm compromises)
Select ONE archetype and commit fully:

| Archetype | Dominant Visual Signal | When to Use |
|-----------|------------------------|-----------------|
| Organic Editorial | Asymmetry, massive typography, generous spacing | Startups, portfolios, creative products |
| Neo-Brutalist | Extreme contrasts, thick borders, raw feel | Dev tools, technical tools, "rebel" products |
| Precise Minimalism | Surgical spacing, single accent color | B2B SaaS, finance, productivity tools |
| Material & Depth | Grain, subtle textures, surface effects | Premium, lifestyle, digitized physical products |
| Cinematic | Narrative scroll, temporal pacing, full screen | Immersive landings, portfolios, consumer products |

**3. Validate Direction** with the user if ambiguous, then code.

**4. Apply Non-Negotiable Rules** (below) before delivery.

---

## Non-Negotiable Rules

### ✅ Absolute Do's

- **Colors in OKLCH exclusively** — see `references/oklch.md`
- **Wrap every Shadcn component** before use — see `references/shadcn-components.md`
- **Test WCAG contrast** (AA minimum, AAA for body text) upon generation
- **Include `prefers-reduced-motion`** for every animation
- **Organic grain** on any premium project (0.03–0.06 opacity, `mix-blend-mode: overlay`)
- **One emotional functional micro-interaction** minimum per interface

### 🚫 Absolute Don'ts — Generic Anti-patterns

These elements immediately signal a "mass-produced" interface:

**Visual effects to ban:**
- Heavy or multi-layered `box-shadow` → replace with **sharp edges, elevation via OKLCH color contrast, or ultra-fine directional shadows** (`0 1px 2px oklch(0 0 0 / 0.08)`)
- Overly bold `gradient` (purple→pink on white, full-screen hero gradient) → replace with **subtle hue transitions** (`oklch(L C H1)` → `oklch(L C H2)`, delta H ≤ 30°)
- Over-saturated radial spotlight / glow effects → replace with **directional light grain** or a **focus zone via L variation only**
- Hover zoom on cards or images → replace with **light translation** (`translateY(-2px)`), **border-color change**, or **hidden content reveal**
- Empty "wow" animations (aggressive parallax, floating particles) → replace with **animations serving meaning** (data revelation, narrative progression)

**Layout patterns to ban:**
- 3-column grid of identical cards → vary sizes, play with rhythm
- Centered hero: logo + title + CTA on solid background → build a composition instead
- Sticky navigation with identical blur-backdrop → explore navigation alternatives

**Typography to ban:**
- Inter, Roboto, Arial, system-ui as main font → choose a variable font with personality
- Hierarchy only by size → use weight, spacing, OKLCH color, and movement

---

## Shadcn Component Integration

When the user provides a Shadcn installation command, follow this exact protocol:

### Step 1 — Identify the Installed Component
```bash
# Example command provided by the user:
npx shadcn@latest add card button badge
```
Identify each component: `Card`, `Button`, `Badge`.

### Step 2 — Read Generated Files (never assume structure)
```
components/ui/card.tsx      ← raw Shadcn component
components/ui/button.tsx    ← raw Shadcn component
```

### Step 3 — Create Brand Wrappers (NEVER modify `/ui/` files directly)

```tsx
// components/primitives/AppCard.tsx
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface AppCardProps extends React.ComponentProps<typeof Card> {
  variant?: "default" | "elevated" | "ghost"
  grain?: boolean
}

export function AppCard({ variant = "default", grain = false, className, children, ...props }: AppCardProps) {
  return (
    <Card
      className={cn(
        // Brand tokens — replace Shadcn defaults
        "rounded-xl border-[oklch(var(--border))] bg-[oklch(var(--card))]",
        // No heavy box-shadow — elevation via contrast
        variant === "elevated" && "border-[oklch(var(--border-strong))] bg-[oklch(var(--card-elevated))]",
        variant === "ghost" && "border-transparent bg-transparent",
        // Optional grain
        grain && "relative overflow-hidden after:absolute after:inset-0 after:bg-[url('/grain.svg')] after:opacity-[0.04] after:mix-blend-overlay after:pointer-events-none",
        className
      )}
      {...props}
    >
      {children}
    </Card>
  )
}
```

### Step 4 — Adapt to Specific Project

For each Shadcn component received, ask yourself:
1. **What is the business context?** (analytics dashboard, SaaS landing, e-commerce...)
2. **What contextual variants are needed?** (empty state, loading state, error state...)
3. **What distinctive micro-interaction to add?** (no zoom — look for an original effect)

Consult `references/shadcn-components.md` for wrapping patterns by component type.

---

## Color System — OKLCH Mandatory

Use OKLCH only. Consult `references/oklch.md` for the full guide.

**Essential Principle — derivation from a single hue:**
```css
:root {
  /* Base Color: fixed H, variable L and C */
  --brand-h: 264;           /* The hue NEVER changes */
  
  --primary:     oklch(0.25 0.08 var(--brand-h));
  --primary-sub: oklch(0.35 0.06 var(--brand-h));
  --accent:      oklch(0.55 0.14 var(--brand-h));  /* +C for accent */
  --muted:       oklch(0.70 0.02 var(--brand-h));  /* -C for muted */
  
  --background:  oklch(0.98 0.005 var(--brand-h)); /* Quasi-neutral, light tint */
  --foreground:  oklch(0.12 0.02 var(--brand-h));
  
  /* Surfaces — never pure white/black */
  --card:        oklch(0.96 0.008 var(--brand-h));
  --border:      oklch(0.88 0.01 var(--brand-h));
}

.dark {
  /* Same H, invert L, slightly adjust C */
  --background:  oklch(0.13 0.01 var(--brand-h));
  --foreground:  oklch(0.95 0.01 var(--brand-h));
  --card:        oklch(0.18 0.015 var(--brand-h));
  --border:      oklch(0.28 0.02 var(--brand-h));
}
```

**Contrast Validation Tool:** always check the ratio between `--foreground` and `--background` (target ≥ 4.5:1).

---

## Original Effects — Replacement Catalog

These effects replace banned generic patterns. Choose based on the aesthetic archetype.

### Instead of Hover Zoom → Content Reveal
```css
.card-content-hidden {
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 200ms ease, transform 200ms ease;
}
.card:hover .card-content-hidden {
  opacity: 1;
  transform: translateY(0);
}
```

### Instead of Heavy Box-shadow → Directional Colored Border
```css
.card {
  border: 1px solid oklch(var(--border));
  transition: border-color 150ms ease;
}
.card:hover {
  border-color: oklch(var(--accent));
  /* Single side for a directional effect */
  border-left-color: oklch(var(--primary));
}
```

### Instead of Spotlight Gradient → Focus via OKLCH Brightness
```css
/* The focused element is brighter, not lit by a spot */
.focus-zone {
  background: oklch(0.22 0.04 264);
}
.focus-zone:hover {
  background: oklch(0.28 0.05 264); /* +6% L only */
}
```

### Instead of Aggressive Parallax → Native CSS Scroll-Driven Animation
```css
@keyframes reveal-up {
  from { opacity: 0; translate: 0 20px; }
  to   { opacity: 1; translate: 0 0; }
}

.section {
  animation: reveal-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}
```

### Organic Grain (premium effect, no sticky texture)
```css
/* Overlay via pseudo-element, does not affect interactivity */
.surface-premium {
  position: relative;
}
.surface-premium::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='1'/%3E%3C/svg%3E");
  opacity: 0.035;
  mix-blend-mode: overlay;
  pointer-events: none;
  border-radius: inherit;
}
```

### Kinetic Typography — Reactive Variable Font
```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100..900&display=swap');

.headline-reactive {
  font-family: 'Fraunces', serif;
  font-variation-settings: 'SOFT' 0, 'WONK' 0;
  transition: font-variation-settings 300ms ease;
}
.headline-reactive:hover {
  font-variation-settings: 'SOFT' 100, 'WONK' 1;
}
```

---

## Scrollytelling & Narration

Every scroll must **tell a story**. Five rules:

1. **Data IS the story** — reveal figures/stats progressively, not in a dump
2. **Temporal Breathing** — alternate dense sections and "breathing" spaces
3. **One Message per Screen** — no visual competition between elements
4. **Movement Serving Clarity** — if an animation doesn't clarify, remove it
5. **Interaction = Exploration** — let the user "discover" rather than "receive"

```css
/* View Transitions API — state transitions without JS */
@view-transition { navigation: auto; }

::view-transition-old(root) {
  animation: 200ms ease out slide-out;
}
::view-transition-new(root) {
  animation: 300ms ease in slide-in;
}
```

---

## Delivery Checklist

Before delivering any interface, validate point by point:

- [ ] **Colors** — 100% in OKLCH, no HSL/RGB/hex values in tokens
- [ ] **Contrast** — ratio ≥ 4.5:1 for body, ≥ 3:1 for UI components
- [ ] **Components** — all wrapped in `/primitives/` or `/blocks/`, never modified `/ui/` directly
- [ ] **Shadows** — no heavy `box-shadow` (max `0 1px 3px oklch(0 0 0 / 0.08)`)
- [ ] **Gradients** — no saturated gradients on white/black background, delta H ≤ 30° if gradient
- [ ] **Zoom** — no `scale()` on card hover; replaced by alternative effect
- [ ] **Animations** — all with `prefers-reduced-motion: reduce` → `animation: none`
- [ ] **Grain** — present on at least the hero surface for any premium project
- [ ] **Typo** — variable or characteristic font, no Inter/Roboto/Arial
- [ ] **Dark Mode** — `.dark` tokens defined and tested

---

## Code Architecture

```
src/
├── components/
│   ├── ui/            ← Raw Shadcn (NEVER modified directly)
│   ├── primitives/    ← Brand wrappers (AppButton, AppCard, AppInput...)
│   └── blocks/        ← Business compositions (HeroSection, PricingCard, FeatureGrid...)
├── styles/
│   └── tokens.css     ← OKLCH variables (:root + .dark)
└── lib/
    └── utils.ts       ← cn() and helpers
```

---

## References

- `references/oklch.md` — Full OKLCH guide: syntax, derivation, tools, examples
- `references/shadcn-components.md` — Wrapping patterns per component (Button, Card, Input, Dialog, Table, Badge, etc.)
- `references/effects-catalog.md` — Extended catalog of original effects with ready-to-use code

*This skill is alive. Update it with every major evolution of Tailwind, Shadcn UI, or native CSS.*
ntaxe, dérivation, outils, exemples
- `references/shadcn-components.md` — Patterns de wrapping par composant (Button, Card, Input, Dialog, Table, Badge, etc.)
- `references/effects-catalog.md` — Catalogue étendu d'effets originaux avec code prêt à l'emploi

*Ce skill est vivant. Le mettre à jour à chaque évolution majeure de Tailwind, Shadcn UI ou CSS natif.*
