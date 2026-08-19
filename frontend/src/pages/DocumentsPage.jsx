import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getDocuments, uploadDocument, deleteDocument } from "../services/api";

function DocumentsPage() {
  const navigate = useNavigate();

  const fileInputRef = useRef(null);

  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const loadDocuments = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getDocuments();

      setDocuments(data.documents);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Only PDF files are supported.");

      return;
    }

    try {
      setUploading(true);
      setError("");

      await uploadDocument(file);

      await loadDocuments();
    } catch (error) {
      setError(error.message);
    } finally {
      setUploading(false);

      event.target.value = "";
    }
  };

  const handleDelete = async (documentId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document?",
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");

      await deleteDocument(documentId);

      setDocuments((currentDocuments) =>
        currentDocuments.filter(
          (document) => document.document_id !== documentId,
        ),
      );
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <main className="documents-page">
      <header className="documents-header">
        <div>
          <p className="eyebrow">YOUR WORKSPACE</p>

          <h1>Your Documents</h1>

          <p>Upload a PDF and start a conversation with your document.</p>
        </div>

        <button
          className="upload-button"
          onClick={() => fileInputRef.current.click()}
          disabled={uploading}
        >
          {uploading ? "Processing..." : "Upload PDF"}
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          hidden
          onChange={handleUpload}
        />
      </header>

      {error && <div className="error-message">{error}</div>}

      <section className="documents-section">
        <div className="section-heading">
          <h2>Your PDFs</h2>

          <span>{documents.length} documents</span>
        </div>

        {loading ? (
          <div className="empty-state">Loading documents...</div>
        ) : documents.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">PDF</div>

            <h3>No documents yet</h3>

            <p>Upload your first PDF to start chatting with it.</p>

            <button
              className="upload-button"
              onClick={() => fileInputRef.current.click()}
            >
              Upload your first PDF
            </button>
          </div>
        ) : (
          <div className="documents-grid">
            {documents.map((document) => (
              <article
                className="document-card-item"
                key={document.document_id}
              >
                <div className="document-icon">PDF</div>

                <div className="document-info">
                  <h3 title={document.filename}>{document.filename}</h3>

                  <p>{document.status}</p>
                </div>

                <div className="document-actions">
                  <button
                    onClick={() => navigate(`/chat/${document.document_id}`)}
                    disabled={document.status !== "processed"}
                  >
                    Chat
                  </button>
                  <button
                    onClick={() => navigate(`/quiz/${document.document_id}`)}
                    disabled={document.status !== "processed"}
                  >
                    Quiz
                  </button>
                  <button
                    className="delete-button"
                    onClick={() => handleDelete(document.document_id)}
                  >
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default DocumentsPage;
