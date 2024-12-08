from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
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

# Sample endpoint to fetch all adopters (GET)
@app.route('/api/adopters', methods=['GET'])
def get_adopters():
    db = connect_to_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Adopter")
    adopters = cursor.fetchall()
    
    # Convert the results to a list of dictionaries (for better JSON formatting)
    adopters_list = []
    for adopter in adopters:
        adopter_dict = {
            "shelterID": adopter[0],
            "SSN": adopter[1],
            "name": adopter[2],
            "phoneNumber": adopter[3],
            "address": adopter[4]
        }
        adopters_list.append(adopter_dict)
    
    cursor.close()
    db.close()
    
    return jsonify(adopters_list)

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

if __name__ == "__main__":
    app.run(debug=True)
