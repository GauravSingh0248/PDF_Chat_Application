from pathlib import Path
from uuid import uuid4

from app.database.document_repository import (
    create_document,
    update_document_status,
)
from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vector_store import create_vector_store


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

        return {
            "document_id": document_id,
            "filename": filename,
            "status": "processed",
        }

    except Exception:
        # Processing failed
        update_document_status(
            document_id=document_id,
            status="failed",
        )

        raise