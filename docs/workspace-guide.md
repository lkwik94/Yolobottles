---
tags: [meta, guide, workspace, onboarding]
created: 2026-04-28
updated: 2026-04-28
status: active
---

# Workspace Usage Guide | Guide d'utilisation du workspace

See also: [[index]] · [[schema]] · [[log]] · [[architecture/overview]]

---

## English

### Overview

This workspace combines three tools that work together as a "second brain" for the project:

| Tool | Purpose | Location |
|------|---------|----------|
| **`docs/`** | Human-written project wiki (Obsidian) | `docs/` |
| **`wiki/`** | LLM-synthesized knowledge base (llm-wiki) | `wiki/` |
| **`inspector/`** | Rust inference application | `inspector/` |
| **`training/`** | Python YOLO training scripts | `training/` |

The governing rules for all documentation are in [[schema]].
Everything Claude does in this project must follow `CLAUDE.md` at the project root.

---

### Prerequisites (one-time, system-wide)

| Tool | Version | Install |
|------|---------|---------|
| Python | ≥ 3.10 | [python.org](https://www.python.org/downloads/) |
| Rust | latest stable | `winget install Rustlang.Rustup` or [rustup.rs](https://rustup.rs) |
| Git | any | [git-scm.com](https://git-scm.com) |
| NVIDIA driver | ≥ 525 for CUDA 12.x | optional — CPU works but training is slow |

---

### First-time Setup

#### 1. Python environment

Always use a **dedicated virtual environment** — do not install into the global Python. This avoids conflicts with other tools (aider-chat, etc.) that pin different numpy/torch versions.

```bash
cd training

# Create the venv (once)
python -m venv .venv

# Activate — PowerShell (Windows)
.venv\Scripts\Activate.ps1
# Activate — bash/zsh (Linux / macOS)
# source .venv/bin/activate

# Install — prompt must show (.venv) prefix before running this

# GPU machine with CUDA 12.4 driver (recommended):
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu124

# CPU-only machine (or CUDA version unknown):
# pip install -r requirements.txt
```

Installs: PyTorch, Ultralytics YOLOv8, OpenCV, ONNX export tools.

> [!NOTE] CUDA version
> The `cu124` index is compatible with CUDA drivers ≥ 525 (CUDA 12.x). If your driver is older, use `cu118` or drop the `--extra-index-url` flag entirely (CPU build).

> [!NOTE] onnxruntime-gpu on CPU machines
> If you have no GPU, edit `requirements.txt` and replace `onnxruntime-gpu` with `onnxruntime`. The training scripts don't need it; it's only for local ONNX inference tests.

> [!WARNING] Activate before every session
> If you see `ModuleNotFoundError: ultralytics` or similar, you forgot to activate the venv.
> The venv is in `training/.venv/` — never commit it (gitignored).

#### 2. Rust environment

Run from the **project root** (`E:\OneDrive\Yolobottles`), not from inside `training/`:

```powershell
cd E:\OneDrive\Yolobottles\inspector
cargo build               # debug build, fast compile
cargo build --release     # optimized build for benchmarking
```

On first build, `ort` (ONNX Runtime) downloads its prebuilt binaries automatically (~80 MB). This requires internet access.

#### 3. Obsidian (optional but recommended)

Open Obsidian → **Open folder as vault** → select `e:/OneDrive/Yolobottles/docs/`

The graph view will show the link structure between all documentation pages.

#### 4. GitHub CLI (for git operations)

```bash
gh auth login
# Choose: GitHub.com → HTTPS → Login with a web browser
```

---

### Daily Workflow

#### Starting a work session

1. Open this project in Claude Code (`e:/OneDrive/Yolobottles`)
2. Claude automatically loads `CLAUDE.md` — no manual setup needed
3. Check recent activity: read [[log]] (last few entries)

#### Ending a work session

Before closing:
1. Update the relevant `docs/` page(s) for anything changed
2. Append to [[log]]:
   ```
   ## YYYY-MM-DD
   [what was done, what was decided, what was learned]
   ```

---

### Working with Images (Dataset)

#### Folder structure for raw images

```
datasets/raw/
  ok/                ← confirmed good bottles
  ng/
    color_defect/    ← abnormal coloration
    hole/            ← perforation, crack
    contamination/   ← foreign particle, black spot
    whitening/       ← PET stress whitening
    mold_defect/     ← missing/deformed bottom imprint
```

#### Annotation workflow

1. Drop raw images into the appropriate `datasets/raw/ng/<class>/` folder
2. Use [LabelImg](https://github.com/HumanSignal/labelImg) or Roboflow to draw bounding boxes
3. Export in **YOLO format** (one `.txt` per image, same name)
4. Place annotated images + labels into:
   - `datasets/labeled/images/train/` (80%)
   - `datasets/labeled/images/val/` (15%)
   - `datasets/labeled/images/test/` (5%)
   - `datasets/labeled/labels/train/`, `val/`, `test/` (same split)

> [!TIP] Label format (YOLO)
> Each `.txt` file contains one line per bounding box:
> `<class_id> <cx> <cy> <w> <h>` — all values normalized 0–1.
> Class IDs: 0=color_defect, 1=hole, 2=contamination, 3=whitening, 4=mold_defect

---

### Training a Model

```bash
cd training

# Basic run (YOLOv8s, 50 epochs)
python train.py

# Custom run
python train.py --model yolov8m.pt --epochs 100 --batch 8 --name bottle_v2

# Monitor training (opens browser)
# tensorboard --logdir ../models/runs/   (if tensorboard installed)
```

Outputs land in `models/runs/<name>/`:
- `weights/best.pt` — best checkpoint (use this)
- `weights/last.pt` — last checkpoint
- `results.csv` — metrics per epoch

Key metrics to watch: `mAP50` and `mAP50-95`. Log them in [[training/experiments]] after each run.

> [!IMPORTANT] Rotation augmentation
> `degrees=360.0` is set in `train.py`. This is intentional — bottle bottoms have no preferred orientation. Do not reduce this value.

---

### Exporting to ONNX

After training, export the best model for the Rust inspector:

```bash
cd training
python export_onnx.py --run bottle_v2
# → saves to models/exports/onnx/bottle_v2.onnx
```

The exported model has:
- Input: `[1, 3, 640, 640]` — batch=1, RGB, float32, values 0–1
- Output: `[1, 9, 8400]` — 4 bbox coords + 5 class scores, 8400 candidate boxes

---

### Running the Inspector (Rust)

```bash
cd inspector

# Run on image bank (dry-run, no ejector)
./target/release/inspector \
  --model ../models/exports/onnx/bottle_v2.onnx \
  --images ../datasets/raw \
  --threshold 0.5 \
  --eject-delay-ms 0

# Run with simulated ejector
./target/release/inspector \
  --model ../models/exports/onnx/bottle_v2.onnx \
  --images ../datasets/raw \
  --threshold 0.5 \
  --eject-delay-ms 50
```

Open `http://localhost:8080` to see the live OK/NG dashboard.

#### Adjusting the confidence threshold

| Threshold | Effect |
|-----------|--------|
| 0.3 | More sensitive — fewer missed defects, more false positives |
| 0.5 | Default — balanced |
| 0.7 | More precise — fewer false positives, may miss subtle defects |

Start at 0.5, adjust based on false positive rate observed on OK bottles.

#### Log output

The inspector logs to stdout:
```
INFO OK  [  12ms] bottle_001.jpg
INFO NG  [  15ms] bottle_042.jpg  — 2 defect(s): whitening 87%, contamination 61%
INFO NG  [  11ms] bottle_107.jpg  — 1 defect(s): hole 94%
```

---

### Knowledge Base (LLM Wiki)

The `wiki/` directory is a synthesized knowledge base. Feed it technical documents and it automatically builds structured wiki pages with cross-references.

#### Adding a document

```
wiki-input path/to/document.pdf
wiki-input path/to/datasheet.pdf --topic datasheets
wiki-input https://arxiv.org/pdf/some-paper.pdf --topic papers
```

Documents are archived in `raw/<topic>/` and synthesized into:
- `wiki/sources/<slug>.md` — summary of the document
- `wiki/concepts/*.md` — key concepts found (e.g., `YOLOv8.md`, `ONNX.md`)
- `wiki/entities/*.md` — key entities (e.g., `Ultralytics.md`, `NVIDIA.md`)

Suggested topics for this project:

| Topic folder | What goes there |
|-------------|-----------------|
| `raw/papers/` | Research papers (YOLO, vision inspection, PET defects) |
| `raw/datasheets/` | Camera datasheets, Jetson specs |
| `raw/specs/` | GigE Vision standard, GenICam docs |
| `raw/inbox/` | Anything not yet categorized |

#### Searching the knowledge base

```
wiki-query: How does YOLOv8 non-maximum suppression work?
wiki-query: What are the GigE Vision trigger modes?
wiki-query: What Jetson model is recommended for 36ms inference budget?
```

#### Generating the knowledge graph

```
wiki-graph
```

Opens `graph/graph.html` — an interactive visualization of all pages and their connections. Blue = source, Green = concept, Orange = entity, Purple = synthesis.

#### Health check

```
wiki-lint
```

Reports orphaned pages, broken links, contradictions between sources, and knowledge gaps.

---

### Using the Skills

Skills are pre-loaded tools available in every Claude Code session.

#### `xlsx` — Export training results to Excel

Say: *"create an Excel table with the training runs results"*

Claude will generate a properly formatted `.xlsx` with formulas, color coding, and no hardcoded values.

#### `webapp-testing` — Test the HMI dashboard

Say: *"test the inspector HMI at localhost:8080"*

Claude writes Playwright scripts to verify the dashboard, capture screenshots, and check API responses.

#### `pptx` — Customer presentation

Say: *"create a presentation showing the inspection system for a Sidel customer demo"*

#### `pdf` — Extract from datasheets

Say: *"extract the trigger specifications table from this GigE Vision datasheet"*

#### `mcp-builder` — Build integrations

Say: *"build an MCP server to expose the inspector stats to Claude"*

#### `skill-creator` — Create new skills

Say: *"create a skill for analyzing YOLO training curves"*

---

### Git Workflow

#### Prerequisites — first time on a machine

```bash
# 1. Install GitHub CLI (if not already installed)
winget install GitHub.cli           # Windows
# or: https://cli.github.com/

# 2. Authenticate (opens browser)
gh auth login
# Choose: GitHub.com → HTTPS → Login with a web browser

# 3. Configure your identity (once per machine)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

#### Clone the repository on a new PC

```bash
# Clone via HTTPS (recommended, uses gh credentials)
gh repo clone <owner>/yolobottles       # if repo is on GitHub
# or:
git clone https://github.com/<owner>/yolobottles.git
cd yolobottles
```

#### Check what changed

```bash
# See which files are modified / untracked
git status

# See the actual diff of unstaged changes
git diff

# See the diff of already-staged changes
git diff --staged

# See the full commit history (one line per commit)
git log --oneline
```

#### Stage and commit

```bash
# Stage specific files — NEVER use "git add ." or "git add -A"
# (would accidentally include datasets, models, venv…)
git add docs/log.md
git add inspector/src/inference.rs
git add training/requirements.txt

# Commit with a clear message
git commit -m "feat: add whitening detection improvements"

# Commit message conventions used in this project:
#   feat:     new feature or capability
#   fix:      bug fix
#   docs:     documentation only
#   refactor: code restructure, no behavior change
#   train:    dataset or training change
#   chore:    tooling, CI, dependencies
```

#### Push to GitHub

```bash
# First push ever on a branch (sets the upstream)
git push -u origin main

# All subsequent pushes
git push
```

#### Undo changes

```bash
# Discard unstaged changes to a file
git restore inspector/src/inference.rs

# Unstage a file (keep changes in working tree)
git restore --staged inspector/src/inference.rs

# Amend the last commit message (before pushing only)
git commit --amend -m "corrected message"
```

#### What NOT to commit (gitignored automatically)

| Path | Reason |
|------|--------|
| `datasets/raw/`, `datasets/labeled/` | Images — too large |
| `models/runs/`, `models/exports/` | Training outputs, binary |
| `*.onnx`, `*.trt` | Binary models |
| `training/.venv/` | Python virtual environment |
| `inspector/target/` | Rust build artifacts |
| `raw/`, `graph/` | Wiki raw docs and generated graph |
| `.obsidian/workspace.json` | Obsidian local window state |
| `.claude/settings.local.json` | Local Claude Code permissions |

> [!NOTE] `wiki/` IS committed
> The synthesized knowledge base (`wiki/`) is versioned. Only the raw source documents (`raw/`) and the generated graph (`graph/`) are excluded.

---

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `cargo build` fails — ONNX Runtime not found | Check internet connection; `ort` downloads binaries on first build |
| `cargo build` — `SessionBuilder: not Send+Sync` | Use `.map_err(\|e\| anyhow::anyhow!("{e}"))` instead of `?` on builder methods |
| `cargo build` — `From<ArrayView> not implemented for SessionInputValue` | ndarray feature not enabled; use `ort::value::Tensor::from_array((shape_i64, data_vec))` |
| PyTorch CUDA not available | Reinstall with `--extra-index-url https://download.pytorch.org/whl/cu124` |
| Training OOM (out of memory) | Reduce `--batch` from 16 to 8 |
| Inspector panic on ONNX load | Check model path; ensure export was done with `dynamic=False` |
| HMI not loading | Check port 8080 is free: `netstat -an | grep 8080` |
| LabelImg labels wrong format | In LabelImg, set format to **YOLO** before annotating |

---

## Français

### Vue d'ensemble

Ce workspace combine trois outils qui fonctionnent ensemble comme un "second cerveau" pour le projet :

| Outil | Rôle | Emplacement |
|-------|------|-------------|
| **`docs/`** | Wiki projet co-écrit (Obsidian) | `docs/` |
| **`wiki/`** | Base de connaissance synthétisée par LLM | `wiki/` |
| **`inspector/`** | Application d'inférence Rust | `inspector/` |
| **`training/`** | Scripts d'entraînement YOLO Python | `training/` |

Les règles de documentation sont dans [[schema]].
Tout ce que Claude fait dans ce projet suit `CLAUDE.md` à la racine.

---

### Prérequis système (une seule fois)

| Outil | Version | Installation |
|-------|---------|-------------|
| Python | ≥ 3.10 | [python.org](https://www.python.org/downloads/) |
| Rust | stable | `winget install Rustlang.Rustup` ou [rustup.rs](https://rustup.rs) |
| Git | quelconque | [git-scm.com](https://git-scm.com) |
| Driver NVIDIA | ≥ 525 pour CUDA 12.x | optionnel — CPU fonctionne mais lent |

---

### Installation initiale

#### 1. Environnement Python

Toujours utiliser un **environnement virtuel dédié** — ne jamais installer dans le Python global. Cela évite les conflits avec d'autres outils (aider-chat, etc.) qui épinglent des versions différentes de numpy/torch.

```bash
cd training

# Créer le venv (une seule fois)
python -m venv .venv

# Activer — PowerShell (Windows)
.venv\Scripts\Activate.ps1
# Activer — bash/zsh (Linux / macOS)
# source .venv/bin/activate

# Installer — le prompt doit afficher (.venv) avant de lancer ceci

# Machine GPU avec driver CUDA 12.4 (recommandé) :
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu124

# Machine CPU uniquement :
# pip install -r requirements.txt
```

> [!NOTE] Version CUDA
> L'index `cu124` est compatible avec les drivers CUDA ≥ 525 (CUDA 12.x). Driver plus ancien → utiliser `cu118`. Pas de GPU → supprimer le `--extra-index-url`.

> [!NOTE] onnxruntime-gpu sans GPU
> Sans GPU, modifier `requirements.txt` et remplacer `onnxruntime-gpu` par `onnxruntime`. Non utilisé par les scripts d'entraînement, seulement pour les tests ONNX locaux.

> [!WARNING] Activer avant chaque session
> Si `ModuleNotFoundError: ultralytics` apparaît, le venv n'est pas activé.
> Le venv est dans `training/.venv/` — ne jamais le commiter (gitignored).

#### 2. Environnement Rust

```bash
cd inspector
cargo build        # build debug, compilation rapide
cargo build --release  # build optimisé pour les benchmarks
```

Au premier build, `ort` télécharge automatiquement les binaires ONNX Runtime précompilés (~80 Mo). Nécessite internet.

#### 3. Obsidian (optionnel mais recommandé)

Ouvrir Obsidian → **Open folder as vault** → sélectionner `e:/OneDrive/Yolobottles/docs/`

La vue graphe montrera la structure des liens entre toutes les pages de documentation.

---

### Workflow quotidien

#### Démarrage d'une session

1. Ouvrir ce projet dans Claude Code (`e:/OneDrive/Yolobottles`)
2. Claude charge automatiquement `CLAUDE.md` — pas de configuration manuelle
3. Vérifier l'activité récente : lire [[log]] (dernières entrées)

#### Fin de session

Avant de fermer :
1. Mettre à jour la ou les pages `docs/` concernées
2. Ajouter une entrée dans [[log]]

---

### Entraînement d'un modèle

```bash
cd training
python train.py                                    # run de base
python train.py --model yolov8m.pt --epochs 100   # run personnalisé
python export_onnx.py --run bottle_v2             # export ONNX
```

Métriques clés à surveiller : `mAP50` et `mAP50-95`. Les noter dans [[training/experiments]] après chaque run.

---

### Lancer l'inspector Rust

```bash
cd inspector
./target/release/inspector \
  --model ../models/exports/onnx/bottle_v2.onnx \
  --images ../datasets/raw \
  --threshold 0.5
```

Dashboard : `http://localhost:8080`

---

### Base de connaissance (wiki LLM)

```
wiki-input chemin/vers/document.pdf                    # ingérer un document local
wiki-input https://arxiv.org/pdf/paper.pdf --topic papers  # ingérer depuis URL
wiki-query: Comment fonctionne la NMS dans YOLOv8 ?   # rechercher
wiki-graph                                              # générer le graphe
wiki-lint                                               # vérifier la santé du wiki
```

Dossiers suggérés pour les documents bruts :

| Dossier | Contenu |
|---------|---------|
| `raw/papers/` | Articles de recherche (YOLO, vision industrielle, défauts PET) |
| `raw/datasheets/` | Fiches techniques caméras, specs Jetson |
| `raw/specs/` | Standard GigE Vision, docs GenICam |
| `raw/inbox/` | Tout ce qui n'est pas encore catégorisé |

---

### Workflow Git

#### Prérequis — première fois sur une machine

```bash
# 1. Installer le CLI GitHub (si pas encore présent)
winget install GitHub.cli           # Windows
# ou : https://cli.github.com/

# 2. S'authentifier (ouvre le navigateur)
gh auth login
# Choisir : GitHub.com → HTTPS → Login with a web browser

# 3. Configurer son identité (une seule fois par machine)
git config --global user.name "Prénom Nom"
git config --global user.email "toi@example.com"
```

#### Cloner le dépôt sur un nouveau PC

```bash
gh repo clone <owner>/yolobottles
# ou :
git clone https://github.com/<owner>/yolobottles.git
cd yolobottles
```

#### Vérifier l'état du dépôt

```bash
git status                  # fichiers modifiés / non suivis
git diff                    # diff des changements non stagés
git diff --staged           # diff des changements stagés
git log --oneline           # historique compact
```

#### Stager et committer

```bash
# Toujours stager par fichier — jamais "git add ." ou "git add -A"
git add docs/log.md
git add inspector/src/inference.rs

# Committer avec un message structuré
git commit -m "feat: amélioration détection whitening"

# Conventions de messages utilisées dans ce projet :
#   feat:     nouvelle fonctionnalité
#   fix:      correction de bug
#   docs:     documentation uniquement
#   refactor: restructuration sans changement de comportement
#   train:    dataset ou configuration d'entraînement
#   chore:    outillage, dépendances
```

#### Pousser vers GitHub

```bash
# Premier push (définit l'upstream)
git push -u origin main

# Tous les pushes suivants
git push
```

#### Annuler des changements

```bash
# Annuler les modifications non stagées d'un fichier
git restore inspector/src/inference.rs

# Désindexer un fichier (garder les modifications)
git restore --staged inspector/src/inference.rs

# Modifier le dernier message de commit (avant push uniquement)
git commit --amend -m "message corrigé"
```

#### Ce qu'il ne faut PAS committer (gitignored automatiquement)

| Chemin | Raison |
|--------|--------|
| `datasets/raw/`, `datasets/labeled/` | Images — trop volumineuses |
| `models/runs/`, `models/exports/` | Sorties d'entraînement, binaires |
| `*.onnx`, `*.trt` | Modèles binaires |
| `training/.venv/` | Environnement virtuel Python |
| `inspector/target/` | Artefacts de build Rust |
| `raw/`, `graph/` | Docs bruts wiki et graphe généré |
| `.obsidian/workspace.json` | État local Obsidian |
| `.claude/settings.local.json` | Permissions locales Claude Code |

> [!NOTE] `wiki/` EST versionné
> La base de connaissance synthétisée (`wiki/`) est versionnée. Seuls les documents sources bruts (`raw/`) et le graphe généré (`graph/`) sont exclus.

---

### Problèmes courants

| Problème | Solution |
|---------|----------|
| `cargo build` échoue — ONNX Runtime introuvable | Vérifier la connexion internet ; `ort` télécharge les binaires au premier build |
| PyTorch CUDA non disponible | Réinstaller avec `--extra-index-url https://download.pytorch.org/whl/cu124` |
| OOM à l'entraînement | Réduire `--batch` de 16 à 8 |
| Panic inspector au chargement ONNX | Vérifier le chemin du modèle ; vérifier que l'export a été fait avec `dynamic=False` |
| HMI ne charge pas | Vérifier que le port 8080 est libre |
| Labels LabelImg mauvais format | Dans LabelImg, régler le format sur **YOLO** avant d'annoter |
