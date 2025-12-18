import fitz  # PyMuPDF

def get_pdf_info(pdf_path):
    doc = fitz.open(pdf_path)
    return {
        "page_count": doc.page_count,
        "is_encrypted": doc.is_encrypted
    }