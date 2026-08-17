# PDF Chat Application

A full-stack **RAG-powered PDF chat application** that lets users upload PDF documents and ask questions about their content. Relevant sections are retrieved from the selected PDF and passed to an LLM to generate grounded answers with source and page references.

## ✨ Features

- Upload and process PDF documents
- Manage uploaded documents from a document library
- Chat with a specific PDF using its unique `document_id`
- Retrieval-Augmented Generation (RAG)
- Source and page references with answers
- MySQL document metadata and status tracking
- Chroma vector storage for document embeddings
- Pydantic request/response validation
- Global FastAPI exception handling
- Modern responsive React interface
- Markdown rendering for formatted AI responses

## 🛠 Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, React Router, React Markdown |
| Backend | Python, FastAPI, Pydantic |
| RAG | LangChain |
| LLM | Google Gemini |
| Vector Store | Chroma |
| Database | MySQL |
| PDF Processing | LangChain document loaders & text splitters |

## 🏗 Architecture

```text
                         User
                          │
                          ▼
                   React Frontend
                          │
                     REST API
                          │
                          ▼
                    FastAPI Backend
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
           MySQL      PDF Files      RAG Pipeline
                                       │
                                  ┌────┴────┐
                                  ▼         ▼
                               Chroma     Gemini
```

- **MySQL** stores document metadata such as ID, filename, status and creation time.
- **Filesystem** stores uploaded PDFs.
- **Chroma** stores document chunks, embeddings and metadata.
- **Gemini** generates answers using context retrieved from Chroma.
- **React** provides document management and chat interfaces.

## 🔄 How It Works

### Document Processing

```text
Upload PDF
    ↓
Generate document_id
    ↓
Save PDF + document metadata
    ↓
Load and split PDF
    ↓
Generate embeddings
    ↓
Store chunks in Chroma
    ↓
Mark document as processed
```

Each chunk contains metadata such as `document_id`, source and page. This lets multiple PDFs share the same Chroma collection while retrieval remains specific to the selected document.

### Question Answering

```text
Question + document_id
          ↓
Validate document
          ↓
Retrieve relevant chunks
          ↓
Build RAG context
          ↓
Gemini
          ↓
Answer + Sources
```

The frontend sends the selected document ID and question. Retrieval and LLM interaction remain on the backend.

## 🖥 Frontend

The React application follows this flow:

```text
Landing Page
    ↓
Documents Page
    ↓
Select / Upload PDF
    ↓
Chat Page
```

The **Landing Page** contains a modern navbar, hero, `Let's Start` CTA, Features, How It Works, About and footer sections.

The **Documents Page** lets users upload PDFs, view uploaded documents and their processing status, open a document in chat, and delete documents.

The **Chat Page** provides document-specific conversations with user/AI messages, loading and error states, Markdown-formatted answers, and source/page references.

## 🔌 API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/documents/upload` | Upload and process a PDF |
| `GET` | `/api/documents` | List uploaded documents |
| `GET` | `/api/documents/{document_id}` | Get one document |
| `DELETE` | `/api/documents/{document_id}` | Delete a document |
| `POST` | `/api/chat` | Ask a question about a PDF |

Example chat request:

```json
{
  "document_id": "efe5b980-527c-497a-ac89-e0a2170fd02b",
  "question": "Give me a summary of this document."
}
```

Example response:

```json
{
  "answer": "The document discusses...",
  "sources": [
    {
      "document": "example.pdf",
      "page": 2
    }
  ]
}
```

## 📁 Project Structure

```text
PDF_Chat_Application/
│
├── backend/
│   ├── app/
│   │   ├── core/          # Exceptions and global handlers
│   │   ├── database/      # MySQL and repositories
│   │   ├── rag/           # Embeddings, retriever, prompt and chain
│   │   ├── routes/        # FastAPI routes
│   │   ├── schemas/       # Pydantic schemas
│   │   └── main.py
│   └── data/
│       ├── uploads/
│       ├── processed/
│       └── chroma/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/      # Backend API calls
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
│
└── .gitignore
```

## 🚀 Getting Started

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure the backend `.env` with the required Gemini and MySQL credentials, then run:

```powershell
uvicorn app.main:app --reload
```

Backend: `http://127.0.0.1:8000`  
Swagger: `http://127.0.0.1:8000/docs`

### Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

Configure the frontend API URL when required:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

> Keep real `.env` files out of Git. Use `.env.example` for safe configuration templates.

## 📌 Current Status

The complete core workflow is functional:

```text
Upload PDF
   ↓
Process & Embed
   ↓
Store
   ↓
Select Document
   ↓
Ask Question
   ↓
Retrieve Context
   ↓
Generate Answer
   ↓
Display Sources
```

The project is currently at a functional **full-stack MVP** stage with the RAG backend and React frontend integrated.

## 🚧 Improvements & Upcoming Features

- **Source deduplication** — avoid repeated page references when several chunks come from the same page.
- **Better upload UX** — drag-and-drop upload, progress indicators and clearer processing states.
- **Background processing** — move embedding/indexing work away from the upload request for large PDFs.
- **Storage consistency** — improve synchronization and cleanup between MySQL, the PDF filesystem and Chroma.
- **Improved retrieval** — evaluate MMR, reranking, MultiQuery and contextual compression.
- **Streaming responses** — progressively display generated answers in the chat UI.
- **PDF preview & clickable sources** — open referenced PDF pages directly from answers.
- **Conversation history** — persist previous chats.
- **Authentication & authorization** — associate PDFs and conversations with individual users.
- **Search, sorting & pagination** — improve document management as the library grows.
- **Production deployment** — cloud storage, managed databases, monitoring, CI/CD and scalable deployment.

## 🔐 Git & Local Data

Sensitive and generated data is excluded from version control:

```text
.env
backend/venv/
backend/data/uploads/
backend/data/processed/
backend/data/chroma/
frontend/node_modules/
frontend/dist/
frontend/.vite/
```

This keeps API keys, local PDFs, vector data, dependencies and generated build files out of the repository.

## 📈 Project Direction

The goal is to evolve the MVP into a production-ready document intelligence application while keeping the architecture modular:

```text
React UI → FastAPI → Document Services → RAG → Vector Store / LLM
```

This separation allows the frontend, retrieval strategy, storage layer and deployment infrastructure to evolve independently.
