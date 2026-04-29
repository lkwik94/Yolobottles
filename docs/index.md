---
tags: [meta, index]
created: 2026-04-28
updated: 2026-04-28
status: active
---

# Yolobottles — Knowledge Index | Index des connaissances

> Central hub for all project documentation.
> Hub central de toute la documentation du projet.

See [[schema]] for writing rules. See [[log]] for activity history. See [[workspace-guide]] to get started.

---

## English

### What is this project?

Real-time vision inspection system for empty blown PET bottles on a Sidel SBO blower line.
Camera mounted above, filming the **bottle bottom through the neck**. YOLO-based defect detection, Rust inference engine, standalone ejector.

> [!NOTE] Current phase
> **Mockup** — working with image banks. No live camera, no PLC connection.
> Target deployment: NVIDIA Jetson + GigE Vision camera at up to 100,000 bottles/hour.

---

### Getting started

| Page | Description |
|------|-------------|
| [[workspace-guide]] | Full workspace usage guide — setup, daily workflow, all tools |

### Tools

| Page | Description |
|------|-------------|
| [[tools/importer]] | Visual image triage — classify raw images into the dataset structure |
| [[tools/annotator]] | Browser-based bounding box annotator — draw YOLO labels on NG images |

### Architecture

| Page | Description |
|------|-------------|
| [[architecture/overview]] | Full system diagram, data flow, component roles |
| [[architecture/pipeline]] | Frame processing pipeline (image → inference → decision) |
| [[architecture/hardware]] | GPU workstation, target Jetson, camera specs |

### Defects

| Page | Description |
|------|-------------|
| [[defects/catalog]] | All 5 defect classes, visual examples, severity |
| [[defects/color_defect]] | Abnormal coloration, yellowing |
| [[defects/hole]] | Perforation, crack, tear in PET wall |
| [[defects/contamination]] | Foreign particle, black spot, inclusion |
| [[defects/whitening]] | PET stress whitening, opaque zone |
| [[defects/mold_defect]] | Missing or deformed mold imprint on bottle bottom |

### Training

| Page | Description |
|------|-------------|
| [[training/dataset-guide]] | How to acquire, sort, and annotate images |
| [[training/augmentation]] | Augmentation strategy — why 360° rotation |
| [[training/yolo-config]] | YOLOv8 hyperparameters and rationale |
| [[training/experiments]] | Results table: model × dataset × metrics |

### Deployment

| Page | Description |
|------|-------------|
| [[deployment/onnx-export]] | Export pipeline .pt → ONNX → Rust |
| [[deployment/jetson]] | Jetson setup, TensorRT conversion, latency budget |

### Machine context

| Page | Description |
|------|-------------|
| [[machine/sidel-sbo]] | Sidel SBO blower — machine overview, cycle, cavities |
| [[machine/inspection-point]] | Camera position, bottle flow, trigger strategy |

---

## Français

### Qu'est-ce que ce projet ?

Système de vision industrielle pour l'inspection de bouteilles PET vides soufflées sur une ligne Sidel SBO.
Caméra montée au-dessus, filmant le **fond de bouteille par le goulot**. Détection de défauts par YOLO, moteur d'inférence Rust, éjecteur autonome.

> [!NOTE] Phase actuelle
> **Maquette** — travail sur banque d'images. Pas de caméra live, pas de connexion API.
> Déploiement cible : NVIDIA Jetson + caméra GigE Vision jusqu'à 100 000 bouteilles/heure.

---

### Outils

| Page | Description |
|------|-------------|
| [[tools/importer]] | Triage visuel d'images — classer les images brutes dans la structure dataset |
| [[tools/annotator]] | Annoteur de bounding boxes dans le navigateur — dessiner les labels YOLO sur les NG |

### Architecture

| Page | Description |
|------|-------------|
| [[architecture/overview]] | Schéma système complet, flux de données, rôles des composants |
| [[architecture/pipeline]] | Pipeline de traitement d'image (image → inférence → décision) |
| [[architecture/hardware]] | Station GPU, Jetson cible, caractéristiques caméra |

### Défauts

| Page | Description |
|------|-------------|
| [[defects/catalog]] | Les 5 classes de défauts, exemples visuels, sévérité |
| [[defects/color_defect]] | Coloration anormale, jaunissement |
| [[defects/hole]] | Perforation, criqure, déchirure dans la paroi PET |
| [[defects/contamination]] | Particule étrangère, point noir, inclusion |
| [[defects/whitening]] | Blanchissement du PET sous contrainte |
| [[defects/mold_defect]] | Empreinte de moule manquante ou déformée sur le fond |

### Entraînement

| Page | Description |
|------|-------------|
| [[training/dataset-guide]] | Comment acquérir, trier et annoter les images |
| [[training/augmentation]] | Stratégie d'augmentation — pourquoi rotation 360° |
| [[training/yolo-config]] | Hyperparamètres YOLOv8 et justifications |
| [[training/experiments]] | Tableau de résultats : modèle × dataset × métriques |

### Pour commencer

| Page | Description |
|------|-------------|
| [[workspace-guide]] | Guide complet d'utilisation — installation, workflow quotidien, tous les outils |

### Déploiement

| Page | Description |
|------|-------------|
| [[deployment/onnx-export]] | Pipeline d'export .pt → ONNX → Rust |
| [[deployment/jetson]] | Configuration Jetson, conversion TensorRT, budget latence |

### Contexte machine

| Page | Description |
|------|-------------|
| [[machine/sidel-sbo]] | Souffleuse Sidel SBO — vue d'ensemble, cycle, empreintes |
| [[machine/inspection-point]] | Position caméra, flux bouteilles, stratégie de déclenchement |
