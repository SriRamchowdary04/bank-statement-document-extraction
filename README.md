# Document Extraction POC

A small document-extraction pipeline built around the requirements in the supplied POC brief.

## Scope

The pipeline:
1. Detects whether a PDF is native-text or image-based.
2. Routes native PDFs to direct text extraction.
3. Routes image PDFs to OCR/vision extraction.
4. Detects password-protected PDFs and stops safely.
5. Detects merged statements and treats them as separate statement documents.
6. Rejects documents that are not bank statements.
7. Sends normalized document content to multiple LLM adapters.
8. Produces one JSON result per document/model combination.
9. Records routing and comparison metadata.

## Project layout

```text
document_extraction_poc/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── detector.py
│   ├── pipeline.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── validators.py
│   ├── extractors/
│   │   ├── native_text.py
│   │   └── ocr.py
│   └── llm/
│       ├── base.py
│       ├── openai_adapter.py
│       ├── anthropic_adapter.py
│       └── gemini_adapter.py
├── data/
│   ├── input/
│   └── output/
├── tests/
├── requirements.txt
├── .env.example
└── run.py
```

## Setup

Python 3.10+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

For OCR, install the Tesseract executable separately if you want OCR fallback:

- macOS: `brew install tesseract`
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- Windows: install Tesseract and add it to PATH.

Copy `.env.example` to `.env` and add whichever provider keys you want.

## Run

Put PDFs in:

```text
data/input/
```

Then:

```bash
python run.py
```

Results are written to:

```text
data/output/
```

Each result follows the requested top-level shape:

```json
{
  "detected_format": "native_text",
  "model": "openai",
  "document_status": "extracted",
  "transactions": [
    {
      "date": "2026-01-05",
      "description": "ATM Withdrawal",
      "amount": -100.00,
      "running_balance": 2400.00
    }
  ]
}
```

If a document cannot be processed:

```json
{
  "detected_format": "image_based",
  "model": "openai",
  "document_status": "could_not_process",
  "reason": "Password-protected PDF. Password required."
}
```

## Important

The seven employer documents were not supplied, so this repository is designed to run against local test PDFs. Do not represent synthetic test results as results from the employer's files.
