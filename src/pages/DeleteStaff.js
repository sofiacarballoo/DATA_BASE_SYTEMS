import React, { useState } from "react";
import axios from "axios";

function DeleteStaff() {
  const [staffID, setStaffID] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!staffID) {
      setError("Staff ID is required.");
      setMessage("");
      return;
    }

    // Make a DELETE request to the backend
    axios
      .delete("http://127.0.0.1:5000/api/delete-staff", {
        data: { staffID: staffID }, // Send staffID as part of the request body
      })
      .then((response) => {
        setMessage(response.data.message);
        setError(""); // Clear error message
        setStaffID(""); // Reset input field
      })
      .catch((err) => {
        setMessage(""); // Clear success message
        setError("Error deleting staff. Please try again.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Delete Staff</h1>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>Staff ID: </label>
        <input
          type="text"
          value={staffID}
          onChange={(e) => setStaffID(e.target.value)}
          placeholder="Enter staff ID"
          required
        />
        <button type="submit">Delete Staff</button>
      </form>
    </div>
  );
}

export default DeleteStaff;
