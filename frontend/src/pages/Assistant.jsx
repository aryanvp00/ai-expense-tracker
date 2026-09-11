import { useState } from "react";

import api from "../services/api";

function Assistant() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question.trim();

    setMessages((currentMessages) => [
      ...currentMessages,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setQuestion("");
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/ai/assistant", {
        question: currentQuestion,
      });

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: "assistant",
          content: response.data.answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setError(
        "Sorry, I couldn't process your question. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleSuggestedQuestion(questionText) {
    setQuestion(questionText);
  }

  return (
    <main className="page">
      <header className="page-header">
        <h1 className="page-title">
          AI Financial Assistant
        </h1>

        <p className="page-subtitle">
          Ask questions about your spending and get
          intelligent answers.
        </p>
      </header>

      <section className="card assistant-card">
        <div className="assistant-intro">
          <span className="ai-badge">
            AI ASSISTANT
          </span>

          <h2>
            Your personal financial assistant
          </h2>

          <p>
            Ask about your spending, categories,
            comparisons, or financial patterns.
          </p>
        </div>

        {messages.length === 0 && (
          <div className="assistant-suggestions">
            <span>Try asking</span>

            <button
              type="button"
              className="example-button"
              onClick={() =>
                handleSuggestedQuestion(
                  "How much have I spent?"
                )
              }
            >
              How much have I spent?
            </button>

            <button
              type="button"
              className="example-button"
              onClick={() =>
                handleSuggestedQuestion(
                  "What category do I spend the most on?"
                )
              }
            >
              Highest spending category?
            </button>

            <button
              type="button"
              className="example-button"
              onClick={() =>
                handleSuggestedQuestion(
                  "How much did I spend this month?"
                )
              }
            >
              This month's spending?
            </button>
          </div>
        )}

        {messages.length > 0 && (
          <div className="assistant-messages">
            {messages.map((message, index) => (
              <div
                className={`assistant-message ${
                  message.role === "user"
                    ? "assistant-message-user"
                    : "assistant-message-ai"
                }`}
                key={index}
              >
                <span className="assistant-message-label">
                  {message.role === "user"
                    ? "You"
                    : "AI Assistant"}
                </span>

                <p>{message.content}</p>
              </div>
            ))}

            {loading && (
              <div className="assistant-message assistant-message-ai">
                <span className="assistant-message-label">
                  AI Assistant
                </span>

                <p className="assistant-loading">
                  Thinking...
                </p>
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="assistant-error">
            {error}
          </div>
        )}

        <form
          className="assistant-form"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            placeholder="Ask something about your spending..."
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            disabled={loading}
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
          >
            {loading ? "Thinking..." : "Ask AI"}
          </button>
        </form>
      </section>
    </main>
  );
}
export default Assistant;