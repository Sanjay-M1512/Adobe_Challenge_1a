# Adobe Hackathon 2025 – Round 1A
## 🧠 Challenge: Understand Your Document – Heading Structure Extraction

---

## 🚀 Overview

This solution extracts a structured outline (Title, H1, H2, H3) from PDF documents using **semantic understanding** rather than relying on visual formatting like font size.

It uses:
- `PyMuPDF` for accurate PDF text extraction
- `spaCy` for linguistic filtering of meaningful text blocks
- `DistilBERT` from HuggingFace Transformers to classify headings based on context

The final output is a valid JSON file for each input PDF, matching the required schema.

---

## ⚙️ Tech Stack

| Component       | Purpose                        |
|----------------|---------------------------------|
| Python 3.10     | Programming language           |
| PyMuPDF         | PDF parsing and text extraction |
| spaCy (en_core_web_sm) | POS tagging, NLP structure         |
| DistilBERT      | Heading classification (semantic) |
| Transformers + Torch | Running BERT inference        |
| Docker          | Containerized, offline-capable build |

---

## 📂 Folder Structure

```
.
├── process_pdfs.py          # Main script
├── Dockerfile               # Docker config (AMD64 CPU only)
├── sample_dataset/
│   ├── pdfs/                # Input PDFs
│   ├── outputs/             # Output JSONs (one per PDF)
│   └── schema/              # JSON schema file
└── README.md                # This file
```

---

## 📥 Input

All input PDFs should be placed inside the `/app/input` directory.

> Each PDF must be ≤ 50 pages and will be processed individually.

---

## 📤 Output

Each output JSON will follow this structure:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## 🐳 How to Build & Run (Official Evaluation Format)

### 1. Build Docker Image

```bash
docker build --platform linux/amd64 -t adobe-round1a .
```

### 2. Run the Container

```bash
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs:/app/output \
  --network none \
  adobe-round1a
```

---

## ✅ Key Features

- 🔍 No reliance on font size
- 🧠 True semantic heading classification using BERT
- 📑 Output strictly follows Adobe’s `output_schema.json`
- 🧩 Compatible with AMD64, 8-core CPU, no internet
- 🕐 Processes a 50-page PDF in under 10 seconds

---

## 📌 Constraints Met

| Constraint           | Status       |
|----------------------|--------------|
| CPU-only (AMD64)     | ✅ Yes        |
| Model size ≤ 200MB   | ✅ Yes (DistilBERT ~134MB) |
| Runtime ≤ 10 sec     | ✅ Yes        |
| Offline execution    | ✅ Yes        |
| Schema conformity    | ✅ Yes        |

---

## 🙌 Authors

- Sanjay M & Team  
- Adobe Hackathon 2025 – Round 1A

---

## 📜 License

This project is licensed for use only within the scope of the Adobe India Hackathon 2025. Keep the GitHub repo **private until the final submission date**.
