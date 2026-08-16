from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        title='User Question',
        min_length=1,
        max_length=2000,
        description="Question asked by the user",
        examples={'Give the Summary of the pdf'}
    )

class Source(BaseModel):
    document: str
    page: int = Field(..., ge=1)


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]