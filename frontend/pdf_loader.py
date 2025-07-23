# pdf_loader.py
import os
import PyPDF2


def load_pdf_text(path, single_file=False):
    text = ""
    if single_file:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    else:
        for filename in os.listdir(path):
            if filename.endswith(".pdf"):
                with open(os.path.join(path, filename), "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text()
    return text

