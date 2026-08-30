from app.extractors.native_text import extract_native_text


pdf_path = "data/input/01_native_bank_statement.pdf"

text = extract_native_text(pdf_path)

print("=" * 60)
print("EXTRACTED TEXT")
print("=" * 60)

print(text)

print("=" * 60)
print("TOTAL CHARACTERS:", len(text))
print("=" * 60)