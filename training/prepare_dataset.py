"""
Prepare the dataset for YOLOv8 training.

1. Checks that every NG image has a non-empty label file
2. Creates empty label files for OK images (true negatives for YOLO)
3. Shuffles randomly and copies to datasets/labeled/ (train + val)

Usage:
    python prepare_dataset.py                      # 80/20 split, seed 42
    python prepare_dataset.py --val-ratio 0.15
    python prepare_dataset.py --dry-run            # preview without copying
    python prepare_dataset.py --val-ratio 0        # all images in train
"""

import argparse
import random
import shutil
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
RAW_DIR     = REPO_ROOT / "datasets" / "raw"
LABELED_DIR = REPO_ROOT / "datasets" / "labeled"

SUPPORTED_IMG = {".bmp", ".jpg", ".jpeg", ".png", ".tiff", ".tif"}
NG_CLASSES    = ["color_defect", "hole", "contamination", "whitening", "mold_defect"]


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------

def collect_ok() -> list[Path]:
    d = RAW_DIR / "ok"
    return sorted(f for f in d.iterdir() if f.suffix.lower() in SUPPORTED_IMG) if d.exists() else []


def collect_ng() -> dict[str, list[Path]]:
    result = {}
    for cls in NG_CLASSES:
        d = RAW_DIR / "ng" / cls
        if d.exists():
            imgs = sorted(f for f in d.iterdir() if f.suffix.lower() in SUPPORTED_IMG)
            if imgs:
                result[cls] = imgs
    return result


# ---------------------------------------------------------------------------
# Label helpers
# ---------------------------------------------------------------------------

def has_label(img: Path) -> bool:
    lbl = img.with_suffix(".txt")
    return lbl.exists() and lbl.stat().st_size > 0


def create_empty_labels(images: list[Path]) -> int:
    created = 0
    for img in images:
        lbl = img.with_suffix(".txt")
        if not lbl.exists():
            lbl.touch()
            created += 1
    return created


# ---------------------------------------------------------------------------
# Split + copy
# ---------------------------------------------------------------------------

def split(pairs: list, val_ratio: float, seed: int):
    r = random.Random(seed)
    shuffled = pairs.copy()
    r.shuffle(shuffled)
    n_val = max(0, round(len(shuffled) * val_ratio))
    return shuffled[n_val:], shuffled[:n_val]


def copy_pair(img: Path, split_name: str) -> None:
    lbl = img.with_suffix(".txt")
    for kind, src in [("images", img), ("labels", lbl)]:
        dest_dir = LABELED_DIR / kind / split_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare YOLOv8 dataset")
    parser.add_argument("--val-ratio", type=float, default=0.2,
                        help="Fraction for validation set (default: 0.2, use 0 to skip)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed (default: 42)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without copying any files")
    args = parser.parse_args()

    ok_images = collect_ok()
    ng_images = collect_ng()

    # --- Summary ---
    print(f"\n{'-'*52}")
    print(f"  Dataset preparation -- {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"{'-'*52}")
    print(f"  OK images : {len(ok_images)}")
    ng_total = 0
    for cls, imgs in ng_images.items():
        n_lbl = sum(1 for i in imgs if has_label(i))
        print(f"  {cls:<22}: {len(imgs):>3} images  ({n_lbl} annotated)")
        ng_total += len(imgs)
    print(f"  {'TOTAL':<22}: {len(ok_images) + ng_total:>3} images")
    print()

    # --- Check NG labels ---
    missing = [img for imgs in ng_images.values() for img in imgs if not has_label(img)]
    if missing:
        print(f"[!] {len(missing)} NG image(s) have no label file yet:")
        for f in missing:
            print(f"     {f.relative_to(REPO_ROOT)}")
        print()
        print("  Annotate these images with LabelImg before running this script.")
        print("  See docs/training/dataset-guide.md for instructions.")
        if not args.dry_run:
            raise SystemExit(1)
        print("  [dry-run] Continuing anyway to show split preview.")
        print()

    # --- Build pairs ---
    pairs: list[Path] = []
    pairs.extend(ok_images)
    for imgs in ng_images.values():
        pairs.extend(img for img in imgs if has_label(img))

    if not pairs:
        print("  No annotated images found. Nothing to do.")
        return

    # --- Split ---
    train_imgs, val_imgs = split(pairs, args.val_ratio, args.seed)
    print(f"  Split  : {len(train_imgs)} train / {len(val_imgs)} val"
          f"  (val_ratio={args.val_ratio}, seed={args.seed})")
    print(f"  Output : datasets/labeled/")

    if args.dry_run:
        print("\n  [dry-run] No files copied.\n")
        return

    # --- Clean previous labeled dir ---
    for sub in ["images", "labels"]:
        shutil.rmtree(LABELED_DIR / sub, ignore_errors=True)

    # --- Create empty OK labels ---
    created = create_empty_labels(ok_images)
    if created:
        print(f"  Created {created} empty label file(s) for OK images")

    # --- Copy ---
    for img in train_imgs:
        copy_pair(img, "train")
    for img in val_imgs:
        copy_pair(img, "val")

    print(f"\n  [OK] Done -- {len(train_imgs)} train, {len(val_imgs)} val")
    print(f"  Next : python train.py\n")


if __name__ == "__main__":
    main()
