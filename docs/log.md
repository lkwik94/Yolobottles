---
tags: [meta, log]
created: 2026-04-28
status: active
---

# Activity Log | Journal d'activité

> Append-only. One entry per session. Never edit past entries.
> Append-only. Une entrée par session. Ne jamais modifier les entrées passées.

Format: `YYYY-MM-DD — [EN] description | [FR] description`

---

## 2026-04-28

**Project initialization | Initialisation du projet**

- Created full workspace structure (datasets, training, inspector, docs)
- Defined 5 defect classes: `color_defect`, `hole`, `contamination`, `whitening`, `mold_defect`
- Architecture decision: YOLOv8s → ONNX → Rust/ort inference
- HMI: Axum web server, dark dashboard on port 8080
- Hardware baseline: RTX PRO 500 Black (6GB VRAM), Intel Ultra 7 265H, 32 GB RAM, CUDA 13.0
- PyTorch and Ultralytics not yet installed
- Documentation structure set up following Karpathy's LLM Wiki pattern

---

## 2026-04-28 (suite)

**Workspace documentation | Documentation du workspace**

- Created `docs/workspace-guide.md` — full bilingual usage guide (setup, training, inspector, wiki, skills)
- Created `CLAUDE.md` — enforces systematic documentation, loaded automatically by Claude Code
- Installed llm-wiki skill (build_graph.py, 6 reference files, vis.js template)
- Initialized wiki workspace: `wiki/`, `raw/`, `graph/` with base files
- Configured `.claude/config/llm-wiki.json` pointing to project root
- Added wiki workspace to `.gitignore`
- 8 skills now active: llm-wiki, xlsx, webapp-testing, pptx, pdf, mcp-builder, skill-creator, troubleshooting-sidel-blower

---

## 2026-04-28 (suite 2)

**Rust inspector — first successful build | Premier build Rust réussi**

- Fixed all ort 2.0.0-rc.12 API incompatibilities blocking `cargo build`
- `SessionBuilder` methods return `ort::Error<SessionBuilder>` which is not Send+Sync — must use `.map_err(|e| anyhow::anyhow!("{e}"))` instead of `?`
- ndarray feature is not enabled in ort by default — ndarray views cannot be passed to `inputs!` macro directly
- Replaced `Array4::from_shape_vec` + view with `ort::value::Tensor::from_array((shape_i64, data_vec))`
- `session.run()` requires `&mut self` in rc.12 — changed `Model::infer` to `&mut self`
- `Arc<Model>` cannot borrow mutably — changed to `Arc<parking_lot::Mutex<Model>>` in pipeline + main
- `SessionOutputs` keeps a mutable borrow on session — copy raw slice to `Vec<f32>` and `drop(outputs)` before calling `decode_output`
- Removed `ndarray` dependency from `Cargo.toml` (no longer needed)
- `cargo build` passes cleanly (debug profile, 7.87s)

---

## 2026-04-28 (suite 3)

**Portabilité workspace — audit et corrections | Workspace portability — audit and fixes**

- Ajout section "Prérequis système" dans workspace-guide (EN+FR) : Python, Rust, Git, driver NVIDIA
- Ajout commande d'activation Linux/macOS (`source .venv/bin/activate`) en commentaire
- Ajout variante CPU-only pour `pip install` (sans `--extra-index-url`)
- Note `onnxruntime-gpu` → `onnxruntime` pour les machines sans GPU
- `requirements.txt` clarifié : deux commandes commentées (GPU / CPU), `onnxruntime-gpu` marqué optionnel
- Partie 2 (Rust) : prête sans modification, `cargo build` compile sur tout PC avec Rust installé

---

## 2026-04-29

**Image importer — outil de triage visuel | Visual triage tool**

- Créé `tools/importer/app.py` — application Streamlit de triage d'images
- Interface navigateur : image pleine largeur + 6 boutons de classification + Ignorer + Annuler
- Déplacement automatique vers `datasets/raw/ok/` ou `ng/<classe>/` à chaque clic
- Compteurs de session + totaux dataset live dans la sidebar
- Gestion des conflits de noms, annulation de la dernière action
- Créé `tools/importer/requirements.txt` — streamlit + Pillow uniquement
- Dossier `datasets/import/` créé et ajouté au `.gitignore`
- `tools/importer/.venv/` ajouté au `.gitignore`
- Créé `docs/tools/importer.md` — guide bilingue complet (installation, workflow, dépannage)
- `docs/index.md` mis à jour — section Outils ajoutée (EN + FR)

---

## 2026-04-29 (suite)

**Dataset annotation guide + prepare_dataset script**

- Creé `docs/training/dataset-guide.md` — guide bilingue complet (étapes 2 et 3 du pipeline)
  - Installation LabelImg, création classes.txt, workflow annotation, format label YOLO
  - Explication bounding boxes, raccourcis clavier, cas particuliers (multi-défauts)
  - Étape 3 : script prepare_dataset.py, options dry-run/val-ratio
- Créé `training/prepare_dataset.py` — script de préparation du dataset
  - Vérifie les labels NG manquants (bloque si absent, sauf --dry-run)
  - Crée les fichiers labels vides pour les images OK
  - Split aléatoire reproductible (seed=42), ratio configurable
  - Copie vers datasets/labeled/images/ et labels/
- Test dry-run : 24 OK + 5 NG détectés, 5 annotations manquantes signalées, split 19/5 prévisualisé

---
## 2026-04-29 (suite 2)

**Annoteur Streamlit — remplacement de LabelImg | Streamlit annotator — LabelImg replacement**

- LabelImg 1.8.6 incompatible avec Python 3.12 : `ModuleNotFoundError: No module named 'distutils'`
- Créé `tools/importer/annotate.py` — annoteur de bounding boxes dans le navigateur
  - `streamlit-drawable-canvas` pour le dessin de rectangles sur canvas Fabric.js
  - Sélecteur de classe actif + couleur distincte par classe (5 couleurs)
  - Sélecteur de classe individuel par boîte (pour images multi-défauts)
  - Chargement des annotations existantes (`.txt` → canvas initial_drawing)
  - Sauvegarde en format YOLO normalisé avec gestion scaleX/scaleY
  - Navigation sidebar (liste cliquable, indicateur [OK]/[ ])
  - Boutons : Précédente / Suivante / Sauvegarder / Sauvegarder + Suivante
- Ajouté `streamlit-drawable-canvas>=0.9.3` dans `tools/importer/requirements.txt`
- Créé `docs/tools/annotator.md` — guide bilingue complet (installation, workflow, dépannage)
- Mis à jour `docs/index.md` — ajout de l'annoteur dans la section Outils (EN + FR)
- Mis à jour `docs/training/dataset-guide.md` — étape 2 remplacée : LabelImg → annoteur Streamlit

## 2026-04-29 (suite 3)

**Corrections doc + fix compatibilité Streamlit | Doc fixes + Streamlit compatibility fix**

- `streamlit-drawable-canvas` 0.9.3 incompatible avec Streamlit 1.37+ (`image_to_url` supprimé)
- Pin `streamlit<1.37` dans `requirements.txt` ; Streamlit 1.36.0 installé dans le venv
- `app.py` et `annotate.py` améliorés : `@st.cache_data` sur les scans disque, `setdefault` session state
- `docs/tools/importer.md` : références LabelImg remplacées par l'annoteur Streamlit (EN + FR)
- `docs/tools/annotator.md` : note de compatibilité Streamlit ajoutée (EN + FR)
- Skill `developing-with-streamlit` installé dans `.claude/skills/` (17 sous-skills + templates)

## 2026-04-29 (suite 4)

**HMI dashboard étendu | Extended HMI dashboard**

- `Stats` étendu : `class_counts[5]`, `history: VecDeque<InspectionRecord>`, `pipeline_done`
- `pipeline.rs` : enregistre historique + compteurs par classe, `pipeline_done = true` en fin de run
- `hmi/mod.rs` : nouvel endpoint `/api/history` (50 dernières inspections), `/api/stats` enrichi
- `index.html` : dashboard complet — breakdown par classe (barres colorées), table des 50 dernières détections, badge statut Running/Complete
- `docs/tools/hmi.md` : guide bilingue complet (prérequis, CLI, sections dashboard, API endpoints)
- `docs/index.md` : hmi ajouté dans la section Outils (EN + FR)

<!-- New entries go above this line, below the last entry -->
