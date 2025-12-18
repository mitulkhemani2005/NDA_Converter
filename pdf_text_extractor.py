import fitz  # PyMuPDF

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_blocks = []

    for page_index, page in enumerate(doc):
        blocks = page.get_text("blocks")
        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            if text.strip():
                extracted_blocks.append({
                    "page": page_index,
                    "bbox": (x0, y0, x1, y1),
                    "text": text.strip()
                })

    return extracted_blocks
