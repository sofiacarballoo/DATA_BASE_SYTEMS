import React, { useState } from "react";
import axios from "axios";

function DeleteVaccine() {
  const [vaccineId, setVaccineId] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleDelete = () => {
    if (!vaccineId) {
      setError("Please enter a valid Vaccine ID.");
      return;
    }

    axios
      .delete(`http://127.0.0.1:5000/api/vaccine/${vaccineId}`)
      .then((response) => {
        setMessage(response.data.message);
        setError("");
      })
      .catch((err) => {
        if (err.response) {
          setError(err.response.data.error || "Failed to delete the vaccine.");
        } else {
          setError("Network error. Please try again.");
        }
        setMessage("");
      });
  };

  return (
    <div>
      <h1>Delete Vaccine</h1>
      <div>
        <label>
          Vaccine ID:
          <input
            type="text"
            value={vaccineId}
            onChange={(e) => setVaccineId(e.target.value)}
          />
        </label>
        <button onClick={handleDelete}>Delete</button>
      </div>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default DeleteVaccine;
