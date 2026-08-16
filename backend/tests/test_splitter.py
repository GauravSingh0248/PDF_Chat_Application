from app.rag.loader import load_pdf
from app.rag.splitter import split_documents


pdf_path = "data/uploads/Machine_Learning.pdf"

documents = load_pdf(pdf_path)

chunks = split_documents(documents)

print(f"Number of pages: {len(documents)}")
print(f"Number of chunks: {len(chunks)}")

# for i, chunk in enumerate(chunks[:5]):
#     print("\n==============================")
#     print(f"Chunk {i + 1}")
#     print("==============================")
#     print("Content:", chunk.page_content[:500])
#     print("Metadata:", chunk.metadata)


for i, chunk in enumerate(chunks[:5]):
    print(f"Chunk {i + 1}")
    print("Length:", len(chunk.page_content))
    print("Content:", chunk.page_content)
    print("Page:", chunk.metadata.get("page"))
    print()