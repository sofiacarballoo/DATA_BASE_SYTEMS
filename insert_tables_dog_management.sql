-- Insert into Shelter
INSERT INTO Shelter (phoneNumber, address, name) 
VALUES
    ('123-456-7890', '123 Dog St, Cityville', 'City Dog Pound'),
    ('987-654-3210', '456 Pet Ave, Townsville', 'Townsville Animal Shelter'),
    ('555-123-4567', '789 Adoption Lane, Petville', 'Petville Animal Center'),
    ('444-987-6543', '101 Humane Rd, Animalton', 'Animalton Shelter'),
    ('333-555-1234', '202 Pawprint Blvd, Barktown', 'Barktown Animal Rescue');

-- Insert into Staff
INSERT INTO Staff (name) 
VALUES
    ('John Doe'),
    ('Jane Smith'),
    ('Alice Johnson'),
    ('Bob Martin'),
    ('Carla White'),
    ('David Brown');

-- Insert into Dog
INSERT INTO Dog (name, breed, sex, age, adoptabilityScore, arrivalDate, spayedNeuteredStatus) 
VALUES
    ('Rex', 'German Shepherd', 'Male', 3, 8.5, '2024-01-01', TRUE),
    ('Bella', 'Labrador Retriever', 'Female', 2, 9.0, '2024-01-05', TRUE),
    ('Max', 'Bulldog', 'Male', 4, 7.5, '2024-02-10', FALSE),
    ('Milo', 'Beagle', 'Male', 1, 8.0, '2024-03-15', TRUE),
    ('Daisy', 'Golden Retriever', 'Female', 5, 8.8, '2024-02-20', TRUE),
    ('Charlie', 'Poodle', 'Male', 2, 7.0, '2024-03-01', TRUE),
    ('Sadie', 'Boxer', 'Female', 3, 6.5, '2024-01-25', FALSE),
    ('Oscar', 'Shih Tzu', 'Male', 1, 9.2, '2024-03-10', TRUE),
    ('Zoe', 'Rottweiler', 'Female', 6, 6.0, '2024-02-05', TRUE),
    ('Rocky', 'Doberman', 'Male', 2, 8.0, '2024-01-30', TRUE);

-- Insert into Dog_Image
INSERT INTO Dog_Image (dogID, imageUrl, isMain)
VALUES
    (1, 'https://example.com/images/rex.jpg', TRUE),
    (2, 'https://example.com/images/bella.jpg', TRUE),
    (3, 'https://example.com/images/max.jpg', FALSE),
    (4, 'https://example.com/images/milo.jpg', TRUE),
    (5, 'https://example.com/images/daisy.jpg', TRUE),
    (6, 'https://example.com/images/charlie.jpg', TRUE),
    (7, 'https://example.com/images/sadie.jpg', FALSE),
    (8, 'https://example.com/images/oscar.jpg', TRUE),
    (9, 'https://example.com/images/zoe.jpg', TRUE),
    (10, 'https://example.com/images/rocky.jpg', FALSE);

-- Insert into Medical_Procedure
INSERT INTO Medical_Procedure (dogID, procedureDate, typeOfProcedure)
VALUES
    (1, '2024-01-10', 'Vaccination'),
    (2, '2024-01-12', 'Spay Surgery'),
    (3, '2024-02-15', 'Vaccination'),
    (4, '2024-03-20', 'Check-up'),
    (5, '2024-02-18', 'Vaccination'),
    (6, '2024-03-05', 'Spay Surgery'),
    (7, '2024-01-28', 'Check-up'),
    (8, '2024-03-15', 'Vaccination'),
    (9, '2024-02-10', 'Spay Surgery'),
    (10, '2024-01-25', 'Check-up');

-- Insert into Vaccine
INSERT INTO Vaccine (dogID, vaccineType, vaccineDate)
VALUES
    (1, 'Rabies', '2024-01-10'),
    (2, 'Distemper', '2024-01-12'),
    (3, 'Parvovirus', '2024-02-15'),
    (4, 'Leptospirosis', '2024-03-20'),
    (5, 'Canine Flu', '2024-02-18'),
    (6, 'Rabies', '2024-03-05'),
    (7, 'Parvovirus', '2024-01-28'),
    (8, 'Distemper', '2024-03-15'),
    (9, 'Leptospirosis', '2024-02-10'),
    (10, 'Canine Flu', '2024-01-25');

-- Insert into Status_Record
INSERT INTO Status_Record (dogID, recordDate)
VALUES
    (1, '2024-01-01'),
    (2, '2024-01-05'),
    (3, '2024-02-10'),
    (4, '2024-03-15'),
    (5, '2024-02-20'),
    (6, '2024-03-01'),
    (7, '2024-01-25'),
    (8, '2024-03-10'),
    (9, '2024-02-05'),
    (10, '2024-01-30');

-- Insert into Availability_Record
INSERT INTO Availability_Record (recordID, dateStartAvailability, kennelNo)
VALUES
    (1, '2024-01-01', 101),
    (2, '2024-01-05', 102),
    (3, '2024-02-10', 103),
    (4, '2024-03-15', 104),
    (5, '2024-02-20', 105),
    (6, '2024-03-01', 106),
    (7, '2024-01-25', 107),
    (8, '2024-03-10', 108),
    (9, '2024-02-05', 109),
    (10, '2024-01-30', 110);

-- Insert into Natural_Death_Record
INSERT INTO Natural_Death_Record (recordID, causeOfDeath)
VALUES
    (1, 'Heart Failure'),
    (2, 'Cancer'),
    (3, 'Old Age');

-- Insert into Euthanasia_Record
INSERT INTO Euthanasia_Record (recordID, reasonDescription)
VALUES
    (4, 'Severe Injury'),
    (5, 'Behavioral Issues');

-- Insert into Adoption_Record
INSERT INTO Adoption_Record (recordID, adoptionType)
VALUES
    (1, 'Standard Adoption'),
    (2, 'Emergency Adoption'),
    (3, 'Senior Adoption');

-- Insert into Adopter
INSERT INTO Adopter (SSN, shelterID, name, phoneNumber, address)
VALUES
    (123456789, 1, 'Alice Johnson', '555-123-4567', '789 Adopter Rd, Cityville'),
    (987654321, 2, 'Bob Smith', '555-987-6543', '456 Pet Lover Blvd, Townsville'),
    (112233445, 3, 'Charlie Evans', '555-112-2334', '321 New Home St, Petville'),
    (223344556, 4, 'David Adams', '555-223-3445', '987 Greenway Ave, Animalton'),
    (334455667, 5, 'Emma Turner', '555-334-4556', '654 Paws Rd, Barktown');

-- Insert into Is_Responsible_For
INSERT INTO Is_Responsible_For (dogID, shelterID)
VALUES
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 2),
    (5, 3),
    (6, 3),
    (7, 4),
    (8, 4),
    (9, 5),
    (10, 5);

-- Insert into Registers
INSERT INTO Registers (dogID, staffID)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 1),
    (8, 2),
    (9, 3),
    (10, 4);

-- Insert into Works_at
INSERT INTO Works_at (staffID, shelterID)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 1);
