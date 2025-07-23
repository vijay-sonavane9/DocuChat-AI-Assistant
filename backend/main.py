from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    with open(file.filename, "wb") as f:
        f.write(contents)

    # Extract text using PyMuPDF
    text = ""
    with fitz.open(file.filename) as doc:
        for page in doc:
            text += page.get_text()

    return {"text": text}
