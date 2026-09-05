from langchain_groq import ChatGroq

from app.rag.pyq_prompt import PYQ_PROMPT
from app.rag.retriever import get_document_chunks
from app.schemas.pyq import PYQAnalysis


def analyze_pyq(document_id: str) -> PYQAnalysis:

    result = get_document_chunks(document_id)

    documents = result["documents"]

    if not documents:
        raise ValueError("No content found for this document.")

    context = "\n\n".join(documents)

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
    )

    structured_llm = llm.with_structured_output(PYQAnalysis)

    prompt = PYQ_PROMPT.invoke({
        "context": context
    })

    response = structured_llm.invoke(prompt)

    return response