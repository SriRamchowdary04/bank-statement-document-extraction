from pypdf import PdfReader

def extract_native_text(path: str) -> str:
    reader = PdfReader(path)
    chunks = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"\n--- PAGE {i} ---\n{text}")
    return "\n".join(chunks).strip()
