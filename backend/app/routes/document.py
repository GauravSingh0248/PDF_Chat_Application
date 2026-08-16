from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.document import DocumentResponse
from app.services.document_service import process_document


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    return process_document(file)