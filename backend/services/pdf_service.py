import os
import shutil

PDF_DIR = "data"

def get_pdf_path(filename):
    return os.path.join(PDF_DIR, filename)

async def save_pdf(file):
    os.makedirs(PDF_DIR, exist_ok=True)
    file_path = get_pdf_path(file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file.filename
