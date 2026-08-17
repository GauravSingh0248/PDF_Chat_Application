from fastapi import APIRouter, HTTPException

from app.database.document_repository import get_document
from app.rag.chain import ask_question
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    document = get_document(request.document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    if document["status"] != "processed":
        raise HTTPException(
            status_code=409,
            detail="Document is not ready for chat.",
        )

    return ask_question(
        question=request.question,
        document_id=request.document_id,
    )