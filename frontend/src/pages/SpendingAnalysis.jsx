import { useEffect, useState } from "react";

import api from "../services/api";

function SpendingAnalysis() {
  const token = localStorage.getItem("access_token");

  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    async function fetchAnalysis() {
      try {
        const response = await api.get(
          "/ai/spending-analysis"
        );

        setAnalysis(response.data);
      } catch (error) {
        console.error(error);
      }
    }

    if (token) {
      fetchAnalysis();
    }
  }, [token]);

  return (
    <main className="page">
      <header className="page-header">
        <h1 className="page-title">
          Spending Analysis
        </h1>

        <p className="page-subtitle">
          Understand where your money is going.
        </p>
      </header>

      {!analysis ? (
        <section className="card">
          <p className="page-subtitle">
            Loading your spending analysis...
          </p>
        </section>
      ) : (
        <section className="card analysis-preview">
          <div className="analysis-highlight">
            <span>Total Spending</span>

            <strong>
              ₹{analysis.total_spending}
            </strong>
          </div>

          <div className="analysis-row">
            <span>Highest Category</span>

            <strong>
              {analysis.highest_category}
            </strong>
          </div>

          <div className="analysis-row">
            <span>Category Amount</span>

            <strong>
              ₹{analysis.highest_category_amount}
            </strong>
          </div>

          <div className="analysis-insight">
            <h2>AI Insight</h2>

            <p>{analysis.insight}</p>
          </div>
        </section>
      )}
    </main>
  );
}

export default SpendingAnalysis;