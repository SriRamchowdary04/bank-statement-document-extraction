from app.extractors.native_text import extract_native_text
from app.validators import looks_like_bank_statement

pdfs = [
    "data/input/01_native_bank_statement.pdf",
    "data/input/07_not_a_bank_statement.pdf",
]

for pdf_path in pdfs:

    print("\n" + "=" * 60)
    print("FILE:", pdf_path)
    print("=" * 60)

    text = extract_native_text(pdf_path)

    result = looks_like_bank_statement(text)

    print("Bank statement:", result)
