from app.services.quiz_service import generate_quiz, submit_quiz
from app.services.quiz_store import quiz_store
from app.schemas.quiz import QuizSubmitRequest


DOCUMENT_ID = "5c6a191d-0597-47e8-b693-5c0e956f2c91"


def main():

    # -----------------------------------------
    # 1. Generate a quiz
    # -----------------------------------------

    generated_quiz = generate_quiz(
        document_id=DOCUMENT_ID,
        number_of_questions=5,
    )

    quiz_id = "test-quiz-123"

    quiz_store[quiz_id] = {
        "document_id": DOCUMENT_ID,
        "questions": generated_quiz.questions,
    }

    print("\nQuiz generated.")
    print("Quiz ID:", quiz_id)

    # -----------------------------------------
    # 2. Create user's answers
    # -----------------------------------------

    answers = {}

    for index, question in enumerate(
        generated_quiz.questions,
        start=1,
    ):
        answers[index] = question.correct_option

    # -----------------------------------------
    # 3. Create QuizSubmitRequest
    # -----------------------------------------

    request = QuizSubmitRequest(
        quiz_id=quiz_id,
        answers=answers,
    )

    # -----------------------------------------
    # 4. Submit quiz
    # -----------------------------------------

    result = submit_quiz(request)

    # -----------------------------------------
    # 5. Display result
    # -----------------------------------------

    print("\n" + "=" * 60)
    print("QUIZ SUBMISSION RESULT")
    print("=" * 60)

    print(f"\nScore: {result.score}/{result.total_questions}")
    print(f"Percentage: {result.percentage}%")

    for item in result.results:

        print("\nQuestion ID:", item.question_id)
        print("Selected option:", item.selected_option)
        print("Correct option:", item.correct_option)
        print("Correct:", item.is_correct)
        print("Explanation:", item.explanation)


if __name__ == "__main__":
    main()