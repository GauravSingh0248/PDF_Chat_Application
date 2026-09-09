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


def get_document_chunks(document_id: str):
    """Load all stored chunks for one document."""

    vector_store = get_vector_store()

    result = vector_store._collection.get(
        where={
            "document_id": document_id
        },
        include=["documents", "metadatas"],
    )

    return result


def get_documents_chunks(document_ids: list[str]):
    """Load all stored chunks for multiple documents."""

    if not document_ids:
        return {
            "ids": [],
            "documents": [],
            "metadatas": [],
        }

    vector_store = get_vector_store()

    result = vector_store._collection.get(
        where={
            "document_id": {
                "$in": document_ids
            }
        },
        include=["documents", "metadatas"],
    )

    return result