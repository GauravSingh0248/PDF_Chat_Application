from pydantic import BaseModel
from typing import List


class TopicAnalysis(BaseModel):
    topic: str
    frequency: int
    importance: str
    reason: str


class RepeatedQuestion(BaseModel):
    question: str
    frequency: int
    topic: str


class PYQAnalysis(BaseModel):
    topics: List[TopicAnalysis]
    repeated_questions: List[RepeatedQuestion]
    important_topics: List[str]