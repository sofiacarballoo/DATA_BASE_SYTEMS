import React, { useState } from "react";
import axios from "axios";

function UpdateMedicalRecords() {
  const [dogId, setDogId] = useState("");
  const [choice, setChoice] = useState("");
  const [spayedNeutered, setSpayedNeutered] = useState(null);
  const [vaccineId, setVaccineId] = useState("");
  const [vaccineChoice, setVaccineChoice] = useState("");
  const [newVaccineType, setNewVaccineType] = useState("");
  const [newVaccineDate, setNewVaccineDate] = useState("");
  const [procedureId, setProcedureId] = useState("");
  const [procedureChoice, setProcedureChoice] = useState("");
  const [newProcedureType, setNewProcedureType] = useState("");
  const [newProcedureDate, setNewProcedureDate] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = () => {
    if (!dogId || !choice) {
      setError("Please fill in all required fields.");
      return;
    }

    const data = {
      dogID: dogId,
      choice: choice,
    };

    if (choice === "1") {
      if (spayedNeutered === null) {
        setError("Please specify spayed/neutered status.");
        return;
      }
      data.spayedNeutered = spayedNeutered;
    }

    if (choice === "2") {
      if (!vaccineId || !vaccineChoice) {
        setError("Please select vaccine ID and choice.");
        return;
      }
      data.vaccineID = vaccineId;
      data.vaccineChoice = vaccineChoice;
      if (vaccineChoice === "1") data.newVaccineType = newVaccineType;
      if (vaccineChoice === "2") data.newVaccineDate = newVaccineDate;
    }

    if (choice === "3") {
      if (!procedureId || !procedureChoice) {
        setError("Please select procedure ID and choice.");
        return;
      }
      data.procedureID = procedureId;
      data.procedureChoice = procedureChoice;
      if (procedureChoice === "1") data.newProcedureType = newProcedureType;
      if (procedureChoice === "2") data.newProcedureDate = newProcedureDate;
    }

    axios
      .post("http://127.0.0.1:5000/api/update-medical-records", data)
      .then((response) => {
        setMessage(response.data.message);
        setError("");
      })
      .catch((err) => {
        setError("Failed to update medical records.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Update Medical Records</h1>
      <div>
        <label>Dog ID:</label>
        <input
          type="text"
          value={dogId}
          onChange={(e) => setDogId(e.target.value)}
        />
      </div>
      <div>
        <label>What would you like to update?</label>
        <select onChange={(e) => setChoice(e.target.value)}>
          <option value="">Select</option>
          <option value="1">Spayed/Neutered Status</option>
          <option value="2">Vaccine Record</option>
          <option value="3">Medical Procedure Record</option>
        </select>
      </div>

      {choice === "1" && (
        <div>
          <label>Is the dog spayed/neutered?</label>
          <select onChange={(e) => setSpayedNeutered(e.target.value === "yes")}>
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>
      )}

      {choice === "2" && (
        <div>
          <label>Vaccine ID:</label>
          <input
            type="text"
            value={vaccineId}
            onChange={(e) => setVaccineId(e.target.value)}
          />
          <label>What would you like to update?</label>
          <select onChange={(e) => setVaccineChoice(e.target.value)}>
            <option value="">Select</option>
            <option value="1">Vaccine Type</option>
            <option value="2">Vaccine Date</option>
          </select>
          {vaccineChoice === "1" && (
            <input
              type="text"
              placeholder="New Vaccine Type"
              value={newVaccineType}
              onChange={(e) => setNewVaccineType(e.target.value)}
            />
          )}
          {vaccineChoice === "2" && (
            <input
              type="date"
              value={newVaccineDate}
              onChange={(e) => setNewVaccineDate(e.target.value)}
            />
          )}
        </div>
      )}

      {choice === "3" && (
        <div>
          <label>Procedure ID:</label>
          <input
            type="text"
            value={procedureId}
            onChange={(e) => setProcedureId(e.target.value)}
          />
          <label>What would you like to update?</label>
          <select onChange={(e) => setProcedureChoice(e.target.value)}>
            <option value="">Select</option>
            <option value="1">Type of Procedure</option>
            <option value="2">Procedure Date</option>
          </select>
          {procedureChoice === "1" && (
            <input
              type="text"
              placeholder="New Procedure Type"
              value={newProcedureType}
              onChange={(e) => setNewProcedureType(e.target.value)}
            />
          )}
          {procedureChoice === "2" && (
            <input
              type="date"
              value={newProcedureDate}
              onChange={(e) => setNewProcedureDate(e.target.value)}
            />
          )}
        </div>
      )}

      <button onClick={handleSubmit}>Update Medical Record</button>

      {message && <p>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default UpdateMedicalRecords;
