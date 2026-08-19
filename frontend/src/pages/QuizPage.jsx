import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";

import { generateQuiz, submitQuiz } from "../services/api";

function QuizPage() {
  const { documentId } = useParams();
  const navigate = useNavigate();

  const [numberOfQuestions, setNumberOfQuestions] = useState(5);
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // -----------------------------------------
  // Generate Quiz
  // -----------------------------------------

  const handleGenerateQuiz = async () => {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data = await generateQuiz(documentId, numberOfQuestions);

      setQuiz(data);
      setAnswers({});
      setCurrentQuestion(0);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------------------
  // Select Answer
  // -----------------------------------------

  const handleAnswerSelect = (optionIndex) => {
    const question = quiz.questions[currentQuestion];

    setAnswers((currentAnswers) => ({
      ...currentAnswers,
      [question.id]: optionIndex,
    }));
  };

  // -----------------------------------------
  // Next Question
  // -----------------------------------------

  const handleNext = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion((current) => current + 1);
    }
  };

  // -----------------------------------------
  // Previous Question
  // -----------------------------------------

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion((current) => current - 1);
    }
  };

  // -----------------------------------------
  // Submit Quiz
  // -----------------------------------------

  const handleSubmitQuiz = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await submitQuiz(quiz.quiz_id, answers);

      setResult(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------------------
  // Reset Quiz
  // -----------------------------------------

  const handleRetake = () => {
    setQuiz(null);
    setResult(null);
    setAnswers({});
    setCurrentQuestion(0);
    setError("");
  };

  // -----------------------------------------
  // Quiz Setup
  // -----------------------------------------

  if (!quiz && !result) {
    return (
      <main className="quiz-page">
        <header className="quiz-header">
          <button
            className="back-button"
            onClick={() => navigate("/documents")}
          >
            ←
          </button>

          <div>
            <p className="eyebrow">PDF QUIZ</p>

            <h1>Test Your Knowledge</h1>

            <p>Generate an MCQ quiz from your document.</p>
          </div>
        </header>

        {error && <div className="quiz-error">{error}</div>}

        <section className="quiz-setup">
          <div className="quiz-setup-card">
            <div className="quiz-icon">?</div>

            <p className="eyebrow">CREATE QUIZ</p>

            <h2>How well do you know this PDF?</h2>

            <p className="quiz-setup-description">
              Choose the number of questions and test your understanding of the
              document.
            </p>

            <label>Number of Questions</label>

            <select
              value={numberOfQuestions}
              onChange={(event) =>
                setNumberOfQuestions(Number(event.target.value))
              }
            >
              <option value={5}>5 Questions</option>
              <option value={10}>10 Questions</option>
              <option value={15}>15 Questions</option>
              <option value={20}>20 Questions</option>
            </select>

            <button
              className="generate-quiz-button"
              onClick={handleGenerateQuiz}
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Quiz →"}
            </button>
          </div>
        </section>
      </main>
    );
  }

  // -----------------------------------------
  // Result Screen
  // -----------------------------------------

  if (result) {
    return (
      <main className="quiz-page">
        <header className="quiz-header">
          <button
            className="back-button"
            onClick={() => navigate("/documents")}
          >
            ←
          </button>

          <div>
            <p className="eyebrow">QUIZ COMPLETE</p>

            <h1>Your Results</h1>

            <p>Here's how you performed.</p>
          </div>
        </header>

        <section className="quiz-result">
          <div className="result-card">
            <div className="result-score">
              <span>{result.score}</span>

              <small>/ {result.total_questions}</small>
            </div>

            <p className="result-percentage">{result.percentage}%</p>

            <p>
              {result.score === result.total_questions
                ? "Perfect score! Excellent work."
                : result.score >= result.total_questions / 2
                  ? "Good job! Keep learning."
                  : "Keep practicing. You can do better!"}
            </p>
          </div>

          <div className="quiz-results">
            <h2>Answer Review</h2>

            {result.results.map((item) => (
              <article
                className={
                  item.is_correct
                    ? "result-item correct"
                    : "result-item incorrect"
                }
                key={item.question_id}
              >
                <div className="result-question-header">
                  <span>Question {item.question_id}</span>

                  <span>{item.is_correct ? "✓ Correct" : "✕ Incorrect"}</span>
                </div>

                <p>
                  Your answer:{" "}
                  <strong>
                    {String.fromCharCode(65 + item.selected_option)}
                  </strong>
                </p>

                {!item.is_correct && (
                  <p>
                    Correct answer:{" "}
                    <strong>
                      {String.fromCharCode(65 + item.correct_option)}
                    </strong>
                  </p>
                )}

                <div className="result-explanation">
                  <span>Explanation</span>

                  <p>{item.explanation}</p>
                </div>
              </article>
            ))}
          </div>

          <button className="generate-quiz-button" onClick={handleRetake}>
            Take Quiz Again →
          </button>
        </section>
      </main>
    );
  }

  // -----------------------------------------
  // Active Quiz
  // -----------------------------------------

  const question = quiz.questions[currentQuestion];

  const selectedAnswer = answers[question.id];

  const isLastQuestion = currentQuestion === quiz.questions.length - 1;

  const progress = ((currentQuestion + 1) / quiz.questions.length) * 100;

  return (
    <main className="quiz-page">
      {/* Header */}

      <header className="quiz-header">
        <button className="back-button" onClick={() => navigate("/documents")}>
          ←
        </button>

        <div>
          <p className="eyebrow">PDF QUIZ</p>

          <h1>Test Your Knowledge</h1>

          <p>Answer the questions based on your PDF.</p>
        </div>
      </header>

      {/* Error */}

      {error && <div className="quiz-error">{error}</div>}

      {/* Quiz */}

      <section className="quiz-container">
        {/* Progress */}

        <div className="quiz-progress-header">
          <span>
            Question {currentQuestion + 1} of {quiz.questions.length}
          </span>

          <span>{Math.round(progress)}%</span>
        </div>

        <div className="quiz-progress">
          <div
            className="quiz-progress-bar"
            style={{
              width: `${progress}%`,
            }}
          />
        </div>

        {/* Question */}

        <article className="quiz-question">
          <p className="question-number">
            QUESTION {String(currentQuestion + 1).padStart(2, "0")}
          </p>

          <h2>{question.question}</h2>

          {/* Options */}

          <div className="quiz-options">
            {question.options.map((option, index) => {
              const isSelected = selectedAnswer === index;

              return (
                <button
                  key={index}
                  className={
                    isSelected ? "quiz-option selected" : "quiz-option"
                  }
                  onClick={() => handleAnswerSelect(index)}
                >
                  <span className="option-letter">
                    {String.fromCharCode(65 + index)}
                  </span>

                  <span>{option}</span>
                </button>
              );
            })}
          </div>
        </article>

        {/* Navigation */}

        <div className="quiz-navigation">
          <button
            className="quiz-nav-button secondary"
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
          >
            ← Previous
          </button>

          {!isLastQuestion ? (
            <button
              className="quiz-nav-button primary"
              onClick={handleNext}
              disabled={selectedAnswer === undefined}
            >
              Next →
            </button>
          ) : (
            <button
              className="quiz-nav-button primary"
              onClick={handleSubmitQuiz}
              disabled={
                loading || Object.keys(answers).length !== quiz.questions.length
              }
            >
              {loading ? "Submitting..." : "Submit Quiz ✓"}
            </button>
          )}
        </div>
      </section>
    </main>
  );
}

export default QuizPage;
