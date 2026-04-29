---
tags: [tool, dataset, import, annotation]
created: 2026-04-29
updated: 2026-04-29
status: active
---

# Image Importer | Importeur d'images

See also: [[index]] · [[training/dataset-guide]] · [[workspace-guide]]

---

## English

### Purpose

The importer is a browser-based visual triage tool.
It solves the first step of the dataset preparation workflow:

```
Raw images (BMP/JPG/PNG)
        ↓
  datasets/import/        ← drop images here
        ↓
  [Importer — visual triage, 1 click per image]
        ↓
  datasets/raw/ok/        ← good bottles
  datasets/raw/ng/<class>/  ← defective bottles by class
        ↓
  [Annotator — draw bounding boxes]
        ↓
  datasets/labeled/       ← ready for training
```

The importer handles **classification only** (which class is this?).
Bounding box annotation is a separate step done with the [[tools/annotator]] tool.

---

### Installation

The importer uses its own minimal virtual environment — separate from the
training venv — to avoid dependency conflicts.

```bash
cd tools/importer

# Create venv (once)
python -m venv .venv

# Activate — Windows PowerShell
.venv\Scripts\Activate.ps1
# Activate — bash/zsh (Linux / macOS)
# source .venv/bin/activate

# Mettre pip à jour (évite le notice "new release available")
python -m pip install --upgrade pip -q

# Install dependencies (prompt must show (.venv) prefix)
pip install -r requirements.txt
```

---

### Running

```bash
# From tools/importer/, with venv activated:
streamlit run app.py

# The browser opens automatically at http://localhost:8501
# If not, open it manually.
```

To stop the server: `Ctrl+C` in the terminal.

---

### Workflow

#### 1. Drop images into the import folder

Copy or move your raw images (BMP, JPG, PNG, TIFF) into:

```
datasets/import/
```

Any subfolder structure is ignored — only files directly in `import/` are loaded.

#### 2. Open the importer

```
http://localhost:8501
```

The interface shows:
- **Left panel (sidebar)** — session stats and live dataset counts per class
- **Center** — current image, large, with filename and resolution
- **Right panel** — classification buttons

#### 3. Classify each image

Click one of the 6 buttons to classify the current image:

| Button | Shortcut | Destination |
|--------|----------|-------------|
| ✅ OK — good bottle | — | `datasets/raw/ok/` |
| 🟡 Color defect | — | `datasets/raw/ng/color_defect/` |
| 🔴 Hole / crack | — | `datasets/raw/ng/hole/` |
| ⚫ Contamination | — | `datasets/raw/ng/contamination/` |
| ⬜ Whitening | — | `datasets/raw/ng/whitening/` |
| 🔧 Mold defect | — | `datasets/raw/ng/mold_defect/` |

After each click, the image moves to the correct folder and the next one
appears automatically.

#### 4. Skip and undo

- **Ignore** — keeps the image in `import/`, skips it for this session.
  Use for images you are unsure about. Click **Reset ignored** in the
  sidebar to revisit them.

- **Delete ignored (n)** — permanently deletes all currently ignored images
  from `import/`. Use for erroneous imports or irrelevant data.
  Requires a two-click confirmation (button → **Confirm**) to prevent
  accidental deletion. Only visible when at least one image is ignored.

- **Cancel (last)** — moves the last classified image back to `import/`
  and decrements the counter. Only the most recent action can be undone.

#### 5. What happens to the files

The importer **moves** (not copies) files. The original is gone from
`import/` once classified.

If a file with the same name already exists in the destination, the importer
appends `_1`, `_2`, etc. to avoid overwrites.

---

### After classification — next steps

1. Open [[tools/annotator]] to draw bounding boxes on NG images
2. Run `python training/prepare_dataset.py` to create the train/val split
3. Run training: `python training/train.py`

---

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Browser does not open | Navigate manually to `http://localhost:8501` |
| `ModuleNotFoundError: streamlit` | venv not activated; run `.venv\Scripts\Activate.ps1` |
| Images not visible after drop | Click **Refresh** in the browser (F5) |
| Classified image went to wrong class | Use **Cancel (last)** then reclassify |
| Image shows pink/wrong colors | Expected for grayscale BMP — the app converts to RGB for display |

---

## Français

### Objectif

L'importeur est un outil de triage visuel dans le navigateur.
Il gère la première étape de préparation du dataset :

```
Images brutes (BMP/JPG/PNG)
        ↓
  datasets/import/          ← déposer les images ici
        ↓
  [Importeur — triage visuel, 1 clic par image]
        ↓
  datasets/raw/ok/           ← bonnes bouteilles
  datasets/raw/ng/<classe>/  ← bouteilles défectueuses par classe
        ↓
  [Annotateur — dessiner les bounding boxes]
        ↓
  datasets/labeled/          ← prêt pour l'entraînement
```

L'importeur gère uniquement la **classification** (quelle classe ?).
L'annotation des bounding boxes est une étape séparée dans l'outil [[tools/annotator]].

---

### Installation

L'importeur utilise son propre environnement virtuel minimal, séparé du
venv d'entraînement, pour éviter les conflits de dépendances.

```bash
cd tools/importer

# Créer le venv (une seule fois)
python -m venv .venv

# Activer — Windows PowerShell
.venv\Scripts\Activate.ps1
# Activer — bash/zsh (Linux / macOS)
# source .venv/bin/activate

# Installer les dépendances (le prompt doit afficher (.venv))
pip install -r requirements.txt
```

---

### Lancement

```bash
# Depuis tools/importer/, venv activé :
streamlit run app.py

# Le navigateur s'ouvre automatiquement sur http://localhost:8501
```

Pour arrêter le serveur : `Ctrl+C` dans le terminal.

---

### Utilisation

#### 1. Déposer les images dans le dossier d'import

Copier ou déplacer les images brutes (BMP, JPG, PNG, TIFF) dans :

```
datasets/import/
```

#### 2. Ouvrir l'importeur

```
http://localhost:8501
```

L'interface affiche :
- **Panneau gauche (sidebar)** — stats de session et compteurs par classe
- **Centre** — image courante, grande, avec nom et résolution
- **Panneau droit** — boutons de classification

#### 3. Classer chaque image

Cliquer sur l'un des 6 boutons pour classifier l'image courante :

| Bouton | Destination |
|--------|-------------|
| ✅ OK — bonne bouteille | `datasets/raw/ok/` |
| 🟡 Défaut couleur | `datasets/raw/ng/color_defect/` |
| 🔴 Trou / fissure | `datasets/raw/ng/hole/` |
| ⚫ Contamination | `datasets/raw/ng/contamination/` |
| ⬜ Blanchiment | `datasets/raw/ng/whitening/` |
| 🔧 Défaut moule | `datasets/raw/ng/mold_defect/` |

Après chaque clic, l'image se déplace dans le bon dossier et la suivante
apparaît automatiquement.

#### 4. Ignorer et annuler

- **Ignorer** — laisse l'image dans `import/`, la saute pour cette session.
  Utiliser pour les images incertaines. Cliquer **Réinitialiser ignorées**
  dans la sidebar pour les revoir.

- **Supprimer ignorées (n)** — supprime définitivement toutes les images
  ignorées du dossier `import/`. À utiliser pour les imports erronés ou
  les données non pertinentes copiées par erreur.
  Requiert une confirmation en deux clics (bouton → **Confirmer**) pour
  éviter toute suppression accidentelle. Visible uniquement si au moins
  une image est ignorée.

- **Annuler** — remet la dernière image classifiée dans `import/` et
  décrémente le compteur. Uniquement la dernière action est annulable.

#### 5. Ce qui arrive aux fichiers

L'importeur **déplace** (ne copie pas) les fichiers. L'original disparaît
de `import/` une fois classifié.

En cas de conflit de nom, `_1`, `_2`, etc. sont ajoutés automatiquement.

---

### Après la classification — prochaines étapes

1. Ouvrir [[tools/annotator]] pour dessiner les bounding boxes sur les images NG
2. Lancer `python training/prepare_dataset.py` pour créer le split train/val
3. Lancer l'entraînement : `python training/train.py`

---

### Problèmes courants

| Problème | Solution |
|---------|----------|
| Le navigateur ne s'ouvre pas | Aller manuellement sur `http://localhost:8501` |
| `ModuleNotFoundError: streamlit` | venv non activé ; exécuter `.venv\Scripts\Activate.ps1` |
| Images non visibles après dépôt | Rafraîchir le navigateur (F5) |
| Image classifiée dans la mauvaise classe | Utiliser **Annuler** puis reclassifier |
| Couleurs étranges sur les images | Normal pour les BMP niveaux de gris — converti en RGB pour l'affichage |
