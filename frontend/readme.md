# PDF Chat Application — Frontend

A modern React frontend for the PDF Chat Application. It provides a clean interface for uploading PDF documents, browsing uploaded documents, and chatting with a selected PDF through the FastAPI RAG backend.

## Overview

The frontend provides three main experiences:

```text
Landing Page
     |
     | Let's Start
     v
Documents Page
     |
     | Select PDF
     v
Chat Page
```

The frontend does not perform RAG itself. PDF splitting, embeddings, Chroma retrieval, Gemini calls, and MySQL operations are handled by the backend.

## Features

### Landing Page

- Modern dark-themed interface
- AI/SaaS-inspired visual design
- Hero section
- `Let's Start` call-to-action
- Responsive layout
- PDF + AI chat visual preview

### Document Library

- Upload PDF
- List uploaded documents
- Show processing status
- Open a document in chat
- Delete documents
- Loading state
- Empty state
- Error handling

### Chat

- Document-specific chat
- User and AI messages
- Loading/Thinking state
- Source information
- Page numbers
- Error messages
- Back navigation
- Responsive layout
- Markdown rendering for AI responses

## Technology Stack

| Technology | Purpose |
|---|---|
| React | UI framework |
| Vite | Development/build tool |
| JavaScript | Programming language |
| React Router DOM | Client-side routing |
| React Markdown | Render AI Markdown responses |
| CSS | Styling and responsive design |
| Fetch API | Backend communication |

## Application Flow

```text
                    Landing Page
                         |
                   Let's Start
                         |
                         v
                  Documents Page
                         |
              +----------+----------+
              |                     |
              v                     v
          Upload PDF             Select PDF
              |                     |
              v                     v
       Backend Upload API      /chat/:documentId
                                    |
                                    v
                               Chat Page
                                    |
                                    v
                              User Question
                                    |
                                    v
                              Backend API
                                    |
                                    v
                              RAG Pipeline
                                    |
                                    v
                              AI Response
                                    |
                                    v
                          Answer + Sources
```

## Pages

### Landing Page

Route:

```text
/
```

Component:

```text
src/pages/LandingPage.jsx
```

The main CTA navigates to:

```text
/documents
```

### Documents Page

Route:

```text
/documents
```

Component:

```text
src/pages/DocumentsPage.jsx
```

It fetches documents, uploads PDFs, displays status, opens chat, and deletes documents.

### Chat Page

Route:

```text
/chat/:documentId
```

Component:

```text
src/pages/ChatPage.jsx
```

The document ID is obtained with:

```javascript
const { documentId } = useParams();
```

## Project Structure

```text
frontend/
│
├── public/
│
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   └── Button.jsx
│   │
│   ├── pages/
│   │   ├── LandingPage.jsx
│   │   ├── DocumentsPage.jsx
│   │   └── ChatPage.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── .env
├── .env.example
├── package.json
├── package-lock.json
└── vite.config.js
```

## Routing

Current routes:

```text
/                       → LandingPage
/documents              → DocumentsPage
/chat/:documentId       → ChatPage
```

Routing is configured in `src/App.jsx` using React Router.

## API Integration

All backend communication is centralized in:

```text
src/services/api.js
```

### Get Documents

```http
GET /api/documents
```

Frontend function:

```javascript
getDocuments()
```

### Upload Document

```http
POST /api/documents/upload
```

Frontend function:

```javascript
uploadDocument(file)
```

The PDF is sent using `FormData`.

### Delete Document

```http
DELETE /api/documents/{document_id}
```

Frontend function:

```javascript
deleteDocument(documentId)
```

### Chat With Document

```http
POST /api/chat
```

Frontend function:

```javascript
chatWithDocument(documentId, question)
```

Request:

```json
{
  "document_id": "a7c91e25-...",
  "question": "Explain gradient descent."
}
```

Response:

```json
{
  "answer": "Gradient descent is...",
  "sources": [
    {
      "document": "data/uploads/Machine_Learning.pdf",
      "page": 4
    }
  ]
}
```

## Environment Variables

Create:

```text
.env
```

with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Maintain a template:

```text
.env.example
```

with the same variable name.

The frontend accesses it through:

```javascript
const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL;
```

The real `.env` file should not be committed.

## Installation

From the project root:

```powershell
cd frontend
npm install
```

## Running the Frontend

Start the Vite development server:

```powershell
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

## Running With the Backend

### Terminal 1 — Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

### Terminal 2 — Frontend

```powershell
cd frontend
npm run dev
```

Frontend:

```text
http://localhost:5173
```

The backend must be running for document listing, uploads, deletion, and chat.

## CORS

During development, the frontend and backend run on different ports:

```text
Frontend
localhost:5173

        ↓ HTTP

Backend
127.0.0.1:8000
```

The FastAPI backend therefore needs CORS configured to allow the frontend origin.

## User Flow

1. Open `/`.
2. Click `Let's Start`.
3. Navigate to `/documents`.
4. Upload or select a PDF.
5. Click `Chat`.
6. Navigate to `/chat/{document_id}`.
7. Ask a question.
8. The frontend sends the document ID and question to the backend.
9. The backend performs retrieval and generation.
10. The frontend renders the answer and sources.

## Chat Interface

The chat interface contains:

- User messages on the right
- AI responses on the left
- AI avatar
- Loading/Thinking state
- Fixed chat input
- Empty-chat state
- Error state
- Source information
- Page references
- Responsive mobile styling

## Markdown Responses

The LLM may return Markdown such as:

```text
**Statement of Purpose**

**Key Points**

- Background
- Projects
- Goals
```

The frontend uses `react-markdown` so Markdown is rendered instead of displaying literal `**` characters.

Example:

```jsx
<ReactMarkdown>
    {message.content}
</ReactMarkdown>
```

The CSS also styles headings, bold text, lists, code, code blocks, blockquotes, and links.

## Source Display

The backend can return:

```json
{
  "sources": [
    {
      "document": "data/uploads/Machine_Learning.pdf",
      "page": 4
    }
  ]
}
```

The frontend displays the source document and page below the AI response.

The frontend only displays this metadata; the backend RAG pipeline is responsible for generating it.

## Error Handling

The API service checks unsuccessful HTTP responses:

```javascript
if (!response.ok) {
    ...
}
```

Backend error messages are extracted when available:

```javascript
error?.error?.message
```

For example:

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document not found."
  }
}
```

The message is shown in the frontend UI.

## Frontend vs Backend Responsibilities

Frontend:

```text
UI
Routing
User interaction
File selection
API requests
Loading states
Error presentation
Answer rendering
Source rendering
```

Backend:

```text
PDF storage
PDF loading
PDF splitting
Document metadata
MySQL
Embeddings
Chroma
Retrieval
RAG
Gemini
Exception handling
```

Architecture:

```text
             FRONTEND
                 |
                 | REST API
                 v
              FASTAPI
                 |
       +---------+---------+
       |                   |
       v                   v
     MySQL                RAG
                            |
                     +------+------+
                     |             |
                   Chroma        Gemini
```

## Git and Ignored Files

Generated dependencies and build output should not be committed.

Important ignored paths:

```text
frontend/node_modules/
frontend/dist/
frontend/dist-ssr/
frontend/.vite/
frontend/.env
```

The root `.gitignore` also ignores environment files while keeping `.env.example`:

```gitignore
.env
.env.*
!.env.example
```

## Current Status

```text
[✓] React + Vite
[✓] JavaScript
[✓] React Router
[✓] Landing page
[✓] Modern dark UI
[✓] Let's Start navigation
[✓] Documents page
[✓] PDF upload
[✓] Document listing
[✓] Document deletion
[✓] Document status
[✓] Document-specific chat route
[✓] Chat interface
[✓] Backend API integration
[✓] Loading states
[✓] Error states
[✓] Source/page display
[✓] Markdown AI responses
[✓] Responsive chat UI
[✓] Environment-based API URL
[✓] Frontend Git ignore configuration
```

## Future Improvements

### UI/UX

```text
[ ] Display actual PDF filename in chat header
[ ] Deduplicate repeated source/page entries
[ ] PDF preview
[ ] Drag-and-drop upload
[ ] Upload progress indicator
[ ] Better processing status UI
[ ] Toast notifications
[ ] Skeleton loaders
[ ] Chat auto-scroll
[ ] Copy AI response
[ ] Regenerate answer
[ ] Suggested questions
```

### Chat

```text
[ ] Streaming AI responses
[ ] Conversation persistence
[ ] Multiple chat sessions
[ ] Message timestamps
[ ] Stop generation
[ ] Better Markdown/code styling
[ ] Clickable source pages
```

### Document Management

```text
[ ] Search documents
[ ] Sort documents
[ ] Pagination when document count becomes large
[ ] Document preview
[ ] Rename documents
[ ] Multiple PDF upload
```

### Authentication

Future versions can introduce:

```text
User
 |
 +-- Documents
 |
 +-- Chat Sessions
 |
 +-- Conversations
```

### Production

```text
[ ] Production API URL
[ ] Authentication
[ ] Protected routes
[ ] HTTPS
[ ] Deployment
[ ] Network retry handling
[ ] Performance optimization
[ ] Monitoring
```

## Full Application Structure

```text
PDF_Chat_Application/
│
├── backend/
│   ├── FastAPI
│   ├── MySQL
│   ├── LangChain
│   ├── Chroma
│   └── Gemini
│
└── frontend/
    ├── React
    ├── Vite
    ├── JavaScript
    ├── React Router
    └── React Markdown
```

The frontend is currently integrated with:

```text
GET    /api/documents
POST   /api/documents/upload
GET    /api/documents/{document_id}
DELETE /api/documents/{document_id}
POST   /api/chat
```

The project is currently at a functional frontend + backend integrated MVP stage.
