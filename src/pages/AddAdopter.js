import React, { useState } from "react";
import axios from "axios";

function AddAdopter() {
  const [formData, setFormData] = useState({
    shelterID: "",
    SSN: "",
    name: "",
    address: "",
    phoneNumber: "",
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Submit the form data
  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate required fields
    if (!formData.shelterID || !formData.SSN || !formData.name || !formData.address || !formData.phoneNumber) {
      setError("All fields are required.");
      setMessage("");
      return;
    }

    // Make the POST request to the backend API
    axios
      .post("http://127.0.0.1:5000/api/adopters", formData)
      .then((response) => {
        setMessage(response.data.message);
        setError("");  // Clear error message
      })
      .catch((err) => {
        setMessage(""); // Clear success message
        setError("Error adding adopter. Please try again.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Add New Adopter</h1>

      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Shelter ID: </label>
          <input
            type="text"
            name="shelterID"
            value={formData.shelterID}
            onChange={handleChange}
            placeholder="Enter shelter ID"
            required
          />
        </div>

        <div>
          <label>SSN: </label>
          <input
            type="text"
            name="SSN"
            value={formData.SSN}
            onChange={handleChange}
            placeholder="Enter SSN"
            required
          />
        </div>

        <div>
          <label>Name: </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter adopter's name"
            required
          />
        </div>

        <div>
          <label>Address: </label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
            placeholder="Enter adopter's address"
            required
          />
        </div>

        <div>
          <label>Phone Number: </label>
          <input
            type="text"
            name="phoneNumber"
            value={formData.phoneNumber}
            onChange={handleChange}
            placeholder="Enter adopter's phone number"
            required
          />
        </div>

        <button type="submit">Add Adopter</button>
      </form>
    </div>
  );
}

export default AddAdopter;
