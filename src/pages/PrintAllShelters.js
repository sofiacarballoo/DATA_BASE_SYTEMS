import React, { useEffect, useState } from "react";
import axios from "axios";

function SheltersList() {
  const [shelters, setShelters] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch shelters from the backend
    axios
      .get("http://127.0.0.1:5000/api/shelters")
      .then((response) => {
        setShelters(response.data); // Set the shelters list
        setError(""); // Clear any previous errors
      })
      .catch((err) => {
        setError("Error fetching shelters list.");
        console.error(err);
      });
  }, []);

  return (
    <div>
      <h1>Shelters List</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {shelters.length > 0 ? (
        <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Shelter ID</th>
              <th>Phone Number</th>
              <th>Address</th>
              <th>Name</th>
            </tr>
          </thead>
          <tbody>
            {shelters.map((shelter, index) => (
              <tr key={index}>
                <td>{shelter.shelterID}</td>
                <td>{shelter.phoneNumber}</td>
                <td>{shelter.address}</td>
                <td>{shelter.name}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No shelters found.</p>
      )}
    </div>
  );
}

export default SheltersList;
