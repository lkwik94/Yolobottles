---
tags: [defects, mold, geometry, imprint]
created: 2026-04-28
updated: 2026-04-28
status: draft
---

# Mold Defect | Défaut de moule

See also: [[defects/catalog]] · [[machine/sidel-sbo]] · [[training/dataset-guide]]

---

## English

### Definition

Absence, distortion, or deformation of the **mold imprint on the bottle bottom**. The bottom of a blown PET bottle carries the geometric pattern stamped by the blow mold (petaloidal base, punt, ribs, etc.). A mold defect means this pattern is missing, incomplete, or incorrectly formed.

### Normal bottom geometry (reference)

Sidel SBO bottles typically use one of:

| Base type | Description |
|-----------|-------------|
| **Champagne / punt** | Central dome punched inward — common for CSD |
| **Petaloidal (star base)** | 5 or 6 feet radiating from center — common for still water |
| **Flat base** | Flat with central gate vestige — common for hot-fill |

> [!IMPORTANT] Know your bottle
> The mold defect definition depends entirely on the **expected base geometry**.
> Document the reference pattern in [[machine/inspection-point]] before collecting NG images.

### Defect subtypes

| Subtype | Appearance | Cause |
|---------|-----------|-------|
| **Missing imprint** | Bottom looks flat / smooth where pattern expected | Too low blow pressure, short blow time |
| **Partial imprint** | Pattern present on one side only | Uneven mold contact, cold zone on preform |
| **Excess material (blob)** | Thick bulge at bottom center or edge | Gate vestige too large, preform not aligned |
| **Sunken panel** | One petal/foot is collapsed inward | Mold vent blocked, localized cooling issue |
| **Mold flash** | Thin PET fin along parting line | Worn mold, excessive blow pressure |

### Annotation guidance

- Box the **region of the bottom where the defect is located** (not the entire bottom unless fully absent)
- For missing imprint: box the full expected pattern area
- For partial imprint: box only the missing/malformed section
- For flash: box along the parting line where the fin is visible

### Training notes

- This class requires **domain knowledge** to annotate correctly — reviewer must know what the reference pattern looks like
- Collect from **known bad mold cavities** (cavity number correlates with consistent defect pattern on SBO)
- On a 34-cavity SBO, one bad cavity generates ~1/34 of all NG mold defects → check per-cavity reject rate
- Consider creating a separate `reference/bottom_patterns/` folder with annotated reference images

---

## Français

### Définition

Absence, distorsion ou déformation de **l'empreinte du moule sur le fond de bouteille**. Le fond d'une bouteille PET soufflée porte le motif géométrique imprimé par le moule de soufflage (fond pétaloïde, pieds, nervures, etc.). Un défaut de moule signifie que ce motif est absent, incomplet ou mal formé.

### Géométrie de fond normale (référence)

Les bouteilles Sidel SBO utilisent typiquement l'un des fonds suivants :

| Type de fond | Description |
|--------------|-------------|
| **Champagne / punt** | Dôme central rentrant — courant pour les boissons gazeuses |
| **Pétaloïde (étoile)** | 5 ou 6 pieds rayonnant depuis le centre — courant pour l'eau plate |
| **Fond plat** | Plat avec vestige de carotte central — courant pour le remplissage à chaud |

> [!IMPORTANT] Connaître la bouteille
> La définition du défaut de moule dépend entièrement de la **géométrie de fond attendue**.
> Documenter le motif de référence dans [[machine/inspection-point]] avant de collecter des images NG.

### Sous-types de défauts

| Sous-type | Aspect | Cause |
|-----------|--------|-------|
| **Empreinte manquante** | Fond lisse là où un motif est attendu | Pression de soufflage trop faible, temps de soufflage court |
| **Empreinte partielle** | Motif présent d'un seul côté | Contact moule inégal, zone froide sur préforme |
| **Excès de matière (bosse)** | Bourrelet épais au centre ou au bord du fond | Carotte trop grosse, préforme mal centrée |
| **Panneau affaissé** | Un pied / pétale effondré vers l'intérieur | Évent moule bouché, problème de refroidissement localisé |
| **Flash de moule** | Fine nervure PET le long de la ligne de joint | Moule usé, pression de soufflage excessive |

### Notes d'entraînement

- Cette classe nécessite une **connaissance métier** pour annoter correctement — l'annotateur doit connaître le motif de référence
- Collecter depuis des **empreintes de moule défectueuses connues** (le numéro de cavité est corrélé à un motif de défaut cohérent sur le SBO)
- Sur un SBO 34 empreintes, une mauvaise cavité génère ~1/34 de tous les défauts de moule NG → vérifier le taux de rejet par cavité
- Envisager un dossier `reference/bottom_patterns/` avec des images de référence annotées
