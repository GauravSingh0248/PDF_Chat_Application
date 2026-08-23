from pydantic import BaseModel, Field


class NotesRequest(BaseModel):
    document_id: str = Field(
        ...,
        title="Document ID",
        description="ID of the PDF from which notes should be generated",
        min_length=1,
    )


class NotesResponse(BaseModel):
    document_id: str
    notes: str