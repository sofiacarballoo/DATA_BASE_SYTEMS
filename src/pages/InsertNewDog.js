import React, { useState } from "react";
import axios from "axios";

function InsertNewDog({ staffId }) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: "",
    breed: "",
    age: "",
    adoptabilityScore: "",
    sex: "",
    initialStatus: "",
    kennelNo: "",
    dateStartAvailability: "",
    spayedNeutered: false,
    arrivalDate: "",
    mainImageUrl: "",
    extraImageUrls: "",
  });
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleNextStep = () => {
    setStep(step + 1);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const data = {
      ...formData,
      staffID: staffId,
      age: parseInt(formData.age),
      adoptabilityScore: parseFloat(formData.adoptabilityScore),
    };

    axios
      .post("http://127.0.0.1:5000/api/insert-dog", data)
      .then((response) => {
        setMessage(response.data.message);
        setError("");
      })
      .catch((err) => {
        setError("Error adding dog. Please try again.");
        setMessage("");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Insert New Dog</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}

      <form onSubmit={handleSubmit}>
        {step === 1 && (
          <div>
            <label>Name:</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
            <button type="button" onClick={handleNextStep}>Next</button>
          </div>
        )}
        {/* Additional steps similar to above for breed, age, etc. */}
        <div>
          <label>Initial Status:</label>
          <select
            name="initialStatus"
            value={formData.initialStatus}
            onChange={handleChange}
            required
          >
            <option value="">Select Initial Status</option>
            <option value="available">Available</option>
            <option value="undergoing treatment">Undergoing Treatment</option>
            <option value="not ready">Not Ready</option>
          </select>
          {formData.initialStatus === "available" && (
            <div>
              <label>Kennel Number:</label>
              <input
                type="text"
                name="kennelNo"
                value={formData.kennelNo}
                onChange={handleChange}
                required
              />
              <label>Start Availability Date:</label>
              <input
                type="date"
                name="dateStartAvailability"
                value={formData.dateStartAvailability}
                onChange={handleChange}
                required
              />
            </div>
          )}
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
}

export default InsertNewDog;
