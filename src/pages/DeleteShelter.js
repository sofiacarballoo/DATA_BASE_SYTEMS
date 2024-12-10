import React, { useState } from "react";
import axios from "axios";

function DeleteShelter() {
  const [shelterID, setShelterID] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!shelterID) {
      setError("Shelter ID is required.");
      setMessage("");
      return;
    }

    // Make a DELETE request to the backend
    axios
      .delete("http://127.0.0.1:5000/api/delete-shelter", {
        data: { shelterID: shelterID }, // Send shelterID in the request body
      })
      .then((response) => {
        setMessage(response.data.message);
        setError(""); // Clear error message
        setShelterID(""); // Reset input field
      })
      .catch((err) => {
        setMessage(""); // Clear success message
        setError("Error deleting shelter. Please try again.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Delete Shelter</h1>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>Shelter ID: </label>
        <input
          type="text"
          value={shelterID}
          onChange={(e) => setShelterID(e.target.value)}
          placeholder="Enter shelter ID"
          required
        />
        <button type="submit">Delete Shelter</button>
      </form>
    </div>
  );
}

export default DeleteShelter;

