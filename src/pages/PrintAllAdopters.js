import React, { useEffect, useState } from "react";
import axios from "axios";

function AdoptersList() {
  const [adopters, setAdopters] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch adopters from the backend
    axios
      .get("http://127.0.0.1:5000/api/adopters")
      .then((response) => {
        setAdopters(response.data); // Set the adopters list
        setError(""); // Clear any previous errors
      })
      .catch((err) => {
        setError("Error fetching adopters list.");
        console.error(err);
      });
  }, []);

  return (
    <div>
      <h1>Adopters List</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {adopters.length > 0 ? (
        <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>SSN</th>
              <th>Shelter ID</th>
              <th>Name</th>
              <th>Phone Number</th>
              <th>Address</th>
            </tr>
          </thead>
          <tbody>
            {adopters.map((adopter, index) => (
              <tr key={index}>
                <td>{adopter.SSN}</td>
                <td>{adopter.shelterID}</td>
                <td>{adopter.name}</td>
                <td>{adopter.phoneNumber}</td>
                <td>{adopter.address}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No adopters found.</p>
      )}
    </div>
  );
}

export default AdoptersList;

