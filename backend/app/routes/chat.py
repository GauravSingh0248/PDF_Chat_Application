from fastapi import APIRouter, HTTPException

from app.database.document_repository import get_document
from app.rag.chain import ask_question
from app.schemas.chat import ChatRequest, ChatResponse

from app.core.exceptions import (DocumentNotFoundException,DocumentNotReadyException,)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    document = get_document(request.document_id)

    if document is None:
        raise DocumentNotFoundException()

    if document["status"] != "processed":
        raise DocumentNotReadyException()

    return ask_question(
        question=request.question,
        document_id=request.document_id,
    )



# def chat(request):

#     try:
#         document = get_document(request.document_id)

#         if document is None:
#             raise DocumentNotFoundException()

#     except DocumentNotFoundException:
#         return {
#             "error": "Document not found"
#         }


# @router.post("", response_model=ChatResponse)
# def chat(request: ChatRequest):

#     document = get_document(request.document_id)

#     if document is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Document not found.",
#         )

#     return ask_question(
#         question=request.question,
#         document_id=request.document_id,
#     )



# User
#  ↓
# POST /api/chat
#  ↓
# chat()
#  ↓
# get_document()
#  ↓
# MySQL → None
#  ↓
# raise HTTPException(404)
#  ↓
# FastAPI
#  ↓
# FastAPI's built-in HTTPException handler
#  ↓
# 404 response