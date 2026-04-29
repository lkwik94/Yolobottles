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
<!-- New entries go above this line, below the last entry -->
