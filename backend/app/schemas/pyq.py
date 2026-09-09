from typing import List, Optional
from typing import Literal
from pydantic import BaseModel, Field


class PYQAnalysisRequest(BaseModel):
    document_ids: List[str] = Field(
        ...,
        min_length=2,
        description=(
            "IDs of multiple previous-year question papers "
            "(e.g. OS 2025, 2024, 2023). At least 2 papers required."
        ),
    )

    subject: Optional[str] = Field(
        default=None,
        description="Optional subject label, e.g. Operating System",
        max_length=120,
    )

# creating Outputt model
class TopicAnalysis(BaseModel):
    topic: str
    frequency: int = Field(
        ...,
        ge=1,
        description="How many times this topic appears across all papers",
    )
    years_appeared: List[str] = Field(
        ...,
        description="Paper filenames/years where this topic appeared",
    )
    importance: Literal["High", "Medium", "Low"]
    reason: str


class RepeatedQuestion(BaseModel):
    question: str = Field(
        ...,
        description="Canonical form of a question that repeats across years",
    )
    frequency: int = Field(
        ...,
        ge=1,
        description="Number of papers where this question (or near-identical) appears",
    )
    years_appeared: List[str]
    topic: str


class SimilarQuestionGroup(BaseModel):
    representative_question: str
    similar_variants: List[str] = Field(
        ...,
        description="Wording variants of the same underlying question",
    )
    frequency: int = Field(..., ge=1)
    years_appeared: List[str]
    topic: str


class PYQAnalysis(BaseModel):
    subject: Optional[str] = None
    papers_analyzed: List[str] = Field(
        ...,
        description="Filenames of the PYQ PDFs used in this analysis",
    )
    topics: List[TopicAnalysis]
    repeated_questions: List[RepeatedQuestion]
    similar_questions: List[SimilarQuestionGroup]
    important_topics: List[str]
    exam_focus_summary: str = Field(
        ...,
        description="Short summary of what the exam tends to focus on",
    )


# optional - whether it is present or absent doesn;t matter 