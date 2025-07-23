# backend/pdf_loader.py
import os
import fitz  # PyMuPDF

def load_pdfs_from_folder(folder_path):
    all_text = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            text = extract_text_from_pdf(file_path)
            all_text.append(text)
    return all_text

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()
