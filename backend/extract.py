import pdfplumber, io
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract

def extract_text_pdf(file_bytes):
    """Extract text from PDF. Try pdfplumber first, else OCR with Tesseract."""
    full_text, per_page = "", []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                per_page.append(text)
                full_text += text + "\n"
    except:
        pass

    # fallback OCR if text too short
    if len(full_text.strip()) < 20:
        ocr_texts = []
        try:
            images = convert_from_bytes(file_bytes)
            for im in images:
                text = pytesseract.image_to_string(im)
                ocr_texts.append(text)
            full_text = "\n".join(ocr_texts)
            per_page = ocr_texts
        except:
            pass
    return full_text, per_page
