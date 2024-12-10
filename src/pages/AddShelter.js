import React, { useState } from "react";
import axios from "axios";

function InsertShelter() {
  const [shelterData, setShelterData] = useState({
    name: "",
    address: "",
    phoneNumber: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setShelterData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Submit form data
  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("http://127.0.0.1:5000/api/insert-shelter", shelterData)
      .then((response) => {
        setMessage(response.data.message);
        setError(""); // Clear error
      })
      .catch((err) => {
        setMessage(""); // Clear success message
        setError("Error adding shelter. Please try again.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Insert New Shelter</h1>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <label>Name: </label>
        <input
          type="text"
          name="name"
          value={shelterData.name}
          onChange={handleChange}
          placeholder="Enter shelter name"
          required
        />
        <br />

        <label>Address: </label>
        <input
          type="text"
          name="address"
          value={shelterData.address}
          onChange={handleChange}
          placeholder="Enter shelter address"
          required
        />
        <br />

        <label>Phone Number: </label>
        <input
          type="text"
          name="phoneNumber"
          value={shelterData.phoneNumber}
          onChange={handleChange}
          placeholder="Enter phone number"
          required
        />
        <br />

        <button type="submit">Add Shelter</button>
      </form>
    </div>
  );
}

export default InsertShelter;
