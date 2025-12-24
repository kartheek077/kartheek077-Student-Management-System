from flask import Flask, request, jsonify, render_template #pip install flask
import psycopg2 # pip install psycopg2
from psycopg2 import sql

students_app = Flask (__name__)

# Database connection configuration
DB_HOST = '127.0.0.1'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Function to get a database connection
def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD
    )
    return connection

#Create the 'students' table if it doesn't exist
def create_students_table_if_not_exists():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students ( 
            student_id SERIAL PRIMARY KEY, 
            student_name TEXT NOT NULL, 
            mobile_number TEXT NOT NULL UNIQUE, 
            email TEXT NOT NULL UNIQUE, 
            branch TEXT NOT NULL,
            is_passed_out BOOLEAN NOT NULL
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()
create_students_table_if_not_exists()

@students_app.route("/register-student", methods=["POST"])
def register_student():
    student_name = request.json["student_name"]
    mobile_number = request.json["mobile_number"]
    email = request.json["email"]
    branch = request.json["branch"]
    is_passed_out=request.json["is_passed_out"]
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO students (student_name, mobile_number, email, branch, is_passed_out) VALUES (%s, %s, %s, %s, %s);
        """, (student_name, mobile_number, email, branch, is_passed_out))
    connection.commit()
    cursor.close()
    connection.close()

    response_json = {
        "message": "Successfully registered student"
    }

    return jsonify(response_json)

@students_app.route("/retrieve-single-student", methods=["GET"])
def retrieve_single_student():
    student_id = request.args["student_id"]
    
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM students WHERE student_id = " + str(student_id)
    cursor.execute(query)
    student_details = cursor.fetchone()
    cursor.close()
    connection.close()
    if student_details:
        response_json = {
            "student_id": student_details[0],
            "student_name": student_details [1],
            "mobile_number": student_details[2],
            "email": student_details[3],
            "branch": student_details[4],
            "is_passed_out": student_details[5]
        }
        return jsonify(response_json)
    else:
        return jsonify({"error": "Student not found"})
    
@students_app.route("/update-student", methods=["PUT"])
def update_student():
    student_id = request.args["student_id"]
    student_name = request.json["student_name"]
    mobile_number = request.json["mobile_number"]
    email = request.json["email"]
    branch = request.json["branch"]
    is_passed_out = request.json["is_passed_out"]

    connection= get_db_connection()
    cursor= connection.cursor()
    cursor.execute("""
                 UPDATE students SET student_name=%s,mobile_number=%s,email=%s,branch=%s,is_passed_out=%s WHERE student_id=%s;
             """ , (student_name, mobile_number, email, branch, is_passed_out,str(student_id)))
    connection.commit()
    cursor.close()
    connection.close()

    responce_json = {
        "message" : "Successfully updated student"
    }
    return jsonify(responce_json)

@students_app.route("/delete-student", methods=["DELETE"])
def delete_student():
    student_id = request.args["student_id"]

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(""" DELETE  FROM students WHERE student_id =%s; """,(str(student_id)))
    connection.commit()
    cursor.close()
    connection.close()
    if cursor.rowcount == 0:
        response_json = {
            "error": "Student not found"
        }
        return jsonify(response_json)
    else:
        return jsonify({"message" : "Successfully deleted student"})
    
@students_app.route("/", methods=["GET"])
def index():
    return render_template("index.html")




if __name__ == "__main__":
    students_app.run()