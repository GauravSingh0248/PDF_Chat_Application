from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag.prompt import QUIZ_PROMPT
from app.rag.retriever import get_document_chunks
from app.schemas.quiz import GeneratedQuiz, QuizSubmitRequest, QuizResult, QuizSubmitResponse
from app.core.exceptions import QuizNotFoundException,InvalidQuizQuestionException
from app.services.quiz_store import quiz_store

    # Get context from a specific PDF for quiz generation.

# max_chunk size is reduced to 3 cause of model we have right now 
def get_quiz_context(document_id: str, max_chunks: int = 3):
    """Get context from a specific PDF for quiz generation."""

    result = get_document_chunks(document_id)

    documents = result["documents"]

    if not documents:
        return ""

    documents = documents[:max_chunks]

    context = "\n\n".join(documents)

    return context


def generate_quiz(document_id: str, number_of_questions: int):

    context = get_quiz_context(document_id)

    if not context:
        raise ValueError("No content found for this document.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
    )

    structured_llm = llm.with_structured_output(
        GeneratedQuiz
    )

    prompt = QUIZ_PROMPT.invoke(
        {
            "number_of_questions": number_of_questions,
            "context": context,
        }
    )

    quiz = structured_llm.invoke(prompt)

    return quiz



def submit_quiz(request: QuizSubmitRequest) -> QuizSubmitResponse:

    quiz = quiz_store.get(request.quiz_id)

    if not quiz:
        raise QuizNotFoundException(request.quiz_id)
    score = 0
    results = []

    for question_id, selected_option in request.answers.items():

        question_index = question_id - 1

        if question_index < 0 or question_index >= len(quiz["questions"]):
            raise InvalidQuizQuestionException(question_id)

        question = quiz["questions"][question_index]

        is_correct = (
            selected_option == question.correct_option
        )

        if is_correct:
            score += 1

        results.append(
            QuizResult(
                question_id=question_id,
                selected_option=selected_option,
                correct_option=question.correct_option,
                is_correct=is_correct,
                explanation=question.explanation,
            )
        )

    total_questions = len(quiz["questions"])

    percentage = (
        (score / total_questions) * 100
        if total_questions > 0
        else 0
    )

    return QuizSubmitResponse(
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        results=results,
    )


