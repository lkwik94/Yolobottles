---
tags: [training, dataset, annotation, labelimg]
created: 2026-04-29
updated: 2026-04-29
status: active
---

# Dataset Guide | Guide Dataset

See also: [[index]] · [[tools/importer]] · [[training/yolo-config]] · [[training/experiments]]

---

## English

### Position in the pipeline

```
✅ 1. Classify          importer tool     → datasets/raw/ok/  +  ng/<class>/
→  2. Annotate          annotator tool    → draw bounding boxes on NG images
→  3. Prepare split     prepare_dataset   → datasets/labeled/  (train / val)
   4. Train             train.py          → models/runs/
   5. Export ONNX       export_onnx.py    → models/exports/onnx/
   6. Inspect           inspector (Rust)  → http://localhost:8080
```

This page covers steps 2 and 3.

---

### Step 2 — Annotate with the Annotator tool

See the full guide: [[tools/annotator]]

The annotator is a browser-based tool built with Streamlit.
It replaces LabelImg (incompatible with Python 3.12 — `distutils` removed).

#### Run the annotator

```bash
cd tools/importer
.venv\Scripts\Activate.ps1           # Windows PowerShell
# source .venv/bin/activate          # Linux / macOS

streamlit run annotate.py
# Browser opens at http://localhost:8501
```

#### Workflow

1. Select the active **class** in the right panel (before drawing)
2. **Click and drag** on the image to draw a bounding box around the defect
3. Adjust the class per box if needed (dropdown below the canvas)
4. Click **Sauvegarder + Suivante** to save and move to the next image

> [!TIP] One box per defect
> If a bottle has two separate contamination spots, draw two boxes.
> If two different defect types are visible, draw one box per class.

> [!NOTE] OK images — no annotation needed
> Do not open `datasets/raw/ok/` in the annotator.
> The `prepare_dataset.py` script creates empty label files for OK images automatically.

#### What a label file looks like

After annotating, LabelImg creates a `.txt` file alongside each image:

```
# datasets/raw/ng/whitening/good_S1_I072.txt
3 0.412 0.631 0.180 0.240
```

Each line = one bounding box:
```
<class_id>  <cx>  <cy>  <width>  <height>
```

All values are **normalized** (0–1 relative to image size):
- `cx`, `cy` = center of the box
- `width`, `height` = size of the box

Class IDs as defined in `datasets/dataset.yaml`:

| ID | Class |
|----|-------|
| 0  | color_defect |
| 1  | hole |
| 2  | contamination |
| 3  | whitening |
| 4  | mold_defect |

---

### Step 3 — Prepare the train/val split

Once all NG images in `datasets/raw/ng/` are annotated (each has a `.txt` label file),
run the preparation script:

```bash
cd training

# Dry run first — shows what would be done without copying anything
python prepare_dataset.py --dry-run

# Run for real (default: 80% train / 20% val)
python prepare_dataset.py

# Custom split ratio
python prepare_dataset.py --val-ratio 0.15
```

The script:
1. Checks that every NG image has a non-empty label file (stops if any are missing)
2. Creates empty `.txt` label files for OK images (YOLO negative examples)
3. Shuffles randomly (seed=42 for reproducibility)
4. Copies image + label pairs to:
   - `datasets/labeled/images/train/` + `datasets/labeled/labels/train/`
   - `datasets/labeled/images/val/`   + `datasets/labeled/labels/val/`

> [!NOTE] Small datasets
> With fewer than 50 images total, use `--val-ratio 0.2` (20% val).
> With fewer than 20 images, skip the split and put everything in train:
> `python prepare_dataset.py --val-ratio 0`

---

### Verify before training

```powershell
# Count images and labels (must be equal) — PowerShell
(Get-ChildItem datasets/labeled/images/train/).Count
(Get-ChildItem datasets/labeled/labels/train/).Count

# Quick visual check — open a label file
Get-Content datasets/labeled/labels/train/some_image.txt
# Expected: one line per box, e.g.  3 0.412 0.631 0.180 0.240
# Empty file = OK image (correct, not an error)
```

---

### After this step

Run training:
```bash
cd training
.venv\Scripts\Activate.ps1
python train.py --model yolov8s.pt --epochs 50 --batch 16
```

Results appear in `models/runs/<name>/`. Log them in [[training/experiments]].

---

## Français

### Position dans le pipeline

```
✅ 1. Classifier        outil importer    → datasets/raw/ok/  +  ng/<classe>/
→  2. Annoter           outil annotator   → dessiner les bounding boxes sur les NG
→  3. Préparer le split prepare_dataset   → datasets/labeled/  (train / val)
   4. Entraîner         train.py          → models/runs/
   5. Exporter ONNX     export_onnx.py    → models/exports/onnx/
   6. Inspecter         inspector (Rust)  → http://localhost:8080
```

Cette page couvre les étapes 2 et 3.

---

### Étape 2 — Annoter avec l'outil Annotator

Guide complet : [[tools/annotator]]

L'annoteur est un outil dans le navigateur basé sur Streamlit.
Il remplace LabelImg (incompatible avec Python 3.12 — module `distutils` supprimé).

#### Lancer l'annoteur

```bash
cd tools/importer
.venv\Scripts\Activate.ps1

streamlit run annotate.py
# Le navigateur s'ouvre sur http://localhost:8501
```

#### Workflow

1. Sélectionner la **classe** active dans le panneau de droite (avant de dessiner)
2. **Cliquer-glisser** sur l'image pour dessiner une bounding box autour du défaut
3. Ajuster la classe par boîte si nécessaire (menu déroulant sous le canvas)
4. Cliquer **Sauvegarder + Suivante** pour sauvegarder et passer à l'image suivante

> [!TIP] Une boîte par défaut
> Deux taches de contamination séparées = deux boîtes.
> Deux types de défauts différents = une boîte par classe.

> [!NOTE] Images OK — pas d'annotation
> Ne pas ouvrir `datasets/raw/ok/` dans l'annoteur.
> Le script `prepare_dataset.py` crée automatiquement les fichiers labels vides.

#### Format d'un fichier label

```
# datasets/raw/ng/whitening/image.txt
3 0.412 0.631 0.180 0.240
```

Une ligne = une bounding box :
```
<class_id>  <cx>  <cy>  <largeur>  <hauteur>
```

Toutes les valeurs sont **normalisées** (0–1 par rapport à la taille de l'image).

| ID | Classe |
|----|--------|
| 0  | color_defect |
| 1  | hole |
| 2  | contamination |
| 3  | whitening |
| 4  | mold_defect |

---

### Étape 3 — Préparer le split train/val

Une fois toutes les images NG annotées :

```bash
cd training
.venv\Scripts\Activate.ps1

# Vérification sans copier
python prepare_dataset.py --dry-run

# Exécuter (80% train / 20% val par défaut)
python prepare_dataset.py

# Ratio personnalisé
python prepare_dataset.py --val-ratio 0.15
```

Le script :
1. Vérifie que chaque image NG a un fichier label non-vide
2. Crée des fichiers labels vides pour les images OK
3. Mélange aléatoirement (seed=42)
4. Copie les paires image + label vers `datasets/labeled/`

> [!NOTE] Petits datasets
> Moins de 50 images : utiliser `--val-ratio 0.2`.
> Moins de 20 images : `--val-ratio 0` (tout en train).

---

### Vérifier avant d'entraîner

```powershell
# PowerShell — les deux compteurs doivent être égaux
(Get-ChildItem datasets/labeled/images/train/).Count
(Get-ChildItem datasets/labeled/labels/train/).Count
```

---

### Étape suivante

```bash
cd training
.venv\Scripts\Activate.ps1
python train.py --model yolov8s.pt --epochs 50 --batch 16
```

Noter les résultats dans [[training/experiments]].
