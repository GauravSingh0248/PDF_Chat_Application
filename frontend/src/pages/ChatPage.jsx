import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

import { chatWithDocument } from "../services/api";

function ChatPage() {
  const { documentId } = useParams();
  const navigate = useNavigate();

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    // Add user's question to the chat
    setMessages((currentMessages) => [
      ...currentMessages,
      {
        role: "user",
        content: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);
    setError("");

    try {
      const response = await chatWithDocument(documentId, trimmedQuestion);

      // Add AI response
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: "assistant",
          content: response.answer,
          sources: response.sources || [],
        },
      ]);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="chat-page">
      {/* Header */}

      <header className="chat-header">
        <button className="back-button" onClick={() => navigate("/documents")}>
          ←
        </button>

        <div className="chat-document-info">
          <div className="chat-pdf-icon">PDF</div>

          <div>
            <h1>PDF Chat</h1>

            <p>Document ID: {documentId}</p>
          </div>
        </div>
      </header>

      {/* Messages */}

      <section className="chat-messages">
        {messages.length === 0 && !loading ? (
          <div className="chat-empty">
            <div className="chat-empty-icon">✦</div>

            <h2>Ask anything about your PDF</h2>

            <p>
              Your questions will be answered using the content of this
              document.
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message-row ${message.role}`}>
              {message.role === "assistant" && (
                <div className="message-avatar">AI</div>
              )}

              <div className="message-content">
                <div className="message-bubble">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
                {message.sources && message.sources.length > 0 && (
                  <div className="sources">
                    <p className="sources-title">Sources</p>

                    <div className="source-list">
                      {message.sources.map((source, sourceIndex) => (
                        <div className="source-item" key={sourceIndex}>
                          <span>Page {source.page}</span>

                          <span>{source.document}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="message-row assistant">
            <div className="message-avatar">AI</div>

            <div className="message-bubble typing">Thinking...</div>
          </div>
        )}
      </section>

      {/* Error */}

      {error && <div className="chat-error">{error}</div>}

      {/* Input */}

      <form className="chat-input-container" onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask something about your PDF..."
          disabled={loading}
        />

        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? "..." : "↑"}
        </button>
      </form>

      <p className="chat-disclaimer">
        Answers are generated from your uploaded document.
      </p>
    </main>
  );
}

export default ChatPage;
