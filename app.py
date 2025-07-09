from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# RDS MySQL configuration
db_config = {
    'host': 'your-rds-endpoint.amazonaws.com',
    'user': 'your-username',
    'password': 'your-password',
    'database': 'your-database-name'
}

# Connect to DB
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM students WHERE id = %s', (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(row)
    return jsonify({'message': 'Student not found'}), 404

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age) VALUES (%s, %s)', (name, age))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student created successfully'}), 201

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    name = data.get('name')
    age = data.get('age')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET name=%s, age=%s WHERE id=%s', (name, age, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student updated successfully'})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
