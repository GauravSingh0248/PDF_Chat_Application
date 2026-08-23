from app.rag.notes_prompt import NOTES_PROMPT
from app.rag.retriever import get_document_chunks
from langchain_groq import ChatGroq


def generate_notes(document_id: str):

    result = get_document_chunks(document_id)

    documents = result["documents"]

    if not documents:
        raise ValueError("No content found for this document.")

    context = "\n\n".join(documents)

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
    )

    prompt = NOTES_PROMPT.invoke({
        "context": context
    })

    response = llm.invoke(prompt)

    return response.content