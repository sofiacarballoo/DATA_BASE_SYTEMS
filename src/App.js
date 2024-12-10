import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import StaffSelection from "./pages/StaffSelection";
import Menu from "./pages/Menu";
import InsertNewDog from "./pages/InsertNewDog";
import InsertVaccineRecord from "./pages/InsertVaccineRecord";
import AddAdopter from "./pages/AddAdopter";
import AddShelter from "./pages/AddShelter";
import DeleteDog from "./pages/DeleteDog";
import DeleteMedicalRecord from "./pages/DeleteMedicalRecord";
import DeleteShelter from "./pages/DeleteShelter";
import DeleteStaff from "./pages/DeleteStaff";
import DeleteVaccine from "./pages/DeleteVaccine";
import GetMostRecentDogStatus from "./pages/GetMostRecentDogStatus";
import InsertMedicalProcedureRecord from "./pages/InsertMedicalProcedureRecord";
import ModifyDogStatus from "./pages/ModifyDogStatus";
import PrintAllAdopters from "./pages/PrintAllAdopters";
import PrintAllAvailableDogs from "./pages/PrintAllAvailableDogs";
import PrintAllShelters from "./pages/PrintAllShelters";
import PrintDogsRegisteredByStaff from "./pages/PrintDogsRegisteredByStaff";
import PrintMedicalRecords from "./pages/PrintMedicalRecords";
import UpdateMedicalRecord from "./pages/UpdateMedicalRecord";
import UpdateShelter from "./pages/UpdateShelter";


function App() {
  const [staffId, setStaffId] = useState(null);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<StaffSelection setStaffId={setStaffId} />} />
        <Route path="/menu" element={<Menu staffId={staffId} />} />
        <Route path="/insert-new-dog" element={<InsertNewDog />} />
        <Route path="/insert-vaccine-record" element={<InsertVaccineRecord />} />
        <Route path="/add-adopter" element={<AddAdopter />} />
        <Route path="/add-shelter" element={<AddShelter />} />
        <Route path="/delete-dog" element={<DeleteDog />} />
        <Route path="/delete-medical-record" element={<DeleteMedicalRecord />} />
        <Route path="/delete-shelter" element={<DeleteShelter />} />
        <Route path="/delete-staff" element={<DeleteStaff />} />
        <Route path="/delete-vaccine" element={<DeleteVaccine />} />
        <Route path="/get-most-recent-dog-status" element={<GetMostRecentDogStatus />} />
        <Route path="/insert-medical-procedure-record" element={<InsertMedicalProcedureRecord />} />
        <Route path="/insert-vaccine-record" element={<InsertVaccineRecord />} />
        <Route path="/modify-dog-status" element={<ModifyDogStatus />} />
        <Route path="/print-all-adopters" element={<PrintAllAdopters />} />
        <Route path="/print-all-available-dogs" element={<PrintAllAvailableDogs />} />
        <Route path="/print-all-shelters" element={<PrintAllShelters />} />
        <Route path="/print-dogs-registered-by-staff" element={<PrintDogsRegisteredByStaff />} />
        <Route path="/print-medical-records" element={<PrintMedicalRecords />} />
        <Route path="/update-medical-record" element={<UpdateMedicalRecord />} />
        <Route path="/update-shelter" element={<UpdateShelter/>} />
        

      </Routes>
    </Router>
  );
}

export default App;
