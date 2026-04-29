---
tags: [tool, inspector, hmi, rust, dashboard]
created: 2026-04-29
updated: 2026-04-29
status: active
---

# HMI Dashboard | Tableau de bord HMI

See also: [[index]] · [[architecture/overview]] · [[training/dataset-guide]]

---

## English

### Purpose

The HMI (Human-Machine Interface) is a live web dashboard served by the Rust inspector at `http://localhost:8080`.
It shows real-time inspection statistics while the inspector processes an image bank.

```
inspector (Rust) ──→ http://localhost:8080
                          ↓
                  Dark web dashboard
                  - KPI cards (Total / OK / NG / Reject%)
                  - Per-class defect breakdown
                  - Recent inspections table (last 50)
                  - Pipeline status (Running / Complete)
```

---

### Prerequisites

The inspector requires a trained ONNX model. Follow the full pipeline first:

```
1. Classify    → tools/importer
2. Annotate    → tools/annotator
3. Split       → training/prepare_dataset.py
4. Train       → training/train.py
5. Export ONNX → training/export_onnx.py
6. Inspect ✓   → inspector (this page)
```

---

### Build

```bash
# From project root
cd inspector
cargo build --release
```

Build output: `target/release/inspector.exe`

---

### Run

```bash
./target/release/inspector \
  --model ../models/exports/onnx/bottle_v1.onnx \
  --images ../datasets/raw \
  --threshold 0.5 \
  --port 8080
```

Then open: **http://localhost:8080**

| Argument | Default | Description |
|----------|---------|-------------|
| `--model` | required | Path to the `.onnx` model |
| `--images` | required | Folder of images to inspect (scanned recursively) |
| `--threshold` | `0.5` | Confidence threshold for detection |
| `--port` | `8080` | HMI web server port |
| `--eject-delay-ms` | `50` | Simulated ejector delay in ms (0 = disabled) |

---

### Dashboard sections

**KPI cards** — updated every second:
- **Inspected** — total images processed
- **OK** — no defect detected
- **NG** — at least one defect detected
- **Reject %** — NG / Total × 100

**OK/NG bar** — green = OK fraction, red = NG fraction

**Defect breakdown** — per-class NG count with a proportional bar.
Colors match the annotator tool:

| Class | Color |
|-------|-------|
| color_defect | orange |
| hole | red |
| contamination | purple |
| whitening | blue |
| mold_defect | teal |

**Recent inspections** — last 50 images, most recent first.
Each row shows: filename · OK/NG badge · detected class + confidence · inference time (ms)

**Status badge** — top-right corner:
- `Running…` (pulsing green dot) — pipeline in progress
- `Complete` (blue dot) — all images processed

---

### API endpoints

The inspector exposes two JSON endpoints:

```
GET /api/stats    → overall statistics + per-class counts + pipeline status
GET /api/history  → last 50 inspections (newest first)
```

Example `/api/stats` response:
```json
{
  "total": 29,
  "ok": 24,
  "ng": 5,
  "reject_rate_pct": 17.2,
  "pipeline_done": true,
  "class_counts": [
    {"name": "color_defect",   "count": 0},
    {"name": "hole",           "count": 4},
    {"name": "contamination",  "count": 1},
    {"name": "whitening",      "count": 0},
    {"name": "mold_defect",    "count": 0}
  ]
}
```

---

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `Error loading model` | Check that the `.onnx` file exists at the specified path |
| Dashboard shows `—` values | Server is starting; wait 1–2 seconds and refresh |
| No images processed | Check `--images` path; inspector scans for `.jpg`, `.jpeg`, `.png`, `.bmp` |
| Low confidence detections | Lower `--threshold` (e.g. `0.3`); retrain with more images |

---

## Français

### Objectif

Le HMI est un tableau de bord web en temps réel servi par l'inspector Rust sur `http://localhost:8080`.
Il affiche les statistiques d'inspection pendant que l'inspector traite une banque d'images.

---

### Prérequis

L'inspector nécessite un modèle ONNX entraîné. Suivre le pipeline complet :

```
1. Classifier  → tools/importer
2. Annoter     → tools/annotator
3. Préparer    → training/prepare_dataset.py
4. Entraîner   → training/train.py
5. Exporter    → training/export_onnx.py
6. Inspecter ✓ → inspector (cette page)
```

---

### Compilation

```bash
cd inspector
cargo build --release
```

---

### Lancement

```bash
./target/release/inspector \
  --model ../models/exports/onnx/bottle_v1.onnx \
  --images ../datasets/raw \
  --threshold 0.5 \
  --port 8080
```

Puis ouvrir : **http://localhost:8080**

---

### Sections du tableau de bord

- **Cartes KPI** — Total / OK / NG / Taux de rejet
- **Barre OK/NG** — proportion visuelle en temps réel
- **Breakdown par classe** — compteurs NG par type de défaut
- **Inspections récentes** — 50 dernières images avec résultat, défauts détectés et temps d'inférence
- **Badge statut** — `En cours…` ou `Terminé`

---

### Endpoints API

```
GET /api/stats    → statistiques globales + compteurs par classe + statut pipeline
GET /api/history  → 50 dernières inspections (plus récent en premier)
```
