from langchain_google_genai import ChatGoogleGenerativeAI

from app.rag.prompt import RAG_PROMPT
from app.rag.retriever import get_retriever


# validation import 
from app.schemas.chat import ChatResponse, Source

def get_rag_chain(document_id: str):
    retriever = get_retriever(
        document_id=document_id,
        k=4,
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
    )

    return retriever, llm

def ask_question(question: str, document_id: str,)-> ChatResponse:
    retriever, llm = get_rag_chain(document_id)

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    response = llm.invoke(prompt)

    # return {
    #     "answer": response.content[0]["text"],
    #     "sources": documents,
    # }
    sources = []

    for document in documents:
        page = document.metadata.get("page")

        if page is not None:
            sources.append(
                Source(
                    document=document.metadata.get(
                        "source",
                        "Unknown"
                    ),
                    page=page + 1,
                )
            )

    return ChatResponse(
        answer=response.content[0]["text"],
        sources=sources,
    )
