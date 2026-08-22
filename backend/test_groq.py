from dotenv import load_dotenv

from app.rag.groq.notes_chain import get_notes_chain


load_dotenv()


document_id = "YOUR_DOCUMENT_ID"


retriever, llm = get_notes_chain(document_id)


print("Retriever:", retriever)
print("LLM:", llm)


# Test retrieval
documents = retriever.invoke("Neural Networks")


print("\n========== RETRIEVED DOCUMENTS ==========\n")

for document in documents:
    print("CONTENT:")
    print(document.page_content)

    print("\nMETADATA:")
    print(document.metadata)

    print("\n" + "=" * 80)


# Test Groq
response = llm.invoke(
    "Explain what a neural network is in one sentence."
)


print("\n========== GROQ RESPONSE ==========\n")
print(response.content)