import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const [therapists, setTherapists] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:5000/therapists", {
      method: "GET",
      credentials: "include", 
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch therapists");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Therapists data from API:", data);
        setTherapists(data);
      })
      .catch((error) => console.error("Error fetching therapists:", error));
  }, []);

  const handleCardClick = (id) => {
    console.log("Clicked Therapist ID:", id);
    if (id) {
      navigate(`/therapist/${id}`);
    } else {
      console.error("Therapist ID is undefined!");
    }
  };

  return (
    <div>
      <h1 id="therapists-page-title">Gabinet Psychologiczno-Terapeutyczny</h1>
      <h2 id="therapists-page-slogon">Pomagamy odnaleźć równowagę i harmonię</h2>
      <div className="therapist-cards">
        {therapists.map((therapist) => (
          <div
            key={therapist.id}
            className="therapist-card"
            onClick={() => handleCardClick(therapist.id)}
          >
            <h3>{therapist.first_name} {therapist.last_name}</h3>
            <p>Specialization: {therapist.specialization}</p>
            <p>Rating: {therapist.rating}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
