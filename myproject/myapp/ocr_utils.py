"""
OCR utility module - extracted from ocr.ipynb
Handles image/PDF OCR processing using Tesseract
"""
from pathlib import Path
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


# Tesseract configuration
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if Path(TESSERACT_CMD).exists():
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Poppler path for PDF to image conversion
POPPLER_PATH = r"C:\Users\tsheikh\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
if POPPLER_PATH and not Path(POPPLER_PATH).exists():
    POPPLER_PATH = None


def assert_tesseract_available():
    """Raise a helpful error if Tesseract is missing."""
    cmd = Path(pytesseract.pytesseract.tesseract_cmd or "tesseract")
    if not cmd.exists() and cmd.name == "tesseract":
        raise FileNotFoundError(
            "Tesseract not found. Install it and/or set TESSERACT_CMD to the exe path."
        )
    if cmd.exists():
        return
    raise FileNotFoundError(f"Tesseract binary not found at: {cmd}")


def load_image(path):
    """Load an image from file path"""
    img_path = Path(path)
    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")
    image = cv2.imread(str(img_path))
    if image is None:
        raise ValueError(f"Failed to read image: {img_path}")
    return image


def preprocess_image(image):
    """Lightweight cleanup tuned for filled forms"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=15)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15
    )
    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.dilate(thresh, kernel, iterations=1)
    return processed


def load_document_pages(path):
    """Load document pages - handles both images and PDFs"""
    doc_path = Path(path)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document not found: {doc_path}")

    if doc_path.suffix.lower() == ".pdf":
        pil_pages = convert_from_path(doc_path, poppler_path=POPPLER_PATH)
        pages = []
        for pil_img in pil_pages:
            rgb = np.array(pil_img)
            bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            pages.append(bgr)
        return pages

    return [load_image(str(doc_path))]


def run_ocr_on_image(image, lang="eng", psm=6, oem=3, extra_config=None):
    """Run OCR on a single image"""
    assert_tesseract_available()
    preprocessed = preprocess_image(image)

    config_parts = [f"--psm {psm}", f"--oem {oem}"]
    if extra_config:
        config_parts.append(extra_config)
    config = " ".join(config_parts)

    text = pytesseract.image_to_string(preprocessed, lang=lang, config=config)
    data = pytesseract.image_to_data(
        preprocessed, lang=lang, config=config, output_type=pytesseract.Output.DICT
    )

    return {
        "text": text.strip(),
        "raw_data": data,
        "config_used": config,
    }


def extract_text(image_path, lang="eng", psm=6, oem=3, extra_config=None):
    """OCR for a single image file"""
    image = load_image(image_path)
    return run_ocr_on_image(image, lang=lang, psm=psm, oem=oem, extra_config=extra_config)


def extract_text_document(doc_path, lang="eng", psm=6, oem=3, extra_config=None):
    """OCR for PDFs or images. Returns per-page results and combined text."""
    pages = load_document_pages(doc_path)
    results = []
    for idx, page in enumerate(pages, start=1):
        page_result = run_ocr_on_image(page, lang=lang, psm=psm, oem=oem, extra_config=extra_config)
        results.append({"page": idx, **page_result})

    combined_text = "\n\n".join(r["text"] for r in results)
    return {"pages": results, "combined_text": combined_text, "page_count": len(pages)}
