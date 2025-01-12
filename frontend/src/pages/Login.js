import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Login.css";

function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    fetch("http://localhost:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    })
      .then((response) => {
        if (!response.ok) {
          alert("Invalid email or password. Please try again."); 
          throw new Error("Invalid email or password");
        }
        return response.json();
      })
      .then((data) => {
        setUser(data);
        navigate("/");
      })
      .catch((error) => {
        console.error("Login error:", error);
      });
  };

  return (
    <div className="login-container">
      <h1 className="login-title">Login</h1>
      <form className="login-form" onSubmit={handleLogin}>
        <div className="form-group">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="form-input"
            required
          />
        </div>
        <div className="form-group">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="form-input"
            required
          />
        </div>
        <button type="submit" className="login-button">Log In</button>
      </form>
      <p className="register-text">Don't have an account?</p>
      <Link to="/register">
        <button className="register-button">Register</button>
      </Link>
    </div>
  );
}

export default Login;
