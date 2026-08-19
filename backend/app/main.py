from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.document import router as document_router

from app.core.exceptions import AppException

from app.routes.quiz import router as quiz_router

from app.core.exception_handlers import (
    app_exception_handler,
    global_exception_handler,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PDF Chat API",
    description="RAG-based PDF chat application",
    version="1.0.0",
)

app.include_router(chat_router)
app.include_router(document_router)
app.include_router(quiz_router)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)