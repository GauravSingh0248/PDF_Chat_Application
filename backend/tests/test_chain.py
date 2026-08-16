from app.rag.chain import ask_question


# question = "Different Types of Component Learning?"
question = "Application of Machine Learning?"

result = ask_question(question)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")

for document in result["sources"]:
    print(
        f"Page: {document.metadata.get('page')}, "
        f"Source: {document.metadata.get('source')}"
    )