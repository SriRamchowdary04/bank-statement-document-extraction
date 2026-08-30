from pathlib import Path
from app.detector import inspect_pdf

input_dir = Path("data/input")

for pdf in sorted(input_dir.glob("*.pdf")):
    result = inspect_pdf(str(pdf))

    print("\n" + "=" * 50)
    print(pdf.name)
    print("=" * 50)

    print("Status:", result["status"])
    print("Format:", result["detected_format"])
    print("Pages:", result["page_count"])
    print("Text characters:", result["text_chars"])
    print("Pages with text:", result.get("pages_with_text"))