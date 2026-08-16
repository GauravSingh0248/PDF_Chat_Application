from fastapi import APIRouter

from app.rag.chain import ask_question
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    return ask_question(
        question=request.question,
        document_id=request.document_id,
    )