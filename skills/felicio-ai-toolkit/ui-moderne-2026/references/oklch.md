# OKLCH Reference — Perceptual Color Space

## Why OKLCH instead of HSL

- **HSL**: Perceived brightness varies by hue → HSL(60, 100%, 50%) yellow seems MUCH brighter than HSL(240, 100%, 50%) blue at the same L value. Result: manual contrast reworking in dark mode.
- **OKLCH**: Perceptually uniform brightness → `oklch(0.55 0.15 H)` has the same level of perceived brightness regardless of hue H. Dark mode generates mechanically.

## Syntax

```css
oklch(L C H)
oklch(L C H / alpha)

/* L: 0 (black) → 1 (white) */
/* C: 0 (gray) → ~0.4 (maximum color) */
/* H: 0→360 (hue, in degrees) */
```

## Hue Reference Table

| H | Color | Typical Uses |
|---|---------|-----------------|
| 0–30 | Red → Orange | Alerts, urgent CTAs |
| 30–60 | Orange → Yellow | Warnings, energy |
| 80–150 | Yellow-green → Green | Success, health, finance |
| 160–220 | Cyan → Sky-blue | Tech, light trust |
| 220–270 | Blue → Violet-blue | SaaS, productivity |
| 270–320 | Violet → Magenta | Creative, premium |
| 320–360 | Pink → Red | Emotion, soft urgency |

## Palette Derivation from a Base Color

**Principle: Fix H, vary L and C only.**

```css
/* Chosen base color: H = 240 (blue) */
:root {
  /* Primaries */
  --color-900: oklch(0.20 0.10 240);  /* very dark */
  --color-700: oklch(0.35 0.12 240);
  --color-500: oklch(0.50 0.15 240);  /* reference */
  --color-300: oklch(0.70 0.08 240);
  --color-100: oklch(0.92 0.02 240);  /* very light */
  
  /* Complementary Accent: H + 180° */
  --accent:    oklch(0.55 0.14 60);   /* H = 240 + 180° = 60° (gold-yellow) */
  
  /* Tinted Neutral (H unchanged, C near-zero) */
  --neutral:   oklch(0.95 0.005 240);
}
```

## Automated Dark Mode Generation

```css
.dark {
  /* Invert L: 0.20 → 0.85, 0.92 → 0.15 */
  /* Slightly reduce C in dark (saturated dark surfaces < light surfaces) */
  --color-900: oklch(0.85 0.08 240);
  --color-700: oklch(0.72 0.10 240);
  --color-500: oklch(0.55 0.13 240);
  --color-300: oklch(0.38 0.08 240);
  --color-100: oklch(0.20 0.02 240);
}
```

## Recommended Tools

- **oklch.com** — interactive picker with real-time contrast preview
- **tweakcn.com** — Shadcn theme generator in OKLCH
- **Oklch Color Picker (VS Code extension)** — autocompletion in CSS

## Shadcn v4 Semantic Tokens (Tailwind v4)

In `tailwind.config.ts` or `globals.css` with Tailwind v4:

```css
@layer base {
  :root {
    --background:   0.98 0.005 240;   /* Note: without oklch() here, Tailwind injects it */
    --foreground:   0.12 0.02 240;
    --primary:      0.25 0.10 240;
    --primary-foreground: 0.97 0.005 240;
    --secondary:    0.92 0.01 240;
    --secondary-foreground: 0.20 0.05 240;
    --muted:        0.94 0.005 240;
    --muted-foreground: 0.50 0.03 240;
    --accent:       0.55 0.14 60;
    --accent-foreground: 0.10 0.02 60;
    --destructive:  0.45 0.20 20;
    --border:       0.88 0.01 240;
    --input:        0.88 0.01 240;
    --ring:         0.50 0.15 240;
    --card:         0.97 0.006 240;
    --card-foreground: 0.12 0.02 240;
    --radius: 0.5rem;
  }
  .dark {
    --background:   0.13 0.01 240;
    --foreground:   0.95 0.01 240;
    --primary:      0.70 0.12 240;
    --primary-foreground: 0.10 0.02 240;
    --secondary:    0.20 0.02 240;
    --secondary-foreground: 0.90 0.01 240;
    --muted:        0.20 0.01 240;
    --muted-foreground: 0.60 0.03 240;
    --accent:       0.65 0.12 60;
    --accent-foreground: 0.10 0.02 60;
    --destructive:  0.55 0.18 20;
    --border:       0.28 0.02 240;
    --input:        0.28 0.02 240;
    --ring:         0.65 0.12 240;
    --card:         0.18 0.015 240;
    --card-foreground: 0.95 0.01 240;
  }
}
```

## Mandatory Contrast Validation

```js
// Utility function (copy into a helper)
function oklchContrast(l1, l2) {
  // Quick approximation — use oklch.com for precise validation
  const lum1 = Math.pow(l1, 2.2);
  const lum2 = Math.pow(l2, 2.2);
  const lighter = Math.max(lum1, lum2);
  const darker  = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

// WCAG Goals:
// Body text: ≥ 4.5:1
// Large text (>18px): ≥ 3:1
// UI components: ≥ 3:1
```
