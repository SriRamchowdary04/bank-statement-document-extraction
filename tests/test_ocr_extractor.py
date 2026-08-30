from app.extractors.ocr import extract_ocr_text


pdfs = [
    "data/input/02_image_only_statement.pdf",
    "data/input/03_scanned_statement.pdf",
    "data/input/04_photocopy_statement.pdf",
]


for pdf_path in pdfs:

    print("\n")
    print("=" * 70)
    print("FILE:", pdf_path)
    print("=" * 70)

    try:

        text = extract_ocr_text(pdf_path)

        print(text)

        print("\nCharacters extracted:", len(text))

    except Exception as e:

        print("OCR FAILED")
        print(type(e).__name__, ":", e)