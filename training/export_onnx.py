"""
Export a trained YOLOv8 .pt model to ONNX for the Rust inspector.

Usage:
    python export_onnx.py --run bottle_v1
    python export_onnx.py --weights path/to/best.pt
"""

import argparse
import shutil
from pathlib import Path
from ultralytics import YOLO


REPO_ROOT = Path(__file__).parent.parent
RUNS_DIR   = REPO_ROOT / "models" / "runs"
EXPORT_DIR = REPO_ROOT / "models" / "exports" / "onnx"


def parse_args():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--run",     help="Run name in models/runs/ (uses best.pt)")
    g.add_argument("--weights", help="Explicit path to .pt file")
    p.add_argument("--imgsz",   type=int, default=640)
    p.add_argument("--opset",   type=int, default=17,
                   help="ONNX opset. 17 is safe for ort 1.18+")
    p.add_argument("--simplify", action="store_true", default=True,
                   help="Run onnx-simplifier (cleaner graph for Rust/ort)")
    return p.parse_args()


def main():
    args = parse_args()

    if args.run:
        weights = RUNS_DIR / args.run / "weights" / "best.pt"
    else:
        weights = Path(args.weights)

    if not weights.exists():
        raise FileNotFoundError(f"Weights not found: {weights}")

    model = YOLO(str(weights))

    # Export — ultralytics writes alongside the .pt file
    exported = model.export(
        format="onnx",
        imgsz=args.imgsz,
        opset=args.opset,
        simplify=args.simplify,
        dynamic=False,          # fixed batch=1 for embedded inference
        half=False,             # fp32 for CPU/Rust ort compat
    )

    # Move to canonical export location
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    stem = weights.parent.parent.name  # run name, e.g. bottle_v1
    dest = EXPORT_DIR / f"{stem}.onnx"
    shutil.copy2(exported, dest)

    print(f"ONNX model saved → {dest}")
    print(f"Input shape : [1, 3, {args.imgsz}, {args.imgsz}]  (BCHW, float32, 0-1)")
    print(f"Output shape: [1, 9, 8400]  (4 bbox + 5 classes, no objectness)")


if __name__ == "__main__":
    main()
