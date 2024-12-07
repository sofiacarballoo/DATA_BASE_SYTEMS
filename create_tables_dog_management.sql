CREATE TABLE Shelter (
    shelterID INT PRIMARY KEY AUTO_INCREMENT,
    phoneNumber VARCHAR(15),
    address VARCHAR(255),
    name VARCHAR(100)
);

CREATE TABLE Staff (
    staffID INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Dog (
    dogID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    breed VARCHAR(100),
    sex ENUM('Female', 'Male'),
    age INT, 
    adoptabilityScore FLOAT, 
    arrivalDate DATE,
    spayedNeuteredStatus BOOLEAN
);

CREATE TABLE Dog_Image (
    imageID INT PRIMARY KEY AUTO_INCREMENT,
    dogID INT,
    imageUrl VARCHAR(255), 
    isMain BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (dogID) REFERENCES Dog(dogID)
);

CREATE TABLE Medical_Procedure (
    procedureID INT PRIMARY KEY AUTO_INCREMENT, 
    dogID INT, 
    procedureDate DATE,
    typeOfProcedure VARCHAR(255),
    FOREIGN KEY (dogID) REFERENCES Dog(dogID)
);

CREATE TABLE Vaccine (
    vaccineID INT PRIMARY KEY AUTO_INCREMENT, 
    dogID INT,
    vaccineType VARCHAR(255),
    vaccineDate DATE,
    FOREIGN KEY (dogID) REFERENCES Dog(dogID)
);

CREATE TABLE Status_Record (
    recordID INT PRIMARY KEY AUTO_INCREMENT, 
    dogID INT,
    recordDate DATE,
    FOREIGN KEY (dogID) REFERENCES Dog(dogID)
);

CREATE TABLE Availability_Record (
    recordID INT PRIMARY KEY AUTO_INCREMENT,
    dateStartAvailability DATE,
    kennelNo INT,
    FOREIGN KEY (recordID) REFERENCES Status_Record(recordID)
);

CREATE TABLE Natural_Death_Record (
    recordID INT PRIMARY KEY AUTO_INCREMENT,
    causeOfDeath VARCHAR(255),
    FOREIGN KEY (recordID) REFERENCES Status_Record(recordID)
);

CREATE TABLE Euthanasia_Record (
    recordID INT PRIMARY KEY AUTO_INCREMENT,
    reasonDescription VARCHAR(255),
    FOREIGN KEY (recordID) REFERENCES Status_Record(recordID)
);

CREATE TABLE Adoption_Record (
    recordID INT PRIMARY KEY AUTO_INCREMENT,
    adoptionType VARCHAR(255),
    FOREIGN KEY (recordID) REFERENCES Status_Record(recordID)
);

CREATE TABLE Adopter (
    SSN INT PRIMARY KEY, -- AUTO_INCREMENT removed, as SSN is user-provided
    shelterID INT,
    name VARCHAR(100),
    phoneNumber VARCHAR(15),
    address VARCHAR(255),
    FOREIGN KEY (shelterID) REFERENCES Shelter(shelterID)
);

CREATE TABLE Is_Responsible_For (
    dogID INT,
    shelterID INT,
    PRIMARY KEY (dogID, shelterID),
    FOREIGN KEY (dogID) REFERENCES Dog(dogID),
    FOREIGN KEY (shelterID) REFERENCES Shelter(shelterID)
);

CREATE TABLE Registers (
    dogID INT,
    staffID INT,
    PRIMARY KEY (dogID, staffID),
    FOREIGN KEY (dogID) REFERENCES Dog(dogID),
    FOREIGN KEY (staffID) REFERENCES Staff(staffID)
);

CREATE TABLE Works_at (
    staffID INT,
    shelterID INT,
    PRIMARY KEY (staffID, shelterID),
    FOREIGN KEY (staffID) REFERENCES Staff(staffID),
    FOREIGN KEY (shelterID) REFERENCES Shelter(shelterID)
);
