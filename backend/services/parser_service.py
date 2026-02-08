import os
import pdfplumber
from docx import Document


def extract_text_from_pdf(path: str) -> str:
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts).strip()


def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def load_resume_text(resume_path: str) -> str:
    if not os.path.exists(resume_path):
        raise FileNotFoundError(f"Resume not found: {resume_path}")

    ext = resume_path.lower().split(".")[-1]

    if ext == "pdf":
        return extract_text_from_pdf(resume_path)
    elif ext == "docx":
        return extract_text_from_docx(resume_path)
    else:
        raise ValueError("Resume must be PDF or DOCX")
