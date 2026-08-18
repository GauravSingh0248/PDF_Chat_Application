from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    document_id: str = Field(
        ...,
        title="Document ID",
        description="ID of the PDF from which the quiz should be generated",
        min_length=1,
    )

    number_of_questions: int = Field(
        ...,
        title="Number of Questions",
        description="Number of MCQ questions to generate",
        ge=1,
        le=20,
    )


class QuizQuestion(BaseModel):
    id: int = Field(
        ...,
        description="Question number",
        ge=1,
    )

    question: str = Field(
        ...,
        title="Question",
        min_length=1,
    )

    options: list[str] = Field(
        ...,
        title="Options",
        min_length=4,
        max_length=4,
        description="Four options for the MCQ",
    )


class QuizResponse(BaseModel):
    quiz_id: str
    document_id: str
    questions: list[QuizQuestion]


class QuizSubmitRequest(BaseModel):
    quiz_id: str
    answers: dict[int, int]


class QuizResult(BaseModel):
    question_id: int
    selected_option: int
    correct_option: int
    is_correct: bool
    explanation: str


class QuizSubmitResponse(BaseModel):
    score: int
    total_questions: int
    percentage: float
    results: list[QuizResult]




# ... this field is required 










# thiss is the flow diagram --

# Operation 1 — Generate Quiz


            # Frontend
            # ↓
            # QuizRequest
            # ↓
            # Backend
            # ↓
            # QuizResponse
            # ↓
            # Frontend


# ------------------------------------------------------

# Operation 2 — Submit Quiz

#             Frontend
#    ↓
#             QuizSubmitRequest
#             ↓
#             Backend checks answers
#             ↓
#             QuizSubmitResponse
#             ↓
#             Frontend

# | Schema               | Simple meaning                         |
# | -------------------- | -------------------------------------- |
# | `QuizRequest`        | **I want a quiz from this PDF**        |
# | `QuizQuestion`       | **This is one question**               |
# | `QuizResponse`       | **Here is your quiz**                  |
# | `QuizSubmitRequest`  | **Here are my answers**                |
# | `QuizResult`         | **Here is the result of one question** |
# | `QuizSubmitResponse` | **Here is your complete score/result** |
