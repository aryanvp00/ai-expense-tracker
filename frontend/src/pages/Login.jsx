import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../services/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  async function handleLogin(event) {
    event.preventDefault();

    if (loading) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await api.post("/login", {
        username,
        password,
      });

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      navigate("/dashboard");
    } catch (error) {
      console.error(error);

      setError(
        "Invalid username or password. Please try again."
      );
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
          Manage your expenses with the help of AI.
        </p>
      </header>

      <section className="card auth-card">
        <h2>Welcome back</h2>

        <p className="auth-description">
          Login to access your personal expense dashboard.
        </p>

        <form onSubmit={handleLogin}>
          <label htmlFor="login-username">
            Username
          </label>

          <input
            id="login-username"
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(event) =>
              setUsername(event.target.value)
            }
            autoComplete="username"
            disabled={loading}
          />

          <label htmlFor="login-password">
            Password
          </label>

          <div className="password-input-wrapper">
            <input
              id="login-password"
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              autoComplete="current-password"
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

          <button
            type="submit"
            disabled={
              loading ||
              !username.trim() ||
              !password.trim()
            }
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        <p className="auth-link">
          Don't have an account?{" "}
          <Link to="/register">
            Register
          </Link>
        </p>
      </section>
    </main>
  );
}

export default Login;