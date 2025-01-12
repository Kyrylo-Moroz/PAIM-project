import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./UserInfo.css";

function UserInfo({ user }) {
  const [userInfo, setUserInfo] = useState(null);
  const [selectedVisit, setSelectedVisit] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      console.error("User is not logged in. Redirecting to login.");
      navigate("/login");
      return;
    }

    fetch("http://localhost:5000/user_info", {
      method: "GET",
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch user info");
        }
        return response.json();
      })
      .then((data) => {
        console.log("User info loaded:", data);
        setUserInfo(data);
      })
      .catch((error) => {
        console.error("Error fetching user info:", error);
        navigate("/login");
      });
  }, [user, navigate]);

  const handleCardClick = (visit) => {
    if (isVisitExpired(visit)) return;
    setSelectedVisit(visit === selectedVisit ? null : visit);
  };

  const isVisitExpired = (visit) => {
    const now = new Date();
    const visitDateTime = new Date(`${visit.date}T${visit.time_slot.split(" - ")[0]}`);
    return visitDateTime < now;
  };

  const handleDeleteClick = (reservationId) => {
    if (!reservationId) {
      console.error("Reservation ID is undefined!");
      return;
    }

    fetch(`http://localhost:5000/delete_reservation/${reservationId}`, {
      method: "DELETE",
      credentials: "include",
    })
      .then((response) => {
        if (response.ok) {
          console.log("Reservation deleted successfully");
          setUserInfo((prev) => ({
            ...prev,
            visits: prev.visits.filter((visit) => visit.id !== reservationId),
          }));
        } else {
          console.error("Failed to delete reservation");
        }
      })
      .catch((error) => console.error("Error deleting reservation:", error));
  };

  if (!userInfo) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>Info About Me</h1>
      <p><strong>Email:</strong> {userInfo.email}</p>
      <p><strong>First Name:</strong> {userInfo.first_name}</p>
      <p><strong>Last Name:</strong> {userInfo.last_name}</p>

      <h2>My Visits</h2>
      {userInfo.visits.length > 0 ? (
        <div className="visit-cards">
          {userInfo.visits.map((visit) => (
            <div
              key={visit.id}
              className={`visit-card ${isVisitExpired(visit) ? "expired" : ""} ${selectedVisit === visit ? "selected" : ""}`}
              onClick={() => handleCardClick(visit)}
            >
              <p><strong>Date:</strong> {visit.date}</p>
              <p><strong>Time Slot:</strong> {visit.time_slot}</p>
              <p><strong>Therapist:</strong> {visit.therapist.first_name} {visit.therapist.last_name}</p>
              <p><strong>Specialization:</strong> {visit.therapist.specialization}</p>
              {!isVisitExpired(visit) && selectedVisit === visit && (
                <button onClick={() => handleDeleteClick(visit.id)} className="visit-button">
                  Delete Reservation
                </button>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p>No visits found.</p>
      )}
    </div>
  );
}

export default UserInfo;
