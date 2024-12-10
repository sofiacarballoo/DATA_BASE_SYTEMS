import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import './StaffSelection.css';  


function StaffSelection({ setStaffId }) {
  const [staffList, setStaffList] = useState([]);
  const [newStaffName, setNewStaffName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false); // New loading state
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    axios
      .get("http://127.0.0.1:5000/api/staff/")
      .then((response) => {
        setStaffList(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Error fetching staff list.");
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleAddStaff = () => {
    if (!newStaffName) {
      setError("Staff name is required.");
      return;
    }

    axios
      .post("http://127.0.0.1:5000/api/staff/", { name: newStaffName })
      .then((response) => {
        const { staffId } = response.data;
        setStaffId(staffId);
        setNewStaffName(""); // Clear input
        setError(""); // Clear error
        navigate("/menu");
      })
      .catch((err) => {
        setError("Error adding new staff.");
        console.error(err);
      });
  };

  return (
    <div>
      <h1>Welcome to Dog Management</h1>
      <h2>Staff Selection</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {loading ? (
        <p>Loading staff list...</p>
      ) : (
        <>
          <h3>Existing Staff</h3>
          {staffList.length > 0 ? (
            <ul>
              {staffList.map((staff) => (
                <li key={staff.staffId}>
                  {staff.name}{" "}
                  <button
                    onClick={() => {
                      setStaffId(staff.staffId);
                      navigate("/menu");
                    }}
                  >
                    Select
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p>No staff found.</p>
          )}
        </>
      )}
      <h3>Add New Staff</h3>
      <input
        type="text"
        placeholder="Enter staff name"
        value={newStaffName}
        onChange={(e) => setNewStaffName(e.target.value)}
      />
      <button onClick={handleAddStaff}>Add Staff</button>
    </div>
  );
}

export default StaffSelection;
