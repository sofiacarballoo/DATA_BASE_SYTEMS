import React, { useEffect, useState } from 'react';
import axios from 'axios';

function AdoptersList() {
  const [adopters, setAdopters] = useState([]);  // state to store adopters
  const [loading, setLoading] = useState(true);   // state to handle loading
  const [error, setError] = useState(null);       // state to handle errors

  useEffect(() => {
    // Fetch adopters data from the Flask API
    axios.get('http://127.0.0.1:5000/api/adopters')
      .then(response => {
        setAdopters(response.data);   // set adopters in state
        setLoading(false);             // stop loading
      })
      .catch(error => {
        setError('Error fetching data');
        setLoading(false);             // stop loading even if there's an error
        console.error('There was an error fetching adopters:', error);
      });
  }, []);  // Empty dependency array to fetch only once when component mounts

  // If data is loading, show loading message
  if (loading) {
    return <div>Loading...</div>;
  }

  // If there's an error, show error message
  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>Adopter List</h2>
      <ul>
        {adopters.length === 0 ? (
          <p>No adopters found.</p>
        ) : (
          adopters.map(adopter => (
            <li key={adopter.SSN}>
              {adopter.name} - {adopter.phoneNumber}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default AdoptersList;
