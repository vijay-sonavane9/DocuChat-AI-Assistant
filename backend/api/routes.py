from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from backend.services import pdf_service, rag_service

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    filename = await pdf_service.save_pdf(file)
    return {"message": "PDF uploaded", "filename": filename}

@router.post("/chat")
async def chat_with_doc(query: str = Form(...)):
    response = rag_service.answer_query(query)
    return JSONResponse(content={"response": response})
