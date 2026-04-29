"""
Yolobottles - Annotator
Draw bounding boxes on NG images and save YOLO-format label files.

Usage:
    cd tools/importer
    streamlit run annotate.py
"""

from pathlib import Path

import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_NG    = REPO_ROOT / "datasets" / "raw" / "ng"

CLASSES = ["color_defect", "hole", "contamination", "whitening", "mold_defect"]

COLORS = ["#e67e22", "#e74c3c", "#8e44ad", "#3498db", "#1abc9c"]
FILLS  = [
    "rgba(230,126,34,0.2)", "rgba(231,76,60,0.2)", "rgba(142,68,173,0.2)",
    "rgba(52,152,219,0.2)", "rgba(26,188,156,0.2)",
]

SUPPORTED = {".bmp", ".jpg", ".jpeg", ".png", ".tiff", ".tif"}
CANVAS_W  = 800

# ---------------------------------------------------------------------------
# Cached helpers
# ---------------------------------------------------------------------------

@st.cache_data(ttl=5)
def get_images() -> list[str]:
    """Scan all NG subfolders — cached to avoid rescanning on every widget interaction."""
    if not RAW_NG.exists():
        return []
    return sorted(
        str(f)
        for d in RAW_NG.iterdir() if d.is_dir()
        for f in d.iterdir() if f.suffix.lower() in SUPPORTED
    )


@st.cache_data(ttl=3)
def count_annotated(ng_root: str) -> int:
    """Count annotated images — cached separately from the full list scan."""
    root = Path(ng_root)
    if not root.exists():
        return 0
    return sum(
        1 for d in root.iterdir() if d.is_dir()
        for f in d.iterdir()
        if f.suffix.lower() in SUPPORTED and f.with_suffix(".txt").exists()
        and f.with_suffix(".txt").stat().st_size > 0
    )

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def folder_class(img: Path) -> int:
    try:
        return CLASSES.index(img.parent.name)
    except ValueError:
        return 0


def is_annotated(img: Path) -> bool:
    lp = img.with_suffix(".txt")
    return lp.exists() and lp.stat().st_size > 0


def load_initial_drawing(img: Path, cw: int, ch: int) -> tuple[dict, dict]:
    """Read existing .txt labels → (canvas initial_drawing, {box_idx: class_id})."""
    lp = img.with_suffix(".txt")
    objs, classes = [], {}
    if lp.exists() and lp.stat().st_size > 0:
        for i, line in enumerate(lp.read_text().strip().splitlines()):
            parts = line.split()
            if len(parts) != 5:
                continue
            cid = int(parts[0])
            cx, cy, bw, bh = map(float, parts[1:])
            left = (cx - bw / 2) * cw
            top  = (cy - bh / 2) * ch
            wpx  = bw * cw
            hpx  = bh * ch
            objs.append({
                "type": "rect", "left": left, "top": top,
                "width": wpx, "height": hpx,
                "fill": FILLS[cid], "stroke": COLORS[cid],
                "strokeWidth": 2, "strokeUniform": True,
                "scaleX": 1.0, "scaleY": 1.0,
            })
            classes[i] = cid
    return {"version": "4.4.0", "objects": objs}, classes


def save_labels(img: Path, objs: list, box_classes: dict, cw: int, ch: int) -> int:
    """Convert canvas objects → YOLO .txt. Returns number of boxes written."""
    lines = []
    for i, obj in enumerate(objs):
        if obj.get("type") != "rect":
            continue
        cid = box_classes.get(i, folder_class(img))
        wpx = obj["width"]  * obj.get("scaleX", 1.0)
        hpx = obj["height"] * obj.get("scaleY", 1.0)
        cx  = max(0.0, min(1.0, (obj["left"] + wpx / 2) / cw))
        cy  = max(0.0, min(1.0, (obj["top"]  + hpx / 2) / ch))
        bw  = max(0.001, min(1.0, wpx / cw))
        bh  = max(0.001, min(1.0, hpx / ch))
        lines.append(f"{cid} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
    img.with_suffix(".txt").write_text("\n".join(lines) + ("\n" if lines else ""))
    count_annotated.clear()
    return len(lines)

# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Yolobottles - Annotator",
    page_icon="✏️",
    layout="wide",
)

st.session_state.setdefault("idx", 0)
st.session_state.setdefault("box_classes", {})
st.session_state.setdefault("n_saved", 0)

image_paths = get_images()
images      = [Path(p) for p in image_paths]
n_total     = len(images)
n_done      = count_annotated(str(RAW_NG))

# Sidebar
with st.sidebar:
    st.header("Annotator")
    c1, c2 = st.columns(2)
    c1.metric("Total NG", n_total)
    c2.metric("Annotees", n_done)
    st.metric("Restantes", n_total - n_done)
    st.metric("Session", st.session_state.n_saved)
    st.divider()
    st.subheader("Navigation")
    for i, f in enumerate(images):
        icon  = "[OK]" if is_annotated(f) else "[  ]"
        label = f"{icon} {f.parent.name}/{f.name}"
        if st.button(label, key=f"nav_{i}", use_container_width=True):
            st.session_state.idx = i
            st.session_state.box_classes = {}
            st.rerun()

# Main
st.title("Annotator - Bounding Boxes YOLO")

if not images:
    st.warning("Aucune image NG dans `datasets/raw/ng/`. Importez d'abord des images.")
    st.stop()

st.session_state.idx = min(st.session_state.idx, n_total - 1)
current = images[st.session_state.idx]

pct = n_done / n_total if n_total else 0
st.progress(
    pct,
    text=f"**{n_done}/{n_total}** annotees  |  {current.parent.name} / {current.name}"
)

# Load image + scale to fit canvas
img_pil = Image.open(current).convert("RGB")
ow, oh  = img_pil.size
scale   = min(CANVAS_W / ow, 1.0)
cw, ch  = int(ow * scale), int(oh * scale)
display = img_pil.resize((cw, ch), Image.LANCZOS)

# Load existing labels for this image
init_drawing, loaded_classes = load_initial_drawing(current, cw, ch)
if not st.session_state.box_classes:
    st.session_state.box_classes = loaded_classes.copy()

# Layout: canvas left, controls right
img_col, ctrl_col = st.columns([3, 1])

with ctrl_col:
    st.subheader("Classe active")
    st.caption("Choisir avant de dessiner")
    default_cid = folder_class(current)
    active_cls  = st.selectbox(
        "cls", CLASSES, index=default_cid,
        key="active_cls", label_visibility="collapsed",
    )
    active_cid = CLASSES.index(active_cls)
    st.markdown(
        f"<span style='color:{COLORS[active_cid]};font-size:1.2em'>&#9632;</span> "
        f"`{active_cls}`",
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("**Dessiner** : cliquer-glisser")
    st.caption("**Deplacer** : cliquer sur la boite")
    st.caption("**Supprimer** : selectionner + Delete")
    st.caption("**Redimensionner** : poignees de coin")

with img_col:
    result = st_canvas(
        fill_color=FILLS[active_cid],
        stroke_color=COLORS[active_cid],
        stroke_width=2,
        background_image=display,
        update_streamlit=True,
        height=ch,
        width=cw,
        drawing_mode="rect",
        initial_drawing=init_drawing,
        key=f"canvas_{current.stem}",
    )

# Box list with per-box class selector
objs = [
    o for o in (result.json_data or {}).get("objects", [])
    if o.get("type") == "rect"
]

if len(objs) < len(st.session_state.box_classes):
    st.session_state.box_classes = {
        i: st.session_state.box_classes.get(i, folder_class(current))
        for i in range(len(objs))
    }

if objs:
    st.subheader(f"{len(objs)} boite(s)")
    hdr = st.columns([1, 4, 2])
    hdr[0].caption("#")
    hdr[1].caption("Position normalisee (cx  cy  w  h)")
    hdr[2].caption("Classe")
    for i, obj in enumerate(objs):
        wpx  = obj["width"]  * obj.get("scaleX", 1.0)
        hpx  = obj["height"] * obj.get("scaleY", 1.0)
        cx_n = (obj["left"] + wpx / 2) / cw
        cy_n = (obj["top"]  + hpx / 2) / ch
        row  = st.columns([1, 4, 2])
        row[0].write(f"**{i + 1}**")
        row[1].caption(
            f"cx={cx_n:.3f}  cy={cy_n:.3f}  "
            f"w={wpx / cw:.3f}  h={hpx / ch:.3f}"
        )
        cur_cls = st.session_state.box_classes.get(i, active_cid)
        chosen  = row[2].selectbox(
            f"b{i}", CLASSES, index=cur_cls,
            key=f"bls_{current.stem}_{i}",
            label_visibility="collapsed",
        )
        st.session_state.box_classes[i] = CLASSES.index(chosen)
else:
    st.info("Aucune boite dessinee — cliquer-glisser sur l'image pour en ajouter.")

# Navigation + save bar
st.divider()
b1, b2, b3, b4 = st.columns(4)

if b1.button("< Precedente", use_container_width=True,
             disabled=st.session_state.idx == 0):
    st.session_state.idx -= 1
    st.session_state.box_classes = {}
    st.rerun()

if b2.button("Suivante >", use_container_width=True,
             disabled=st.session_state.idx == n_total - 1):
    st.session_state.idx += 1
    st.session_state.box_classes = {}
    st.rerun()

if b3.button("Sauvegarder", use_container_width=True, type="primary"):
    n = save_labels(current, objs, st.session_state.box_classes, cw, ch)
    st.session_state.n_saved += 1
    st.toast(f"{n} boite(s) sauvegardee(s)")

if b4.button("Sauvegarder + Suivante >>", use_container_width=True, type="primary",
             disabled=st.session_state.idx == n_total - 1):
    save_labels(current, objs, st.session_state.box_classes, cw, ch)
    st.session_state.n_saved += 1
    st.session_state.idx += 1
    st.session_state.box_classes = {}
    st.rerun()
