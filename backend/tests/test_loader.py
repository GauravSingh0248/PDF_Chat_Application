from app.rag.loader import load_pdf

pdf_path = "data/uploads/Machine_Learning.pdf"
documents = load_pdf(pdf_path)

print(f"Number of pages: {len(documents)}")

for document in documents[:3]:
    print("\n--------------------")
    print("Page:", document.metadata.get("page"))
    print("Source:", document.metadata.get("source"))
    print("Content:")
    print(document.page_content[:500])