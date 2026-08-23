from pydantic import BaseModel
from typing import Literal


class FAQSource(BaseModel):
    type: Literal["pdf", "web"]
    title: str
    url: str | None = None
    page: int | None = None


class FAQItem(BaseModel):
    question: str
    answer: str
    sources: list[FAQSource]


class FAQResponse(BaseModel):
    pdf_faqs: list[FAQItem]