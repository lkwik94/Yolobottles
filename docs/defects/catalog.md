---
tags: [defects, catalog, yolo]
created: 2026-04-28
updated: 2026-04-28
status: active
---

# Defect Catalog | Catalogue des défauts

See also: [[index]] · [[architecture/overview]] · [[training/dataset-guide]]

---

## English

### Camera view reminder

All defects are observed from **above**, through the bottle neck, looking at the **bottom of the bottle**. The image is roughly **circular** (bounded by the neck opening). The mold gate vestige (injection point of the preform) is typically visible at the center.

```
        ┌─────────┐
       /  neck rim  \       ← image boundary
      │  ┌───────┐  │
      │  │ gate  │  │       ← center: preform gate vestige
      │  │vestige│  │
      │  └───────┘  │
      │   PET wall  │       ← sidewall visible near edge
       \           /
        └─────────┘
```

### Defect classes

| ID | Class | Severity | Frequency |
|----|-------|----------|-----------|
| 0 | [[defects/color_defect\|color_defect]] | Medium | Low |
| 1 | [[defects/hole\|hole]] | Critical | Very low |
| 2 | [[defects/contamination\|contamination]] | High | Low–Medium |
| 3 | [[defects/whitening\|whitening]] | Medium–High | Medium |
| 4 | [[defects/mold_defect\|mold_defect]] | Medium | Low |

> [!WARNING] Class imbalance
> On a healthy production line, OK bottles far outnumber NG (typically 1–5% reject rate).
> Dataset must be **balanced** during training — see [[training/dataset-guide#Class balance]].

### Decision logic

A bottle is **NG** if **any detection** exceeds the confidence threshold (default: 0.5).
Multiple defects on a single bottle are possible and all are reported.

```
detections = model.infer(frame)
result = "NG" if len(detections) > 0 else "OK"
```

### Severity definitions

| Level | Meaning | Action |
|-------|---------|--------|
| **Critical** | Safety or structural failure risk | Always eject, alert operator |
| **High** | Likely to cause downstream issue | Eject |
| **Medium** | Cosmetic or minor structural | Eject (configurable threshold) |
| **Low** | Borderline — monitor rate | Log only (future: configurable) |

### Data collection priority

Collect images in this priority order:

1. **Whitening** — most common, easiest to generate (mechanical stress on preform)
2. **Contamination** — common, varied in appearance
3. **Mold defect** — controlled: use known bad molds
4. **Color defect** — less common, may require artificial generation
5. **Hole** — very rare, consider synthetic augmentation

---

## Français

### Rappel vue caméra

Tous les défauts sont observés **depuis le dessus**, à travers le goulot, en regardant le **fond de la bouteille**. L'image est approximativement **circulaire** (délimitée par l'ouverture du goulot). Le vestige de la carotte (point d'injection de la préforme) est généralement visible au centre.

### Classes de défauts

| ID | Classe | Sévérité | Fréquence |
|----|--------|----------|-----------|
| 0 | [[defects/color_defect\|color_defect]] | Moyenne | Faible |
| 1 | [[defects/hole\|hole]] | Critique | Très faible |
| 2 | [[defects/contamination\|contamination]] | Haute | Faible–Moyenne |
| 3 | [[defects/whitening\|whitening]] | Moyenne–Haute | Moyenne |
| 4 | [[defects/mold_defect\|mold_defect]] | Moyenne | Faible |

> [!WARNING] Déséquilibre de classes
> Sur une ligne saine, les bouteilles OK sont très majoritaires (typiquement 1–5% de rejet).
> Le dataset doit être **équilibré** à l'entraînement — voir [[training/dataset-guide#Class balance]].

### Logique de décision

Une bouteille est **NG** si **au moins une détection** dépasse le seuil de confiance (défaut : 0,5).
Plusieurs défauts sur une même bouteille sont possibles et tous sont reportés.

### Priorité de collecte des données

Collecter les images dans cet ordre de priorité :

1. **Blanchissement** — le plus courant, facilement reproductible (contrainte mécanique sur la préforme)
2. **Contamination** — courant, aspect varié
3. **Défaut de moule** — contrôlé : utiliser des moules défectueux connus
4. **Défaut de couleur** — moins courant, peut nécessiter une génération artificielle
5. **Trou** — très rare, envisager l'augmentation synthétique
