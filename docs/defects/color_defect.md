---
tags: [defects, color, pet]
created: 2026-04-28
updated: 2026-04-28
status: draft
---

# Color Defect | Défaut de couleur

See also: [[defects/catalog]] · [[defects/whitening]] · [[training/dataset-guide]]

---

## English

### Definition

Abnormal coloration of the PET bottle bottom visible from above through the neck. Includes yellowing, brownish tint, black areas, or uneven color distribution not explained by [[defects/whitening|stress whitening]].

### Root causes on SBO blower

| Cause | Mechanism |
|-------|-----------|
| **Preform resin degradation** | Overheated PET in the injection molding stage → acetaldehyde formation, yellowing |
| **Oven over-heating** | Excessive IR exposure in the stretch-blow oven → localized browning |
| **Contaminated preform batch** | Off-spec colorant, recycled PET impurity |
| **Hot mold contact** | Localized heat mark on the bottom |

> [!NOTE] Visual signature
> Unlike [[defects/whitening]], color defects show **hue shift** (yellow, brown, black), not opacity change.
> Whitening keeps the PET transparent but turns it milky-white.

### Annotation guidance

- Draw a **bounding box** around the discolored zone
- If the entire bottom is uniformly off-color, box the full visible circle
- Minimum confidence threshold: 0.5 (adjustable — color is harder to detect under varying lighting)

> [!TIP] Lighting matters
> Color defects are **very sensitive to illumination color temperature**. Annotate only images captured under the same lighting setup as production.

### Training notes

- Difficult to collect naturally — may require intentionally degraded preforms
- Consider synthetic augmentation: hue-shift OK bottles in HSV color space
- Watch for confusion with [[defects/contamination]] (small dark spot vs. large dark area)

---

## Français

### Définition

Coloration anormale du fond de bouteille PET visible depuis le dessus par le goulot. Inclut le jaunissement, la teinte brunâtre, les zones noires, ou une distribution de couleur non uniforme non expliquée par le [[defects/whitening|blanchissement sous contrainte]].

### Causes racines sur souffleuse SBO

| Cause | Mécanisme |
|-------|-----------|
| **Dégradation de la résine préforme** | PET surchauffé en injection → formation d'acétaldéhyde, jaunissement |
| **Surchauffe four** | Exposition IR excessive dans le four d'étirage-soufflage → brunissement localisé |
| **Lot de préformes contaminé** | Colorant hors-spec, impureté PET recyclé |
| **Contact moule chaud** | Marque thermique localisée sur le fond |

### Conseils d'annotation

- Tracer une **bounding box** autour de la zone décolorée
- Si tout le fond est uniformément hors couleur, encadrer l'ensemble du cercle visible
- Seuil de confiance minimum : 0,5 (ajustable — la couleur est plus difficile à détecter avec un éclairage variable)

### Notes d'entraînement

- Difficile à collecter naturellement — peut nécessiter des préformes intentionnellement dégradées
- Envisager l'augmentation synthétique : décaler la teinte des bouteilles OK dans l'espace HSV
- Surveiller la confusion avec [[defects/contamination]] (petite tache sombre vs grande zone sombre)
