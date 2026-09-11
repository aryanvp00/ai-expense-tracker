import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const token = localStorage.getItem("access_token");
  const navigate = useNavigate();

  const [menuOpen, setMenuOpen] = useState(false);

  function handleLogout() {
    localStorage.removeItem("access_token");
    setMenuOpen(false);
    navigate("/");
  }

  function closeMenu() {
    setMenuOpen(false);
  }

  return (
    <>
      <nav className="navbar">
        {token && (
          <button
            className="navbar-menu-button"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle navigation menu"
            aria-expanded={menuOpen}
          >
            {menuOpen ? "✕" : "☰"}
          </button>
        )}

        <Link
          to="/dashboard"
          className="navbar-brand"
          onClick={closeMenu}
        >
          AI Expense Tracker
        </Link>

        {token && (
          <div className="navbar-desktop-links">
            <Link to="/dashboard">Dashboard</Link>

            <Link to="/expenses">Expenses</Link>

            <Link to="/ai-expense">AI Expense</Link>

            <Link to="/spending-analysis">
              Analysis
            </Link>

            <Link to="/assistant">
              Assistant
            </Link>

            <button
              className="navbar-logout"
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        )}
      </nav>

      {token && (
        <>
          <div
            className={`mobile-menu ${
              menuOpen ? "mobile-menu-open" : ""
            }`}
          >
            <Link to="/dashboard" onClick={closeMenu}>
              Dashboard
            </Link>

            <Link to="/expenses" onClick={closeMenu}>
              Expenses
            </Link>

            <Link to="/ai-expense" onClick={closeMenu}>
              AI Expense
            </Link>

            <Link
              to="/spending-analysis"
              onClick={closeMenu}
            >
              Analysis
            </Link>

            <Link to="/assistant" onClick={closeMenu}>
              Assistant
            </Link>

            <button
              className="mobile-menu-logout"
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>

          {menuOpen && (
            <div
              className="mobile-menu-overlay"
              onClick={closeMenu}
            />
          )}
        </>
      )}
    </>
  );
}

export default Navbar;