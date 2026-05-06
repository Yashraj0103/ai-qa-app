import PyPDF2
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page_num, page in enumerate(pdf_reader.pages):
        text += f"\n[Page {page_num + 1}]\n"
        text += page.extract_text() or ""
    return text