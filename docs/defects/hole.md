---
tags: [defects, structural, critical]
created: 2026-04-28
updated: 2026-04-28
status: draft
---

# Hole | Trou / Criqure

See also: [[defects/catalog]] · [[defects/whitening]] · [[training/dataset-guide]]

---

## English

### Definition

Perforation, crack, or tear in the PET wall of the bottle bottom. Ranges from a pinhole (< 1 mm) to a visible crack or full split. **Critical severity** — a bottle with a hole will leak and cannot be filled.

### Visual appearance (top-down view)

- **Pinhole**: very small dark dot, can look like [[defects/contamination]] — key difference is that a hole shows **transmitted light** if backlit, or a **distinct dark core** with sharp edges
- **Crack**: linear dark mark, often radiating from the gate vestige center
- **Split**: visible gap in the PET wall

> [!WARNING] Detection difficulty
> Pinholes are the hardest defect to detect in this class.
> A backlit setup (light source below the bottle) dramatically improves pinhole visibility.
> With top-down coaxial light only, very small holes may be missed.

### Root causes on SBO blower

| Cause | Zone |
|-------|------|
| Stretch rod over-extension | Bottom center (gate area) |
| Insufficient pre-blow pressure | Bottom / sidewall transition |
| Cold spot on preform (oven fault) | Anywhere |
| Mold damage or contamination | Near mold parting line |

### Annotation guidance

- Box the hole tightly — small boxes are fine, YOLO handles them
- For cracks: box the full crack length, not just the tip
- If uncertain whether it's a hole or contamination: label as [[defects/contamination]] and note in filename

### Training notes

- **Very rare** in real production — synthetic generation may be necessary
- Generate synthetic holes: erode small circular masks on OK images
- May require lower confidence threshold (0.4) due to rarity and small size

---

## Français

### Définition

Perforation, criqure ou déchirure dans la paroi PET du fond de bouteille. Va du micropore (< 1 mm) à une criqure visible ou une fissure complète. **Sévérité critique** — une bouteille percée fuit et ne peut pas être remplie.

### Aspect visuel (vue de dessus)

- **Micropore** : très petite tache sombre, ressemble à [[defects/contamination]] — différence clé : un trou laisse passer la lumière en transmission, ou présente un **cœur sombre distinct** aux bords nets
- **Criqure** : marque sombre linéaire, souvent rayonnant depuis la carotte centrale
- **Fissure** : espace visible dans la paroi PET

> [!WARNING] Difficulté de détection
> Les micropores sont les défauts les plus difficiles à détecter dans cette classe.
> Un éclairage par transmission (source lumineuse sous la bouteille) améliore considérablement la visibilité.
> Avec uniquement un éclairage coaxial vue de dessus, les très petits trous peuvent être manqués.

### Causes racines sur souffleuse SBO

| Cause | Zone |
|-------|------|
| Sur-extension de la tige d'étirage | Centre fond (zone carotte) |
| Pression de pré-soufflage insuffisante | Fond / transition paroi |
| Point froid sur préforme (défaut four) | Partout |
| Moule endommagé ou contaminé | Près de la ligne de joint |

### Notes d'entraînement

- **Très rare** en production réelle — génération synthétique probablement nécessaire
- Générer des trous synthétiques : éroder de petits masques circulaires sur des images OK
- Peut nécessiter un seuil de confiance plus bas (0,4) en raison de la rareté et de la petite taille
