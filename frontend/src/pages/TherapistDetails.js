import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "./TherapistDetails.css";

function TherapistDetails({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [therapist, setTherapist] = useState(null);
  const [availableTimes, setAvailableTimes] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTime, setSelectedTime] = useState("");
  const [message, setMessage] = useState("");
  const today = new Date();
  const maxDate = new Date();
  maxDate.setDate(today.getDate() + 14);

  useEffect(() => {
    fetch(`http://localhost:5000/therapist/${id}`, {
      method: "GET",
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch therapist details");
        }
        return response.json();
      })
      .then((data) => {
        setTherapist(data);
        console.log("Therapist data loaded:", data);
      })
      .catch((error) => console.error("Error fetching therapist details:", error));
  }, [id]);


  useEffect(() => {
    if (selectedDate) {
      const formattedDate = formatDate(selectedDate);
      const url = `http://localhost:5000/therapist/${id}/available-times?date=${formattedDate}`;
      console.log("Fetching available times from URL:", url);

      fetch(url, {
        method: "GET",
        credentials: "include",
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to fetch available times");
          }
          return response.json();
        })
        .then((data) => {
          setAvailableTimes(data.available_times);
          console.log("Available times received:", data.available_times);
        })
        .catch((error) => console.error("Error fetching available times:", error));
    }
  }, [id, selectedDate]);

  const handleDateChange = (date) => {
    setSelectedDate(date);
    setSelectedTime("");
    console.log("Date selected:", formatDate(date));
  };

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const handleTimeSlotClick = (timeSlot) => {
    setSelectedTime(timeSlot);
    console.log("Time slot selected:", timeSlot);
  };

  const handleBooking = () => {
    if (!user) {
      console.error("User is not logged in. Redirecting to login.");
      navigate("/login");
      return;
    }

    if (!selectedDate || !selectedTime) {
      setMessage("Please select both a date and a time slot.");
      console.log("Booking failed: Missing date or time slot.");
      return;
    }

    const bookingData = {
      user_id: user.id,
      therapist_id: id,
      date: formatDate(selectedDate),
      time_slot: selectedTime,
    };

    console.log("Sending booking request with data:", bookingData);

    fetch("http://localhost:5000/booking", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bookingData),
    })
      .then((response) => {
        if (response.ok) {
          setMessage("Booking created successfully!");
          console.log("Booking successful.");
          const formattedDate = formatDate(selectedDate);
          return fetch(`http://localhost:5000/therapist/${id}/available-times?date=${formattedDate}`, {
            method: "GET",
            credentials: "include",
          });
        } else if (response.status === 409) {
          setMessage("This time slot is already booked.");
          console.log("Booking failed: Time slot already booked.");
        } else {
          setMessage("Failed to create booking. Please try again.");
          console.log("Booking failed: Server error.");
        }
      })
      .then((response) => response?.json())
      .then((data) => {
        if (data) {
          setAvailableTimes(data.available_times);
          console.log("Updated available times after booking:", data.available_times);
        }
      })
      .catch((error) => console.error("Error during booking process:", error));
  };

  if (!therapist) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>{therapist.first_name} {therapist.last_name}</h1>
      <p><strong>Specialization:</strong> {therapist.specialization}</p>
      <p><strong>Rating:</strong> {therapist.rating}</p>
      <p><strong>Biography:</strong> {therapist.biography}</p>
      <p><strong>Contact Email:</strong> {therapist.contact_email}</p>

      <h2>Select a Date for Consultation</h2>
      <Calendar
        onChange={handleDateChange}
        value={selectedDate}
        minDate={today}
        maxDate={maxDate}
      />
      {selectedDate && <p>Selected Date: <strong>{formatDate(selectedDate)}</strong></p>}

      {selectedDate && (
        <>
          <h2>Select a Time Slot</h2>
          <div className="time-slots">
            {availableTimes.length > 0 ? (
              availableTimes.map((timeSlot, index) => (
                <div
                  key={index}
                  className={`time-slot ${selectedTime === timeSlot ? "selected" : ""}`}
                  onClick={() => handleTimeSlotClick(timeSlot)}
                >
                  {timeSlot}
                </div>
              ))
            ) : (
              <p>No available time slots for the selected date.</p>
            )}
          </div>
        </>
      )}

      <button onClick={handleBooking} className="booking-button">
        Book Appointment
      </button>

      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default TherapistDetails;
