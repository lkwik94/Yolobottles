---
tags: [tool, dataset, annotation, bounding-box]
created: 2026-04-29
updated: 2026-04-29
status: active
---

# Annotator | Annoteur

See also: [[index]] · [[tools/importer]] · [[training/dataset-guide]] · [[workspace-guide]]

---

## English

### Purpose

The annotator is a browser-based bounding box drawing tool.
It covers **step 2** of the dataset preparation pipeline:

```
✅ 1. Classify          importer     → datasets/raw/ok/  +  ng/<class>/
→  2. Annotate          annotator    → draw bounding boxes on NG images (.txt labels)
→  3. Prepare split     prepare_dataset → datasets/labeled/  (train / val)
   4. Train             train.py     → models/runs/
```

It replaces LabelImg, which is incompatible with Python 3.12 (`distutils` removed).

---

### Installation

The annotator shares the importer venv — no extra setup needed once the importer is installed.
If you haven't set up the venv yet:

```bash
cd tools/importer

# Create venv (once)
python -m venv .venv

# Activate — Windows PowerShell
.venv\Scripts\Activate.ps1
# Activate — bash/zsh (Linux / macOS)
# source .venv/bin/activate

python -m pip install --upgrade pip -q
pip install -r requirements.txt
```

The `requirements.txt` includes `streamlit-drawable-canvas`, which powers the canvas.

---

### Running

```bash
# From tools/importer/, with venv activated:
streamlit run annotate.py

# The browser opens automatically at http://localhost:8501
```

To stop the server: `Ctrl+C` in the terminal.

---

### Interface

The annotator scans all images in `datasets/raw/ng/` and its subfolders.

**Sidebar**
- **Total NG** — total number of NG images found
- **Annotated** — images with at least one bounding box saved
- **Remaining** — not yet annotated
- **Session** — labels saved in this session
- **Navigation list** — click any image to jump to it directly; `[OK]` prefix = already annotated

**Main area**
- Progress bar showing annotation completion
- Image displayed at up to 800 px wide (proportionally scaled)
- Controls panel on the right:
  - Class selector — choose the active class before drawing
  - Color swatch showing the active class color
  - Usage tips

---

### Workflow

#### 1. Select the active class

In the right panel, choose the defect class that matches what you are about to annotate.
The canvas stroke and fill color will update accordingly.

| Class | Color |
|-------|-------|
| color_defect | orange |
| hole | red |
| contamination | purple |
| whitening | blue |
| mold_defect | teal |

#### 2. Draw a bounding box

- **Draw** — click and drag on the image to draw a rectangle
- **Move** — click an existing box and drag it
- **Resize** — drag the corner handles of a selected box
- **Delete** — select a box and press `Delete`

#### 3. Assign a class to each box

Below the canvas, each box appears in a list with its normalized coordinates.
You can change the class of any individual box using its dropdown — useful when
a single image contains two different defect types.

#### 4. Save

- **Sauvegarder** — saves the current labels to `<image_name>.txt` in the same folder
- **Sauvegarder + Suivante** — saves and moves to the next image

> [!TIP] Save before navigating
> Using the sidebar navigation or Previous/Next buttons without saving will lose unsaved boxes.
> Always click Save first, or use **Sauvegarder + Suivante** to save automatically.

#### 5. Label file format

The annotator saves YOLO-format `.txt` files alongside each image:

```
# datasets/raw/ng/whitening/image.txt
3 0.412 0.631 0.180 0.240
```

Each line = one bounding box: `<class_id> <cx> <cy> <width> <height>`
All values are normalized (0–1 relative to image size).

| ID | Class |
|----|-------|
| 0  | color_defect |
| 1  | hole |
| 2  | contamination |
| 3  | whitening |
| 4  | mold_defect |

---

### After annotation

Once all NG images are annotated:

```bash
cd training
.venv\Scripts\Activate.ps1

# Dry run — preview without copying
python prepare_dataset.py --dry-run

# Create the train/val split
python prepare_dataset.py
```

Then run training: see [[training/dataset-guide]].

---

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Browser does not open | Navigate manually to `http://localhost:8501` |
| `ModuleNotFoundError: streamlit_drawable_canvas` | venv not activated, or run `pip install -r requirements.txt` again |
| Canvas is blank | Refresh the browser (F5) — canvas rerenders on page load |
| Box disappears when I switch class | The canvas rerenders — this is a Streamlit limitation. Draw boxes after selecting the class. |
| Annotations not loading on reopen | Check that `<image>.txt` exists next to the image and is non-empty |
| Images not found | Check that `datasets/raw/ng/` contains subfolders named after the 5 defect classes |

---

## Français

### Objectif

L'annoteur est un outil de dessin de bounding boxes dans le navigateur.
Il couvre l'**étape 2** du pipeline de préparation du dataset.

Il remplace LabelImg, incompatible avec Python 3.12 (module `distutils` supprimé).

---

### Installation

L'annoteur utilise le même venv que l'importeur — aucune installation supplémentaire
si l'importeur est déjà configuré.

```bash
cd tools/importer
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Lancement

```bash
# Depuis tools/importer/, venv activé :
streamlit run annotate.py
# Le navigateur s'ouvre sur http://localhost:8501
```

---

### Interface

L'annoteur parcourt toutes les images dans `datasets/raw/ng/` et ses sous-dossiers.

**Sidebar**
- **Total NG** — nombre total d'images NG
- **Annotées** — images avec au moins une bounding box sauvegardée
- **Restantes** — pas encore annotées
- **Session** — labels sauvegardés dans cette session
- **Liste de navigation** — cliquer sur une image pour y aller directement

---

### Workflow

#### 1. Choisir la classe active

Dans le panneau de droite, sélectionner la classe du défaut avant de dessiner.
La couleur du tracé se met à jour automatiquement.

#### 2. Dessiner une bounding box

- **Dessiner** — cliquer-glisser sur l'image pour créer un rectangle
- **Déplacer** — cliquer sur une boîte existante et la faire glisser
- **Redimensionner** — tirer sur les poignées de coin
- **Supprimer** — sélectionner une boîte et appuyer sur `Delete`

#### 3. Changer la classe d'une boîte

Sous le canvas, chaque boîte a son propre sélecteur de classe.
Utile si une image contient deux types de défauts différents.

#### 4. Sauvegarder

- **Sauvegarder** — sauvegarde les labels dans `<nom_image>.txt`
- **Sauvegarder + Suivante** — sauvegarde et passe à l'image suivante

> [!TIP] Sauvegarder avant de naviguer
> La navigation sans sauvegarde fait perdre les boîtes non sauvegardées.

#### 5. Format du fichier label

```
3 0.412 0.631 0.180 0.240
```

Une ligne = une bounding box : `<class_id> <cx> <cy> <largeur> <hauteur>`
Toutes les valeurs normalisées (0–1).

---

### Après l'annotation

```bash
cd training
.venv\Scripts\Activate.ps1
python prepare_dataset.py --dry-run
python prepare_dataset.py
```

Voir [[training/dataset-guide]] pour la suite.

---

### Problèmes courants

| Problème | Solution |
|---------|----------|
| Le navigateur ne s'ouvre pas | Aller sur `http://localhost:8501` manuellement |
| `ModuleNotFoundError: streamlit_drawable_canvas` | Exécuter `pip install -r requirements.txt` dans le venv |
| Le canvas est vide | Rafraîchir (F5) |
| Les annotations ne chargent pas | Vérifier que `<image>.txt` existe à côté de l'image et est non-vide |
