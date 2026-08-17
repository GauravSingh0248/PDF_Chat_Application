from pathlib import Path
from uuid import uuid4

from app.database.document_repository import (
    create_document,
    update_document_status,
)
from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vector_store import create_vector_store

from app.database.document_repository import (
    delete_document as delete_document_record,
    get_document,
)

from app.rag.vector_store import delete_document as delete_document_vectors

UPLOAD_DIR = Path("data/uploads")


def process_document(file):
    document_id = str(uuid4())

    filename = Path(file.filename).name
    file_path = UPLOAD_DIR / f"{document_id}_{filename}"

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Register document in MySQL
    create_document(
        document_id=document_id,
        filename=filename,
        file_path=str(file_path),
        status="processing",
    )

    try:
        # Load PDF
        documents = load_pdf(str(file_path))

        # Attach document ID to metadata
        for document in documents:
            document.metadata["document_id"] = document_id

        # Split into chunks
        chunks = split_documents(documents)

        # Create embeddings + store in Chroma
        create_vector_store(chunks)

        # Processing successful
        update_document_status(
            document_id=document_id,
            status="processed",
        )

        # return {
        #     "document_id": document_id,
        #     "filename": filename,
        #     "status": "processed",
        # }
        return get_document(document_id)

    except Exception:
        # Processing failed
        update_document_status(
            document_id=document_id,
            status="failed",
        )

        raise

def remove_document(document_id: str):
    """Remove a document and all associated data."""

    document = get_document(document_id)

    if document is None:
        return None

    file_path = Path(document["file_path"])

    # Delete vectors from Chroma
    delete_document_vectors(document_id)

    # Delete the actual PDF
    if file_path.exists():
        file_path.unlink()

    # Delete database record
    delete_document_record(document_id)

    return document