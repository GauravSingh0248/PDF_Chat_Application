import json

from app.rag.faq_prompt import FAQ_PROMPT
from app.rag.retriever import get_document_chunks, get_retriever
from langchain_groq import ChatGroq


def generate_pdf_faqs(document_id: str):

    result = get_document_chunks(document_id)

    documents = result["documents"]

    if not documents:
        raise ValueError("No content found for this document.")

    context_parts = []

    for index, document in enumerate(documents):

        metadata = (
            result["metadatas"][index]
            if index < len(result.get("metadatas", []))
            else {}
        )

        page = metadata.get("page_label", "Unknown")

        context_parts.append(
            f"""
SOURCE:
Page: {page}

CONTENT:
{document}
"""
        )

    context = "\n\n".join(context_parts)

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
    )

    prompt = FAQ_PROMPT.invoke({
        "context": context
    })

    response = llm.invoke(prompt)

    try:
        faq_data = json.loads(response.content)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"LLM returned invalid JSON: {error}\n\n"
            f"Response:\n{response.content}"
        )

    retriever = get_retriever(
        document_id=document_id,
        k=1,
    )

    for faq in faq_data.get("pdf_faqs", []):

        question = faq["question"]

        relevant_documents = retriever.invoke(question)

        if not relevant_documents:
            faq["sources"] = []
            continue

        relevant_document = relevant_documents[0]

        metadata = relevant_document.metadata

        page_label = metadata.get("page_label")

        title = metadata.get(
            "title",
            "PDF Document"
        )

        faq["sources"] = [
            {
                "type": "pdf",
                "title": title,
                "url": None,
                "page": int(page_label)
                if page_label is not None
                else None,
            }
        ]

    return faq_data