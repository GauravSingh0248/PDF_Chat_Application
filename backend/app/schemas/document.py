from datetime import datetime

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    document_id: str = Field(
        ...,
        title="Document ID",
        description="Unique identifier of the uploaded PDF",
        examples=["fbc121"],
        min_length=1,
    )

    filename: str = Field(
        ...,
        title="Filename",
        description="Original name of the uploaded PDF",
        examples=["abc.pdf"],
        min_length=1,
    )

    status: str = Field(
        ...,
        title="Processing Status",
        description="Current processing status of the document",
        examples=["processed"],
        min_length=1,
    )

    created_at: datetime = Field(
        ...,
        title="Created At",
        description="Date and time when the document was uploaded",
    )


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]