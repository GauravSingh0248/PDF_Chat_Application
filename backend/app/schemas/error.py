from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(
        ...,
        title="Error Code",
        description="Machine-readable error code",
        examples=["DOCUMENT_NOT_FOUND"],
    )

    message: str = Field(
        ...,
        title="Error Message",
        description="Human-readable error message",
        examples=["Document not found."],
    )


class ErrorResponse(BaseModel):
    error: ErrorDetail