import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  analyzePyq,
  getDocuments,
  uploadDocument,
} from "../services/api";

import "./PyqPage.css";

function PyqPage() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [documents, setDocuments] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [subject, setSubject] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");

  const loadDocuments = async () => {
    try {
      setLoadingDocs(true);
      setError("");

      const data = await getDocuments();
      setDocuments(data.documents || []);
    } catch (err) {
      setError(err.message || "Failed to load documents.");
    } finally {
      setLoadingDocs(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const processedDocuments = documents.filter(
    (document) => document.status === "processed",
  );

  const toggleSelection = (documentId) => {
    setSelectedIds((current) => {
      if (current.includes(documentId)) {
        return current.filter((id) => id !== documentId);
      }

      return [...current, documentId];
    });
  };

  const handleUpload = async (event) => {
    const files = Array.from(event.target.files || []);

    if (files.length === 0) {
      return;
    }

    const pdfFiles = files.filter(
      (file) =>
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf"),
    );

    if (pdfFiles.length === 0) {
      setError("Only PDF files are supported.");
      event.target.value = "";
      return;
    }

    try {
      setUploading(true);
      setError("");

      const failures = [];

      for (const file of pdfFiles) {
        try {
          await uploadDocument(file);
        } catch (err) {
          failures.push(
            `${file.name}: ${err.message || "upload failed"}`,
          );
        }
      }

      await loadDocuments();

      if (failures.length > 0) {
        const skipped = files.length - pdfFiles.length;
        const parts = [
          `Uploaded ${pdfFiles.length - failures.length} of ${pdfFiles.length} PDF(s).`,
          ...failures,
        ];

        if (skipped > 0) {
          parts.push(`${skipped} non-PDF file(s) skipped.`);
        }

        setError(parts.join(" "));
      }
    } catch (err) {
      setError(err.message || "Failed to upload PDF.");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  const runAnalysis = async () => {
    if (selectedIds.length < 2) {
      setError(
        "Select at least 2 previous-year papers (e.g. 2025, 2024, 2023).",
      );
      return;
    }

    try {
      setAnalyzing(true);
      setError("");
      setAnalysis(null);

      const data = await analyzePyq(selectedIds, subject.trim() || null);
      setAnalysis(data);
    } catch (err) {
      setError(err.message || "Failed to analyze PYQ papers.");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <main className="pyq-page">
      <div className="pyq-container">
        <button className="pyq-back-button" onClick={() => navigate("/")}>
          <span>←</span>
          <span>Back to Home</span>
        </button>

        <header className="pyq-header">
          <p className="eyebrow">SEPARATE WORKSPACE</p>
          <h1>PYQ Analysis</h1>
          <p>
            Upload multiple previous-year papers for the same subject, select
            them, and find repeated questions, similar patterns, and important
            topics across years.
          </p>
        </header>

        <section className="pyq-controls">
          <div className="pyq-control-row">
            <label htmlFor="pyq-subject">Subject (optional)</label>
            <input
              id="pyq-subject"
              type="text"
              placeholder="e.g. Operating System"
              value={subject}
              onChange={(event) => setSubject(event.target.value)}
              disabled={analyzing}
            />
          </div>

          <div className="pyq-meta">
            <button
              className="pyq-secondary-button"
              onClick={() => fileInputRef.current.click()}
              disabled={uploading || analyzing}
            >
              {uploading ? "Uploading..." : "Upload PYQ PDFs"}
            </button>

            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              multiple
              hidden
              onChange={handleUpload}
            />

            <span>{selectedIds.length} selected</span>

            <button
              className="pyq-analyze-button"
              onClick={runAnalysis}
              disabled={analyzing || selectedIds.length < 2}
            >
              {analyzing ? "Analyzing..." : "Analyze selected papers"}
            </button>
          </div>
        </section>

        {error && (
          <div className="pyq-error">
            <strong>Something went wrong</strong>
            <p>{error}</p>
          </div>
        )}

        <section className="pyq-card">
          <div className="pyq-card-heading">
            <h2>Select year papers</h2>
            <span>
              {processedDocuments.length} ready · pick at least 2
            </span>
          </div>

          {loadingDocs ? (
            <p className="pyq-muted">Loading documents...</p>
          ) : processedDocuments.length === 0 ? (
            <p className="pyq-muted">
              No processed PDFs yet. Upload previous-year papers here (e.g.
              OS_2025.pdf, OS_2024.pdf).
            </p>
          ) : (
            <div className="pyq-select-grid">
              {processedDocuments.map((document) => {
                const selected = selectedIds.includes(document.document_id);

                return (
                  <label
                    key={document.document_id}
                    className={`pyq-select-card${selected ? " selected" : ""}`}
                  >
                    <input
                      type="checkbox"
                      checked={selected}
                      onChange={() => toggleSelection(document.document_id)}
                    />
                    <div>
                      <h3 title={document.filename}>{document.filename}</h3>
                      <p>{document.status}</p>
                    </div>
                  </label>
                );
              })}
            </div>
          )}
        </section>

        {analyzing && !analysis && (
          <div className="pyq-loading">
            Comparing questions across selected years...
          </div>
        )}

        {analysis && (
          <div className="pyq-results">
            <section className="pyq-card">
              <h2>Papers analyzed</h2>
              <ul className="pyq-paper-list">
                {analysis.papers_analyzed?.map((paper) => (
                  <li key={paper}>{paper}</li>
                ))}
              </ul>
              {analysis.subject && (
                <p className="pyq-subject-line">Subject: {analysis.subject}</p>
              )}
              {analysis.exam_focus_summary && (
                <p className="pyq-summary">{analysis.exam_focus_summary}</p>
              )}
            </section>

            <section className="pyq-card">
              <h2>Most important topics</h2>
              <div className="pyq-chip-row">
                {(analysis.important_topics || []).map((topic) => (
                  <span className="pyq-chip" key={topic}>
                    {topic}
                  </span>
                ))}
              </div>
            </section>

            <section className="pyq-card">
              <h2>Topic frequency</h2>
              <div className="pyq-list">
                {(analysis.topics || []).map((topic) => (
                  <article
                    className="pyq-item"
                    key={`${topic.topic}-${topic.frequency}`}
                  >
                    <div className="pyq-item-top">
                      <h3>{topic.topic}</h3>
                      <span
                        className={`pyq-badge importance-${topic.importance?.toLowerCase()}`}
                      >
                        {topic.importance}
                      </span>
                    </div>
                    <p>Appeared {topic.frequency} times</p>
                    <p className="pyq-muted">
                      Years: {(topic.years_appeared || []).join(", ")}
                    </p>
                    <p>{topic.reason}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="pyq-card">
              <h2>Most repeated questions</h2>
              <div className="pyq-list">
                {(analysis.repeated_questions || []).length === 0 ? (
                  <p className="pyq-muted">No clear repeated questions found.</p>
                ) : (
                  analysis.repeated_questions.map((item) => (
                    <article
                      className="pyq-item"
                      key={`${item.question}-${item.frequency}`}
                    >
                      <h3>{item.question}</h3>
                      <p>
                        Repeated in {item.frequency} papers · Topic:{" "}
                        {item.topic}
                      </p>
                      <p className="pyq-muted">
                        Years: {(item.years_appeared || []).join(", ")}
                      </p>
                    </article>
                  ))
                )}
              </div>
            </section>

            <section className="pyq-card">
              <h2>Similar question groups</h2>
              <div className="pyq-list">
                {(analysis.similar_questions || []).length === 0 ? (
                  <p className="pyq-muted">No similar question groups found.</p>
                ) : (
                  analysis.similar_questions.map((group) => (
                    <article
                      className="pyq-item"
                      key={`${group.representative_question}-${group.frequency}`}
                    >
                      <h3>{group.representative_question}</h3>
                      <p>
                        {group.frequency} related variants · Topic:{" "}
                        {group.topic}
                      </p>
                      <p className="pyq-muted">
                        Years: {(group.years_appeared || []).join(", ")}
                      </p>
                      <ul>
                        {(group.similar_variants || []).map((variant) => (
                          <li key={variant}>{variant}</li>
                        ))}
                      </ul>
                    </article>
                  ))
                )}
              </div>
            </section>
          </div>
        )}
      </div>
    </main>
  );
}

export default PyqPage;
