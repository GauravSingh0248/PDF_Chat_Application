import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { generateNotes } from "../services/api";

import "./NotesPage.css";

function NotesPage() {
  const { documentId } = useParams();
  const navigate = useNavigate();

  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchNotes() {
      try {
        setLoading(true);
        setError("");

        const data = await generateNotes(documentId);

        setNotes(data.notes);
      } catch (error) {
        setError(error.message || "Failed to generate notes.");
      } finally {
        setLoading(false);
      }
    }

    if (documentId) {
      fetchNotes();
    }
  }, [documentId]);

  return (
    <main className="notes-page">
      <div className="notes-container">
        {/* Back Button */}
        <button
          className="notes-back-button"
          onClick={() => navigate("/documents")}
        >
          <span>←</span>
          <span>Back to Documents</span>
        </button>

        {/* Page Header */}
        <header className="notes-header">
          <p className="eyebrow">DOCUMENT NOTES</p>

          <h1>Study Notes</h1>

          <p>Simple and clear notes generated from your uploaded document.</p>
        </header>

        {/* Error */}
        {error && (
          <div className="notes-error">
            <strong>Something went wrong</strong>
            <p>{error}</p>
          </div>
        )}

        {/* Notes Card */}
        {!error && (
          <section className="notes-card">
            {/* Card Header */}
            <div className="notes-card-header">
              <div>
                <span className="notes-label">AI GENERATED</span>

                <h2>Study Notes</h2>
              </div>
            </div>

            {/* Loading */}
            {loading ? (
              <div className="notes-loading">
                <div className="loading-spinner"></div>

                <h3>Generating your notes...</h3>

                <p>Reading the document and creating simple study notes.</p>
              </div>
            ) : (
              /* Markdown Content */
              <article className="notes-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    /* Main Markdown Title */
                    h1: ({ children }) => (
                      <h1 className="notes-main-title">{children}</h1>
                    ),

                    /* Section Heading */
                    h2: ({ children }) => (
                      <div className="notes-section-heading">
                        <span className="section-line"></span>

                        <h2>{children}</h2>
                      </div>
                    ),

                    /* Subheading */
                    h3: ({ children }) => (
                      <h3 className="notes-subheading">{children}</h3>
                    ),

                    /* Paragraph */
                    p: ({ children }) => (
                      <p className="notes-paragraph">{children}</p>
                    ),

                    /* Unordered List */
                    ul: ({ children }) => (
                      <ul className="notes-list">{children}</ul>
                    ),

                    /* Ordered List */
                    ol: ({ children }) => (
                      <ol className="notes-list">{children}</ol>
                    ),

                    /* List Item */
                    li: ({ children }) => (
                      <li className="notes-list-item">{children}</li>
                    ),

                    /* Bold */
                    strong: ({ children }) => (
                      <strong className="notes-strong">{children}</strong>
                    ),

                    /* Italic */
                    em: ({ children }) => (
                      <em className="notes-emphasis">{children}</em>
                    ),

                    /* Table */
                    table: ({ children }) => (
                      <div className="notes-table-wrapper">
                        <table>{children}</table>
                      </div>
                    ),

                    /* Table Header */
                    th: ({ children }) => <th>{children}</th>,

                    /* Table Cell */
                    td: ({ children }) => <td>{children}</td>,

                    /* Blockquote */
                    blockquote: ({ children }) => (
                      <blockquote className="notes-quote">
                        {children}
                      </blockquote>
                    ),

                    /* Horizontal Line */
                    hr: () => <hr />,

                    /* Inline Code */
                    code: ({ children }) => <code>{children}</code>,
                  }}
                >
                  {notes}
                </ReactMarkdown>
              </article>
            )}
          </section>
        )}
      </div>
    </main>
  );
}

export default NotesPage;
