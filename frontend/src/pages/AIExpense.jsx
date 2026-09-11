import { useState } from "react";

import api from "../services/api";

function AIExpense() {
  const token = localStorage.getItem("access_token");

  const [text, setText] = useState("");
  const [expense, setExpense] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!text.trim() || loading) {
      return;
    }

    setLoading(true);
    setExpense(null);
    setError("");

    try {
      const response = await api.post("/ai/expenses", {
        text: text.trim(),
      });

      setExpense(response.data);
      setText("");
    } catch (error) {
      console.error(error);

      setError(
        "Couldn't add this expense. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleExampleClick(example) {
    if (!loading) {
      setText(example);
      setError("");
    }
  }

  return (
    <main className="page">
      <header className="page-header">
        <h1 className="page-title">
          Add Expense with AI
        </h1>

        <p className="page-subtitle">
          Describe your expense naturally and let AI
          organize it for you.
        </p>
      </header>

      <section className="card ai-expense-card">
        <div className="ai-expense-intro">
          <span className="ai-badge">
            AI POWERED
          </span>

          <h2>
            Tell me what you spent
          </h2>

          <p>
            You don't need to enter the amount,
            description, and category separately.
            Just describe your expense.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <textarea
            className="ai-expense-input"
            placeholder='Example: "Spent ₹450 on dinner with friends"'
            value={text}
            onChange={(event) =>
              setText(event.target.value)
            }
            rows="4"
            disabled={loading}
          />

          <button
            type="submit"
            disabled={loading || !text.trim()}
          >
            {loading
              ? "Understanding your expense..."
              : "Add Expense with AI"}
          </button>
        </form>

        <div className="ai-examples">
          <span>Try an example</span>

          <button
            type="button"
            className="example-button"
            disabled={loading}
            onClick={() =>
              handleExampleClick(
                "Spent ₹450 on dinner with friends"
              )
            }
          >
            Dinner ₹450
          </button>

          <button
            type="button"
            className="example-button"
            disabled={loading}
            onClick={() =>
              handleExampleClick(
                "Paid ₹1200 for electricity bill"
              )
            }
          >
            Electricity ₹1200
          </button>

          <button
            type="button"
            className="example-button"
            disabled={loading}
            onClick={() =>
              handleExampleClick(
                "Spent ₹300 on Uber"
              )
            }
          >
            Uber ₹300
          </button>
        </div>

        {error && (
          <div className="ai-expense-error">
            {error}
          </div>
        )}
      </section>

      {expense && (
        <section className="card ai-result">
          <div className="ai-result-header">
            <span className="success-badge">
              ✓ Expense added successfully
            </span>
          </div>

          <div className="ai-result-main">
            <div>
              <span>
                ₹{expense.amount}
              </span>

              <p>
                {expense.description}
              </p>
            </div>

            <strong>
              {expense.category}
            </strong>
          </div>
        </section>
      )}
    </main>
  );
}

export default AIExpense;