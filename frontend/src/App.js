import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import UserInfo from "./pages/UserInfo";
import Register from "./pages/Register";
import TherapistDetails from "./pages/TherapistDetails";

function App() {
  const [user, setUser] = useState(null);

  const logout = () => {
    setUser(null);
    fetch("http://localhost:5000/logout", {
      method: "POST",
      credentials: "include",
    }).catch((error) => console.error("Error logging out:", error));
  };

  return (
    <Router>
      <NavBar user={user} logout={logout} />
      <Routes>
        <Route path="/" element={<Home user={user} />} />
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/user_info" element={<UserInfo user={user} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/therapist/:id" element={<TherapistDetails user={user} />} />
      </Routes>
    </Router>
  );
}

function NavBar({ user, logout }) {
  const navigate = useNavigate(); 

  return (
    <nav className="nav-bar">
      <div className="nav-logo">
        <img
          src="/logo.png"
          alt="Logo"
          className="logo-img"
          onClick={() => navigate("/")}
        />
        <span className="nav-title">Gabinet Psychologiczno-Terapeutyczny</span> {}
      </div>
      <div className="nav-links">
        {!user && <Link to="/login" className="nav-button">Login</Link>}
        {user && (
          <>
            <button onClick={logout} className="nav-button">Logout</button>
            <Link to="/user_info" className="nav-button">Info About Me</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default App;
