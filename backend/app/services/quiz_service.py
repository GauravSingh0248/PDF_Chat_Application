from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag.prompt import QUIZ_PROMPT
from app.rag.retriever import get_document_chunks
from app.schemas.quiz import GeneratedQuiz
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



