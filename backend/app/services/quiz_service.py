from app.rag.retriever import get_retriever


def generate_quiz(document_id: str, number_of_questions: int):


    retriever = get_retriever(document_id)

    documents = retriever.invoke(
        "Generate important questions from this document"
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context