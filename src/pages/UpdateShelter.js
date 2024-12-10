import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function UpdateShelter() {
  const [formData, setFormData] = useState({
    shelterID: "",
    name: "",
    address: "",
    phoneNumber: "",
  });

  const [updateOption, setUpdateOption] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleOptionChange = (e) => {
    setUpdateOption(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Ensure the user has selected an option to update
    if (!updateOption) {
      setError("Please select an option to update.");
      return;
    }

    // Send the update request to the backend
    axios
      .put("http://127.0.0.1:5000/api/update-shelter", formData)
      .then((response) => {
        setMessage(response.data.message);
        setError(""); // Clear error
      })
      .catch((err) => {
        setError("Error updating shelter. Please try again.");
        console.error(err);
      });
  };
  

  return (
    <div>
      <h1>Update Shelter</h1>

      {/* Display error or success message */}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Shelter ID:
            <input
              type="text"
              name="shelterID"
              value={formData.shelterID}
              onChange={handleChange}
              placeholder="Enter shelter ID"
              required
            />
          </label>
        </div>

        <div>
          <label>
            What would you like to update?
            <select onChange={handleOptionChange} value={updateOption} required>
              <option value="">Select an option</option>
              <option value="name">Name</option>
              <option value="address">Address</option>
              <option value="phoneNumber">Phone Number</option>
            </select>
          </label>
        </div>

        {updateOption && (
          <div>
            {updateOption === "name" && (
              <div>
                <label>
                  New Shelter Name:
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Enter new shelter name"
                  />
                </label>
              </div>
            )}

            {updateOption === "address" && (
              <div>
                <label>
                  New Shelter Address:
                  <input
                    type="text"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    placeholder="Enter new address"
                  />
                </label>
              </div>
            )}

            {updateOption === "phoneNumber" && (
              <div>
                <label>
                  New Shelter Phone Number:
                  <input
                    type="text"
                    name="phoneNumber"
                    value={formData.phoneNumber}
                    onChange={handleChange}
                    placeholder="Enter new phone number"
                  />
                </label>
              </div>
            )}
          </div>
        )}

        <button type="submit">Update Shelter</button>
      </form>
    </div>
  );
}

export default UpdateShelter;
