---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf | See FORMS.md |

For advanced features and JavaScript libraries, see REFERENCE.md.
If filling a PDF form, read FORMS.md first.

---

## Python Libraries

### pypdf — Basic Operations

```python
from pypdf import PdfReader, PdfWriter

# Read
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = "".join(page.extract_text() for page in reader.pages)

# Merge
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
with open("merged.pdf", "wb") as f:
    writer.write(f)

# Split
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    w = PdfWriter()
    w.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        w.write(f)

# Rotate
page = reader.pages[0]
page.rotate(90)
```

### pdfplumber — Text and Table Extraction

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    # Text
    for page in pdf.pages:
        print(page.extract_text())

    # Tables → DataFrame
    all_tables = []
    for page in pdf.pages:
        for table in page.extract_tables():
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

combined_df = pd.concat(all_tables, ignore_index=True)
combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab — Create PDFs

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Report Title", styles['Title']))
story.append(Spacer(1, 12))
story.append(Paragraph("Body content here.", styles['Normal']))
story.append(PageBreak())
story.append(Paragraph("Page 2", styles['Heading1']))

doc.build(story)
```

> **IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂, ⁰¹²) in ReportLab — fonts lack these glyphs. Use XML tags instead:
> ```python
> Paragraph("H<sub>2</sub>O and x<super>2</super>", styles['Normal'])
> ```

---

## Command-Line Tools

```bash
# pdftotext
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt
pdftotext -f 1 -l 5 input.pdf output.txt

# qpdf
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf

# pdftk
pdftk file1.pdf file2.pdf cat output merged.pdf
```

---

## Common Tasks

### OCR Scanned PDFs
```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = "\n\n".join(f"Page {i+1}:\n{pytesseract.image_to_string(img)}"
                   for i, img in enumerate(images))
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter
watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
with open("watermarked.pdf", "wb") as f:
    writer.write(f)
```

### Password Protection
```python
from pypdf import PdfWriter
writer = PdfWriter()
# ... add pages ...
writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as f:
    writer.write(f)
```
