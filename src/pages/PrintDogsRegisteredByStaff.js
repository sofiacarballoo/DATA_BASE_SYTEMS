import React, { useEffect, useState } from "react";
import axios from "axios";

function StaffDogsList() {
  const [staffDogs, setStaffDogs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch data from the backend
    axios
      .get("http://127.0.0.1:5000/api/staff-dogs")
      .then((response) => {
        setStaffDogs(response.data); // Set the data
        setError(""); // Clear any previous errors
      })
      .catch((err) => {
        setError("Error fetching data.");
        console.error(err);
      });
  }, []);

  return (
    <div>
      <h1>Dogs Registered by Staff</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {staffDogs.length > 0 ? (
        <div>
          {staffDogs.map((staff, index) => (
            <div key={index}>
              <h2>Staff Name: {staff.staffName}</h2>
              {staff.dogs.length > 0 ? (
                <ul>
                  {staff.dogs.map((dog, idx) => (
                    <li key={idx}>
                      Dog ID: {dog.dogID}, Dog Name: {dog.dogName}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No dogs registered.</p>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p>No data available.</p>
      )}
    </div>
  );
}

export default StaffDogsList;
