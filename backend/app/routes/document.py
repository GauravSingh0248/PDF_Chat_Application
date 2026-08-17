from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.document import DocumentResponse, DocumentListResponse
# from app.services.document_service import process_document
from app.database.document_repository import get_all_documents

from app.services.document_service import (
    process_document,
    remove_document,
)

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


@router.get("", response_model=DocumentListResponse)
def get_documents():
    documents = get_all_documents()

    return DocumentListResponse(
        documents=documents
    )

@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: str):

    document = remove_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )


