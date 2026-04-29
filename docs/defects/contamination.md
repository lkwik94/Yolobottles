---
tags: [defects, contamination, inclusion]
created: 2026-04-28
updated: 2026-04-28
status: draft
---

# Contamination | Contamination

See also: [[defects/catalog]] · [[defects/hole]] · [[defects/color_defect]] · [[training/dataset-guide]]

---

## English

### Definition

Foreign particle, inclusion, or surface deposit on or within the PET wall visible from the bottle bottom. Typically appears as a **dark spot, speck, or irregular mark** embedded in or on the transparent PET.

### Types

| Type | Appearance | Location |
|------|-----------|----------|
| **Carbon black inclusion** | Sharp black dot, defined edges | In PET wall |
| **Metal particle** | Bright or dark speck, sometimes reflective | In PET wall |
| **Mold release agent residue** | Diffuse white haze or streaks | Surface (bottom) |
| **Dust / debris** | Irregular shape, variable color | Surface |
| **Burnt PET flake** | Dark, often with yellowish halo | In PET wall |

> [!NOTE] In-wall vs surface
> Surface contaminants can be washed off — they are a cosmetic issue.
> In-wall inclusions are structural and should always trigger ejection.
> In top-down camera view, both look similar. Label them all as `contamination`.

### Visual confusion risks

| Looks like | How to distinguish |
|------------|-------------------|
| [[defects/hole\|Hole (pinhole)]] | Hole has transmitted-light effect or sharp bright edge; contamination is flat |
| [[defects/color_defect\|Color defect]] | Contamination is localized (spot); color defect is area-wide |

### Annotation guidance

- Box each contamination spot individually if multiple are present
- Minimum box size: 5×5 px in the 640×640 input — smaller is probably noise
- Annotate all spots regardless of size (let the confidence threshold filter)

### Training notes

- Most varied class in appearance — collect as many different visual examples as possible
- Good candidate for **copy-paste augmentation**: paste contamination crops onto OK images
- High risk of false positives from dirt on the camera lens — dedicate a regular cleaning protocol

---

## Français

### Définition

Particule étrangère, inclusion ou dépôt de surface dans ou sur la paroi PET visible depuis le fond de bouteille. Apparaît généralement comme une **tache sombre, granule ou marque irrégulière** intégrée ou posée sur le PET transparent.

### Types

| Type | Aspect | Localisation |
|------|--------|--------------|
| **Inclusion carbone (noir de carbone)** | Point noir net, bords définis | Dans la paroi PET |
| **Particule métallique** | Granule brillante ou sombre, parfois réfléchissante | Dans la paroi PET |
| **Résidu d'agent démoulant** | Voile blanc diffus ou stries | Surface (fond) |
| **Poussière / débris** | Forme irrégulière, couleur variable | Surface |
| **Paillette de PET brûlé** | Sombre, souvent avec halo jaunâtre | Dans la paroi PET |

> [!NOTE] Incluse vs surface
> Les contaminations de surface peuvent être lavées — c'est un problème cosmétique.
> Les inclusions dans la paroi sont structurelles et doivent toujours déclencher l'éjection.
> En vue caméra de dessus, les deux aspects sont similaires. Les étiqueter toutes comme `contamination`.

### Risques de confusion visuelle

| Ressemble à | Comment distinguer |
|-------------|-------------------|
| [[defects/hole\|Trou (micropore)]] | Le trou a un effet de lumière transmise ou un bord brillant net ; la contamination est plate |
| [[defects/color_defect\|Défaut de couleur]] | La contamination est localisée (spot) ; le défaut de couleur est étendu |

### Notes d'entraînement

- Classe la plus variée en apparence — collecter autant d'exemples visuels différents que possible
- Bon candidat pour l'**augmentation copy-paste** : coller des crops de contamination sur des images OK
- Risque élevé de faux positifs liés à la saleté sur l'objectif — prévoir un protocole régulier de nettoyage
