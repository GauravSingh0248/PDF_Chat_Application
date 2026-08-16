from app.rag.retriever import get_retriever


retriever = get_retriever(k=2)

question = "Different Types of Component Learning?"

results = retriever.invoke(question)

print(f"Number of results: {len(results)}")

for i, document in enumerate(results):
    print("\n==============================")
    print(f"Result {i + 1}")
    print("==============================")

    print("Page:", document.metadata.get("page"))
    print("Source:", document.metadata.get("source"))

    print("\nContent:")
    print(document.page_content)