from pathlib import Path
from uuid import uuid4

from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vector_store import create_vector_store


UPLOAD_DIR = Path("data/uploads")


def process_document(file):
    """
    Save and process an uploaded PDF.
    """

    document_id = str(uuid4())

    filename = Path(file.filename).name
    file_path = UPLOAD_DIR / f"{document_id}_{filename}"

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    documents = load_pdf(str(file_path))
    for document in documents:
        document.metadata["document_id"] = document_id

    chunks = split_documents(documents)

    create_vector_store(chunks)

    return {
        "document_id": document_id,
        "filename": filename,
        "status": "processed",
    }