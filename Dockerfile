FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY process_pdfs.py .

RUN apt-get update && apt-get install -y gcc libgl1 libglib2.0-0
RUN pip install --no-cache-dir torch transformers PyMuPDF spacy
RUN python -m spacy download en_core_web_sm
RUN python -c "from transformers import AutoModelForSequenceClassification, AutoTokenizer; AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased'); AutoTokenizer.from_pretrained('distilbert-base-uncased')"

CMD ["python", "process_pdfs.py"]
