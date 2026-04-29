# CLAUDE.md — Yolobottles

This file is automatically loaded by Claude Code at the start of every session.
It defines conventions, commands, and mandatory behaviors for this project.

---

## Project

**Yolobottles** is an industrial vision inspection system for empty blown PET bottles on Sidel SBO blower lines. The camera films the bottle bottom through the neck from above. YOLO-based defect detection, Rust inference engine, standalone ejector.

**Current phase:** Mockup — image bank, no live camera, no PLC.
**Target:** NVIDIA Jetson + GigE Vision camera at up to 100,000 bottles/hour.

**5 defect classes:** `color_defect` · `hole` · `contamination` · `whitening` · `mold_defect`

---

## Key Commands

### Python — Training
```bash
cd training
# Create and activate venv (first time only — never install globally)
python -m venv .venv
.venv\Scripts\Activate.ps1          # PowerShell (Windows)

# Install dependencies (first time only, inside venv)
# Step 1 — PyTorch with CUDA 12.8 (compatible with CUDA 13.0 drivers / Blackwell RTX PRO 500)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
# Step 2 — rest of dependencies
pip install -r requirements.txt

# Train
python train.py --model yolov8s.pt --epochs 50 --batch 16

# Export to ONNX
python export_onnx.py --run bottle_v1
```

### Rust — Inspector
```bash
# Run from project root: E:\OneDrive\Yolobottles
cd inspector
cargo build --release

# Run on image bank
./target/release/inspector \
  --model ../models/exports/onnx/bottle_v1.onnx \
  --images ../datasets/raw \
  --threshold 0.5 \
  --port 8080

# HMI dashboard → http://localhost:8080
```

---

## Documentation — MANDATORY

**After every significant change, complete ALL three steps:**

1. **Update the relevant `docs/` page** (or create it if it doesn't exist).
   Follow the bilingual format defined in [`docs/schema.md`](docs/schema.md):
   each page has an `## English` section and a `## Français` section.

2. **Append one line to [`docs/log.md`](docs/log.md)**:
   ```
   ## YYYY-MM-DD
   [short description of what changed and why]
   ```

3. **Update [`docs/index.md`](docs/index.md)** if a new page was created.

### What counts as "significant"

| Event | Action |
|-------|--------|
| Architecture decision | Update `docs/architecture/overview.md` |
| New training run | Add row to `docs/training/experiments.md` (create if missing) |
| Hyperparameter change | Update `docs/training/yolo-config.md` |
| New defect insight | Update the relevant `docs/defects/*.md` page |
| Dataset change | Update `docs/training/dataset-guide.md` |
| Jetson / hardware finding | Update `docs/deployment/jetson.md` |
| New external document ingested | Run `wiki-ingest` (see below) |

---

## Two-Layer Knowledge System

This project uses **two complementary documentation systems**:

### Layer 1 — `docs/` (Human-written, Obsidian wiki)
Project-specific documentation written collaboratively. Bilingual (EN + FR).
Open in Obsidian as a vault: `File → Open folder as vault → docs/`.

Structure: [`docs/index.md`](docs/index.md) is the hub.

### Layer 2 — `wiki/` (LLM-synthesized, llm-wiki skill)
Knowledge base built from ingested external documents:
papers, datasheets, Ultralytics docs, GigE Vision specs, Jetson guides, etc.

**Triggers:**
- `wiki-input <path>` — ingest any local or remote file
- `wiki-query: <question>` — search and synthesize an answer
- `wiki-graph` — generate interactive knowledge graph (`graph/graph.html`)
- `wiki-lint` — health check (broken links, contradictions)

**When to use each layer:**

| You want to... | Use |
|----------------|-----|
| Document a project decision | `docs/` |
| Record an experiment result | `docs/training/experiments.md` |
| Add a paper or datasheet | `wiki-input` → `wiki/` |
| Answer "how does YOLOv8 NMS work?" | `wiki-query` |
| Create a customer presentation | `pptx` skill |
| Export training metrics as Excel | `xlsx` skill |

---

## Repository Structure

```
Yolobottles/
├── CLAUDE.md               ← This file
├── .claude/
│   ├── config/
│   │   └── llm-wiki.json   ← wiki workspace config (= project root)
│   └── skills/             ← installed skills
├── datasets/
│   ├── raw/ok/ + raw/ng/*/ ← image bank (gitignored)
│   ├── labeled/            ← annotated images in YOLO format (gitignored)
│   └── dataset.yaml        ← YOLO dataset config (5 classes)
├── training/
│   ├── train.py            ← YOLOv8s training script
│   └── export_onnx.py      ← export .pt → .onnx
├── models/
│   ├── pretrained/         ← .pt weights (gitignored)
│   ├── runs/               ← training outputs (gitignored)
│   └── exports/onnx/       ← .onnx models for inspector
├── inspector/              ← Rust inference application
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs         ← CLI + startup
│       ├── inference.rs    ← ONNX Runtime, NMS
│       ├── pipeline.rs     ← image bank processing loop
│       ├── ejector.rs      ← ejector control (simulated)
│       └── hmi/            ← Axum web server + dashboard
├── docs/                   ← Human-written Obsidian wiki (Layer 1)
│   ├── index.md            ← Hub
│   ├── log.md              ← Append-only changelog
│   ├── schema.md           ← Documentation rules
│   ├── architecture/
│   ├── defects/            ← One page per defect class
│   ├── training/
│   ├── deployment/
│   └── machine/
├── wiki/                   ← LLM-synthesized knowledge base (Layer 2)
│   ├── index.md
│   ├── overview.md
│   ├── log.md
│   ├── sources/
│   ├── entities/
│   └── concepts/
├── raw/                    ← Raw documents for wiki ingestion
│   └── inbox/
└── graph/                  ← Knowledge graph visualization
    └── graph.html
```

---

## Architecture Decisions (summary)

| Decision | Choice |
|----------|--------|
| Inference language | Rust (`ort` crate = ONNX Runtime) |
| Training framework | Python + Ultralytics YOLOv8s |
| Model format (dev) | ONNX |
| Model format (prod) | TensorRT (Jetson) |
| HMI | Axum web server, port 8080 |
| Ejector | Standalone, not connected to Sidel B&R PLC |
| Augmentation | `degrees=360` (bottle has no preferred orientation) |

---

## Hardware

| Component | Value |
|-----------|-------|
| GPU | RTX PRO 500 Black — 6 GB VRAM |
| CPU | Intel Ultra 7 265H — 16 cores |
| RAM | 32 GB |
| CUDA | 13.0 — use PyTorch cu128 build (PyTorch 2.11.0 + CUDA 12.8, Blackwell compatible) |
| Python | 3.12.10 |
| Rust | 1.93.1 |

---

## Code Style

- **Rust**: no unnecessary comments, `tracing` for logging, no `unwrap()` in production paths
- **Python training scripts**: minimal comments, no print-driven debugging — use logging
- **No hardcoded paths**: use `Path(__file__).parent.parent` anchored to repo root
- **Docs**: bilingual EN + FR, Obsidian `[[wiki links]]`, frontmatter on every page

---

## Skills Available

| Skill | Trigger |
|-------|---------|
| `llm-wiki` | `wiki-input`, `wiki-query`, `wiki-graph`, `wiki-lint` |
| `xlsx` | "create/edit spreadsheet", "export to Excel" |
| `webapp-testing` | "test the HMI", "check the dashboard" |
| `pptx` | "create presentation", "slides", "deck" |
| `pdf` | "extract from PDF", "merge PDFs" |
| `mcp-builder` | "build MCP server", "create MCP integration" |
| `skill-creator` | "create a skill", "optimize skill description" |
| `troubleshooting-sidel-blower` | Sidel SBO alarms, B&R PLC diagnostics |
