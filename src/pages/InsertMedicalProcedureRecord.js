import React, { useState } from 'react';
import axios from 'axios';

function InsertMedicalProcedure() {
  const [dogId, setDogId] = useState('');
  const [procedureDate, setProcedureDate] = useState('');
  const [typeOfProcedure, setTypeOfProcedure] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!dogId || !procedureDate || !typeOfProcedure) {
      setError("Please fill in all fields.");
      return;
    }

    axios
      .post("http://127.0.0.1:5000/api/medical-procedure", { dogID: dogId, procedureDate, typeOfProcedure })
      .then((response) => {
        setMessage(response.data.message);
        setError('');
      })
      .catch((err) => {
        setError("Failed to add medical procedure.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Insert Medical Procedure Record</h1>
      <div>
        <label>Dog ID:</label>
        <input type="text" value={dogId} onChange={(e) => setDogId(e.target.value)} />
      </div>
      <div>
        <label>Procedure Date:</label>
        <input type="date" value={procedureDate} onChange={(e) => setProcedureDate(e.target.value)} />
      </div>
      <div>
        <label>Type of Procedure:</label>
        <input type="text" value={typeOfProcedure} onChange={(e) => setTypeOfProcedure(e.target.value)} />
      </div>
      <button onClick={handleSubmit}>Add Medical Procedure</button>
      {message && <p>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default InsertMedicalProcedure;

