"""
Train YOLOv8 on the bottle inspection dataset.

Usage:
    python train.py
    python train.py --model yolov8m.pt --epochs 100 --batch 16
"""

import argparse
from pathlib import Path
from ultralytics import YOLO


REPO_ROOT = Path(__file__).parent.parent
DATASET_YAML = REPO_ROOT / "datasets" / "dataset.yaml"
PRETRAINED_DIR = REPO_ROOT / "models" / "pretrained"
RUNS_DIR = REPO_ROOT / "models" / "runs"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="yolov8s.pt",
                   help="Pretrained weights (yolov8n/s/m/l/x.pt). "
                        "Downloaded automatically on first run.")
    p.add_argument("--epochs", type=int, default=50)
    p.add_argument("--batch",  type=int, default=16,
                   help="Batch size. Reduce to 8 if VRAM OOM.")
    p.add_argument("--imgsz",  type=int, default=640)
    p.add_argument("--device", default="0",
                   help="GPU index (0) or 'cpu'")
    p.add_argument("--name",   default="bottle_v1",
                   help="Run name inside models/runs/")
    return p.parse_args()


def main():
    args = parse_args()

    weights = PRETRAINED_DIR / args.model
    if not weights.exists():
        # ultralytics downloads to cwd by default — redirect
        weights = args.model  # let ultralytics handle download

    model = YOLO(str(weights))

    model.train(
        data=str(DATASET_YAML),
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        project=str(RUNS_DIR),
        name=args.name,

        # Augmentations — tuned for round bottle-bottom images
        degrees=360.0,     # full rotation: bottle has no "up"
        fliplr=0.5,
        flipud=0.5,
        hsv_h=0.015,       # slight hue shift (PET color variation)
        hsv_s=0.4,
        hsv_v=0.4,
        scale=0.3,         # zoom in/out
        mosaic=0.0,        # disable mosaic: single-object images
        mixup=0.0,

        # Reproducibility
        seed=42,
        workers=8,

        # Saves best.pt and last.pt
        save=True,
        save_period=10,
    )

    print(f"\nTraining done. Best model: {RUNS_DIR / args.name / 'weights' / 'best.pt'}")
    print("Next step: python export_onnx.py --run", args.name)


if __name__ == "__main__":
    main()
