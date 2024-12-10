import React, { useState } from 'react';
import axios from 'axios';

function InsertVaccine() {
  const [dogId, setDogId] = useState('');
  const [vaccineType, setVaccineType] = useState('');
  const [vaccineDate, setVaccineDate] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = () => {
    if (!dogId || !vaccineType || !vaccineDate) {
      setError("Please fill in all fields.");
      return;
    }

    axios
      .post("http://127.0.0.1:5000/api/vaccine", { dogID: dogId, vaccineType, vaccineDate })
      .then((response) => {
        setMessage(response.data.message);
        setError('');
      })
      .catch((err) => {
        setError("Failed to add vaccine.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Insert Vaccine Record</h1>
      <div>
        <label>Dog ID:</label>
        <input type="text" value={dogId} onChange={(e) => setDogId(e.target.value)} />
      </div>
      <div>
        <label>Vaccine Type:</label>
        <input type="text" value={vaccineType} onChange={(e) => setVaccineType(e.target.value)} />
      </div>
      <div>
        <label>Vaccine Date:</label>
        <input type="date" value={vaccineDate} onChange={(e) => setVaccineDate(e.target.value)} />
      </div>
      <button onClick={handleSubmit}>Add Vaccine</button>
      {message && <p>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default InsertVaccine;
