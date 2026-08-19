import uuid

from fastapi import APIRouter

from app.schemas.quiz import QuizRequest, QuizResponse, QuizQuestion, QuizSubmitResponse, QuizSubmitRequest
from app.services.quiz_service import generate_quiz,submit_quiz
from app.services.quiz_store import quiz_store


router = APIRouter(
    prefix="/api/quiz",
    tags=["Quiz"],
)


@router.post("",response_model=QuizResponse,)
def create_quiz(request: QuizRequest):

    generated_quiz = generate_quiz(
        document_id=request.document_id,
        number_of_questions=request.number_of_questions,
    )

    quiz_id = str(uuid.uuid4())

    questions = []

    for index, generated_question in enumerate(generated_quiz.questions,start=1,):
        questions.append(
            QuizQuestion(
                id=index,
                question=generated_question.question,
                options=generated_question.options,
            )
        )

    quiz_store[quiz_id] = {
        "document_id": request.document_id,
        "questions": generated_quiz.questions,
    }

    return QuizResponse(
        quiz_id=quiz_id,
        document_id=request.document_id,
        questions=questions,
    )


@router.post("/submit",response_model=QuizSubmitResponse,)
def submit_quiz_route(request: QuizSubmitRequest):

    return submit_quiz(request)