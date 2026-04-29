---
tags: [meta, schema]
created: 2026-04-28
status: active
---

# Documentation Schema | Schéma de documentation

> This file governs how all documentation in this project is written and maintained.
> Ce fichier définit les règles d'écriture et de maintenance de toute la documentation du projet.

---

## English

### Principles (inspired by Karpathy's LLM Wiki pattern)

The documentation is a **persistent, compounding artifact**. It grows incrementally — never rewritten from scratch. Every piece of new knowledge (a decision, a finding, a parameter change) is **ingested** into the relevant page and logged in [[log]].

#### Three layers

| Layer | What it is | Who owns it |
|-------|-----------|-------------|
| **Raw sources** | Papers, datasheets, Ultralytics docs, images | Immutable, linked not copied |
| **Wiki pages** | Summaries, entity pages, cross-references | Claude + developer |
| **Schema** | This file — governs structure and workflows | Developer |

#### File structure

```
docs/
├── index.md          ← Hub: catalog of all pages by category
├── log.md            ← Append-only chronological log
├── schema.md         ← This file
├── architecture/     ← System design, pipeline, hardware
├── defects/          ← One page per defect class + catalog
├── training/         ← Dataset, augmentation, YOLO config
├── deployment/       ← Jetson, ONNX, TensorRT
└── machine/          ← SBO blower context, inspection point
```

#### Page format (mandatory frontmatter)

```markdown
---
tags: [category, subcategory]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | active | archived
---
```

#### Bilingual format

Each page contains **both languages** in separate top-level sections:

```markdown
## English
...content...

---

## Français
...contenu...
```

Cross-language links use the same target: `[[page-name]]`.
Section links add the anchor: `[[page-name#English]]`.

#### Obsidian conventions

- Internal links: `[[page-name]]` (no `.md` extension)
- Section links: `[[page-name#Section heading]]`
- Tags: lowercase, hyphen-separated — `#pet-bottle`, `#yolo`, `#defect`
- Callouts for important content:
  - `> [!NOTE]` — information
  - `> [!WARNING]` — watch out
  - `> [!TIP]` — best practice
  - `> [!IMPORTANT]` — critical constraint

#### Operations

**Ingest** — When new knowledge arrives (experiment result, paper read, parameter tuned):
1. Update the relevant wiki page(s)
2. Append one line to [[log]] with the date and what changed
3. Update [[index]] if a new page was created

**Lint** (periodic) — Check for:
- Orphaned pages (no links pointing to them)
- Stale claims (superseded by newer experiments)
- Missing cross-references between related pages

---

## Français

### Principes (inspirés du pattern LLM Wiki de Karpathy)

La documentation est un **artefact persistant et cumulatif**. Elle grandit de façon incrémentale — jamais réécrite de zéro. Chaque nouvelle connaissance (décision, découverte, changement de paramètre) est **intégrée** dans la page concernée et consignée dans [[log]].

#### Trois couches

| Couche | Contenu | Responsable |
|--------|---------|-------------|
| **Sources brutes** | Articles, datasheets, docs Ultralytics, images | Immuables, liées pas copiées |
| **Pages wiki** | Résumés, pages d'entité, références croisées | Claude + développeur |
| **Schéma** | Ce fichier — gouverne la structure | Développeur |

#### Format des pages (frontmatter obligatoire)

```markdown
---
tags: [catégorie, sous-catégorie]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | active | archived
---
```

#### Format bilingue

Chaque page contient les deux langues dans des sections de premier niveau séparées. Les liens Obsidian sont identiques dans les deux langues — même cible `[[nom-page]]`.

#### Opérations

**Ingestion** — Quand une nouvelle connaissance arrive :
1. Mettre à jour la ou les pages wiki concernées
2. Ajouter une ligne dans [[log]] avec la date et la modification
3. Mettre à jour [[index]] si une nouvelle page a été créée

**Lint** (périodique) — Vérifier :
- Pages orphelines (aucun lien ne pointe vers elles)
- Affirmations obsolètes (dépassées par des expériences plus récentes)
- Références croisées manquantes entre pages liées
