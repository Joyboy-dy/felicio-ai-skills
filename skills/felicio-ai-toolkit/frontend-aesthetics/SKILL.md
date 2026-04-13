---
name: frontend-aesthetics
description: Apply distinctive, opinionated visual design to any frontend component, page, or application. Use whenever building or styling UI to avoid generic "AI slop" aesthetics. Enforces creative typography, cohesive color systems, purposeful motion, and atmospheric backgrounds. Works with React, Next.js, Tailwind CSS, and plain HTML/CSS. Triggers on any request involving visual design, component creation, landing pages, dashboards, or UI polish.
---

# Frontend Aesthetics

You tend to converge toward generic, statistically average outputs. In frontend design, this produces what users call "AI slop" — the same purple gradients, the same Inter font, the same card layouts, the same soft shadows. This skill exists to break that pattern.

Every interface you build must feel **deliberately designed for its specific context**. No two outputs should look the same.

---

## Before Writing Any Code

Commit to a creative direction by answering these four questions:

1. **What is this for?** — The aesthetic must serve the purpose. A medical dashboard and a music player require entirely different visual languages.
2. **What is the tone?** — Pick a specific extreme. Examples below. Do not land in the middle.
3. **What is the one thing someone will remember?** — If you can't answer this, the design isn't distinctive enough.
4. **What would a human designer with taste do here?** — Not what is safe. What is *right*.

### Tone Palette (pick one, commit hard)

| Direction | Character |
|---|---|
| Brutalist / raw | Heavy borders, monospace, stark contrast, no decoration |
| Editorial / magazine | Oversized type, asymmetric grid, black + one color |
| Retro-terminal | Scanlines, phosphor glow, monospace, dark bg |
| Luxe / refined | Generous whitespace, serif, gold or stone accents, restrained |
| Organic / natural | Irregular shapes, earthy palette, variable weight type |
| Maximalist / dense | Information density, tight grid, vivid color, everything has a purpose |
| Industrial / utilitarian | System fonts used *intentionally*, function-first, no ornament |
| Art deco / geometric | Symmetry, ornamental borders, jewel tones, structured grids |
| Playful / toy-like | Rounded everything, saturated colors, bouncy motion |
| Cyberpunk / neon | Dark bg, electric accents, glow effects, angular cuts |

These are starting points. The best outputs combine and subvert them.

---

## Typography

Typography is the fastest path to a distinctive identity. The font choice communicates everything before the user reads a word.

### Rules

- **Never use Inter, Roboto, Arial, or system-ui as the primary display font.** These are defaults, not choices.
- **Never use Space Grotesk.** It is now as generic as Inter.
- **Pair a display font with a body font.** They should create tension — not match too neatly.
- **Use weight contrast aggressively.** A 900-weight headline next to a 300-weight subtitle creates drama. Uniform weight creates flatness.
- **Size dramatically.** A hero headline at `clamp(4rem, 10vw, 9rem)` is a statement. Don't be timid.

### Font Directions by Aesthetic

| Aesthetic | Display | Body |
|---|---|---|
| Editorial | Playfair Display, Cormorant Garamond, Fraunces | Source Serif 4, Lora |
| Brutalist | Bebas Neue, Anton, Black Han Sans | IBM Plex Mono, Courier Prime |
| Luxe | Bodoni Moda, DM Serif Display, Canela | Garamond, EB Garamond |
| Geometric / Deco | Poiret One, Josefin Sans, Futura (self-hosted) | Karla, DM Sans |
| Retro-tech | VT323, Share Tech Mono, Major Mono Display | IBM Plex Mono |
| Organic | Reenie Beanie, Caveat (headers only), Youngserif | Lato, Nunito |
| Cyberpunk | Orbitron, Exo 2, Rajdhani | Share Tech, Roboto Mono |
| Playful | Fredoka, Baloo 2, Righteous | Nunito, Quicksand |

Load from Google Fonts or Fontsource. **Always load only the weights you use.**

```css
/* Example: Editorial direction */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;1,9..144,300&family=Source+Serif+4:wght@300;400&display=swap');

:root {
  --font-display: 'Fraunces', Georgia, serif;
  --font-body: 'Source Serif 4', Georgia, serif;
}
```

---

## Color & Theme

### Rules

- **Commit to a dominant color.** One color owns the palette. Accents exist to serve it.
- **Use CSS custom properties for every color value.** No hardcoded hex in components.
- **Avoid purple-on-white.** It is the most over-represented AI aesthetic. Same for teal, same for "modern blue" (#6366f1).
- **Dark themes are not just `background: #0f0f0f`.** Add depth: use 3–4 background levels (`--bg-base`, `--bg-surface`, `--bg-elevated`, `--bg-overlay`).
- **Derive, don't invent.** Take inspiration from existing visual cultures: IDE themes (Nord, Dracula, Gruvbox, Catppuccin, Tokyo Night), film color grades, fashion palettes, architectural materials.

### Palette Construction

```css
/* Example: Gruvbox-inspired warm dark */
:root {
  --bg-base:      #1d2021;
  --bg-surface:   #282828;
  --bg-elevated:  #32302f;
  --bg-overlay:   #3c3836;

  --text-primary:   #ebdbb2;
  --text-secondary: #a89984;
  --text-muted:     #665c54;

  --accent:         #d79921; /* warm yellow */
  --accent-soft:    #d7992120;
  --destructive:    #cc241d;
  --success:        #98971a;

  --border:         #504945;
  --border-focus:   #d79921;
}

/* Example: Stone editorial light */
:root {
  --bg-base:      #faf7f2;
  --bg-surface:   #f0ebe3;
  --bg-elevated:  #e8e0d5;

  --text-primary:   #1a1714;
  --text-secondary: #5c534a;
  --text-muted:     #9c9188;

  --accent:         #b5451b; /* terracotta */
  --accent-soft:    #b5451b15;

  --border:         #d4ccc4;
  --border-focus:   #b5451b;
}
```

### Color Inspiration Sources

- **IDE themes**: Dracula, Nord, One Dark, Gruvbox, Tokyo Night, Catppuccin, Solarized
- **Film grades**: Teal-orange blockbuster, desaturated Fincher, warm Wes Anderson
- **Fashion/material**: Raw linen, oxidized copper, onyx + gold, chalk + charcoal
- **Cultural palettes**: Japanese wabi-sabi (stone, moss, rust), Bauhaus (primary triads), Soviet constructivism (red + black + white)

---

## Motion

Motion communicates quality. The absence of motion communicates nothing. Gratuitous motion communicates noise.

### Rules

- **One orchestrated entrance beats ten scattered micro-animations.** A staggered page load that reveals content in sequence is more impressive and less annoying than buttons that jiggle on hover.
- **Motion must have a purpose.** Entrance = orient the user. Exit = confirm the action. State change = communicate feedback. Hover = invite interaction.
- **CSS-first for HTML.** `@keyframes` + `animation-delay` handles 80% of cases without JS overhead.
- **Motion library for React** when sequencing, gesture-based interaction, or layout animations are needed.
- **Always respect `prefers-reduced-motion`.** No exceptions.

```css
/* ✅ Staggered entrance — CSS only */
@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fade-up 0.4s ease both;
}
.card:nth-child(1) { animation-delay: 0ms; }
.card:nth-child(2) { animation-delay: 80ms; }
.card:nth-child(3) { animation-delay: 160ms; }
.card:nth-child(4) { animation-delay: 240ms; }

@media (prefers-reduced-motion: reduce) {
  .card { animation: none; }
}
```

```tsx
// ✅ Framer Motion — staggered list
import { motion } from 'framer-motion';

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

const item = {
  hidden: { opacity: 0, y: 12 },
  show:   { opacity: 1, y: 0, transition: { duration: 0.35, ease: [0.25, 0.1, 0.25, 1] } },
};

export function AnimatedList({ children }: { children: React.ReactNode }) {
  return (
    <motion.ul variants={container} initial="hidden" animate="show">
      {React.Children.map(children, (child) => (
        <motion.li variants={item}>{child}</motion.li>
      ))}
    </motion.ul>
  );
}
```

### Motion Vocabulary by Aesthetic

| Aesthetic | Easing | Duration | Character |
|---|---|---|---|
| Luxe / refined | `cubic-bezier(0.76, 0, 0.24, 1)` | 600–900ms | Slow, deliberate |
| Editorial | `cubic-bezier(0.25, 0.1, 0.25, 1)` | 300–500ms | Clean, direct |
| Playful | `cubic-bezier(0.34, 1.56, 0.64, 1)` | 350–500ms | Bouncy overshoot |
| Brutalist | `steps(1)` or instant | — | No easing, snap |
| Cyberpunk | `cubic-bezier(0.2, 0, 0, 1)` | 150–250ms | Fast, electric |

---

## Backgrounds & Atmosphere

A background is not a color. It is the environment in which the interface lives.

### Techniques

```css
/* Mesh gradient — organic, modern */
background:
  radial-gradient(ellipse at 20% 50%, #d7992220 0%, transparent 60%),
  radial-gradient(ellipse at 80% 20%, #98971a15 0%, transparent 50%),
  var(--bg-base);

/* Noise texture overlay — adds tactility */
.noise::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
}

/* Grid pattern — structural, editorial */
background-image:
  linear-gradient(var(--border) 1px, transparent 1px),
  linear-gradient(90deg, var(--border) 1px, transparent 1px);
background-size: 48px 48px;

/* Dot pattern — clean, technical */
background-image: radial-gradient(var(--border) 1px, transparent 1px);
background-size: 24px 24px;

/* Diagonal stripe — brutalist accent */
background-image: repeating-linear-gradient(
  -45deg,
  var(--accent),
  var(--accent) 2px,
  transparent 2px,
  transparent 10px
);

/* Vignette — adds depth to dark themes */
background: radial-gradient(ellipse at center, transparent 40%, #00000060 100%);
```

---

## Component Patterns

### What to Avoid

- Default Tailwind card: `rounded-lg border bg-white shadow-sm p-4` — this is boilerplate, not design
- Hero with centered text + gradient button on white background
- Sidebar with icon + label in Inter Regular
- Dashboard with `grid-cols-4` metric cards, all identical
- Modal that looks like every other modal

### What to Do Instead

Subvert one expectation per component. Examples:

- **Card** → Accent border on left only. Or no border, ink-colored background, white text. Or torn-paper edge via `clip-path`.
- **Button** → Inverse fill (border + transparent, fills on hover). Or skewed `transform: skewX(-8deg)`. Or uppercase tracked letter-spacing with no border.
- **Hero** → Full bleed type bleeding off-screen. Or asymmetric split layout. Or kinetic text cycling through options.
- **Navigation** → Vertical stacked with large numerals. Or a single horizontal rule with items spaced across it. Or floating pill.
- **Table** → Remove most borders, rely on alternating `bg-surface`. Or make the header dramatically larger.

```tsx
// ✅ Distinctive card — not the default
export function Card({ title, description, tag }: CardProps) {
  return (
    <article className="group relative overflow-hidden rounded-none border-l-2 border-[var(--accent)] bg-[var(--bg-surface)] px-5 py-4 transition-colors hover:bg-[var(--bg-elevated)]">
      {tag && (
        <span className="mb-3 inline-block font-mono text-[10px] uppercase tracking-[0.2em] text-[var(--accent)]">
          {tag}
        </span>
      )}
      <h3 className="font-display text-xl font-bold leading-tight text-[var(--text-primary)]">
        {title}
      </h3>
      <p className="mt-1.5 text-sm leading-relaxed text-[var(--text-secondary)]">
        {description}
      </p>
      <div className="mt-4 h-px w-0 bg-[var(--accent)] transition-all duration-500 group-hover:w-full" />
    </article>
  );
}
```

---

## Anti-Patterns (Hard Blacklist)

These combinations are banned. If you find yourself writing them, stop and redesign.

| ❌ Banned | Why |
|---|---|
| `font-family: Inter` as the primary display font | The default. Not a choice. |
| `font-family: Space Grotesk` | Overused in AI outputs. |
| Purple / violet gradient on white (`#6366f1` → `#8b5cf6`) | The signature of generic AI design |
| `rounded-xl shadow-md bg-white` cards on white bg | Invisible, weightless, forgettable |
| Centered hero, gradient CTA button, subtitle in gray | Template, not design |
| `text-gray-500` for everything secondary | Lazy — derive from your palette |
| Identical hover states across all components | No hierarchy of interactivity |
| `transition-all duration-300 ease-in-out` on everything | Default, not intentional |
| Grid of four identical metric cards | Dashboard cliché |
| Decorative blob shapes in corner | 2021 called |

---

## Execution Checklist

Before shipping any UI, verify:

- [ ] Font is distinctive and purposefully paired — not a default
- [ ] Color palette is defined in CSS variables, derived from a coherent inspiration source
- [ ] Background has atmosphere — not a flat color
- [ ] At least one component subverts its default pattern
- [ ] Motion is purposeful, orchestrated, and respects `prefers-reduced-motion`
- [ ] The interface has a recognizable aesthetic identity — someone could describe its "vibe" in one word
- [ ] No item from the anti-patterns blacklist is present