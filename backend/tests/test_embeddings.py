from app.rag.embeddings import get_embedding_model


embedding_model = get_embedding_model()

text = "Gradient descent is an optimization algorithm."

vector = embedding_model.embed_query(text)

print("Vector type:", type(vector))
print("Vector length:", len(vector))
print("First 10 values:", vector[:10])