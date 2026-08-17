from langchain_chroma import Chroma
from app.rag.embeddings import get_embedding_model
from app.rag.retriever import get_vector_store


CHROMA_PATH = "data/chroma"


def create_vector_store(chunks):
    """
    Create a Chroma vector store from document chunks.
    """

    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="pdf_documents",
    )

    return vector_store

def delete_document(document_id: str):
    """Delete all Chroma chunks belonging to a document."""

    vector_store = get_vector_store()

    vector_store._collection.delete(
        where={
            "document_id": document_id
        }
    )