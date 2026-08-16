from langchain_chroma import Chroma
from app.rag.embeddings import get_embedding_model


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