---
name: pptx
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptxgenjs.md) |

---

## Reading Content

```bash
python -m markitdown presentation.pptx
python scripts/thumbnail.py presentation.pptx
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone.

### Before Starting

- **Pick a bold, content-informed color palette**: specific to THIS topic
- **Dominance over equality**: One color dominates 60-70%, with 1-2 supporting tones and one accent
- **Dark/light contrast**: Dark backgrounds for title + conclusion, light for content ("sandwich")
- **Commit to a visual motif**: ONE distinctive element repeated across every slide

### Color Palettes

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` | `CADCFC` | `FFFFFF` |
| **Forest & Moss** | `2C5F2D` | `97BC62` | `F5F5F5` |
| **Coral Energy** | `F96167` | `F9E795` | `2F3C7E` |
| **Warm Terracotta** | `B85042` | `E7E8D1` | `A7BEAE` |
| **Ocean Gradient** | `065A82` | `1C7293` | `21295C` |
| **Charcoal Minimal** | `36454F` | `F2F2F2` | `212121` |
| **Teal Trust** | `028090` | `00A896` | `02C39A` |
| **Berry & Cream** | `6D2E46` | `A26769` | `ECE2D0` |
| **Sage Calm** | `84B59F` | `69A297` | `50808E` |
| **Cherry Bold** | `990011` | `FCF6F5` | `2F3C7E` |

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape.

**Layout options:** Two-column, icon+text rows, 2x2/2x3 grid, half-bleed image

**Typography:**

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Avoid

- Don't repeat the same layout
- Don't center body text
- Don't default to blue
- Don't create text-only slides
- **NEVER use accent lines under titles** — hallmark of AI-generated slides

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA
```bash
python -m markitdown output.pptx
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

### Visual QA

**USE SUBAGENTS** — even for 2-3 slides. Fresh eyes find what you miss.

Convert slides to images:
```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Inspect for: overlapping elements, text overflow, low contrast, placeholder remnants, alignment issues.

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Dependencies

```bash
pip install "markitdown[pptx]"
pip install Pillow
npm install -g pptxgenjs
# LibreOffice (soffice) — auto-configured via scripts/office/soffice.py
# Poppler (pdftoppm) — PDF to images
```
