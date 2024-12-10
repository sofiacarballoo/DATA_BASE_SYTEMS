import React, { useState } from "react";
import axios from "axios";

function MedicalHistory() {
  const [dogId, setDogId] = useState("");
  const [medicalHistory, setMedicalHistory] = useState(null);
  const [error, setError] = useState("");

  const fetchMedicalHistory = () => {
    axios
      .get(`http://127.0.0.1:5000/api/medical-history/${dogId}`)
      .then((response) => {
        setMedicalHistory(response.data);
        setError(""); // Clear any previous errors
      })
      .catch((err) => {
        setError("Error fetching medical history.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Medical History</h1>

      <div>
        <label>Enter Dog ID:</label>
        <input
          type="number"
          value={dogId}
          onChange={(e) => setDogId(e.target.value)}
          placeholder="Dog ID"
        />
        <button onClick={fetchMedicalHistory}>Get Medical History</button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {medicalHistory && (
        <div>
          <h2>Dog ID: {medicalHistory.dogID}</h2>
          <p>Spayed/Neutered: {medicalHistory.spayedNeuteredStatus}</p>

          <h3>Vaccination History:</h3>
          {medicalHistory.vaccines.length > 0 ? (
            <ul>
              {medicalHistory.vaccines.map((vaccine) => (
                <li key={vaccine.vaccineID}>
                  Vaccine ID: {vaccine.vaccineID}, Type: {vaccine.vaccineType}, Date: {vaccine.vaccineDate}
                </li>
              ))}
            </ul>
          ) : (
            <p>No vaccines found.</p>
          )}

          <h3>Medical Procedures:</h3>
          {medicalHistory.procedures.length > 0 ? (
            <ul>
              {medicalHistory.procedures.map((procedure) => (
                <li key={procedure.procedureID}>
                  Procedure ID: {procedure.procedureID}, Type: {procedure.typeOfProcedure}, Date: {procedure.procedureDate}
                </li>
              ))}
            </ul>
          ) : (
            <p>No medical procedures found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default MedicalHistory;
