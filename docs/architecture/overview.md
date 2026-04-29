---
tags: [architecture, overview]
created: 2026-04-28
updated: 2026-04-28
status: active
---

# System Overview | Vue d'ensemble du système

See also: [[architecture/pipeline]] · [[architecture/hardware]] · [[index]]

---

## English

### Goal

Detect defects on empty blown PET bottles in real time. The camera films the **bottle bottom through the neck (goulot)** from above, producing a circular top-down image of the bottom geometry and surface.

### Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **Mockup** | Image bank, no camera, no PLC | Current |
| **Lab prototype** | Live USB/GigE camera, standalone ejector | Next |
| **Production** | Jetson Orin + GigE Vision + encoder trigger | Future |

### System diagram

```
┌─────────────────────────────────────────────────────────┐
│                     TRAINING (Python)                   │
│                                                         │
│  Image bank  →  Annotation  →  YOLOv8s training        │
│  (datasets/raw)   (LabelImg)    (training/train.py)     │
│                                      │                  │
│                              best.pt │                  │
│                                      ▼                  │
│                          export_onnx.py                 │
│                                      │                  │
│                          model.onnx  │                  │
└──────────────────────────────────────┼──────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────┐
│                   INSPECTOR (Rust)                      │
│                                                         │
│  Image source  ──►  pipeline.rs  ──►  inference.rs      │
│  (bank / camera)    (scan loop)      (ONNX Runtime)     │
│                          │                              │
│                    OK/NG decision                       │
│                     │         │                         │
│                  log stats  ejector.rs                  │
│                     │         │                         │
│                  hmi/mod.rs  GPIO/serial (future)       │
│                  (Axum :8080)                           │
└─────────────────────────────────────────────────────────┘
```

### Key architectural decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Inference language | **Rust** | Deterministic, low latency, no GC pauses — required for future real-time |
| Model format in prod | **ONNX** (mockup) → **TensorRT** (Jetson) | ONNX is portable; TRT maximizes Jetson GPU throughput |
| Training framework | **Ultralytics YOLOv8** | Best-in-class pretrained weights, active community, clean export API |
| HMI | **Axum web server** | Zero extra install for operator, works on any device on the network |
| Ejector interface | **Standalone** (no Sidel PLC) | Decoupled from machine, easier to prototype and certify independently |

### Data flow (production target)

```
Encoder pulse (machine cycle)
       │
       ▼
  Camera trigger  →  GigE Vision frame capture
                               │
                         frame buffer
                               │
                     Rust pipeline (≤ 36 ms budget)
                       ├── preprocess (resize, normalize)
                       ├── ONNX/TRT inference
                       ├── NMS + threshold
                       └── OK / NG
                                │
                       ┌────────┴────────┐
                       │                 │
                   log + HMI      ejector pulse
                                  (timed to bottle
                                   position on conveyor)
```

> [!IMPORTANT] Latency budget
> At 100,000 bottles/hour = 27.8 bottles/sec → **36 ms per bottle**.
> YOLOv8s on TensorRT (Jetson Orin NX) typically achieves 8–15 ms inference.
> Full pipeline target: < 25 ms end-to-end.

---

## Français

### Objectif

Détecter les défauts sur des bouteilles PET vides soufflées en temps réel. La caméra filme le **fond de bouteille par le goulot** depuis le dessus, produisant une image circulaire vue de dessus du fond et de sa géométrie.

### Phases

| Phase | Description | Statut |
|-------|-------------|--------|
| **Maquette** | Banque d'images, pas de caméra, pas d'API | En cours |
| **Prototype labo** | Caméra USB/GigE live, éjecteur autonome | Suivant |
| **Production** | Jetson Orin + GigE Vision + déclenchement codeur | Futur |

### Décisions architecturales clés

| Décision | Choix | Justification |
|----------|-------|---------------|
| Langage d'inférence | **Rust** | Déterministe, faible latence, pas de pauses GC — requis pour le temps réel |
| Format modèle en prod | **ONNX** (maquette) → **TensorRT** (Jetson) | ONNX portable ; TRT maximise le débit GPU Jetson |
| Framework d'entraînement | **Ultralytics YOLOv8** | Meilleurs poids pré-entraînés, communauté active, export propre |
| HMI | **Serveur web Axum** | Aucune installation supplémentaire, fonctionne sur tout appareil du réseau |
| Interface éjecteur | **Autonome** (sans API Sidel) | Découplé de la machine, plus simple à prototyper et certifier |

### Budget de latence

À 100 000 bouteilles/heure = 27,8 bouteilles/seconde → **36 ms par bouteille**.
YOLOv8s sous TensorRT (Jetson Orin NX) atteint typiquement 8–15 ms d'inférence.
Objectif pipeline complet : < 25 ms de bout en bout.
