from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
allowed_origins = ["http://localhost:3000","http://localhost:3001","http://localhost:3002","http://localhost:3003","http://localhost:3004"] 
CORS(app, origins=allowed_origins)
# Function to establish a connection to the database
def connect_to_db():
    try:
        # Establishing the connection to MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",       # Database host (localhost in this case)
            user="root",            # MySQL username
            password="Gr@duate22",            # MySQL password (empty string if no password)
            database="dogmanagement"    # Database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
@app.route('/')
def index():
    return "Flask Server is Running!", 200


# Sample endpoint to fetch all adopters (GET)
@app.route('/api/adopters', methods=['GET'])
def get_all_adopters():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Query to fetch all adopters
        query = "SELECT SSN, shelterID, name, phoneNumber, address FROM Adopter"
        cursor.execute(query)

        # Fetch all rows
        adopters = cursor.fetchall()

        # Format the response as a list of dictionaries
        adopters_list = [
            {
                "SSN": adopter[0],
                "shelterID": adopter[1],
                "name": adopter[2],
                "phoneNumber": adopter[3],
                "address": adopter[4],
            }
            for adopter in adopters
        ]

        if not adopters_list:
            return jsonify({"message": "No adopters found."}), 404

        return jsonify(adopters_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()


# Endpoint to insert an adopter (POST)
@app.route('/api/adopters', methods=['POST'])
def add_adopter():
    data = request.get_json()
    
    # Extract data from the request JSON
    shelter_id = data.get('shelterID')
    adopter_ssn = data.get('SSN')
    adopter_name = data.get('name')
    adopter_address = data.get('address')
    adopter_phone = data.get('phoneNumber')

    # Check if all required fields are provided
    if not all([shelter_id, adopter_ssn, adopter_name, adopter_address, adopter_phone]):
        return jsonify({"error": "Missing required fields"}), 400
    
    db = connect_to_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = db.cursor()
    
    query = """
        INSERT INTO Adopter (shelterID, SSN, name, phoneNumber, address)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (shelter_id, adopter_ssn, adopter_name, adopter_phone, adopter_address))
    db.commit()
    
    cursor.close()
    db.close()

    return jsonify({"message": "Adopter added successfully"}), 201

@app.route('/api/staff/', methods=['GET'])
def get_staff():
    db = connect_to_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM Staff")
        staff = cursor.fetchall()
        staff_list = [{"staffId": staff_member[0], "name": staff_member[1]} for staff_member in staff]
        return jsonify(staff_list), 200
    except Exception as e:
        print(f"Error fetching staff: {e}")
        return jsonify({"error": "Failed to fetch staff"}), 500
    finally:
        cursor.close()
        db.close()


@app.route('/api/staff/', methods=['POST'])
def add_staff():
    data = request.get_json()
    new_name = data.get('name')

    if not new_name or len(new_name.strip()) == 0:
        return jsonify({"error": "Staff name is required and cannot be empty"}), 400

    db = connect_to_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = db.cursor()
    try:
        query = "INSERT INTO Staff (name) VALUES (%s)"
        cursor.execute(query, (new_name,))
        db.commit()
        staff_id = cursor.lastrowid
        return jsonify({"staffId": staff_id, "name": new_name}), 201
    except Exception as e:
        print(f"Error adding staff: {e}")
        return jsonify({"error": "Failed to add staff"}), 500
    finally:
        cursor.close()
        db.close()

    
@app.route('/api/delete-staff', methods=['DELETE'])
def delete_staff():
    data = request.get_json()  # Get the JSON payload from the frontend

    staff_id = data.get('staffID')  # Extract the staffID from the JSON
    if not staff_id:
        return jsonify({"error": "Missing staffID"}), 400

    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Delete related records from dependent tables
        delete_works_at = "DELETE FROM Works_at WHERE staffID = %s"
        cursor.execute(delete_works_at, (staff_id,))

        delete_registers = "DELETE FROM Registers WHERE staffID = %s"
        cursor.execute(delete_registers, (staff_id,))

        # Delete staff record
        delete_staff = "DELETE FROM Staff WHERE staffID = %s"
        cursor.execute(delete_staff, (staff_id,))

        db.commit()
        return jsonify({"message": f"Staff ID {staff_id} successfully deleted."}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/insert-dog', methods=['POST'])
def insert_dog():
    data = request.get_json()

    # Required fields
    required_fields = ["staffID", "name", "breed", "age", "arrivalDate", "adoptabilityScore", "sex", "initialStatus"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    # Check for missing fields
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    try:
        # Extract and validate required data
        staff_id = data["staffID"]
        name = data["name"]
        breed = data["breed"]
        age = int(data["age"])
        adoptability_score = float(data["adoptabilityScore"])
        arrival_date = data["arrivalDate"]
        spayed_neutered = data.get("spayedNeutered", False)
        sex = data["sex"]
        initial_status = data["initialStatus"]

        # Validate 'sex' and 'initialStatus' fields
        if sex not in ["Male", "Female"]:
            return jsonify({"error": "Invalid 'sex'. It must be either 'Male' or 'Female'."}), 400
        if initial_status not in ["available", "undergoing treatment", "not ready yet"]:
            return jsonify({"error": "Invalid 'initialStatus'. Valid options are 'available', 'undergoing treatment', or 'not ready yet'."}), 400

        # Optional fields
        kennel_no = data.get("kennelNo")
        date_start_availability = data.get("dateStartAvailability")
        main_image_url = data.get("mainImageUrl")
        extra_image_urls = data.get("extraImageUrls")

        # If "available", validate additional fields
        if initial_status == "available" and (not kennel_no or not date_start_availability):
            return jsonify({"error": "Fields 'kennelNo' and 'dateStartAvailability' are required when 'initialStatus' is 'available'."}), 400

        # Connect to DB
        db = connect_to_db()
        cursor = db.cursor()

        # Insert dog record
        add_dog = """
        INSERT INTO Dog (name, breed, age, adoptabilityScore, arrivalDate, spayedNeuteredStatus, sex) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(add_dog, (name, breed, age, adoptability_score, arrival_date, spayed_neutered, sex))
        dog_id = cursor.lastrowid

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
        if initial_status == "available":
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
        return jsonify({"message": f"Dog '{name}' successfully added.", "dogID": dog_id}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        db.close()


@app.route('/api/staff-dogs', methods=['GET'])
def get_dogs_registered_by_staff():
    try:
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
                staff_dict[staff_name].append({"dogID": dog_id, "dogName": dog_name})

        # Format response
        response = [
            {"staffName": staff_name, "dogs": dogs}
            for staff_name, dogs in staff_dict.items()
        ]

        if not response:
            return jsonify({"message": "No data found."}), 404

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/available-dogs', methods=['GET'])
def get_available_dogs():
    try:
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

        if not available_dogs:
            return jsonify({"message": "No dogs are currently available."}), 404

        # Format response
        dogs_list = [
            {"dogID": dog[0], "name": dog[1], "breed": dog[2], "sex": dog[3]}
            for dog in available_dogs
        ]

        return jsonify(dogs_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/dog-status/<int:dog_id>', methods=['GET'])
def get_most_recent_status(dog_id):
    try:
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

            # Build response object
            response = {
                "dogID": dog_id,
                "name": name,
                "breed": breed,
                "sex": sex,
                "recordDate": record_date,
                "status": {
                    "isAvailable": is_available,
                    "isEuthanized": is_euthanized,
                    "isNaturalDeath": is_natural_death,
                    "isAdopted": is_adopted,
                    "dateStartAvailability": date_start_availability,
                    "kennelNo": kennel_no,
                    "reasonDescription": reason_description,
                    "causeOfDeath": cause_of_death,
                    "adoptionType": adoption_type
                }
            }

            return jsonify(response), 200

        else:
            return jsonify({"message": "Status not available yet for this dog."}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()


@app.route('/api/delete-dog/<int:dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    try:
        db = connect_to_db()
        cursor = db.cursor()

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
        return jsonify({"message": f"Deleted all records for dog ID {dog_id}"}), 200
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({"error": f"Failed to delete dog ID {dog_id}: {err}"}), 500
    finally:
        cursor.close()
        db.close()



@app.route('/api/insert-shelter', methods=['POST'])
def insert_shelter():
    data = request.get_json()  # Get the JSON data sent from the front-end

    # Extract data from the request
    shelter_name = data.get('name')
    shelter_address = data.get('address')
    shelter_phone_number = data.get('phoneNumber')

    # Check for required fields
    if not all([shelter_name, shelter_address, shelter_phone_number]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Insert shelter record into the database
        add_shelter = """
        INSERT INTO Shelter (name, address, phoneNumber) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(add_shelter, (shelter_name, shelter_address, shelter_phone_number))

        shelter_id = cursor.lastrowid  # Get the ID of the newly inserted shelter

        db.commit()
        return jsonify({"message": f"Shelter '{shelter_name}' added successfully with ID {shelter_id}."}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/delete-shelter', methods=['DELETE'])
def delete_shelter():
    data = request.get_json()  # Get the JSON payload from the frontend

    shelter_id = data.get('shelterID')  # Extract the shelterID from the JSON
    if not shelter_id:
        return jsonify({"error": "Missing shelterID"}), 400

    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Delete related records from dependent tables
        delete_adopters = "DELETE FROM Adopter WHERE shelterID = %s"
        cursor.execute(delete_adopters, (shelter_id,))

        delete_works = "DELETE FROM Works_at WHERE shelterID = %s"
        cursor.execute(delete_works, (shelter_id,))

        delete_is_responsible_for = "DELETE FROM Is_Responsible_For WHERE shelterID = %s"
        cursor.execute(delete_is_responsible_for, (shelter_id,))

        # Delete the shelter
        delete_shelter = "DELETE FROM Shelter WHERE shelterID = %s"
        cursor.execute(delete_shelter, (shelter_id,))

        db.commit()
        return jsonify({"message": f"Shelter ID {shelter_id} successfully deleted."}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/shelters', methods=['GET'])
def get_all_shelters():
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Query to fetch all shelters
        query = "SELECT shelterID, phoneNumber, address, name FROM Shelter"
        cursor.execute(query)

        # Fetch all rows
        shelters = cursor.fetchall()

        # Format the response as a list of dictionaries
        shelters_list = [
            {
                "shelterID": shelter[0],
                "phoneNumber": shelter[1],
                "address": shelter[2],
                "name": shelter[3],
            }
            for shelter in shelters
        ]

        if not shelters_list:
            return jsonify({"message": "No shelters found."}), 404

        return jsonify(shelters_list), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/medical-history/<int:dog_id>', methods=['GET'])
def get_medical_history(dog_id):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Fetch spay/neuter status
        cursor.execute("SELECT spayedNeuteredStatus FROM Dog WHERE dogID = %s", (dog_id,))
        spayed_status = cursor.fetchone()

        if not spayed_status:
            return jsonify({"error": f"No medical history found for dog ID {dog_id}"}), 404

        spayed_neutered = "Yes" if spayed_status[0] else "No"

        # Fetch vaccine history
        cursor.execute("SELECT vaccineID, vaccineType, vaccineDate FROM Vaccine WHERE dogID = %s", (dog_id,))
        vaccines = [
            {"vaccineID": vaccine[0], "vaccineType": vaccine[1], "vaccineDate": str(vaccine[2])}
            for vaccine in cursor.fetchall()
        ]

        # Fetch medical procedure history
        cursor.execute("SELECT procedureID, typeOfProcedure, procedureDate FROM Medical_Procedure WHERE dogID = %s", (dog_id,))
        procedures = [
            {"procedureID": procedure[0], "typeOfProcedure": procedure[1], "procedureDate": str(procedure[2])}
            for procedure in cursor.fetchall()
        ]

        # Construct response
        response = {
            "dogID": dog_id,
            "spayedNeuteredStatus": spayed_neutered,
            "vaccines": vaccines,
            "procedures": procedures,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/vaccine/<int:vaccine_id>', methods=['DELETE'])
def delete_vaccine(vaccine_id):
    try:
        db = connect_to_db()
        cursor = db.cursor()
        
        # Delete vaccine record
        delete_vaccine_query = "DELETE FROM Vaccine WHERE vaccineID = %s"
        cursor.execute(delete_vaccine_query, (vaccine_id,))
        
        if cursor.rowcount == 0:
            return jsonify({"error": f"No vaccine found with ID {vaccine_id}"}), 404
        
        db.commit()
        return jsonify({"message": f"Vaccine ID {vaccine_id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/medical-procedure/<int:procedure_id>', methods=['DELETE'])
def delete_medical_procedure(procedure_id):
    try:
        db = connect_to_db()
        cursor = db.cursor()
        
        # Delete medical procedure record
        delete_procedure_query = "DELETE FROM Medical_Procedure WHERE procedureID = %s"
        cursor.execute(delete_procedure_query, (procedure_id,))
        
        if cursor.rowcount == 0:
            return jsonify({"error": f"No medical procedure found with ID {procedure_id}"}), 404
        
        db.commit()
        return jsonify({"message": f"Medical procedure ID {procedure_id} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/vaccine', methods=['POST'])
def insert_vaccine():
    data = request.get_json()
    
    # Extract data from the request
    dog_id = data.get('dogID')
    vaccine_type = data.get('vaccineType')
    vaccine_date = data.get('vaccineDate')

    if not all([dog_id, vaccine_type, vaccine_date]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Insert vaccine record
        add_vaccine = """
        INSERT INTO Vaccine (dogID, vaccineType, vaccineDate) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(add_vaccine, (dog_id, vaccine_type, vaccine_date))
        
        db.commit()
        return jsonify({"message": f"Vaccine record inserted for dog ID {dog_id}"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/medical-procedure', methods=['POST'])
def insert_medical_procedure():
    data = request.get_json()
    
    # Extract data from the request
    dog_id = data.get('dogID')
    procedure_date = data.get('procedureDate')
    type_of_procedure = data.get('typeOfProcedure')

    if not all([dog_id, procedure_date, type_of_procedure]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # Insert medical procedure record
        add_procedure = """
        INSERT INTO Medical_Procedure (dogID, procedureDate, typeOfProcedure) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(add_procedure, (dog_id, procedure_date, type_of_procedure))
        
        db.commit()
        return jsonify({"message": f"Medical procedure record inserted for dog ID {dog_id}"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/update-medical-records', methods=['POST'])
def update_medical_records():
    data = request.get_json()

    dog_id = data.get('dogID')
    choice = data.get('choice')

    if not dog_id or not choice:
        return jsonify({"error": "Missing dogID or choice"}), 400

    try:
        db = connect_to_db()
        cursor = db.cursor()

        if choice == '1':  # Update spayed/neutered status
            spayed_neutered = data.get('spayedNeutered')
            if spayed_neutered is None:
                return jsonify({"error": "Spayed/Neutered status is required"}), 400
            update_spayed_status = "UPDATE Dog SET spayedNeuteredStatus = %s WHERE dogID = %s"
            cursor.execute(update_spayed_status, (spayed_neutered, dog_id))
            db.commit()
            return jsonify({"message": f"Updated spayed/neutered status for dog ID {dog_id}"}), 200

        elif choice == '2':  # Update vaccine record
            vaccine_id = data.get('vaccineID')
            vaccine_choice = data.get('vaccineChoice')
            if not vaccine_id or not vaccine_choice:
                return jsonify({"error": "Vaccine ID and choice are required"}), 400
            
            if vaccine_choice == '1':  # Update vaccine type
                new_vaccine_type = data.get('newVaccineType')
                if not new_vaccine_type:
                    return jsonify({"error": "New vaccine type is required"}), 400
                update_vaccine_type = "UPDATE Vaccine SET vaccineType = %s WHERE vaccineID = %s"
                cursor.execute(update_vaccine_type, (new_vaccine_type, vaccine_id))
            elif vaccine_choice == '2':  # Update vaccine date
                new_vaccine_date = data.get('newVaccineDate')
                if not new_vaccine_date:
                    return jsonify({"error": "New vaccine date is required"}), 400
                update_vaccine_date = "UPDATE Vaccine SET vaccineDate = %s WHERE vaccineID = %s"
                cursor.execute(update_vaccine_date, (new_vaccine_date, vaccine_id))
            db.commit()
            return jsonify({"message": f"Updated vaccine record ID {vaccine_id} for dog ID {dog_id}"}), 200

        elif choice == '3':  # Update medical procedure record
            procedure_id = data.get('procedureID')
            procedure_choice = data.get('procedureChoice')
            if not procedure_id or not procedure_choice:
                return jsonify({"error": "Procedure ID and choice are required"}), 400
            
            if procedure_choice == '1':  # Update procedure type
                new_procedure_type = data.get('newProcedureType')
                if not new_procedure_type:
                    return jsonify({"error": "New procedure type is required"}), 400
                update_procedure_type = "UPDATE Medical_Procedure SET typeOfProcedure = %s WHERE procedureID = %s"
                cursor.execute(update_procedure_type, (new_procedure_type, procedure_id))
            elif procedure_choice == '2':  # Update procedure date
                new_procedure_date = data.get('newProcedureDate')
                if not new_procedure_date:
                    return jsonify({"error": "New procedure date is required"}), 400
                update_procedure_date = "UPDATE Medical_Procedure SET procedureDate = %s WHERE procedureID = %s"
                cursor.execute(update_procedure_date, (new_procedure_date, procedure_id))
            db.commit()
            return jsonify({"message": f"Updated medical procedure ID {procedure_id} for dog ID {dog_id}"}), 200

        else:
            return jsonify({"error": "Invalid choice"}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/modify-dog-status', methods=['POST'])
def modify_dog_status():
    data = request.get_json()

    dog_id = data.get('dogID')
    status_type = data.get('statusType')
    reason = data.get('reason')  # For euthanized status
    cause_of_death = data.get('causeOfDeath')  # For natural death status
    adoption_type = data.get('adoptionType')  # For adoption status
    adopter_ssn = data.get('adopterSSN')  # For adoption status
    adopter_name = data.get('adopterName')  # For adoption status
    adopter_phone = data.get('adopterPhone')  # For adoption status
    adopter_address = data.get('adopterAddress')  # For adoption status

    if not dog_id or not status_type:
        return jsonify({"error": "Dog ID and Status Type are required."}), 400

    try:
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
            if not reason:
                return jsonify({"error": "Euthanasia reason is required."}), 400
            add_euthanasia = """
            INSERT INTO Euthanasia_Record (recordID, reasonDescription) 
            VALUES (%s, %s)
            """
            cursor.execute(add_euthanasia, (status_id, reason))

        elif status_type.lower() == "natural death":
            if not cause_of_death:
                return jsonify({"error": "Cause of death is required."}), 400
            add_death = """
            INSERT INTO Natural_Death_Record (recordID, causeOfDeath) 
            VALUES (%s, %s)
            """
            cursor.execute(add_death, (status_id, cause_of_death))

        elif status_type.lower() == "adopted":
            if not adoption_type or not adopter_ssn:
                return jsonify({"error": "Adoption type and adopter SSN are required."}), 400

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

            # Insert adoption record
            add_adoption = """
            INSERT INTO Adoption_Record (recordID, adoptionType, adopter_ssn) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(add_adoption, (status_id, adoption_type, adopter_ssn))

        db.commit()
        return jsonify({"message": f"Updated status for dog ID {dog_id} with status type '{status_type}'."}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()

@app.route('/api/update-shelter', methods=['PUT'])
def update_shelter():
    data = request.get_json()

    shelter_id = data.get("shelterID")
    new_name = data.get("name")
    new_address = data.get("address")
    new_phone_number = data.get("phoneNumber")

    # Ensure the shelter ID is provided
    if not shelter_id:
        return jsonify({"error": "Shelter ID is required."}), 400

    if not any([new_name, new_address, new_phone_number]):
        return jsonify({"error": "No fields provided to update."}), 400

    db = connect_to_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # Update shelter details based on the input
        if new_name:
            update_name_query = "UPDATE Shelter SET name = %s WHERE shelterID = %s"
            cursor.execute(update_name_query, (new_name, shelter_id))
        
        if new_address:
            update_address_query = "UPDATE Shelter SET address = %s WHERE shelterID = %s"
            cursor.execute(update_address_query, (new_address, shelter_id))

        if new_phone_number:
            update_phone_query = "UPDATE Shelter SET phoneNumber = %s WHERE shelterID = %s"
            cursor.execute(update_phone_query, (new_phone_number, shelter_id))

        db.commit()
        return jsonify({"message": f"Shelter {shelter_id} updated successfully."}), 200
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({"error": f"Error: {err}"}), 500
    finally:
        cursor.close()
        db.close()
if __name__ == "__main__":
    app.run(debug=True)
