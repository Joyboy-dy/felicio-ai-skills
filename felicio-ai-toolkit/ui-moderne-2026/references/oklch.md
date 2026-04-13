# Référence OKLCH — Espace Colorimétrique Perceptuel

## Pourquoi OKLCH et pas HSL

- **HSL** : la luminosité perçue varie selon la teinte → du jaune HSL(60, 100%, 50%) semble BEAUCOUP plus lumineux que du bleu HSL(240, 100%, 50%) à valeur L identique. Résultat : retravailler manuellement les contrastes en dark mode.
- **OKLCH** : luminosité perceptuellement uniforme → `oklch(0.55 0.15 H)` a le même niveau de luminosité perçue quelle que soit la teinte H. Le dark mode se génère mécaniquement.

## Syntaxe

```css
oklch(L C H)
oklch(L C H / alpha)

/* L : 0 (noir) → 1 (blanc) */
/* C : 0 (gris) → ~0.4 (couleur maximale) */
/* H : 0→360 (teinte, en degrés) */
```

## Table de référence des teintes

| H | Couleur | Usages typiques |
|---|---------|-----------------|
| 0–30 | Rouge → Orange | Alertes, CTA urgents |
| 30–60 | Orange → Jaune | Avertissements, énergie |
| 80–150 | Jaune-vert → Vert | Succès, santé, finance |
| 160–220 | Cyan → Bleu-ciel | Tech, confiance légère |
| 220–270 | Bleu → Violet-bleu | SaaS, productivité |
| 270–320 | Violet → Magenta | Créatif, premium |
| 320–360 | Rose → Rouge | Emotion, urgence douce |

## Dérivation de palette depuis une couleur de base

**Principe : fixer H, faire varier L et C uniquement.**

```css
/* Couleur de base choisie : H = 240 (bleu) */
:root {
  /* Primaires */
  --color-900: oklch(0.20 0.10 240);  /* très foncé */
  --color-700: oklch(0.35 0.12 240);
  --color-500: oklch(0.50 0.15 240);  /* référence */
  --color-300: oklch(0.70 0.08 240);
  --color-100: oklch(0.92 0.02 240);  /* très clair */
  
  /* Accent complémentaire : H + 180° */
  --accent:    oklch(0.55 0.14 60);   /* H = 240 + 180° = 60° (jaune-or) */
  
  /* Neutre teinté (H inchangé, C quasi-zéro) */
  --neutral:   oklch(0.95 0.005 240);
}
```

## Génération automatisée du dark mode

```css
.dark {
  /* Inverser L : 0.20 → 0.85, 0.92 → 0.15 */
  /* Légèrement réduire C en dark (surfaces sombres saturées < surfaces claires) */
  --color-900: oklch(0.85 0.08 240);
  --color-700: oklch(0.72 0.10 240);
  --color-500: oklch(0.55 0.13 240);
  --color-300: oklch(0.38 0.08 240);
  --color-100: oklch(0.20 0.02 240);
}
```

## Outils recommandés

- **oklch.com** — picker interactif avec preview de contraste en temps réel
- **tweakcn.com** — générateur de thèmes Shadcn en OKLCH
- **Oklch Color Picker (VS Code extension)** — autocomplétion dans le CSS

## Tokens sémantiques Shadcn v4 (Tailwind v4)

Dans `tailwind.config.ts` ou `globals.css` avec Tailwind v4 :

```css
@layer base {
  :root {
    --background:   0.98 0.005 240;   /* Note : sans oklch() ici, Tailwind l'injecte */
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

## Validation contraste obligatoire

```js
// Fonction utilitaire (à copier dans un helper)
function oklchContrast(l1, l2) {
  // Approximation rapide — utiliser oklch.com pour validation précise
  const lum1 = Math.pow(l1, 2.2);
  const lum2 = Math.pow(l2, 2.2);
  const lighter = Math.max(lum1, lum2);
  const darker  = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Objectifs WCAG :
// Body text : ≥ 4.5:1
// Large text (>18px) : ≥ 3:1
// UI components : ≥ 3:1
```
