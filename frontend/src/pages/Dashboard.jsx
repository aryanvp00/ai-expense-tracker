import { Link, useNavigate } from "react-router-dom";

import CategoryChart from "../components/CategoryChart";
import useDashboardData from "../hooks/useDashboardData";

function Dashboard() {
  const token = localStorage.getItem("access_token");
  const navigate = useNavigate();

  const { expenses, analysis } = useDashboardData(token);

  function handleLogout() {
    localStorage.removeItem("access_token");
    navigate("/");
  }

  return (
    <main className="page">
      <header className="page-header">
        <h1 className="page-title">
          AI Expense Tracker
        </h1>

        <p className="page-subtitle">
          Your personal AI-powered financial dashboard.
        </p>
      </header>

      <section className="dashboard-summary">
        <div className="summary-card">
          <span>Total Spending</span>

          <strong>
            {analysis
              ? `₹${analysis.total_spending}`
              : "Loading..."}
          </strong>
        </div>

        <div className="summary-card">
          <span>Highest Category</span>

          <strong>
            {analysis
              ? analysis.highest_category
              : "Loading..."}
          </strong>
        </div>

        <div className="summary-card">
          <span>Highest Category Amount</span>

          <strong>
            {analysis
              ? `₹${analysis.highest_category_amount}`
              : "Loading..."}
          </strong>
        </div>
      </section>

      <CategoryChart expenses={expenses} />

      <section className="card dashboard-card">
        <h2>Dashboard</h2>

        <p className="page-subtitle">
          Manage your expenses, understand your spending,
          and get insights from AI.
        </p>

        <div className="dashboard-actions">
          <Link to="/expenses">
            <button>My Expenses</button>
          </Link>

          <Link to="/ai-expense">
            <button>Add Expense with AI</button>
          </Link>

          <Link to="/spending-analysis">
            <button>Spending Analysis</button>
          </Link>

          <Link to="/assistant">
            <button>AI Financial Assistant</button>
          </Link>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </section>
    </main>
  );
}

export default Dashboard;