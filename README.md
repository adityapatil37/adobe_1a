# PDF Outline Extractor

## Overview

This solution extracts structured outlines (headings hierarchy) and titles from PDF documents. It analyzes font sizes to identify document titles and heading levels (H1, H2), providing a JSON representation of the document's semantic structure.

---

## 🧠 Approach

The system implements a multi-stage PDF analysis process:

### 1. Title Detection:
- Analyzes the **first page** of the PDF.
- Identifies text with the **largest font size**.
- Filters out **numerical/symbolic content**.

### 2. Heading Extraction:
- Processes **pages 2 onward**.
- Groups consecutive text with the **same font size**.
- Filters out content with font size **≥ title font size**.

### 3. Hierarchy Identification:
- Identifies the top 2 font sizes smaller than the title.
- Maps these to **H1** and **H2** heading levels.
- Creates a structured outline with **page numbers**.

### 4. Noise Filtering:
- Removes purely **numerical/symbolic content**.
- Excludes **duplicate title** occurrences.
- Handles **malformed PDFs** gracefully.

---

## 📦 Libraries Used

### Core Libraries
- `PyMuPDF (fitz)` – PDF text extraction and font analysis
- `pandas` – Data manipulation and heading classification
- `pathlib` – Cross-platform path handling

### Standard Library
- `json` – Output serialization
- `os` – File system operations
- `re` – Regular expressions for noise filtering

---

## 💻 System Requirements

- Docker
- 500 MB disk space
- PDF documents to process

---

## 🛠 Build and Run Instructions

### 1. Create Project Structure

```bash
mkdir pdf-outline-extractor
cd pdf-outline-extractor
mkdir -p input output/repoidentifier
```
