from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vector_store import create_vector_store


pdf_path = "data/uploads/Machine_Learning.pdf"


# 1. Load PDF
documents = load_pdf(pdf_path)

print(f"Pages loaded: {len(documents)}")


# 2. Split documents
chunks = split_documents(documents)

print(f"Chunks created: {len(chunks)}")


# 3. Create vector store
vector_store = create_vector_store(chunks)

print("Vector store created successfully!")