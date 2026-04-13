# Original Effects Catalog — Alternatives to Generic Patterns

This catalog provides ready-to-use effects, organized by what they **replace**.

---

## Hover Zoom Replacement

### 1. Sub-content Reveal (the most memorable)
```css
.card { position: relative; overflow: hidden; }
.card__hidden {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 1rem;
  transform: translateY(100%);
  transition: transform 250ms cubic-bezier(0.16, 1, 0.3, 1);
  background: oklch(var(--card));
}
.card:hover .card__hidden { transform: translateY(0); }
```

### 2. Border Morphing
```css
.card {
  border: 1px solid oklch(var(--border));
  border-radius: 12px;
  transition: border-color 150ms ease, border-radius 150ms ease;
}
.card:hover {
  border-color: oklch(var(--accent));
  border-radius: 20px;
}
```

### 3. Label Slide (ticker effect)
```css
.btn { overflow: hidden; position: relative; }
.btn__text { display: block; transition: transform 200ms ease; }
.btn__text-clone {
  position: absolute; top: 100%; left: 0; width: 100%; text-align: center;
  transition: transform 200ms ease;
}
.btn:hover .btn__text { transform: translateY(-100%); }
.btn:hover .btn__text-clone { transform: translateY(-100%); }
```

### 4. Progressive Focus Line (links and nav items)
```css
.nav-link { position: relative; }
.nav-link::after {
  content: '';
  position: absolute; bottom: -2px; left: 0;
  height: 1px; width: 0;
  background: oklch(var(--primary));
  transition: width 200ms ease;
}
.nav-link:hover::after,
.nav-link[aria-current="page"]::after { width: 100%; }
```

---

## Heavy Box-Shadow Replacement

### 1. Elevation via OKLCH Contrast (recommended)
```css
/* "Elevated" surface = L slightly higher than parent surface */
.card-base     { background: oklch(0.96 0.008 240); }
.card-elevated { background: oklch(0.99 0.004 240); } /* +3% L */
/* In dark mode: elevated surface = L higher as well */
.dark .card-base     { background: oklch(0.16 0.015 240); }
.dark .card-elevated { background: oklch(0.22 0.018 240); } /* +6% L */
```

### 2. Directional Asymmetric Border
```css
/* Simulates a light source coming from top-left */
.surface {
  border-top: 1px solid oklch(var(--border-light, oklch(0.95 0.01 240)));
  border-left: 1px solid oklch(var(--border-light, oklch(0.95 0.01 240)));
  border-bottom: 1px solid oklch(var(--border));
  border-right: 1px solid oklch(var(--border));
}
```

### 3. Ultra-fine Shadow (when a shadow is genuinely necessary)
```css
/* Maximum allowed — never more than this */
.shadow-fine {
  box-shadow:
    0 1px 2px oklch(0 0 0 / 0.06),
    0 0 0 1px oklch(0 0 0 / 0.04);
}
```

---

## Spotlight Gradient and Glow Replacement

### 1. Focus Zone via L variation (subtle, premium)
```css
.hero-background {
  background: oklch(0.12 0.015 240);
}
.hero-focus-zone {
  /* No saturated radial-gradient — just +4% L at center */
  background: radial-gradient(
    ellipse 60% 40% at 50% 30%,
    oklch(0.18 0.018 240) 0%,
    oklch(0.12 0.015 240) 100%
  );
}
```

### 2. Directional Light Line (horizontal laser effect)
```css
.section-divider {
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    oklch(var(--primary) / 0.4) 30%,
    oklch(var(--primary) / 0.4) 70%,
    transparent 100%
  );
}
```

### 3. Edge Halo (on premium cards, dark mode only)
```css
.dark .card-premium {
  box-shadow: inset 0 1px 0 oklch(1 0 0 / 0.06); /* Subtle top reflection */
}
```

### 4. Noise Texture as Gradient Alternative
```css
/* Add depth without saturated color */
.surface-depth {
  background:
    url("data:image/svg+xml,%3Csvg...%3E") repeat,  /* grain SVG */
    oklch(0.14 0.015 240);
  background-blend-mode: overlay;
}
```

---

## Narrative Animations (alternatives to parallax)

### 1. Scroll Reveal — Native CSS (no JS)
```css
@keyframes fade-up {
  from { opacity: 0; translate: 0 16px; }
  to   { opacity: 1; translate: 0 0; }
}

.reveal {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 25%;
}

/* Stagger: increasing delay for sibling elements */
.reveal:nth-child(2) { animation-delay: 60ms; }
.reveal:nth-child(3) { animation-delay: 120ms; }
```

### 2. Animated Counter (key data)
```ts
// hooks/useCountUp.ts
export function useCountUp(target: number, duration = 1200) {
  const [count, setCount] = useState(0)
  const ref = useRef<HTMLElement>(null)
  
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return
      observer.disconnect()
      const start = performance.now()
      const step = (now: number) => {
        const progress = Math.min((now - start) / duration, 1)
        const eased = 1 - Math.pow(1 - progress, 3) // ease-out-cubic
        setCount(Math.round(eased * target))
        if (progress < 1) requestAnimationFrame(step)
      }
      requestAnimationFrame(step)
    }, { threshold: 0.5 })
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [target, duration])
  
  return { count, ref }
}
```

### 3. Reveal Text (masking)
```css
@keyframes reveal-text {
  from { clip-path: inset(0 100% 0 0); }
  to   { clip-path: inset(0 0% 0 0); }
}

.text-reveal {
  animation: reveal-text 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
  animation-timeline: view();
  animation-range: entry 0% entry 20%;
}
```

### 4. SVG Shape Morphing
```tsx
// Transition between two SVG paths on hover — strong visual identity
function MorphIcon() {
  return (
    <svg viewBox="0 0 24 24" className="w-6 h-6">
      <path className="transition-all duration-300 ease-out group-hover:[d:path('M12_2L22_22H2Z')]">
        <animate attributeName="d"
          values="M12 2L22 22H2Z; M2 2H22V22H2Z"
          dur="300ms" fill="freeze" begin="indefinite" />
      </path>
    </svg>
  )
}
```

---

## Emotional Micro-interactions

### Success-pulse Button
```css
@keyframes success-pulse {
  0%   { box-shadow: 0 0 0 0 oklch(var(--primary) / 0.4); }
  70%  { box-shadow: 0 0 0 8px oklch(var(--primary) / 0); }
  100% { box-shadow: 0 0 0 0 oklch(var(--primary) / 0); }
}

.btn--success { animation: success-pulse 600ms ease-out; }
```

### Error-signal Input (no aggressive red)
```css
@keyframes shake-subtle {
  0%, 100% { translate: 0; }
  25%       { translate: -3px 0; }
  75%       { translate: 3px 0; }
}
.input--error { animation: shake-subtle 300ms ease; }
```

### Checkbox with Animated Path
```css
.checkbox-check {
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  transition: stroke-dashoffset 200ms ease;
}
.checkbox:checked + .checkbox-check {
  stroke-dashoffset: 0;
}
```

---

## Recommended Variable Typography

| Family | Style | Available Axes | Use Case |
|---------|-------|-----------------|-------------|
| Fraunces | Organic Serif | `SOFT`, `WONK`, `opsz`, `wght` | Premium landings, editorial |
| Recursive | Mono/Sans hybrid | `MONO`, `CASL`, `CRSV`, `slnt` | Dev tools, technical interfaces |
| Raleway | Geometric | `wght` | Clean, modern SaaS |
| Cabinet Grotesk | Grotesque | `wght` | Tech startups |
| Libre Baskerville | Classic Serif | — | Long-form content, trust |

**Optimized Loading:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preload" as="font" crossorigin>
```

```css
/* Variable Font — enable axes in CSS */
body {
  font-family: 'Fraunces', serif;
  font-variation-settings: 'SOFT' 50;
  font-optical-sizing: auto;
}
```

---

## prefers-reduced-motion — Universal Template

Always include this block in `globals.css`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  
  /* Retain functional transitions (focus, states) */
  :focus-visible {
    transition: outline-offset 0ms !important;
  }
}
```
