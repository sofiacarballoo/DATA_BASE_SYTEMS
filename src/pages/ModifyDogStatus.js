import React, { useState } from "react";
import axios from "axios";

function ModifyDogStatus() {
  const [dogId, setDogId] = useState("");
  const [statusType, setStatusType] = useState("");
  const [reason, setReason] = useState("");
  const [causeOfDeath, setCauseOfDeath] = useState("");
  const [adoptionType, setAdoptionType] = useState("");
  const [adopterSSN, setAdopterSSN] = useState("");
  const [adopterName, setAdopterName] = useState("");
  const [adopterPhone, setAdopterPhone] = useState("");
  const [adopterAddress, setAdopterAddress] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = () => {
    if (!dogId || !statusType) {
      setError("Please provide dog ID and status type.");
      return;
    }

    const data = {
      dogID: dogId,
      statusType: statusType,
      reason: statusType === "euthanized" ? reason : null,
      causeOfDeath: statusType === "natural death" ? causeOfDeath : null,
      adoptionType: statusType === "adopted" ? adoptionType : null,
      adopterSSN: statusType === "adopted" ? adopterSSN : null,
      adopterName: statusType === "adopted" ? adopterName : null,
      adopterPhone: statusType === "adopted" ? adopterPhone : null,
      adopterAddress: statusType === "adopted" ? adopterAddress : null,
    };

    axios
      .post("http://127.0.0.1:5000/api/modify-dog-status", data)
      .then((response) => {
        setMessage(response.data.message);
        setError("");
      })
      .catch((err) => {
        setError("Failed to update dog status.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Modify Dog Status</h1>
      <div>
        <label>Dog ID:</label>
        <input
          type="text"
          value={dogId}
          onChange={(e) => setDogId(e.target.value)}
        />
      </div>
      <div>
        <label>Status Type:</label>
        <select onChange={(e) => setStatusType(e.target.value)}>
          <option value="">Select Status</option>
          <option value="euthanized">Euthanized</option>
          <option value="natural death">Natural Death</option>
          <option value="adopted">Adopted</option>
        </select>
      </div>

      {statusType === "euthanized" && (
        <div>
          <label>Reason for Euthanasia:</label>
          <input
            type="text"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          />
        </div>
      )}

      {statusType === "natural death" && (
        <div>
          <label>Cause of Death:</label>
          <input
            type="text"
            value={causeOfDeath}
            onChange={(e) => setCauseOfDeath(e.target.value)}
          />
        </div>
      )}

      {statusType === "adopted" && (
        <div>
          <label>Adoption Type:</label>
          <input
            type="text"
            value={adoptionType}
            onChange={(e) => setAdoptionType(e.target.value)}
          />
          <label>Adopter SSN:</label>
          <input
            type="text"
            value={adopterSSN}
            onChange={(e) => setAdopterSSN(e.target.value)}
          />
          <label>Adopter Name:</label>
          <input
            type="text"
            value={adopterName}
            onChange={(e) => setAdopterName(e.target.value)}
          />
          <label>Adopter Phone:</label>
          <input
            type="text"
            value={adopterPhone}
            onChange={(e) => setAdopterPhone(e.target.value)}
          />
          <label>Adopter Address:</label>
          <input
            type="text"
            value={adopterAddress}
            onChange={(e) => setAdopterAddress(e.target.value)}
          />
        </div>
      )}

      <button onClick={handleSubmit}>Update Status</button>

      {message && <p>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default ModifyDogStatus;
