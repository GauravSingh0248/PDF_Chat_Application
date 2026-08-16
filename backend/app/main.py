from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.document import router as document_router


app = FastAPI(
    title="PDF Chat API",
    description="RAG-based PDF chat application",
    version="1.0.0",
)

app.include_router(chat_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {
        "message": "Gaurav Portfolio API is running 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }