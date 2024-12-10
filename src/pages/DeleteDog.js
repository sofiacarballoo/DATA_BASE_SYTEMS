import React, { useState } from 'react';
import axios from 'axios';

function DeleteDog() {
  const [dogId, setDogId] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleDelete = () => {
    if (!dogId) {
      setError('Please enter a dog ID');
      return;
    }

    axios
      .delete(`http://127.0.0.1:5000/api/delete-dog/${dogId}`)
      .then((response) => {
        setMessage(response.data.message);
        setError(''); // Clear any previous errors
      })
      .catch((err) => {
        setError(`Error: ${err.response ? err.response.data.error : err.message}`);
        setMessage(''); // Clear success message if error occurs
      });
  };

  return (
    <div>
      <h1>Delete Dog Record</h1>

      <div>
        <label>Enter Dog ID:</label>
        <input
          type="number"
          value={dogId}
          onChange={(e) => setDogId(e.target.value)}
          placeholder="Dog ID"
        />
        <button onClick={handleDelete}>Delete Dog</button>
      </div>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default DeleteDog;

