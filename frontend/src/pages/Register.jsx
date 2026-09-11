import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../services/api";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  async function handleRegister(event) {
    event.preventDefault();

    if (loading) {
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      await api.post("/register", {
        username,
        password,
      });

      setSuccess(
        "Account created successfully. Redirecting to login..."
      );

      setUsername("");
      setPassword("");

      setTimeout(() => {
        navigate("/");
      }, 1200);
    } catch (error) {
      console.error(error);

      if (error.response?.status === 409) {
        setError(
          "Username already exists. Please choose another."
        );
      } else {
        setError(
          "Couldn't create your account. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <header className="page-header">
        <h1 className="page-title">
          AI Expense Tracker
        </h1>

        <p className="page-subtitle">
          Create your account and start tracking your expenses.
        </p>
      </header>

      <section className="card auth-card">
        <h2>Create your account</h2>

        <p className="auth-description">
          Set up your account to start managing your expenses.
        </p>

        <form onSubmit={handleRegister}>
          <label htmlFor="register-username">
            Username
          </label>

          <input
            id="register-username"
            type="text"
            placeholder="Choose a username"
            value={username}
            onChange={(event) =>
              setUsername(event.target.value)
            }
            autoComplete="username"
            disabled={loading}
          />

          <label htmlFor="register-password">
            Password
          </label>

          <div className="password-input-wrapper">
            <input
              id="register-password"
              type={showPassword ? "text" : "password"}
              placeholder="Create a password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              autoComplete="new-password"
              disabled={loading}
            />

            <button
              type="button"
              className="password-toggle"
              onClick={() =>
                setShowPassword(!showPassword)
              }
              disabled={loading}
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>

          <p className="password-hint">
            Password must be at least 6 characters.
          </p>

          <button
            type="submit"
            disabled={
              loading ||
              !username.trim() ||
              !password.trim()
            }
          >
            {loading ? "Registering..." : "Create Account"}
          </button>
        </form>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        {success && (
          <div className="auth-success">
            {success}
          </div>
        )}

        <p className="auth-link">
          Already have an account?{" "}
          <Link to="/">
            Login
          </Link>
        </p>
      </section>
    </main>
  );
}

export default Register;