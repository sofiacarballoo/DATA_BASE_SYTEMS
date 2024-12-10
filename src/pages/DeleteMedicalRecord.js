import React, { useState } from "react";
import axios from "axios";

function DeleteMedicalProcedure() {
  const [procedureId, setProcedureId] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleDelete = () => {
    if (!procedureId) {
      setError("Please enter a valid Procedure ID.");
      return;
    }

    axios
      .delete(`http://127.0.0.1:5000/api/medical-procedure/${procedureId}`)
      .then((response) => {
        setMessage(response.data.message);
        setError("");
      })
      .catch((err) => {
        if (err.response) {
          setError(err.response.data.error || "Failed to delete the medical procedure.");
        } else {
          setError("Network error. Please try again.");
        }
        setMessage("");
      });
  };

  return (
    <div>
      <h1>Delete Medical Procedure</h1>
      <div>
        <label>
          Procedure ID:
          <input
            type="text"
            value={procedureId}
            onChange={(e) => setProcedureId(e.target.value)}
          />
        </label>
        <button onClick={handleDelete}>Delete</button>
      </div>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default DeleteMedicalProcedure;
