"""
Yolobottles — Image Importer
Visual triage tool: classify raw images and sort them into the dataset structure.

Usage:
    cd tools/importer
    streamlit run app.py
"""

import shutil
from pathlib import Path

import streamlit as st
from PIL import Image

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT  = Path(__file__).resolve().parent.parent.parent
IMPORT_DIR = REPO_ROOT / "datasets" / "import"
RAW_DIR    = REPO_ROOT / "datasets" / "raw"

# ---------------------------------------------------------------------------
# Class definitions  (key, button label, destination subfolder)
# ---------------------------------------------------------------------------
CLASSES = [
    ("ok",            "✅  OK — bonne bouteille",    "ok"),
    ("color_defect",  "🟡  Défaut couleur",          "ng/color_defect"),
    ("hole",          "🔴  Trou / fissure",           "ng/hole"),
    ("contamination", "⚫  Contamination",            "ng/contamination"),
    ("whitening",     "⬜  Blanchiment (whitening)",  "ng/whitening"),
    ("mold_defect",   "🔧  Défaut moule",             "ng/mold_defect"),
]

SUPPORTED_EXT = {".bmp", ".jpg", ".jpeg", ".png", ".tiff", ".tif"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_pending() -> list[Path]:
    IMPORT_DIR.mkdir(parents=True, exist_ok=True)
    return sorted(f for f in IMPORT_DIR.iterdir() if f.suffix.lower() in SUPPORTED_EXT)


def dataset_count(subpath: str) -> int:
    d = RAW_DIR / subpath
    if not d.exists():
        return 0
    return sum(1 for f in d.iterdir() if f.suffix.lower() in SUPPORTED_EXT)


def move_to(src: Path, dest_subpath: str) -> Path:
    dest_dir = RAW_DIR / dest_subpath
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    # Avoid overwriting — append _1, _2 … if needed
    if dest.exists():
        i = 1
        while dest.exists():
            dest = dest_dir / f"{src.stem}_{i}{src.suffix}"
            i += 1
    shutil.move(str(src), str(dest))
    return dest

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Yolobottles — Importer",
    page_icon="🫙",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "skip_set"    not in st.session_state:
    st.session_state.skip_set: set  = set()   # noms de fichiers ignorés ce run
if "history"     not in st.session_state:
    st.session_state.history:  list = []       # [(dest_path, src_name)]
if "n_classified" not in st.session_state:
    st.session_state.n_classified: int = 0

# ---------------------------------------------------------------------------
# Image list
# ---------------------------------------------------------------------------
all_images = get_pending()
pending    = [f for f in all_images if f.name not in st.session_state.skip_set]
n_skipped  = len(all_images) - len(pending)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🫙 Importer")
    st.caption(f"Dossier : `datasets/import/`")
    st.divider()

    st.subheader("Session en cours")
    c1, c2 = st.columns(2)
    c1.metric("Classifiées", st.session_state.n_classified)
    c2.metric("Ignorées",    n_skipped)
    st.metric("Restantes",   len(pending))

    st.divider()
    st.subheader("Dataset — totaux")
    for _, label, subpath in CLASSES:
        count = dataset_count(subpath)
        name  = label.split("  ", 1)[1]        # strip emoji prefix
        st.write(f"{name} : **{count}**")

    st.divider()
    if st.button("🔄  Réinitialiser ignorées", use_container_width=True):
        st.session_state.skip_set = set()
        st.rerun()

# ---------------------------------------------------------------------------
# Main area — empty state
# ---------------------------------------------------------------------------
st.title("🫙 Yolobottles — Importeur d'images")

if not pending:
    if n_skipped:
        st.warning(
            f"{n_skipped} image(s) ignorée(s) dans le dossier. "
            "Cliquez **Réinitialiser ignorées** dans le panneau gauche pour les reclassifier."
        )
    else:
        st.success("✅ Dossier `datasets/import/` vide — rien à classer.")
        st.info("Déposez des images dans le dossier puis rechargez la page.")
    st.stop()

# ---------------------------------------------------------------------------
# Current image — toujours la première de la liste pending
# ---------------------------------------------------------------------------
current = pending[0]

# Barre de progression
done  = st.session_state.n_classified
total = done + len(pending)
pct   = done / total if total else 0
st.progress(pct, text=f"**{len(pending)}** restante(s) · **{done}** classifiée(s) cette session")

# Mise en page : grande image à gauche, contrôles à droite
img_col, ctrl_col = st.columns([3, 1])

with img_col:
    img = Image.open(current)
    if img.mode == "L":
        img = img.convert("RGB")   # grayscale → RGB pour l'affichage
    w, h = img.size
    st.image(img, caption=f"{current.name}  ·  {w}×{h} px", use_container_width=True)

with ctrl_col:
    st.subheader("Classer")
    st.caption("Cliquez pour déplacer vers le dataset")
    st.write("")

    for key, label, subpath in CLASSES:
        if st.button(label, key=f"cls_{key}", use_container_width=True):
            dest = move_to(current, subpath)
            st.session_state.history.append((dest, current.name))
            st.session_state.n_classified += 1
            st.rerun()

    st.divider()

    if st.button("⏭️  Ignorer", use_container_width=True,
                 help="Laisse l'image dans import/, revenir plus tard"):
        st.session_state.skip_set.add(current.name)
        st.rerun()

    if st.session_state.history:
        last_dest, last_name = st.session_state.history[-1]
        short = last_name if len(last_name) <= 22 else last_name[:19] + "…"
        if st.button(f"↩️  Annuler ({short})", use_container_width=True):
            last_path = Path(last_dest)
            if last_path.exists():
                shutil.move(str(last_path), str(IMPORT_DIR / last_name))
                st.session_state.n_classified -= 1
            st.session_state.history.pop()
            st.rerun()

    st.divider()
    st.caption("**Flux :**")
    st.caption("1. Classer → image suivante automatique")
    st.caption("2. Ignorer → revenir plus tard")
    st.caption("3. Annuler → remet l'image dans import/")
