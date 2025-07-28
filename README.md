# PDF Outline Extractor

## Overview

This solution extracts structured outlines (headings hierarchy) and titles from PDF documents. It analyzes font sizes to identify document titles and heading levels (H1, H2), providing a JSON representation of the document's semantic structure.

---

## 🧠 Approach

The system implements a multi-stage PDF analysis process:

### 1. Title Detection:

* Analyzes the **first page** of the PDF.
* Identifies text with the **largest font size**.
* Filters out **numerical/symbolic content**.

### 2. Heading Extraction:

* Processes **pages 2 onward**.
* Groups consecutive text with the **same font size**.
* Filters out content with font size **≥ title font size**.

### 3. Hierarchy Identification:

* Identifies the top 2 font sizes smaller than the title.
* Maps these to **H1** and **H2** heading levels.
* Creates a structured outline with **page numbers**.

### 4. Noise Filtering:

* Removes purely **numerical/symbolic content**.
* Excludes **duplicate title** occurrences.
* Handles **malformed PDFs** gracefully.

---

## 📦 Libraries Used

### Core Libraries

* `PyMuPDF (fitz)` – PDF text extraction and font analysis
* `pandas` – Data manipulation and heading classification
* `pathlib` – Cross-platform path handling

### Standard Library

* `json` – Output serialization
* `os` – File system operations
* `re` – Regular expressions for noise filtering

---

## 💻 System Requirements

* Docker
* 500 MB disk space
* PDF documents to process

---

## 🛠 Build and Run Instructions

### 1. Create Project Structure

```bash
mkdir pdf-outline-extractor
cd pdf-outline-extractor
mkdir -p input output/1a
```

### 2. Add Required Files

#### Dockerfile

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

RUN mkdir -p /app/input /app/output

ENTRYPOINT ["python", "main.py"]
```

#### requirements.txt

```ini
pymupdf==1.24.3
pandas==2.2.2
```

#### extract\_outline.py

> *(Place your implementation script here)*

### 3. Add PDF Documents

```bash
cp path/to/your/pdf/*.pdf input/
```

### 4. Build Docker Image

```bash
docker build --platform linux/amd64 -t adityapatil7730/1a .
```

### 5. Run the Container

```bash
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output/repoidentifier:/app/output \
  --network none \
  adityapatil7730/1a
```

Also available at: [Docker Hub - adityapatil7730/1a](https://hub.docker.com/repository/docker/adityapatil7730/1a/general)

---

## 📤 Output

The system generates `.json` files in the `output/repoidentifier/` directory with the naming convention:

```
[original_filename].json
```

### Example Output Format

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Main Heading",
      "page": 2
    },
    {
      "level": "H2",
      "text": "Subheading",
      "page": 3
    }
  ]
}
```

---

## 🔄 Expected Execution Workflow

1. Place PDFs in the `input/` directory.
2. Run the Docker container.
3. Find structured JSON outlines in `output/1a/`.
4. Use the output for document analysis, indexing, or navigation.

---

## 🛠 Troubleshooting

### No Output Files?

* Verify PDFs are in the `input/` directory.
* Check filenames end with `.pdf`.
* Ensure Docker volume mounts are correct.

### Permission Errors?

```bash
chmod a+rwx output/1a
```

### Processing Errors?

Rebuild the image:

```bash
docker build --no-cache --platform linux/amd64 -t adityapatil7730/1a .
```

---

## ⚠ Limitations

* Works best with **text-based PDFs** (not scanned documents).
* Heading detection depends on **consistent font size usage**.
* **Complex layouts** may reduce accuracy.
* First page **must contain a clear title**.

---

## 🎯 Design Philosophy

* **Automatic Processing**: Handles all PDFs in the input directory.
* **Security Focused**:

  * Runs with `--network none`
  * Input directory is **read-only**
* **Efficiency**: Linear time processing.
* **Reproducibility**: Dockerized for consistent results.
* **Structured Output**: Clean and machine-readable JSON.

---

## 📁 Example Directory Structure

```plaintext
pdf-outline-extractor/
├── input/
│   ├── document1.pdf
│   └── document2.pdf
└── output/
    └── repoidentifier/
        ├── document1.json
        └── document2.json
```

---

## ✅ Summary

This solution provides a robust, self-contained system for extracting semantic structure from PDF documents with minimal setup requirements.

**Docker Hub Link:** [https://hub.docker.com/repository/docker/adityapatil7730/1a/general](https://hub.docker.com/repository/docker/adityapatil7730/1a/general)
