import React, { useState } from "react";
import axios from "axios";

function DogStatus() {
  const [dogId, setDogId] = useState("");
  const [dogStatus, setDogStatus] = useState(null);
  const [error, setError] = useState("");

  const fetchDogStatus = () => {
    axios
      .get(`http://127.0.0.1:5000/api/dog-status/${dogId}`)
      .then((response) => {
        setDogStatus(response.data); // Set dog status data
        setError(""); // Clear any previous errors
      })
      .catch((err) => {
        setError("Error fetching dog status.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Dog Status</h1>

      <div>
        <label>Enter Dog ID:</label>
        <input
          type="number"
          value={dogId}
          onChange={(e) => setDogId(e.target.value)}
          placeholder="Dog ID"
        />
        <button onClick={fetchDogStatus}>Get Status</button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {dogStatus && (
        <div>
          <h2>Dog ID: {dogStatus.dogID}</h2>
          <p>Name: {dogStatus.name}</p>
          <p>Breed: {dogStatus.breed}</p>
          <p>Sex: {dogStatus.sex}</p>
          <p>Most Recent Status Date: {dogStatus.recordDate}</p>

          {dogStatus.status.isAvailable && (
            <div>
              <h3>Status: Available</h3>
              <p>Kennel No: {dogStatus.status.kennelNo}</p>
              <p>Date Start Availability: {dogStatus.status.dateStartAvailability}</p>
            </div>
          )}

          {dogStatus.status.isEuthanized && (
            <div>
              <h3>Status: Euthanized</h3>
              <p>Reason for Euthanasia: {dogStatus.status.reasonDescription}</p>
            </div>
          )}

          {dogStatus.status.isNaturalDeath && (
            <div>
              <h3>Status: Natural Death</h3>
              <p>Cause of Death: {dogStatus.status.causeOfDeath}</p>
            </div>
          )}

          {dogStatus.status.isAdopted && (
            <div>
              <h3>Status: Adopted</h3>
              <p>Adoption Type: {dogStatus.status.adoptionType}</p>
            </div>
          )}

          {!dogStatus.status.isAvailable && !dogStatus.status.isEuthanized && !dogStatus.status.isNaturalDeath && !dogStatus.status.isAdopted && (
            <p>Status: Unknown</p>
          )}
        </div>
      )}
    </div>
  );
}

export default DogStatus;

