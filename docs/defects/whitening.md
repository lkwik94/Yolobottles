---
tags: [defects, whitening, pet-stress, mechanical]
created: 2026-04-28
updated: 2026-04-28
status: draft
---

# Whitening | Blanchissement PET

See also: [[defects/catalog]] · [[defects/color_defect]] · [[training/dataset-guide]]

---

## English

### Definition

**Stress whitening** of the PET material — localized loss of transparency producing a milky-white, opaque zone. The PET retains its structure but the crystalline microstructure has been disrupted by excessive mechanical stress during blow molding, causing light scattering.

This is **not a color change** but a **transparency change** — the area turns opaque white, not yellow or brown.

### Physical mechanism

During biaxial stretching in the SBO:
- If PET is stretched **too fast** or at **too low a temperature**, the amorphous chains cannot orient properly
- Stress-induced crystallization creates large crystallites that scatter visible light → white appearance
- This is distinct from thermal crystallization (which also whitens but occurs at high temperature)

### Visual appearance (top-down)

- **Diffuse white cloud**: soft-edged, covers a zone of the bottom
- **Radial streaks**: white lines radiating from gate vestige outward
- **Ring whitening**: annular white band at a specific radius from center (oven cold ring)
- Affected zone appears brighter / more reflective than surrounding transparent PET

> [!NOTE] Most common defect
> Whitening is typically the **most frequently occurring** defect class on a running SBO line.
> It is the best candidate to collect in large quantities for dataset balance.

### Root causes on SBO blower

| Cause | Pattern |
|-------|---------|
| Cold preform zone (oven lamp fault, shadow) | Localized streaks or patches |
| Stretch rod speed too high | Center bottom radial marks |
| Pre-blow pressure too high / too early | Bottom dome whitening |
| Preform wall too thick (design issue) | Full bottom whitening |
| Oven chain speed too fast (short heating time) | Diffuse global whitening |

### Annotation guidance

- Box the white zone(s) — can be large (full bottom) or small (streak)
- Multiple separate white areas on one bottle → multiple bounding boxes
- Do not box the gate vestige normal appearance (naturally slightly hazy in some resins)

### Training notes

- **Most collectable** defect — prioritize for initial dataset
- Strong signal in luminance channel: the white zone is brighter than surrounding transparent PET
- Rotate images freely (360°) — whitening pattern has no preferred orientation
- Can be used to validate that the rotation augmentation is working correctly

---

## Français

### Définition

**Blanchissement sous contrainte** du matériau PET — perte localisée de transparence produisant une zone blanche laiteuse et opaque. Le PET conserve sa structure mais la microstructure cristalline a été perturbée par une contrainte mécanique excessive lors du soufflage, provoquant une diffusion de la lumière.

Ce n'est **pas un changement de couleur** mais un **changement de transparence** — la zone devient opaque blanche, pas jaune ou brune.

### Mécanisme physique

Lors de l'étirage biaxial dans le SBO :
- Si le PET est étiré **trop vite** ou à **trop basse température**, les chaînes amorphes ne peuvent pas s'orienter correctement
- La cristallisation induite par contrainte crée de gros cristallites qui diffusent la lumière visible → aspect blanc
- Distinct de la cristallisation thermique (qui blanchit aussi mais à haute température)

### Aspect visuel (vue de dessus)

- **Nuage blanc diffus** : bords flous, couvre une zone du fond
- **Stries radiales** : lignes blanches rayonnant depuis la carotte vers l'extérieur
- **Blanchissement en anneau** : bande blanche annulaire à un rayon spécifique depuis le centre (anneau froid du four)
- La zone affectée apparaît plus lumineuse / plus réfléchissante que le PET transparent environnant

> [!NOTE] Défaut le plus fréquent
> Le blanchissement est typiquement le défaut **le plus fréquent** sur une ligne SBO en production.
> C'est le meilleur candidat à collecter en grandes quantités pour équilibrer le dataset.

### Causes racines sur souffleuse SBO

| Cause | Motif |
|-------|-------|
| Zone froide sur préforme (panne lampe four, ombre) | Stries ou taches localisées |
| Vitesse tige d'étirage trop élevée | Marques radiales centre fond |
| Pression pré-soufflage trop élevée / trop précoce | Blanchissement dôme fond |
| Paroi préforme trop épaisse (problème conception) | Blanchissement fond complet |
| Vitesse chaîne four trop rapide (temps de chauffe court) | Blanchissement global diffus |

### Notes d'entraînement

- Défaut **le plus collectable** — priorité pour le dataset initial
- Signal fort dans le canal luminance : la zone blanche est plus lumineuse que le PET transparent environnant
- Rotation libre des images (360°) — le motif de blanchissement n'a pas d'orientation préférentielle
- Peut être utilisé pour valider que l'augmentation par rotation fonctionne correctement
