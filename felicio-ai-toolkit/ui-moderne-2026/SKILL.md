---
name: ui-moderne-2026
description: >
  Concevoir des interfaces utilisateur modernes, distinctives et non-génériques en 2026.
  Utilise ce skill dès que l'utilisateur demande de créer, améliorer, styliser ou repenser
  une interface, un composant, une page web, un dashboard, une landing page, une application
  SaaS, un design system, ou tout élément visuel frontend — même s'il ne mentionne pas
  explicitement "UI" ou "design". Déclenche aussi quand l'utilisateur donne des commandes
  d'installation Shadcn (`npx shadcn@latest add ...`), mentionne Tailwind v4, OKLCH, ou
  demande quelque chose "d'original", "de premium", "de non-générique", "de cinématographique"
  ou "d'unique". Ce skill remplace le skill frontend-design générique pour tout contexte
  exigeant un niveau de craft et d'intentionnalité élevé.
---

# UI Moderne 2026 — Skill de Conception Non-Générique

Concevoir des interfaces qui respirent l'intentionnalité, le craft et la singularité de marque.
Ce skill guide chaque décision de design et d'implémentation pour éviter la **fatigue des templates**
et produire des expériences mémorables, humaines et premium.

---

## Workflow — Par où commencer

Avant d'écrire une seule ligne de code, exécute ce workflow dans l'ordre :

**1. Lire le contexte**
- Quel est le produit, la cible, le ton attendu ?
- Y a-t-il des composants Shadcn à intégrer ? (voir section "Intégration de Composants")
- Y a-t-il une palette, une typo, un token de marque existant ?

**2. Choisir une direction esthétique tranchée** (pas un compromis tiède)
Sélectionne UN archétype et engage-toi à fond :

| Archétype | Signal visuel dominant | Quand l'utiliser |
|-----------|------------------------|-----------------|
| Éditorial Organique | Asymétrie, typographie massive, espaces généreux | Startups, portfolios, produits créatifs |
| Néo-Brutaliste | Contrastes extrêmes, bordures épaisses, raw | Dev tools, outils techniques, produits "rebels" |
| Minimalisme Précis | Espacement chirurgical, une seule couleur d'accent | SaaS B2B, finance, outils de productivité |
| Matière & Profondeur | Grain, textures subtiles, effets de surface | Premium, lifestyle, produits physiques digitalisés |
| Cinématographique | Scroll narratif, pacing temporel, plein écran | Landings immersives, portfolios, produits grand public |

**3. Valider la direction** avec l'utilisateur si ambiguïté, puis coder.

**4. Appliquer les règles non-négociables** (ci-dessous) avant de livrer.

---

## Règles Non-Négociables

### ✅ Faire absolument

- **Couleurs en OKLCH exclusivement** — voir `references/oklch.md`
- **Wrappper chaque composant Shadcn** avant de l'utiliser — voir `references/shadcn-components.md`
- **Tester le contraste WCAG** (AA minimum, AAA pour le body text) dès la génération
- **Inclure `prefers-reduced-motion`** pour chaque animation
- **Grain organique** sur tout projet premium (opacité 0.03–0.06, `mix-blend-mode: overlay`)
- **Une micro-interaction fonctionnelle émotionnelle** au minimum par interface

### 🚫 Interdits absolus — Anti-patterns Génériques

Ces éléments signalent immédiatement une interface produite "à la chaîne" :

**Effets visuels à bannir :**
- Ombres `box-shadow` lourdes ou multicouches → remplacer par des **bords nets, élévation via contraste colorimétrique OKLCH, ou ombre directionnelle ultra-fine** (`0 1px 2px oklch(0 0 0 / 0.08)`)
- Dégradés `gradient` trop marquants (dégradé violet→rose sur blanc, dégradé hero plein écran) → remplacer par des **transitions de teinte subtiles** (`oklch(L C H1)` → `oklch(L C H2)`, delta H ≤ 30°)
- Effets spotlight / glow radial trop saturés → remplacer par un **grain lumineux directionnel** ou une **zone de focus via variation de L uniquement**
- Zoom au hover sur cartes ou images → remplacer par **translation légère** (`translateY(-2px)`), **changement de border-color**, ou **reveal de contenu masqué**
- Animations "wow" vides (parallaxe agressive, particules flottantes) → remplacer par des **animations au service du sens** (révélation de donnée, progression narrative)

**Patterns de layout à bannir :**
- Grille 3 colonnes de cards identiques → varier les tailles, jouer le rythme
- Hero centré logo + titre + CTA sur fond uni → construire une composition
- Navigation sticky avec blur-backdrop toujours identique → explorer des alternatives de navigation

**Typographie à bannir :**
- Inter, Roboto, Arial, system-ui comme font principale → choisir une police variable avec personnalité
- Hiérarchie uniquement par taille → utiliser le poids, l'espacement, la couleur OKLCH et le mouvement

---

## Intégration de Composants Shadcn

Quand l'utilisateur fournit une commande d'installation Shadcn, voici le protocole exact :

### Étape 1 — Identifier le composant installé
```bash
# Exemple de commande fournie par l'utilisateur :
npx shadcn@latest add card button badge
```
Identifie chaque composant : `Card`, `Button`, `Badge`.

### Étape 2 — Lire les fichiers générés (ne jamais supposer la structure)
```
components/ui/card.tsx      ← composant brut Shadcn
components/ui/button.tsx    ← composant brut Shadcn
```

### Étape 3 — Créer les wrappers de marque (JAMAIS modifier les fichiers `/ui/` directement)

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
        // Tokens de marque — remplacer les defaults Shadcn
        "rounded-xl border-[oklch(var(--border))] bg-[oklch(var(--card))]",
        // Pas de box-shadow lourde — élévation par contraste
        variant === "elevated" && "border-[oklch(var(--border-strong))] bg-[oklch(var(--card-elevated))]",
        variant === "ghost" && "border-transparent bg-transparent",
        // Grain optionnel
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

### Étape 4 — Adapter au projet spécifique

Pour chaque composant Shadcn reçu, demande-toi :
1. **Quel est le contexte métier ?** (dashboard analytics, landing SaaS, e-commerce...)
2. **Quelles variantes contextuelles sont nécessaires ?** (état vide, état chargement, état erreur...)
3. **Quelle micro-interaction distinctive ajouter ?** (pas de zoom — chercher un effet original)

Consulte `references/shadcn-components.md` pour les patterns de wrapping par type de composant.

---

## Système de Couleurs — OKLCH Obligatoire

Utilise uniquement OKLCH. Consulte `references/oklch.md` pour le guide complet.

**Principe essentiel — dérivation depuis une seule teinte :**
```css
:root {
  /* Couleur de base : H fixe, L et C variables */
  --brand-h: 264;           /* La teinte ne change JAMAIS */
  
  --primary:     oklch(0.25 0.08 var(--brand-h));
  --primary-sub: oklch(0.35 0.06 var(--brand-h));
  --accent:      oklch(0.55 0.14 var(--brand-h));  /* +C pour l'accent */
  --muted:       oklch(0.70 0.02 var(--brand-h));  /* -C pour le muted */
  
  --background:  oklch(0.98 0.005 var(--brand-h)); /* Quasi-neutre, légère teinte */
  --foreground:  oklch(0.12 0.02 var(--brand-h));
  
  /* Surfaces — jamais de blanc/noir pur */
  --card:        oklch(0.96 0.008 var(--brand-h));
  --border:      oklch(0.88 0.01 var(--brand-h));
}

.dark {
  /* Même H, inverser L, légèrement ajuster C */
  --background:  oklch(0.13 0.01 var(--brand-h));
  --foreground:  oklch(0.95 0.01 var(--brand-h));
  --card:        oklch(0.18 0.015 var(--brand-h));
  --border:      oklch(0.28 0.02 var(--brand-h));
}
```

**Outil de validation contraste :** toujours vérifier le ratio entre `--foreground` et `--background` (objectif ≥ 4.5:1).

---

## Effets Originaux — Catalogue de Remplacement

Ces effets remplacent les patterns génériques bannis. Choisir selon l'archétype esthétique.

### Au lieu du zoom hover → Reveal de contenu
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

### Au lieu du box-shadow lourd → Bord coloré directionnel
```css
.card {
  border: 1px solid oklch(var(--border));
  transition: border-color 150ms ease;
}
.card:hover {
  border-color: oklch(var(--accent));
  /* Un seul côté pour un effet directionnel */
  border-left-color: oklch(var(--primary));
}
```

### Au lieu du gradient spotlight → Focus via luminosité OKLCH
```css
/* L'élément focusé est plus lumineux, pas éclairé par un spot */
.focus-zone {
  background: oklch(0.22 0.04 264);
}
.focus-zone:hover {
  background: oklch(0.28 0.05 264); /* +6% L seulement */
}
```

### Au lieu du parallaxe agressif → Scroll-Driven Animation CSS native
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

### Grain organique (effet premium, pas de texture collante)
```css
/* Overlay via pseudo-élément, n'affecte pas l'interactivité */
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

### Typographie cinétique — Variable font réactive
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

Chaque scroll doit **raconter quelque chose**. Cinq règles :

1. **La donnée EST l'histoire** — révéler les chiffres/stats progressivement, pas en dump
2. **Respiration temporelle** — alterner sections denses et espaces de "souffle"
3. **Un message par écran** — pas de compétition visuelle entre éléments
4. **Mouvement au service de la clarté** — si une animation ne clarifie pas, la supprimer
5. **Interaction = exploration** — laisser l'utilisateur "découvrir" plutôt que "recevoir"

```css
/* View Transitions API — transitions entre états sans JS */
@view-transition { navigation: auto; }

::view-transition-old(root) {
  animation: 200ms ease out slide-out;
}
::view-transition-new(root) {
  animation: 300ms ease in slide-in;
}
```

---

## Checklist de Livraison

Avant de livrer toute interface, valider point par point :

- [ ] **Couleurs** — 100% en OKLCH, aucune valeur HSL/RGB/hex dans les tokens
- [ ] **Contraste** — ratio ≥ 4.5:1 pour body, ≥ 3:1 pour UI components
- [ ] **Composants** — tous wrappés dans `/primitives/` ou `/blocks/`, jamais `/ui/` modifié directement
- [ ] **Ombres** — aucune `box-shadow` lourde (max `0 1px 3px oklch(0 0 0 / 0.08)`)
- [ ] **Dégradés** — aucun dégradé saturé sur fond blanc/noir, delta H ≤ 30° si dégradé
- [ ] **Zoom** — aucun `scale()` au hover sur cartes ; remplacé par effet alternatif
- [ ] **Animations** — toutes avec `prefers-reduced-motion: reduce` → `animation: none`
- [ ] **Grain** — présent sur au minimum la surface hero pour tout projet premium
- [ ] **Typo** — police variable ou caractérielle, pas Inter/Roboto/Arial
- [ ] **Mode sombre** — tokens `.dark` définis et testés

---

## Architecture du Code

```
src/
├── components/
│   ├── ui/            ← Shadcn brut (JAMAIS modifié directement)
│   ├── primitives/    ← Wrappers marque (AppButton, AppCard, AppInput...)
│   └── blocks/        ← Compositions métier (HeroSection, PricingCard, FeatureGrid...)
├── styles/
│   └── tokens.css     ← Variables OKLCH (:root + .dark)
└── lib/
    └── utils.ts       ← cn() et helpers
```

---

## Références

- `references/oklch.md` — Guide complet OKLCH : syntaxe, dérivation, outils, exemples
- `references/shadcn-components.md` — Patterns de wrapping par composant (Button, Card, Input, Dialog, Table, Badge, etc.)
- `references/effects-catalog.md` — Catalogue étendu d'effets originaux avec code prêt à l'emploi

*Ce skill est vivant. Le mettre à jour à chaque évolution majeure de Tailwind, Shadcn UI ou CSS natif.*
