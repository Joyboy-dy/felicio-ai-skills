# Catalogue d'Effets Originaux — Alternatives aux Patterns Génériques

Ce catalogue fournit des effets prêts à l'emploi, organisés par ce qu'ils **remplacent**.

---

## Remplacement du Zoom Hover

### 1. Reveal de sous-contenu (le plus mémorable)
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

### 2. Morphing de bordure
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

### 3. Glissement de label (effet ticker)
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

### 4. Ligne de focus progressive (liens et items de nav)
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

## Remplacement des Box-Shadow Lourdes

### 1. Élévation par contraste OKLCH (recommandé)
```css
/* Surface "élevée" = L légèrement plus haute que la surface parent */
.card-base     { background: oklch(0.96 0.008 240); }
.card-elevated { background: oklch(0.99 0.004 240); } /* +3% L */
/* En dark mode : surface élevée = L plus haute aussi */
.dark .card-base     { background: oklch(0.16 0.015 240); }
.dark .card-elevated { background: oklch(0.22 0.018 240); } /* +6% L */
```

### 2. Border asymétrique directionnelle
```css
/* Simule une source de lumière venant du haut-gauche */
.surface {
  border-top: 1px solid oklch(var(--border-light, oklch(0.95 0.01 240)));
  border-left: 1px solid oklch(var(--border-light, oklch(0.95 0.01 240)));
  border-bottom: 1px solid oklch(var(--border));
  border-right: 1px solid oklch(var(--border));
}
```

### 3. Ombre ultra-fine (quand une ombre est vraiment nécessaire)
```css
/* Maximum autorisé — jamais plus que ça */
.shadow-fine {
  box-shadow:
    0 1px 2px oklch(0 0 0 / 0.06),
    0 0 0 1px oklch(0 0 0 / 0.04);
}
```

---

## Remplacement des Dégradés Spotlight et Glows

### 1. Zone de focus par variation L (subtil, premium)
```css
.hero-background {
  background: oklch(0.12 0.015 240);
}
.hero-focus-zone {
  /* Pas de radial-gradient saturé — juste +4% L au centre */
  background: radial-gradient(
    ellipse 60% 40% at 50% 30%,
    oklch(0.18 0.018 240) 0%,
    oklch(0.12 0.015 240) 100%
  );
}
```

### 2. Ligne lumineuse directionnelle (effet laser horizontal)
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

### 3. Halo de bord (sur les cards premium, mode dark uniquement)
```css
.dark .card-premium {
  box-shadow: inset 0 1px 0 oklch(1 0 0 / 0.06); /* Reflet haut subtil */
}
```

### 4. Texture de bruit comme alternative au gradient
```css
/* Ajouter de la profondeur sans couleur saturée */
.surface-depth {
  background:
    url("data:image/svg+xml,%3Csvg...%3E") repeat,  /* grain SVG */
    oklch(0.14 0.015 240);
  background-blend-mode: overlay;
}
```

---

## Animations Narratives (alternatives au parallaxe)

### 1. Reveal au scroll — CSS natif (aucun JS)
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

/* Stagger : délai croissant pour les éléments frères */
.reveal:nth-child(2) { animation-delay: 60ms; }
.reveal:nth-child(3) { animation-delay: 120ms; }
```

### 2. Compteur animé (données clés)
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

### 3. Texte qui se dévoile (masking)
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

### 4. Morphing de forme SVG
```tsx
// Transition entre deux paths SVG au hover — identité visuelle forte
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

## Micro-interactions Émotionnelles

### Bouton qui "respire" au succès
```css
@keyframes success-pulse {
  0%   { box-shadow: 0 0 0 0 oklch(var(--primary) / 0.4); }
  70%  { box-shadow: 0 0 0 8px oklch(var(--primary) / 0); }
  100% { box-shadow: 0 0 0 0 oklch(var(--primary) / 0); }
}

.btn--success { animation: success-pulse 600ms ease-out; }
```

### Input qui signale l'erreur (sans rouge agressif)
```css
@keyframes shake-subtle {
  0%, 100% { translate: 0; }
  25%       { translate: -3px 0; }
  75%       { translate: 3px 0; }
}
.input--error { animation: shake-subtle 300ms ease; }
```

### Checkbox avec path animé
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

## Typographies Variables Recommandées

| Famille | Style | Axes disponibles | Cas d'usage |
|---------|-------|-----------------|-------------|
| Fraunces | Serif organique | `SOFT`, `WONK`, `opsz`, `wght` | Landings premium, édito |
| Recursive | Mono/Sans hybride | `MONO`, `CASL`, `CRSV`, `slnt` | Dev tools, interfaces techniques |
| Raleway | Géométrique | `wght` | SaaS propre, moderne |
| Cabinet Grotesk | Grotesque | `wght` | Startups tech |
| Libre Baskerville | Serif classique | — | Contenu long, confiance |

**Chargement optimisé :**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preload" as="font" crossorigin>
```

```css
/* Font variable — activer les axes dans CSS */
body {
  font-family: 'Fraunces', serif;
  font-variation-settings: 'SOFT' 50;
  font-optical-sizing: auto;
}
```

---

## prefers-reduced-motion — Template universel

Toujours inclure ce bloc dans `globals.css` :

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  
  /* Conserver les transitions fonctionnelles (focus, états) */
  :focus-visible {
    transition: outline-offset 0ms !important;
  }
}
```
