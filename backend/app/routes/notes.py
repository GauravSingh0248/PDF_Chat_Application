from fastapi import APIRouter, HTTPException

from app.schemas.notes import NotesRequest, NotesResponse
from app.services.notes_service import generate_notes


router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"],
)


@router.post("", response_model=NotesResponse)
def create_notes(request: NotesRequest):
    try:
        notes = generate_notes(request.document_id)

        return NotesResponse(
            document_id=request.document_id,
            notes=notes,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )