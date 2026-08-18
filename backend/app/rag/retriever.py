from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model


CHROMA_PATH = "data/chroma"


def get_vector_store():
    """Load the existing Chroma vector store."""

    embeddings = get_embedding_model()

    vector_store = Chroma(
        collection_name="pdf_documents",
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )

    return vector_store


def get_retriever(document_id: str, k: int = 4):
    """Create a retriever for a specific document."""

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": {
                "document_id": document_id
            },
        },
    )

    return retriever
