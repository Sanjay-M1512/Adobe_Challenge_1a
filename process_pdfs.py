import os
import json
from pathlib import Path
import fitz  # PyMuPDF
import spacy
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Load models once
nlp = spacy.load("en_core_web_sm")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
model.eval()  # Evaluation mode

# Threshold for calling something a heading (tune this)
HEADING_CONFIDENCE_THRESHOLD = 0.9

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            full_text = ""
            for line in block["lines"]:
                for span in line["spans"]:
                    full_text += span["text"].strip() + " "
            if full_text.strip():
                blocks.append({
                    "text": full_text.strip(),
                    "page": page_num
                })
    return blocks

def is_potential_heading(text):
    """Use spaCy to filter out bad candidates like paragraphs."""
    if len(text) > 150 or len(text.split()) > 15:
        return False
    doc = nlp(text)
    # Must contain at least one noun or verb
    return any(tok.pos_ in ("NOUN", "PROPN", "VERB") for tok in doc)

def is_heading_with_bert(text):
    """Use DistilBERT to classify if a text block is a heading."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        heading_prob = probs[0][1].item()  # Assuming label 1 = heading

    return heading_prob > HEADING_CONFIDENCE_THRESHOLD, heading_prob

def assign_heading_levels(heading_blocks):
    """Simple rule: first few = H1, next = H2, fallback = H3"""
    result = []
    for i, block in enumerate(heading_blocks):
        if i == 0:
            level = "H1"
        elif i == 1:
            level = "H2"
        else:
            level = "H3"
        result.append({
            "level": level,
            "text": block["text"],
            "page": block["page"]
        })
    return result

def classify_headings(blocks):
    headings = []
    title = ""

    for i, block in enumerate(blocks):
        text = block["text"]
        page = block["page"]

        if not is_potential_heading(text):
            continue

        is_heading, prob = is_heading_with_bert(text)
        if is_heading:
            headings.append({
                "text": text,
                "page": page,
                "confidence": prob
            })

    # Sort by confidence descending
    headings.sort(key=lambda x: x["confidence"], reverse=True)

    if headings:
        title = headings[0]["text"]
        structured_headings = assign_heading_levels(headings[1:])
    else:
        structured_headings = []

    return {
        "title": title,
        "outline": structured_headings
    }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        print(f"[INFO] Processing {pdf_file.name}...")
        blocks = extract_text_blocks(pdf_file)
        structured = classify_headings(blocks)

        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structured, f, indent=2)
        print(f"[DONE] {pdf_file.name} -> {output_file.name}")

if __name__ == "__main__":
    print("🚀 Starting PDF heading extraction...")
    process_pdfs()
    print("✅ Done.")
