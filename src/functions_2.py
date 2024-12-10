import mysql.connector

# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gr@duate22",  # Replace with your MySQL root password
        database="dogmanagement"
    )

# Retrieve or add staff
def select_or_add_staff():
    db = connect_to_db()
    cursor = db.cursor()

    print("\nChoose an option:")
    print("1. Choose existing staff")
    print("2. Add new staff")

    choice = input("Enter your choice: ")

    if choice == '1':
        # Display existing staff names
        cursor.execute("SELECT staffID, name FROM Staff")
        staff_list = cursor.fetchall()
        
        if not staff_list:
            print("No existing staff found. Please add a new staff member.")
            return select_or_add_staff()
        
        print("Existing Staff:")
        for staff_id, name in staff_list:
            print(f"{staff_id}. {name}")
        
        staff_id = int(input("Enter the ID of the staff member to select: "))
    
    elif choice == '2':
        # Add a new staff member
        new_name = input("Enter new staff name: ")
        cursor.execute("INSERT INTO Staff (name) VALUES (%s)", (new_name,))
        db.commit()
        staff_id = cursor.lastrowid
        print(f"New staff member '{new_name}' added with ID {staff_id}")
    
    else:
        print("Invalid choice, please try again.")
        return select_or_add_staff()

    cursor.close()
    db.close()
    return staff_id

# Insert a new dog record with staff registration, status, availability, and images
def insert_dog(staff_id, name, breed, age, arrival_date, spayed_neutered, adoptability_score, sex, initial_status, kennel_no=None, date_start_availability=None, main_image_url=None, extra_image_urls=None):
    db = connect_to_db()
    cursor = db.cursor()

    # Insert dog record
    add_dog = """
    INSERT INTO Dog (name, breed, age, adoptabilityScore, arrivalDate, spayedNeuteredStatus, sex) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(add_dog, (name, breed, age, adoptability_score, arrival_date, spayed_neutered, sex))

    dog_id = cursor.lastrowid  # Get the last inserted dog ID

    # Record the dog registration by staff
    add_register = """
    INSERT INTO Registers (dogID, staffID) 
    VALUES (%s, %s)
    """
    cursor.execute(add_register, (dog_id, staff_id))

    # Insert status record
    add_status = """
    INSERT INTO Status_Record (recordDate, dogID) 
    VALUES (NOW(), %s)
    """
    cursor.execute(add_status, (dog_id,))
    status_id = cursor.lastrowid

    # Insert availability record if status is "available"
    if initial_status.lower() == "available":
        add_availability = """
        INSERT INTO Availability_Record (recordID, dateStartAvailability, kennelNo) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(add_availability, (status_id, date_start_availability, kennel_no))

    # Insert main image if provided
    if main_image_url:
        add_main_image = """
        INSERT INTO Dog_Image (dogID, imageUrl, isMain) 
        VALUES (%s, %s, TRUE)
        """
        cursor.execute(add_main_image, (dog_id, main_image_url))

    # Insert extra images if provided
    if extra_image_urls:
        for url in extra_image_urls.split(","):
            add_extra_image = """
            INSERT INTO Dog_Image (dogID, imageUrl, isMain) 
            VALUES (%s, %s, FALSE)
            """
            cursor.execute(add_extra_image, (dog_id, url.strip()))

    db.commit()
    print(f"Inserted dog record for {name} and registered by staff ID {staff_id}")
    cursor.close()
    db.close()

#insert new shelter
def insert_shelter(shelter_name, shelter_address, shelter_phone_number ):
    db = connect_to_db()
    cursor = db.cursor()

    # Insert dog record
    add_shelter = """
    INSERT INTO Shelter (name, address, phoneNumber) 
    VALUES (%s, %s, %s)
    """
    cursor.execute(add_shelter, (shelter_name, shelter_address, shelter_phone_number))

    shelter_id = cursor.lastrowid 

    db.commit()
    print(f"Inserted new shelter record for {shelter_name}, with new shelterID: {shelter_id}")
    cursor.close()
    db.close()

# Modify a dog's record status
# Modify a dog's record status
def modify_dog_status(dog_id, status_type, reason=None, cause_of_death=None, adoption_type=None, adopter_ssn=None, adopter_name=None, adopter_phone=None, adopter_address=None):
    db = connect_to_db()
    cursor = db.cursor()
    
    # Insert a new record in Status_Record
    add_status = """
    INSERT INTO Status_Record (recordDate, dogID) 
    VALUES (NOW(), %s)
    """
    cursor.execute(add_status, (dog_id,))
    status_id = cursor.lastrowid  # Get the last inserted record ID

    # Depending on the status type, insert additional records
    if status_type.lower() == "euthanized":
        if reason is None:
            print("Euthanasia reason is required.")
            return
        add_euthanasia = """
        INSERT INTO Euthanasia_Record (recordID, reasonDescription) 
        VALUES (%s, %s)
        """
        cursor.execute(add_euthanasia, (status_id, reason))
    
    elif status_type.lower() == "natural death":
        if cause_of_death is None:
            print("Cause of death is required.")
            return
        add_death = """
        INSERT INTO Natural_Death_Record (recordID, causeOfDeath) 
        VALUES (%s, %s)
        """
        cursor.execute(add_death, (status_id, cause_of_death))
    
    elif status_type.lower() == "adopted":
        if adoption_type is None or adopter_ssn is None:
            print("Adoption type and adopter SSN are required.")
            return
        
        # Check if the adopter already exists
        check_adopter = "SELECT SSN FROM Adopter WHERE SSN = %s"
        cursor.execute(check_adopter, (adopter_ssn,))
        adopter_exists = cursor.fetchone()

        # If adopter does not exist, add new adopter
        if not adopter_exists:
            add_adopter = """
            INSERT INTO Adopter (SSN, name, phoneNumber, address) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(add_adopter, (adopter_ssn, adopter_name, adopter_phone, adopter_address))
        
        # Insert adoption record, now using the correct column name `adopter_ssn`
        add_adoption = """
        INSERT INTO Adoption_Record (recordID, adoptionType, adopter_ssn) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(add_adoption, (status_id, adoption_type, adopter_ssn))
    
    db.commit()
    print(f"Updated status for dog ID {dog_id} with status type '{status_type}'.")
    cursor.close()
    db.close()

# Retrieve and print the most recent status record for a dog
# Retrieve and print the most recent status record for a dog
def get_most_recent_status(dog_id):
    db = connect_to_db()
    cursor = db.cursor()

    # Retrieve the most recent status record
    get_recent_status = """
    SELECT sr.recordDate, d.name, d.breed, d.sex, 
           ar.recordID IS NOT NULL AS isAvailable,
           er.recordID IS NOT NULL AS isEuthanized,
           nr.recordID IS NOT NULL AS isNaturalDeath,
           adp.recordID IS NOT NULL AS isAdopted,
           ar.dateStartAvailability, ar.kennelNo,
           er.reasonDescription,
           nr.causeOfDeath,
           adp.adoptionType
    FROM Status_Record sr
    JOIN Dog d ON d.dogID = sr.dogID
    LEFT JOIN Availability_Record ar ON sr.recordID = ar.recordID
    LEFT JOIN Euthanasia_Record er ON sr.recordID = er.recordID
    LEFT JOIN Natural_Death_Record nr ON sr.recordID = nr.recordID
    LEFT JOIN Adoption_Record adp ON sr.recordID = adp.recordID
    WHERE sr.dogID = %s
    ORDER BY sr.recordDate DESC
    LIMIT 1
    """
    cursor.execute(get_recent_status, (dog_id,))
    recent_status = cursor.fetchone()

    # Check if a record was found
    if recent_status:
        # Extract fields from the query result
        (record_date, name, breed, sex, 
         is_available, is_euthanized, is_natural_death, is_adopted,
         date_start_availability, kennel_no,
         reason_description, cause_of_death, adoption_type) = recent_status

        # Print basic dog information
        print(f"Dog ID {dog_id} - Name: {name}, Breed: {breed}, Sex: {sex}")
        print(f"Most Recent Status Date: {record_date}")

        # Determine and print the status type and specific information
        if is_available:
            print("Status: Available")
            print(f"  Kennel No: {kennel_no}")
            print(f"  Date Start Availability: {date_start_availability}")
        
        elif is_euthanized:
            print("Status: Euthanized")
            print(f"  Reason for Euthanasia: {reason_description}")
        
        elif is_natural_death:
            print("Status: Natural Death")
            print(f"  Cause of Death: {cause_of_death}")
        
        elif is_adopted:
            print("Status: Adopted")
            print(f"  Adoption Type: {adoption_type}")
        
        else:
            print("Status: Unknown")
    
    else:
        print("Status not available yet for this dog.")

    cursor.close()
    db.close()


# Retrieve and print all available dogs
def print_available_dogs():
    db = connect_to_db()
    cursor = db.cursor()
    
    # Query to get all dogs with the most recent record as availability
    available_dogs_query = """
    SELECT Dog.dogID, Dog.name, Dog.breed, Dog.sex
    FROM Dog
    JOIN Status_Record ON Dog.dogID = Status_Record.dogID
    JOIN Availability_Record ON Status_Record.recordID = Availability_Record.recordID
    WHERE Status_Record.recordDate = (
        SELECT MAX(recordDate) FROM Status_Record AS sr WHERE sr.dogID = Dog.dogID
    )
    """
    cursor.execute(available_dogs_query)
    available_dogs = cursor.fetchall()
    
    # Print results
    if available_dogs:
        print("Available Dogs:")
        for dog in available_dogs:
            dog_id, name, breed, sex = dog
            print(f"Dog ID: {dog_id}, Name: {name}, Breed: {breed}, Sex: {sex}")
    else:
        print("No dogs are currently available.")
    
    cursor.close()
    db.close()

# Delete a dog and all associated records
def delete_dog(dog_id):
    db = connect_to_db()
    cursor = db.cursor()

    try:
        # Delete from tables referencing Dog (ensuring order to avoid foreign key conflicts)
        delete_registers = "DELETE FROM Registers WHERE dogID = %s"
        cursor.execute(delete_registers, (dog_id,))

        delete_is_responsible_for = "DELETE FROM Is_Responsible_For WHERE dogID = %s"
        cursor.execute(delete_is_responsible_for, (dog_id,))

        delete_medical_procedures = "DELETE FROM Medical_Procedure WHERE dogID = %s"
        cursor.execute(delete_medical_procedures, (dog_id,))

        delete_vaccines = "DELETE FROM Vaccine WHERE dogID = %s"
        cursor.execute(delete_vaccines, (dog_id,))

        delete_images = "DELETE FROM Dog_Image WHERE dogID = %s"
        cursor.execute(delete_images, (dog_id,))

        # Delete status records and associated status-related tables
        delete_availability = """
        DELETE FROM Availability_Record 
        WHERE recordID IN (SELECT recordID FROM Status_Record WHERE dogID = %s)
        """
        cursor.execute(delete_availability, (dog_id,))

        delete_euthanasia = """
        DELETE FROM Euthanasia_Record 
        WHERE recordID IN (SELECT recordID FROM Status_Record WHERE dogID = %s)
        """
        cursor.execute(delete_euthanasia, (dog_id,))

        delete_natural_death = """
        DELETE FROM Natural_Death_Record 
        WHERE recordID IN (SELECT recordID FROM Status_Record WHERE dogID = %s)
        """
        cursor.execute(delete_natural_death, (dog_id,))

        delete_adoption = """
        DELETE FROM Adoption_Record 
        WHERE recordID IN (SELECT recordID FROM Status_Record WHERE dogID = %s)
        """
        cursor.execute(delete_adoption, (dog_id,))

        delete_status_records = "DELETE FROM Status_Record WHERE dogID = %s"
        cursor.execute(delete_status_records, (dog_id,))

        # Finally, delete the dog from the Dog table
        delete_dog = "DELETE FROM Dog WHERE dogID = %s"
        cursor.execute(delete_dog, (dog_id,))

        db.commit()
        print(f"Deleted all records for dog ID {dog_id}")
    except mysql.connector.Error as err:
        print(f"Failed to delete dog ID {dog_id}: {err}")
        db.rollback()
    finally:
        cursor.close()
        db.close()
 
   

# Insert vaccine record
def insert_vaccine(dog_id, vaccine_type, vaccine_date):
    db = connect_to_db()
    cursor = db.cursor()
    
    add_vaccine = """
    INSERT INTO Vaccine (dogID, vaccineType, vaccineDate) 
    VALUES (%s, %s, %s)
    """
    cursor.execute(add_vaccine, (dog_id, vaccine_type, vaccine_date))
    
    db.commit()
    print(f"Inserted vaccine record for dog ID {dog_id}")
    cursor.close()
    db.close()

# Insert medical procedure record
def insert_medical_procedure(dog_id, procedure_date, type_of_procedure):
    db = connect_to_db()
    cursor = db.cursor()
    
    add_procedure = """
    INSERT INTO Medical_Procedure (dogID, procedureDate, typeOfProcedure) 
    VALUES (%s, %s, %s)
    """
    cursor.execute(add_procedure, (dog_id, procedure_date, type_of_procedure))
    
    db.commit()
    print(f"Inserted medical procedure for dog ID {dog_id}")
    cursor.close()
    db.close()

# Insert adopter
def insert_adopter(shelter_id, adopter_SSN, adopter_name, adopter_address, adopter_phone_number):
    db = connect_to_db()
    cursor = db.cursor()
    
    # Ensure the SQL query has 5 placeholders, and you pass 5 values
    add_adopter = """
    INSERT INTO Adopter (shelterID, SSN, name, phoneNumber, address) 
    VALUES (%s, %s, %s, %s, %s)
    """
    
    # Pass all the required parameters
    cursor.execute(add_adopter, (shelter_id, adopter_SSN, adopter_name, adopter_phone_number, adopter_address))
    
    db.commit()
    print(f"Inserted adoption details for adopter {adopter_name}")
    cursor.close()
    db.close()


    
# Delete a specific vaccine record
def delete_vaccine(vaccine_id):
    db = connect_to_db()
    cursor = db.cursor()
    
    delete_vaccine = "DELETE FROM Vaccine WHERE vaccineID = %s"
    cursor.execute(delete_vaccine, (vaccine_id,))
    
    db.commit()
    print(f"Deleted vaccine ID {vaccine_id}")
    cursor.close()
    db.close()

# Delete a specific medical procedure record
def delete_medical_procedure(procedure_id):
    db = connect_to_db()
    cursor = db.cursor()
    
    delete_procedure = "DELETE FROM Medical_Procedure WHERE procedureID = %s"
    cursor.execute(delete_procedure, (procedure_id,))
    
    db.commit()
    print(f"Deleted medical procedure ID {procedure_id}")
    cursor.close()
    db.close()

# Delete a specific shelter
def delete_shelter(shelter_id):
    db = connect_to_db()
    cursor = db.cursor()

    try:
        # Delete related records from dependent tables
        delete_adopters = "DELETE FROM Adopter WHERE shelterID = %s"
        cursor.execute(delete_adopters, (shelter_id,))

        # Correctly delete related records in Works_at
        delete_works = "DELETE FROM Works_at WHERE shelterID = %s"
        cursor.execute(delete_works, (shelter_id,))  # Ensure tuple for parameters

        delete_is_responsible_for = "DELETE FROM Is_Responsible_For WHERE shelterID = %s"
        cursor.execute(delete_is_responsible_for, (shelter_id,))

        # Delete the shelter
        delete_shelter = "DELETE FROM Shelter WHERE shelterID = %s"
        cursor.execute(delete_shelter, (shelter_id,))

        db.commit()
        print(f"Deleted shelter ID {shelter_id}")
    except mysql.connector.Error as err:
        print(f"Failed to delete shelter ID {shelter_id}: {err}")
        db.rollback()
    finally:
        cursor.close()
        db.close()


# Delete a specific staff
def delete_staff(staff_id):
    db = connect_to_db()
    cursor = db.cursor()

    delete_works_at = "DELETE FROM works_at WHERE staffID = %s"
    cursor.execute(delete_works_at, (staff_id,))

    delete_registers = "DELETE FROM Registers WHERE staffID = %s"
    cursor.execute(delete_registers, (staff_id,))
    
    delete_staff = "DELETE FROM Staff WHERE staffID = %s"
    cursor.execute(delete_staff, (staff_id,))
    
    db.commit()
    print(f"Deleted staff ID {staff_id}")
    cursor.close()
    db.close()

# Print full medical history for a dog
def print_medical_history(dog_id):
    db = connect_to_db()
    cursor = db.cursor()

    # Retrieve spay/neuter status
    cursor.execute("SELECT spayedNeuteredStatus FROM Dog WHERE dogID = %s", (dog_id,))
    spayed_status = cursor.fetchone()

    if spayed_status:
        spayed_neutered = "Yes" if spayed_status[0] else "No"
        print(f"Dog ID {dog_id} - Spayed/Neutered: {spayed_neutered}")

        # Retrieve vaccine history
        cursor.execute("SELECT vaccineID, vaccineType, vaccineDate FROM Vaccine WHERE dogID = %s", (dog_id,))
        vaccines = cursor.fetchall()
        print("\nVaccination History:")
        if vaccines:
            for vaccine in vaccines:
                vaccine_id, vaccine_type, vaccine_date = vaccine
                print(f"  Vaccine ID: {vaccine_id}, Type: {vaccine_type}, Date: {vaccine_date}")
        else:
            print("  No vaccines found.")

        # Retrieve medical procedure history
        cursor.execute("SELECT procedureID, typeOfProcedure, procedureDate FROM Medical_Procedure WHERE dogID = %s", (dog_id,))
        procedures = cursor.fetchall()
        print("\nMedical Procedures:")
        if procedures:
            for procedure in procedures:
                procedure_id, procedure_type, procedure_date = procedure
                print(f"  Procedure ID: {procedure_id}, Type: {procedure_type}, Date: {procedure_date}")
        else:
            print("  No medical procedures found.")
    else:
        print(f"No medical history found for dog ID {dog_id}.")

    cursor.close()
    db.close()

# Function to print which dogs have been registered by each staff member
def print_dogs_registered_by_staff():
    db = connect_to_db()
    cursor = db.cursor()

    # Query to get all staff members and the dogs they registered
    query = """
    SELECT s.staffID, s.name AS staffName, d.dogID, d.name AS dogName
    FROM Staff s
    LEFT JOIN Registers r ON s.staffID = r.staffID
    LEFT JOIN Dog d ON r.dogID = d.dogID
    ORDER BY s.staffID, d.dogID
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Organize data by staff
    staff_dict = {}
    for staff_id, staff_name, dog_id, dog_name in results:
        if staff_name not in staff_dict:
            staff_dict[staff_name] = []
        if dog_name:
            staff_dict[staff_name].append((dog_id, dog_name))
    
    # Print the results
    print("Dogs Registered by Staff:")
    for staff_name, dogs in staff_dict.items():
        print(f"\nStaff Name: {staff_name}")
        if dogs:
            for dog_id, dog_name in dogs:
                print(f"  - Dog ID: {dog_id}, Dog Name: {dog_name}")
        else:
            print("  No dogs registered.")
    
    cursor.close()
    db.close()


# Update medical records for a dog
def update_medical_records(dog_id):
    db = connect_to_db()
    cursor = db.cursor()

    print("\nWhat would you like to update?")
    print("1. Spayed/Neutered Status")
    print("2. Vaccine Record")
    print("3. Medical Procedure Record")

    choice = input("Enter your choice: ")

    if choice == '1':
        # Update spayed/neutered status
        spayed_neutered = input("Is the dog spayed/neutered? (yes/no): ").lower() == 'yes'
        update_spayed_status = "UPDATE Dog SET spayedNeuturedStatus = %s WHERE dogID = %s"
        cursor.execute(update_spayed_status, (spayed_neutered, dog_id))
        db.commit()
        print(f"Updated spayed/neutered status for dog ID {dog_id}.")

    elif choice == '2':
        # Update a vaccine record
        cursor.execute("SELECT vaccineID, vaccineType, vaccineDate FROM Vaccine WHERE dogID = %s", (dog_id,))
        vaccines = cursor.fetchall()
        
        if not vaccines:
            print("This dog has no vaccine records.")
        else:
            print("\nVaccine Records:")
            for vaccine in vaccines:
                vaccine_id, vaccine_type, vaccine_date = vaccine
                print(f"Vaccine ID: {vaccine_id}, Type: {vaccine_type}, Date: {vaccine_date}")

            vaccine_id = int(input("Enter the Vaccine ID to update: "))
            print("\nWhat would you like to update?")
            print("1. Vaccine Type")
            print("2. Vaccine Date")

            vaccine_choice = input("Enter your choice: ")

            if vaccine_choice == '1':
                new_vaccine_type = input("Enter new vaccine type: ")
                update_vaccine_type = "UPDATE Vaccine SET vaccineType = %s WHERE vaccineID = %s"
                cursor.execute(update_vaccine_type, (new_vaccine_type, vaccine_id))
            
            elif vaccine_choice == '2':
                new_vaccine_date = input("Enter new vaccine date (YYYY-MM-DD): ")
                update_vaccine_date = "UPDATE Vaccine SET vaccineDate = %s WHERE vaccineID = %s"
                cursor.execute(update_vaccine_date, (new_vaccine_date, vaccine_id))
            
            else:
                print("Invalid choice. No changes made.")
                cursor.close()
                db.close()
                return

            db.commit()
            print(f"Updated vaccine record ID {vaccine_id} for dog ID {dog_id}.")

    elif choice == '3':
        # Update a medical procedure record
        cursor.execute("SELECT procedureID, typeOfProcedure, procedureDate FROM Medical_Procedure WHERE dogID = %s", (dog_id,))
        procedures = cursor.fetchall()
        
        if not procedures:
            print("This dog has no medical procedure records.")
        else:
            print("\nMedical Procedure Records:")
            for procedure in procedures:
                procedure_id, procedure_type, procedure_date = procedure
                print(f"Procedure ID: {procedure_id}, Type: {procedure_type}, Date: {procedure_date}")

            procedure_id = int(input("Enter the Procedure ID to update: "))
            print("\nWhat would you like to update?")
            print("1. Type of Procedure")
            print("2. Procedure Date")

            procedure_choice = input("Enter your choice: ")

            if procedure_choice == '1':
                new_procedure_type = input("Enter new type of procedure: ")
                update_procedure_type = "UPDATE Medical_Procedure SET typeOfProcedure = %s WHERE procedureID = %s"
                cursor.execute(update_procedure_type, (new_procedure_type, procedure_id))
            
            elif procedure_choice == '2':
                new_procedure_date = input("Enter new procedure date (YYYY-MM-DD): ")
                update_procedure_date = "UPDATE Medical_Procedure SET procedureDate = %s WHERE procedureID = %s"
                cursor.execute(update_procedure_date, (new_procedure_date, procedure_id))
            
            else:
                print("Invalid choice. No changes made.")
                cursor.close()
                db.close()
                return

            db.commit()
            print(f"Updated medical procedure ID {procedure_id} for dog ID {dog_id}.")

    else:
        print("Invalid choice. No changes made.")
    
    cursor.close()
    db.close()

# Update shelter details
def update_shelter(shelter_id):
    db = connect_to_db()
    cursor = db.cursor()

    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Address")
    print("3. Phone Number")

    choice = input("Enter your choice: ")

    if choice == '1':
        # Update name
        new_name = input("Enter the new name: ")
        update_shelter_name = "UPDATE Shelter SET name = %s WHERE shelterID = %s"
        cursor.execute(update_shelter_name, (new_name, shelter_id))  # Pass a tuple with new_name and shelter_id
        db.commit()
        print(f"Updated name for shelter ID {shelter_id}.")

    elif choice == '2':
        # Update address
        new_address = input("Enter the new address: ")
        update_shelter_address = "UPDATE Shelter SET address = %s WHERE shelterID = %s"
        cursor.execute(update_shelter_address, (new_address, shelter_id))  # Pass a tuple with new_address and shelter_id
        db.commit()
        print(f"Updated address for shelter ID {shelter_id}.")

    elif choice == '3':
        # Update phone number
        new_phone_number = input("Enter the new phone number: ")
        update_shelter_phone_number = "UPDATE Shelter SET phoneNumber = %s WHERE shelterID = %s"
        cursor.execute(update_shelter_phone_number, (new_phone_number, shelter_id))  # Pass a tuple with new_phone_number and shelter_id
        db.commit()
        print(f"Updated phone number for shelter ID {shelter_id}.")

    else:
        print("Invalid choice. No changes made.")
    
    cursor.close()
    db.close()

def print_all_adopters():
    db = connect_to_db()  # Assuming the connect_to_db function connects to your database
    cursor = db.cursor()

    try:
        # Query to select all adopters
        query = "SELECT * FROM Adopter"
        cursor.execute(query)

        # Fetch all rows
        adopters = cursor.fetchall()

        # Check if there are adopters
        if adopters:
            print("List of all adopters:")
            print(f"{'SSN':<15}{'Shelter ID':<15}{'Name':<30}{'Phone Number':<15}{'Address'}")
            print("-" * 75)  # Print a separator line

            # Print each adopter's details
            for adopter in adopters:
                ssn, shelter_id, name, phone_number, address = adopter
                print(f"{ssn:<15}{shelter_id:<15}{name:<30}{phone_number:<15}{address}")
        else:
            print("No adopters found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def print_all_shelters():
    db = connect_to_db()  # Assuming the connect_to_db function connects to your database
    cursor = db.cursor()

    try:
        # Query to select all shelters
        query = "SELECT * FROM Shelter"
        cursor.execute(query)

        # Fetch all rows
        shelters = cursor.fetchall()

        # Check if there are shelters
        if shelters:
            print("List of all shelters:")
            print(f"{'Shelter ID':<15}{'Phone Number':<15}{'Address':<30}{'Name'}")
            print("-" * 75)  # Print a separator line

            # Print each shelter's details
            for shelter in shelters:
                shelter_id, phone_number, address, name = shelter
                print(f"{shelter_id:<15}{phone_number:<15}{address:<30}{name}")
        else:
            print("No shelters found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()



def main():
    # Select or add a staff member at the beginning
    selected_staff_id = select_or_add_staff()

    while True:
        print("\nChoose an action:")
        print("1. Insert New Dog")
        print("2. Insert Vaccine Record")
        print("3. Insert Medical Procedure Record")
        print("4. Delete Dog")
        print("5. Delete Vaccine")
        print("6. Delete Medical Record")
        print("7. Print Medical Records")
        print("8. Update Medical Record")
        print("9. Delete Staff")
        print("10. Print Dogs Registered By Staff Info")
        print("11. Update Shelter")
        print("12. Delete Shelter")
        print("13. Add Shelter")
        print("14. Add Adopter")
        print("15. Modify Dog Status")
        print("16. Get Most Recent Dog Status")
        print("17. Print Available Dogs")
        print("18. Print All Adopters")
        print("19. Print All Shelters")
        print("20. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter dog name: ")
            breed = input("Enter dog breed: ")
            age = int(input("Enter dog age: "))
            arrival_date = input("Enter arrival date (YYYY-MM-DD): ")
            spayed_neutered = input("Is the dog spayed/neutered? (yes/no): ").lower() == 'yes'
            adoptability_score = float(input("Enter adoptability score: "))
            sex = input("Enter dog sex (Female/Male): ")
            initial_status = input("Enter initial status (available/undergoing treatment/not ready): ").lower()
            
            kennel_no = None
            date_start_availability = None
            if initial_status == "available":
                kennel_no = input("Enter kennel number: ")
                date_start_availability = input("Enter date the dog became available (YYYY-MM-DD): ")
            
            main_image_url = None
            add_main_image = input("Would you like to add a main image for the dog? (yes/no): ").lower()
            if add_main_image == "yes":
                main_image_url = input("Enter URL for the main image: ")
            
            extra_image_urls = None
            add_extra_images = input("Would you like to add extra images for the dog? (yes/no): ").lower()
            if add_extra_images == "yes":
                extra_image_urls = input("Enter URLs for extra images, separated by a comma: ")
            
            insert_dog(selected_staff_id, name, breed, age, arrival_date, spayed_neutered, adoptability_score, sex, initial_status, kennel_no, date_start_availability, main_image_url, extra_image_urls)
        
        
        elif choice == '2':
            dog_id = int(input("Enter dog ID for vaccine record: "))
            vaccine_type = input("Enter vaccine type: ")
            vaccine_date = input("Enter vaccine date (YYYY-MM-DD): ")
            insert_vaccine(dog_id, vaccine_type, vaccine_date)

        elif choice == '3':
            dog_id = int(input("Enter dog ID for medical procedure: "))
            procedure_date = input("Enter procedure date (YYYY-MM-DD): ")
            type_of_procedure = input("Enter type of procedure: ")
            insert_medical_procedure(dog_id, procedure_date, type_of_procedure)


        elif choice == '4':
            dog_id = int(input("Enter dog ID of dog you want to delete: "))
            delete_dog(dog_id)
            print(f'Dog with ID {dog_id} has been deleted')

        elif choice == '5':
            vaccine_id = int(input("Enter vaccine ID to delete: "))
            delete_vaccine(vaccine_id)

        elif choice == '6':
            procedure_id = int(input("Enter medical procedure ID to delete: "))
            delete_medical_procedure(procedure_id)

        elif choice == '7':
            dog_id = int(input("Enter dog ID to view medical history: "))
            print_medical_history(dog_id)
        
        elif choice == '8':
            dog_id = int(input("Enter dog ID to update medical records: "))
            update_medical_records(dog_id)
        
        elif choice == '9':
            staff_id = int(input("Enter staff ID to delete:"))
            delete_staff(staff_id)
        
        elif choice == '10':
            print_dogs_registered_by_staff()

        elif choice == '11':
            shelter_id = int(input("Enter shelter ID to update shelter details: "))
            update_shelter(shelter_id)
        
        elif choice == '12':
            shelter_id = int(input("Enter shelter ID to delete: "))
            delete_shelter(shelter_id)

        elif choice == '13': 
            shelter_name = input("Enter shelter name: ")
            shelter_address = (input("Enter shelter address: "))
            shelter_phone_number = (input("Enter shelter phone number: "))
            insert_shelter(shelter_name, shelter_address, shelter_phone_number)

        elif choice == '14':
            shelter_id = int(input("Enter shelter ID that adopter is being added to: "))
            adopter_ssn = int(input("Enter adopter SSN: "))
            adopter_name = (input("Enter adopter name: "))
            adopter_address = (input("Enter adopter address: "))
            adopter_phone_number = ((input("Enter adopter phone number: ")))
            insert_adopter(shelter_id, adopter_ssn, adopter_name, adopter_address, adopter_phone_number)

            
        elif choice == '15':
            dog_id = int(input("Enter dog ID to modify status: "))
            status_type = input("Enter status type (euthanized/natural death/adopted): ").lower()
            
            if status_type == "euthanized":
                reason = input("Enter reason for euthanasia: ")
                modify_dog_status(dog_id, status_type, reason=reason)
            
            elif status_type == "natural death":
                cause_of_death = input("Enter cause of death: ")
                modify_dog_status(dog_id, status_type, cause_of_death=cause_of_death)
            
            elif status_type == "adopted":
                adoption_type = input("Enter adoption type (international/in state/out of state): ")
                adopter_ssn = input("Enter adopter SSN: ")
                adopter_name = input("Enter adopter name: ")
                adopter_phone = input("Enter adopter phone number: ")
                adopter_address = input("Enter adopter address: ")
                modify_dog_status(dog_id, status_type, adoption_type=adoption_type, adopter_ssn=adopter_ssn, adopter_name=adopter_name, adopter_phone=adopter_phone, adopter_address=adopter_address)

        elif choice == '16':
            dog_id = int(input("Enter dog ID to view most recent status: "))
            get_most_recent_status(dog_id)
        
        elif choice == '17':
            print_available_dogs()
        
        elif choice == '18':
            print_all_adopters()
        
        elif choice == '19':
            print_all_shelters()
        
        elif choice == '20':
            print("Exiting...")
            break
    
        # ... other options remain the same
        
        else:
            print("Invalid choice. Please try again.")

# Run the terminal interface
if __name__ == "__main__":
    main()

