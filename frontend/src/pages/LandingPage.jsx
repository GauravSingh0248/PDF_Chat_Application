import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  const handleStart = () => {
    navigate("/documents");
  };

  return (
    <main className="landing-page">
      <nav className="navbar">
        <div className="logo">
          PDF<span>Chat</span>
        </div>

        <div className="nav-links">
          <a href="#features">Features</a>

          <a href="#how-it-works">How It Works</a>

          <a href="#about">About</a>
        </div>

        <button className="nav-start-button" onClick={handleStart}>
          Let's Start
          <span>→</span>
        </button>
      </nav>

      <section className="hero">
        <div className="hero-content">
          <p className="eyebrow">AI POWERED DOCUMENT INTELLIGENCE</p>

          <h1>
            Your PDFs.
            <br />
            <span>Your Questions.</span>
            <br />
            One Conversation.
          </h1>

          <p className="hero-description">
            Upload your documents and have a conversation with them. Ask
            questions, understand complex topics, and find information
            instantly.
          </p>

          <button className="start-button" onClick={handleStart}>
            Let's Start
            <span>→</span>
          </button>
        </div>

        <div className="hero-visual">
          <div className="document-card">
            <div className="document-header">
              <div className="pdf-icon">PDF</div>

              <div>
                <p>Machine_Learning.pdf</p>
                <small>24 pages</small>
              </div>
            </div>

            <div className="chat-preview">
              <div className="user-message">Explain gradient descent.</div>

              <div className="ai-message">
                <div className="ai-label">AI</div>

                <p>
                  Gradient descent is an optimization algorithm used to minimize
                  a function by iteratively moving in the direction of the
                  steepest descent.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section id="features" className="landing-section features-section">
        <div className="section-intro">
          <p className="eyebrow">WHY PDFCHAT</p>

          <h2>
            Your documents,
            <br />
            <span>finally interactive.</span>
          </h2>

          <p>
            Stop searching through pages manually. Ask questions and let your
            documents give you the answers.
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-number">01</div>

            <div className="feature-icon">?</div>

            <h3>Ask Anything</h3>

            <p>
              Ask questions naturally and get answers based on the content of
              your uploaded documents.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-number">02</div>

            <div className="feature-icon">AI</div>

            <h3>Grounded Answers</h3>

            <p>
              Responses are generated from relevant document content instead of
              relying only on general knowledge.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-number">03</div>

            <div className="feature-icon">↗</div>

            <h3>Source References</h3>

            <p>
              See the document and page from which the retrieved information
              came.
            </p>
          </div>
        </div>
      </section>

      <section id="how-it-works" className="landing-section process-section">
        <div className="section-intro">
          <p className="eyebrow">HOW IT WORKS</p>

          <h2>
            From PDF to
            <br />
            <span>conversation.</span>
          </h2>
        </div>

        <div className="process-list">
          <div className="process-item">
            <span className="process-number">01</span>

            <div>
              <h3>Upload</h3>

              <p>Upload the PDF you want to understand.</p>
            </div>
          </div>

          <div className="process-item">
            <span className="process-number">02</span>

            <div>
              <h3>Process</h3>

              <p>
                Your document is processed, split into meaningful chunks, and
                indexed.
              </p>
            </div>
          </div>

          <div className="process-item">
            <span className="process-number">03</span>

            <div>
              <h3>Ask</h3>

              <p>Ask questions about anything contained in your document.</p>
            </div>
          </div>

          <div className="process-item">
            <span className="process-number">04</span>

            <div>
              <h3>Understand</h3>

              <p>Receive an answer with relevant source and page references.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="about" className="landing-section about-section">
        <div className="about-content">
          <p className="eyebrow">ABOUT PDFCHAT</p>

          <h2>
            Turn static documents
            <br />
            into <span>conversations.</span>
          </h2>

          <p>
            PDFChat is a RAG-powered document assistant designed to make
            information inside PDFs easier to understand and explore.
          </p>

          <p>
            Instead of manually searching through pages, you can simply ask a
            question and receive an answer grounded in your document.
          </p>
        </div>

        <div className="about-highlight">
          <div className="about-highlight-inner">
            <span>PDF</span>

            <span className="arrow">→</span>

            <span>AI</span>

            <span className="arrow">→</span>

            <span>ANSWER</span>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <div className="logo">
          PDF<span>Chat</span>
        </div>

        <p>Chat with your documents.</p>

        <button className="nav-start-button" onClick={handleStart}>
          Let's Start
          <span>→</span>
        </button>
      </footer>
    </main>
  );
}

export default LandingPage;
