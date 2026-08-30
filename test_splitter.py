from app.extractors.native_text import extract_native_text
from app.validators import split_merged_statements

pdf_path = "data/input/05_merged_statements.pdf"

text = extract_native_text(pdf_path)

print("=" * 70)
print("ORIGINAL DOCUMENT")
print("=" * 70)

print(text)

statements = split_merged_statements(text)

print("\n")
print("=" * 70)
print("NUMBER OF STATEMENTS FOUND:", len(statements))
print("=" * 70)

for index, statement in enumerate(statements, start=1):

    print("\n")
    print("-" * 70)
    print("STATEMENT", index)
    print("-" * 70)

    print(statement)
