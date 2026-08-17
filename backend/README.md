# PDF Chat Application --- Backend

A production-oriented **FastAPI backend for chatting with uploaded PDF
documents using RAG (Retrieval-Augmented Generation)**.

The application allows a user to upload a PDF, processes it into chunks,
generates embeddings, stores those embeddings in Chroma, and then
answers questions using only the relevant document context.

The backend is intentionally separated from the frontend so that the API
can later support a web UI, mobile client, or other clients
independently.

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Architecture](#architecture)
-   [Request Flow](#request-flow)
-   [Project Structure](#project-structure)
-   [Technologies](#technologies)
-   [Data Storage](#data-storage)
-   [RAG Pipeline](#rag-pipeline)
-   [Document Metadata](#document-metadata)
-   [API Endpoints](#api-endpoints)
-   [Pydantic Validation](#pydantic-validation)
-   [Exception Handling](#exception-handling)
-   [Environment Variables](#environment-variables)
-   [Installation](#installation)
-   [Running the Backend](#running-the-backend)
-   [Testing the API](#testing-the-api)
-   [Git and Local Data](#git-and-local-data)
-   [Current Limitations / Deferred
    Improvements](#current-limitations--deferred-improvements)
-   [Future Roadmap](#future-roadmap)

------------------------------------------------------------------------

## Overview

The backend implements the following workflow:

``` text
User
  |
  | Upload PDF
  v
FastAPI
  |
  v
Document Service
  |
  +----> Save PDF to filesystem
  |
  +----> Create document_id
  |
  +----> Store document metadata in MySQL
  |
  v
PDF Loader
  |
  v
Document Splitter
  |
  v
Embedding Model
  |
  v
Chroma Vector Store
```

When the user asks a question:

``` text
User Question
      |
      v
FastAPI /api/chat
      |
      v
Validate document_id
      |
      v
MySQL
      |
      | Document exists and is processed
      v
Chroma Retriever
      |
      v
Relevant PDF chunks
      |
      v
RAG Prompt
      |
      v
Gemini LLM
      |
      v
Answer + Sources
```

------------------------------------------------------------------------

## Features

### Document Management

-   Upload PDF documents.
-   Generate a unique `document_id` for every uploaded document.
-   Store the actual PDF on the backend filesystem.
-   Store document metadata in MySQL.
-   Track document processing status.
-   Retrieve all uploaded documents.
-   Retrieve a single document using `document_id`.
-   Delete a document.
-   Delete the corresponding Chroma vectors using `document_id`.

### RAG

-   Load PDFs using LangChain PDF loading.
-   Preserve PDF page metadata.
-   Split documents into chunks.
-   Generate embeddings.
-   Store embeddings/chunks in Chroma.
-   Retrieve relevant chunks for a question.
-   Restrict retrieval to the requested document.
-   Generate an answer using Gemini.
-   Return source document and page information.

### API / Backend Quality

-   FastAPI REST API.
-   Pydantic request/response validation.
-   Structured error responses.
-   Custom application exceptions.
-   Global exception handling.
-   Swagger/OpenAPI documentation.
-   Separate route, service, RAG, database, and schema layers.

------------------------------------------------------------------------

# Architecture

The backend follows a layered structure:

``` text
                    FastAPI
                       |
             +---------+---------+
             |                   |
          Routes              Schemas
             |                   |
             v                   v
          Services           Pydantic
             |
       +-----+------+
       |            |
       v            v
   Database       RAG
       |            |
     MySQL       Chroma
                    |
                  Gemini
```

### Responsibilities

#### Routes

Handle HTTP requests and responses.

``` text
app/routes/
```

#### Schemas

Define and validate API input/output.

``` text
app/schemas/
```

#### Services

Contain application/business logic.

``` text
app/services/
```

#### Database

Handle MySQL operations.

``` text
app/database/
```

#### RAG

Handle loading, splitting, embedding, vector storage, retrieval,
prompting, and generation.

``` text
app/rag/
```

#### Core

Contains application-wide exception handling and core backend
functionality.

``` text
app/core/
```

------------------------------------------------------------------------

# Request Flow

## PDF Upload

``` text
POST /api/documents/upload
        |
        v
Validate file
        |
        v
Generate UUID document_id
        |
        v
Save PDF
        |
        v
Create MySQL document record
        |
        | status = processing
        v
Load PDF
        |
        v
Split into chunks
        |
        v
Add document_id to chunk metadata
        |
        v
Generate embeddings
        |
        v
Store chunks + embeddings in Chroma
        |
        v
Update MySQL
        |
        | status = processed
        v
Return document metadata
```

If processing fails:

``` text
processing
     |
     v
failed
```

------------------------------------------------------------------------

## Chat Flow

``` text
POST /api/chat
      |
      v
Pydantic validation
      |
      v
Check document_id in MySQL
      |
      +---- document not found
      |          |
      |          v
      |        404
      |
      +---- document not processed
      |          |
      |          v
      |        409
      |
      v
Retriever
      |
      v
Chroma
      |
      v
Relevant chunks
      |
      v
RAG prompt
      |
      v
Gemini
      |
      v
ChatResponse
```

------------------------------------------------------------------------

# Project Structure

The backend is organized approximately as follows:

``` text
backend/
│
├── app/
│   │
│   ├── core/
│   │   ├── exception_handlers.py
│   │   └── exceptions.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── document_repository.py
│   │
│   ├── rag/
│   │   ├── chain.py
│   │   ├── embeddings.py
│   │   ├── loader.py
│   │   ├── prompt.py
│   │   ├── retriever.py
│   │   ├── splitter.py
│   │   └── vector_store.py
│   │
│   ├── routes/
│   │   ├── chat.py
│   │   └── document.py
│   │
│   ├── schemas/
│   │   ├── chat.py
│   │   ├── document.py
│   │   └── error.py
│   │
│   ├── services/
│   │   └── document_service.py
│   │
│   └── main.py
│
├── data/
│   ├── uploads/
│   ├── processed/
│   └── chroma/
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── venv/
```

`__init__.py` files may be present in Python packages depending on the
project's package/import setup.

------------------------------------------------------------------------

# Technologies

  Technology                     Purpose
  ------------------------------ -----------------------------
  Python                         Backend language
  FastAPI                        REST API framework
  Pydantic                       Request/response validation
  MySQL                          Document metadata/database
  LangChain                      RAG orchestration
  Chroma                         Vector database
  Gemini                         Embeddings and LLM
  Uvicorn                        ASGI server
  PyPDF / LangChain PDF loader   PDF loading
  Git                            Version control

------------------------------------------------------------------------

# Data Storage

The application currently uses three different storage systems.

## 1. MySQL

MySQL stores document metadata.

Typical information:

``` text
document_id
filename
file_path
status
created_at
```

Example:

``` text
document_id = a7c91e25-...
filename    = Machine_Learning.pdf
status      = processed
created_at  = ...
```

MySQL is used to determine whether a document exists and whether it is
ready for chat.

------------------------------------------------------------------------

## 2. Filesystem

The actual PDF is stored locally:

``` text
data/uploads/
```

The generated `document_id` is used as part of the stored filename to
avoid collisions.

------------------------------------------------------------------------

## 3. Chroma

Chroma stores the vector representation of document chunks.

A chunk contains:

``` text
page_content
embedding
metadata
```

Metadata includes information such as:

``` text
document_id
source
page
```

For example:

``` text
document_id = a7c91e25-...
source      = data/uploads/Machine_Learning.pdf
page        = 5
```

This metadata allows the application to retrieve chunks belonging to a
particular PDF and return source/page information to the user.

------------------------------------------------------------------------

# RAG Pipeline

## 1. PDF Loading

The PDF is loaded into LangChain documents.

A multi-page PDF is represented as multiple `Document` objects,
generally one per page when using the PDF loader.

For example:

``` text
PDF
 |
 +-- Page 1 -> Document
 +-- Page 2 -> Document
 +-- Page 3 -> Document
```

The page information is stored in the document metadata.

------------------------------------------------------------------------

## 2. Splitting

The loaded documents are passed to the text splitter.

For example:

``` text
Page 1
  |
  +-- Chunk 1
  +-- Chunk 2
  +-- Chunk 3
```

The splitter creates smaller pieces of text so that the embedding and
retrieval process works effectively.

Metadata is preserved when the documents are split.

------------------------------------------------------------------------

## 3. Document ID Metadata

Before storing the chunks, the backend adds the generated `document_id`:

``` python
for document in documents:
    document.metadata["document_id"] = document_id
```

This is important because multiple PDFs share the same Chroma
collection.

The `document_id` allows the application to distinguish:

``` text
Machine_Learning.pdf
        |
        +-- chunks

Deep_Learning.pdf
        |
        +-- chunks
```

inside the same vector store.

------------------------------------------------------------------------

## 4. Embeddings

The chunks are converted into vectors using the configured embedding
model.

Conceptually:

``` text
"Gradient descent is..."
          |
          v
     Embedding Model
          |
          v
[0.023, -0.18, 0.72, ...]
```

------------------------------------------------------------------------

## 5. Chroma

The vectors and their associated text/metadata are stored in:

``` text
data/chroma/
```

The application uses a Chroma collection:

``` text
pdf_documents
```

The collection contains chunks from multiple uploaded PDFs.

------------------------------------------------------------------------

## 6. Retrieval

The retriever currently uses similarity search:

``` python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": k},
)
```

The default `k` is currently 4.

So a question such as:

``` text
Explain gradient descent.
```

retrieves the most relevant chunks.

------------------------------------------------------------------------

## 7. Generation

The retrieved chunks are inserted into the RAG prompt:

``` text
Context
+
Question
    |
    v
Gemini
    |
    v
Answer
```

The response is then converted into the application's `ChatResponse`.

------------------------------------------------------------------------

# Document Metadata and Sources

The application returns source information with the answer.

Example:

``` json
{
  "answer": "Gradient descent is an optimization algorithm...",
  "sources": [
    {
      "document": "data/uploads/Machine_Learning.pdf",
      "page": 4
    }
  ]
}
```

The page number returned to the API is converted to a human-readable
1-based page number.

PDF/library metadata may internally use zero-based page indexing, so the
application uses:

``` python
page + 1
```

before returning the page number.

------------------------------------------------------------------------

# API Endpoints

## Health Check

``` http
GET /health
```

Example:

``` json
{
  "status": "healthy"
}
```

------------------------------------------------------------------------

## Upload PDF

``` http
POST /api/documents/upload
```

Multipart form upload.

Example:

``` text
file = Machine_Learning.pdf
```

Successful response:

``` json
{
  "document_id": "a7c91e25-5b3a-4c91-9f21-123456789abc",
  "filename": "Machine_Learning.pdf",
  "status": "processed",
  "created_at": "2026-08-17T..."
}
```

Only PDF files are currently supported.

------------------------------------------------------------------------

## Get All Documents

``` http
GET /api/documents
```

Returns uploaded document metadata.

Example:

``` json
{
  "documents": [
    {
      "document_id": "a7c91e25-...",
      "filename": "Machine_Learning.pdf",
      "status": "processed",
      "created_at": "2026-08-17T..."
    }
  ]
}
```

Pagination was considered but intentionally deferred for now.

------------------------------------------------------------------------

## Get One Document

``` http
GET /api/documents/{document_id}
```

Example:

``` http
GET /api/documents/a7c91e25-...
```

Successful response:

``` json
{
  "document_id": "a7c91e25-...",
  "filename": "Machine_Learning.pdf",
  "status": "processed",
  "created_at": "2026-08-17T..."
}
```

If the document does not exist:

``` http
404 Not Found
```

------------------------------------------------------------------------

## Delete Document

``` http
DELETE /api/documents/{document_id}
```

The current deletion flow removes:

``` text
MySQL record
PDF file
Chroma vectors
```

for the specified document.

Successful response:

``` http
204 No Content
```

------------------------------------------------------------------------

## Chat With a Document

``` http
POST /api/chat
```

Example request:

``` json
{
  "document_id": "a7c91e25-...",
  "question": "Explain gradient descent."
}
```

The backend:

1.  Validates the request.
2.  Checks the document in MySQL.
3.  Checks that its status is `processed`.
4.  Retrieves relevant chunks.
5.  Generates an answer using the RAG prompt and Gemini.
6.  Returns the answer and sources.

Example response:

``` json
{
  "answer": "Gradient descent is an optimization algorithm...",
  "sources": [
    {
      "document": "data/uploads/Machine_Learning.pdf",
      "page": 4
    }
  ]
}
```

------------------------------------------------------------------------

# Pydantic Validation

Pydantic is used to ensure API input/output follows the expected
structure.

## Chat Request

``` python
class ChatRequest(BaseModel):
    document_id: str
    question: str
```

Validation includes constraints such as:

``` text
document_id
- required
- minimum length

question
- required
- minimum length
- maximum length = 2000
```

This prevents invalid requests from reaching the RAG pipeline.

------------------------------------------------------------------------

## Chat Response

``` python
class Source(BaseModel):
    document: str
    page: int = Field(..., ge=1)


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
```

Therefore:

``` text
answer → must be a string

sources → must be a list

page → must be >= 1
```

FastAPI also validates the returned data against the response model.

------------------------------------------------------------------------

# Exception Handling

The backend uses centralized exception handling.

There are two major categories.

## Expected Application Errors

Custom exceptions are defined in:

``` text
app/core/exceptions.py
```

For example:

``` python
raise DocumentNotFoundException()
```

The exception inherits from:

``` text
Exception
   |
AppException
   |
DocumentNotFoundException
```

FastAPI routes the exception to:

``` text
app_exception_handler()
```

The client receives a structured response:

``` json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document not found."
  }
}
```

------------------------------------------------------------------------

## Unexpected Errors

Unexpected errors from components such as:

``` text
MySQL
Chroma
Gemini
PDF processing
Python runtime
```

are handled by:

``` text
global_exception_handler()
```

The backend logs the full exception/traceback while returning a safe
response to the client:

``` json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred."
  }
}
```

This prevents internal implementation details from being exposed through
the API.

------------------------------------------------------------------------

# Example Exception Flow

If the user enters an invalid `document_id`:

``` text
POST /api/chat
      |
      v
ChatRequest validation
      |
      v
get_document(document_id)
      |
      v
MySQL returns None
      |
      v
raise DocumentNotFoundException()
      |
      v
FastAPI exception system
      |
      v
app_exception_handler()
      |
      v
404 response
```

Response:

``` json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document not found."
  }
}
```

The RAG pipeline is never executed for the invalid document.

------------------------------------------------------------------------

# Environment Variables

Sensitive configuration should be stored in `.env`.

Example `.env.example`:

``` env
GOOGLE_API_KEY=your_google_api_key
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=pdf_chat
```

Never commit the real `.env` file.

The repository uses:

``` gitignore
.env
.env.*
!.env.example
```

So:

``` text
.env          → ignored
.env.example  → tracked
```

------------------------------------------------------------------------

# Installation

## 1. Clone the repository

``` bash
git clone <repository-url>
cd PDF_Chat_Application/backend
```

## 2. Create a virtual environment

Windows:

``` powershell
python -m venv venv
```

Activate it:

``` powershell
venv\Scripts\activate
```

## 3. Install dependencies

``` bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create:

``` text
.env
```

and provide the required Google/Gemini and MySQL configuration.

------------------------------------------------------------------------

# MySQL Setup

Create the application database in MySQL.

The `documents` table stores document metadata.

Conceptually:

``` sql
CREATE TABLE documents (
    document_id VARCHAR(36) PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The actual schema used by the project should remain the source of truth
if it evolves.

------------------------------------------------------------------------

# Running the Backend

From the `backend` directory:

``` powershell
uvicorn app.main:app --reload
```

The API will normally be available at:

``` text
http://127.0.0.1:8000
```

Swagger UI:

``` text
http://127.0.0.1:8000/docs
```

OpenAPI schema:

``` text
http://127.0.0.1:8000/openapi.json
```

------------------------------------------------------------------------

# Testing the API

Swagger UI can be used to manually test all endpoints:

``` text
http://127.0.0.1:8000/docs
```

Recommended testing sequence:

### 1. Upload

``` text
POST /api/documents/upload
```

Verify that a `document_id` is returned.

### 2. List

``` text
GET /api/documents
```

Verify the uploaded PDF appears.

### 3. Retrieve

``` text
GET /api/documents/{document_id}
```

Verify the document metadata.

### 4. Chat

``` text
POST /api/chat
```

Example:

``` json
{
  "document_id": "<uploaded-document-id>",
  "question": "Explain gradient descent."
}
```

Verify:

-   answer is returned
-   sources are returned
-   page numbers are valid

### 5. Invalid document

Use a fake `document_id`.

Expected:

``` text
404 DOCUMENT_NOT_FOUND
```

### 6. Delete

``` text
DELETE /api/documents/{document_id}
```

Verify that the document is removed.

------------------------------------------------------------------------

# Git and Local Data

The following are intentionally ignored because they are local/generated
data:

``` text
.env
venv/
data/uploads/
data/processed/
data/chroma/
```

The Chroma vector database should not be committed to Git.

The root `.gitignore` contains:

``` gitignore
# Environment variables
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
venv/
.venv/
env/

# Backend local data
backend/data/uploads/*
backend/data/processed/*
backend/data/chroma/*
```

The Chroma database had previously been committed during development,
but it has been removed from current Git tracking. Old commits were
intentionally left unchanged.

------------------------------------------------------------------------

# Current Limitations / Deferred Improvements

The following production improvements have been identified but
intentionally deferred:

## 1. Cross-storage consistency

The application currently uses:

``` text
MySQL
Filesystem
Chroma
```

These systems do not share one atomic transaction.

A failure during processing can potentially leave partial state.

A stronger lifecycle/state-management strategy is planned.

------------------------------------------------------------------------

## 2. Idempotent ingestion

Repeated processing of the same document should eventually use
deterministic chunk/vector IDs to prevent duplicate Chroma records.

------------------------------------------------------------------------

## 3. Background processing

Currently PDF processing/embedding is part of the request workflow.

For large PDFs, production deployment should move expensive ingestion to
a background worker/job system.

------------------------------------------------------------------------

## 4. Authentication and authorization

The current API does not yet associate documents with authenticated
users.

Future versions should introduce:

``` text
User
  |
  +-- Documents
        |
        +-- document_id
```

and ensure users can only access their own documents.

------------------------------------------------------------------------

## 5. Rate limiting

Rate limiting should eventually be added for:

``` text
PDF uploads
Chat requests
```

to protect API resources and external model quotas.

------------------------------------------------------------------------

## 6. Monitoring and production logging

Future deployment should include structured logging, metrics, health
checks, and monitoring for:

``` text
API latency
MySQL
Chroma
LLM/embedding failures
upload failures
RAG failures
```

------------------------------------------------------------------------

## 7. Pagination

Pagination for the document list was considered but intentionally
deferred.

The current endpoint returns the document list directly.

Pagination can be introduced later if the document library becomes
large.

------------------------------------------------------------------------

# Gemini Embedding Quota

The project uses Gemini-based embeddings.

During development, the Gemini embedding API returned:

``` text
429 RESOURCE_EXHAUSTED
```

when the free-tier embedding request quota was exceeded.

This is an external API quota limitation, not a Chroma or FastAPI error.

If this occurs:

-   Check the Gemini API quota.
-   Wait for the quota window to reset.
-   Review the configured API project/billing/quota.
-   Consider an alternative embedding model for production if
    appropriate.

------------------------------------------------------------------------

# Production Architecture --- Planned

The eventual architecture is intended to look like:

``` text
                    FRONTEND
                       |
                       v
                 FastAPI Backend
                       |
          +------------+-------------+
          |            |             |
          v            v             v
        MySQL      Filesystem      Chroma
          |                          |
          |                          v
          |                       RAG
          |                          |
          |                          v
          |                        Gemini
          |
          v
     Document State
```

The frontend will remain separate from the backend.

------------------------------------------------------------------------

# Development Philosophy

The backend is being developed incrementally with an emphasis on:

-   Separation of concerns
-   API validation
-   Clear document lifecycle
-   RAG isolation by `document_id`
-   Structured errors
-   Database-backed document metadata
-   Clean project organization
-   Git tracking of source code only
-   Keeping generated/local data outside version control

------------------------------------------------------------------------

# Status

Current backend MVP:

``` text
[✓] FastAPI application
[✓] PDF upload
[✓] PDF loading
[✓] Document splitting
[✓] Embeddings
[✓] Chroma vector store
[✓] MySQL document metadata
[✓] document_id-based document isolation
[✓] RAG retrieval
[✓] Gemini answer generation
[✓] Source/page information
[✓] Pydantic validation
[✓] Document listing
[✓] Single-document lookup
[✓] Document deletion
[✓] Global exception handling
[✓] Git/.gitignore cleanup

[ ] Cross-storage consistency
[ ] Idempotent ingestion
[ ] Background processing
[ ] Authentication
[ ] Rate limiting
[ ] Monitoring
```

The backend is now ready to be integrated with the separate frontend.
