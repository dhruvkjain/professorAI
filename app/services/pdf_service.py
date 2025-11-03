import re
import pdfplumber
import os


def extract_syllabus_text(pdf_filepath: str) -> str:
    if not os.path.exists(pdf_filepath):
        raise FileNotFoundError(f"File not found: {pdf_filepath}")

    pattern = re.compile(r"syllabus|contents|curriculum|chapters|index|unit", re.IGNORECASE)
    syllabus_pages = []

    with pdfplumber.open(pdf_filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if pattern.search(text):
                syllabus_pages.append(i)

        first_page = syllabus_pages[0] if syllabus_pages else 0
        end_page = first_page + 20
        combined = []

        for pnum in range(first_page, min(end_page, len(pdf.pages))):
            page = pdf.pages[pnum]
            text = page.extract_text() or ""
            combined.append(f"## Page {pnum+1}\n\n{text.strip()}")

    return "\n\n".join(combined)
