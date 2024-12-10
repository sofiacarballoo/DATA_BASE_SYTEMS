import React from "react";
import { useNavigate } from "react-router-dom";

function Menu({ staffId }) {
  const navigate = useNavigate(); // Hook for navigation

  const handleOptionClick = (option) => {
    console.log(`Staff ID: ${staffId}, Option: ${option}`);
    // Navigate to the respective page based on the option selected
    switch (option) {
      case 1:
        navigate("/insert-new-dog");
        break;
      case 2:
        navigate("/insert-vaccine-record");
        break;
      case 3:
        navigate("/insert-medical-procedure-record");
        break;
      case 4:
        navigate("/delete-dog");
        break;
      case 5:
        navigate("/delete-vaccine");
        break;
      case 6:
        navigate("/delete-medical-record");
        break;
      case 7:
        navigate("/print-medical-records");
        break;
      case 8:
        navigate("/update-medical-record");
        break;
      case 9:
        navigate("/delete-staff");
        break;
      case 10:
        navigate("/print-dogs-registered-by-staff");
        break;
      case 11:
        navigate("/update-shelter");
        break;
      case 12:
        navigate("/delete-shelter");
        break;
      case 13:
        navigate("/add-shelter");
        break;
      case 14:
        navigate("/add-adopter");
        break;
      case 15:
        navigate("/modify-dog-status");
        break;
      case 16:
        navigate("/get-most-recent-dog-status");
        break;
      case 17:
        navigate("/print-all-available-dogs");
        break;
      case 18:
        navigate("/print-all-adopters");
        break;
      case 19:
        navigate("/print-all-shelters");
        break;
      case 20:
        navigate("/"); 
        break;
      default:
        console.error("Invalid option selected");
    }
  };

  const menuOptions = [
    "Insert New Dog",
    "Insert Vaccine Record",
    "Insert Medical Procedure Record",
    "Delete Dog",
    "Delete Vaccine",
    "Delete Medical Record",
    "Print Medical Records",
    "Update Medical Record",
    "Delete Staff",
    "Print Dogs Registered By Staff Info",
    "Update Shelter",
    "Delete Shelter",
    "Add Shelter",
    "Add Adopter",
    "Modify Dog Status",
    "Get Most Recent Dog Status",
    "Print Available Dogs",
    "Print All Adopters",
    "Print All Shelters",
    "Exit",
  ];

  return (
    <div>
      <h1>Main Menu</h1>
      <p>Staff ID: {staffId}</p>
      <ul>
        {menuOptions.map((option, index) => (
          <li key={index}>
            <button onClick={() => handleOptionClick(index + 1)}>
              {option}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Menu;
