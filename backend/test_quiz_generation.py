from app.services.quiz_service import generate_quiz


DOCUMENT_ID = "xxxxxx"


def main():
    number_of_questions = 5

    quiz = generate_quiz(
        document_id=DOCUMENT_ID,
        number_of_questions=number_of_questions,
    )

    print("\n" + "=" * 60)
    print("QUIZ GENERATED SUCCESSFULLY")
    print("=" * 60)

    print(f"\nNumber of questions: {len(quiz.questions)}")

    for question in quiz.questions:

        print(f"\nQuestion: {question.question}")
        print("-" * 60)

        for index, option in enumerate(question.options):
            print(f"{index}. {option}")

        print(f"\nCorrect option: {question.correct_option}")
        print(f"Explanation: {question.explanation}")


if __name__ == "__main__":
    main()