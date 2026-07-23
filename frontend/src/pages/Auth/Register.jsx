import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import "./register.css";

function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!name || !email || !password || !confirmPassword || !role) {
      setError("Please fill in all fields");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    try {
      setLoading(true);

      await api.post("/auth/register", {
        name,
        email,
        password,
        role,
      });

      setSuccess("Account created successfully");

      setName("");
      setEmail("");
      setPassword("");
      setConfirmPassword("");
      setRole("");

      setTimeout(() => {
        navigate("/");
      }, 1500);
    } catch (error) {
      console.error("Registration Error:", error);

      if (error.response?.data?.detail) {
        setError(error.response.data.detail);
      } else {
        setError("Registration failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="register-card">

        <div className="register-header">
          <h1>
            Insider<span>AI</span>
          </h1>

          <p>Create your account</p>
        </div>

        <form onSubmit={handleRegister}>

          <div className="form-group">
            <label htmlFor="name">Full Name</label>

            <input
              id="name"
              type="text"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                setError("");
              }}
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>

            <input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setError("");
              }}
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">Account Role</label>

            <div className="select-wrapper">
              <select
                id="role"
                value={role}
                onChange={(e) => {
                  setRole(e.target.value);
                  setError("");
                }}
              >
                <option value="" disabled>
                  Select your role
                </option>

                <option value="SOC Engineer">
                  SOC Engineer
                </option>

                <option value="Security Analyst">
                  Security Analyst
                </option>

                <option value="Security Manager">
                  Security Manager
                </option>

                <option value="Administrator">
                  Administrator
                </option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>

            <input
              id="password"
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setError("");
              }}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>

            <input
              id="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => {
                setConfirmPassword(e.target.value);
                setError("");
              }}
            />
          </div>

          {error && (
            <p className="register-error">
              {error}
            </p>
          )}

          {success && (
            <p className="register-success">
              {success}
            </p>
          )}

          <button
            type="submit"
            className="register-button"
            disabled={loading}
          >
            {loading ? "Creating Account..." : "Create Account"}
          </button>

        </form>

        <div className="register-footer">
          <p>
            Already have an account?{" "}
            <span onClick={() => navigate("/")}>
              Sign In
            </span>
          </p>
        </div>

      </div>
    </div>
  );
}

export default Register;