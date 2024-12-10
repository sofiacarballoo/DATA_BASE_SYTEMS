import React, { useState, useEffect } from "react";
import axios from "axios";

function AvailableDogs() {
  const [dogs, setDogs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch available dogs from the backend
    axios
      .get("http://127.0.0.1:5000/api/available-dogs")
      .then((response) => {
        setDogs(response.data); // Set the dogs list
        setError(""); // Clear any previous errors
      })
      .catch((err) => {
        setError("Error fetching available dogs.");
        console.error(err);
      });
  }, []);

  return (
    <div>
      <h1>Available Dogs</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {dogs.length > 0 ? (
        <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Dog ID</th>
              <th>Name</th>
              <th>Breed</th>
              <th>Sex</th>
            </tr>
          </thead>
          <tbody>
            {dogs.map((dog) => (
              <tr key={dog.dogID}>
                <td>{dog.dogID}</td>
                <td>{dog.name}</td>
                <td>{dog.breed}</td>
                <td>{dog.sex}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No dogs available at the moment.</p>
      )}
    </div>
  );
}

export default AvailableDogs;
