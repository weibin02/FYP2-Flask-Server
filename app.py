import numpy as np
from flask import Flask, request, jsonify
import pickle
import pandas as pd

import sqlite3
import hashlib
from datetime import datetime

from calendar import month_name



# Create Flask app
app = Flask(__name__)

# Load the pickle model
model = pickle.load(open("model.pkl", "rb"))

DB_PATH = 'database.db'
excel_file = '2022 data raw.xlsx'
excel_info_table_name = 'data'

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            employeeID TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            selectedAvatar TEXT DEFAULT 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKSEuKKwqIqbJH-NRiDHluGbuC9ysMW99BPA&usqp=CAU'
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS processing_summary (
            processing_id TEXT PRIMARY KEY,
            processing_time DATETIME NOT NULL,
            processing_grade TEXT NOT NULL,
            employeeID TEXT NOT NULL,
            FOREIGN KEY (employeeID) REFERENCES employee(employeeID)
        )
    ''')



    conn.commit()
    conn.close()

############################### so far no use ###################################################################
@app.route('/insert_sample_data', methods=['GET'])
def insert_sample_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    password_hash = hashlib.sha256('password'.encode()).hexdigest()
    c.execute("INSERT INTO employee (employeeID, username, fullname, email, password_hash) VALUES (?, ?, ?, ?, ?)", ('A123', 'john_doe', 'John Doe', 'john@example.com', password_hash))
    c.execute("INSERT INTO employee (employeeID, username, fullname, email, password_hash) VALUES (?,?, ?, ?, ?)", ('A111','jane_smith', 'Jane Smith', 'jane@example.com', password_hash))
    conn.commit()
    conn.close()

    return jsonify({'message': 'success'})
#################################################################################################################

@app.route('/initialize', methods=['GET'])
def initialize():
    initialize_database()
    return jsonify({'message': 'Database initialized'})

################################################ so far no use ###################################################
@app.route('/drop', methods=['GET'])
def drop():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS employee")
    conn.commit()
    conn.close()

    return jsonify({'result': 'success'})
###################################################################################################################


##################### so far no use ##############################################################################
@app.route('/check', methods=['GET'])
def check():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA table_info('employee')")
    rows = c.fetchall()
    for row in rows:
        print(row)

    conn.close()

    return jsonify({'result': 'success'})
###################################################################################################################

@app.route('/employees', methods=['GET'])
def get_employees():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM employee")
    employees = c.fetchall()
    conn.close()
    # Convert the list of tuples to a list of dictionaries
    employees_data = [{'employeeID': row[0], 'username': row[1], 'fullname': row[2], 'email': row[3], 'selectedAvatar': row[5]} for row in employees]
    return jsonify({'employees': employees_data})


################################### so far no use #################################################################
@app.route('/newdata', methods=['GET'])
def get_newdata():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    data = c.fetchall()
    conn.close()
    # Convert the list of tuples to a list of dictionaries
    return jsonify({'data': data})
##################################################################################################################

################################### so far no use #############################################################
@app.route('/delete_all_records', methods=['GET'])
def delete_all_records():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM employee")
        conn.commit()
        conn.close()
        return 'All records deleted successfully'
    except Exception as e:
        conn.rollback()
        conn.close()
        return f'Error deleting records: {str(e)}', 500
################################################################################################################

##################################### so far no use ###########################################################
@app.route('/delete_all_summary', methods=['GET'])
def delete_all_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM processing_summary")
        conn.commit()
        conn.close()
        return 'All records deleted successfully'
    except Exception as e:
        conn.rollback()
        conn.close()
        return f'Error deleting records: {str(e)}', 500
##############################################################################################################

def insert_user(employeeID, username, fullname, email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO employee(employeeID, username, fullname, email, password_hash) VALUES (?,?,?,?,?)",
    (employeeID, username, fullname, email, password_hash))
    conn.commit()
    conn.close()


def employeeID_exists(employeeID):
    conn = sqlite3.connect(DB_PATH)  
    c = conn.cursor()
    c.execute("SELECT * FROM employee WHERE employeeID = ?", (employeeID,))
    exists = c.fetchone()
    conn.close()
    return exists

def email_exists(email):
    conn = sqlite3.connect(DB_PATH)  
    c = conn.cursor()
    c.execute("SELECT * FROM employee WHERE email = ?", (email,))
    exists = c.fetchone()
    conn.close()
    return exists

def username_exists(username):
    conn = sqlite3.connect(DB_PATH)  
    c = conn.cursor()
    c.execute("SELECT * FROM employee WHERE username = ?", (username,))
    exists = c.fetchone()
    conn.close()
    return exists

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    employeeID = data.get('employeeID')
    username = data.get('username')
    fullName = data.get('fullName')
    email = data.get('email')
    password = data.get('password')

    if employeeID_exists(employeeID):
        return jsonify({'message': 'Employee ID already registered'}), 400
    elif email_exists(email):
        return jsonify({'message': 'Email already registered'}), 400
    elif username_exists(username):
        return jsonify({'message': 'Username already registered'}), 400

    try:
        insert_user(employeeID, username, fullName, email, password)
        return jsonify({'message': 'Account Created Successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def verify_credentials(employeeID, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    c.execute("SELECT * FROM employee WHERE employeeID=? AND password_hash=?", (employeeID, password_hash))
    user = c.fetchone()

    conn.close()

    if user:
        return True
    else:
        return False

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    employeeID = data.get('employeeID')
    password = data.get('password')

    if verify_credentials(employeeID, password):
        return jsonify({'message': 'Login Successfully'}), 200
    else:
        return jsonify({'message': 'Invalid EmployeeID or Password'}), 401


@app.route('/employee/<employeeID>', methods=['GET'])
def get_employee_info(employeeID):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM employee WHERE employeeID=?", (employeeID,))
        employee_data = c.fetchone()
        conn.close()

        if employee_data:
            employee_info = {
                'employeeID': employee_data[0],
                'username': employee_data[1],
                'fullname': employee_data[2],
                'email': employee_data[3],
                'selectedAvatar': employee_data[5]
                # Add more fields if needed
            }
            return jsonify(employee_info), 200
        else:
            return jsonify({'message': 'Employee Not Found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
def email_exists_when_updating(employeeID, email):
    conn = sqlite3.connect(DB_PATH)  
    c = conn.cursor()
    c.execute("SELECT * FROM employee WHERE email = ? AND employeeID != ?", (email, employeeID))
    exists = c.fetchone()
    conn.close()
    return exists

def username_exists_when_updating(employeeID, username):
    conn = sqlite3.connect(DB_PATH)  
    c = conn.cursor()
    c.execute("SELECT * FROM employee WHERE username = ? AND employeeID != ?", (username, employeeID))
    exists = c.fetchone()
    conn.close()
    return exists

@app.route('/update_profile', methods=['PUT'])
def update_profile():
    try:
        data = request.json
        employeeID = data.get('employeeID')
        username = data.get('username')
        fullName = data.get('fullName')
        email = data.get('email')
        selectedAvatar = data.get('selectedAvatar')

        print("Received data:")
        print("Employee ID:", employeeID)
        print("Username:", username)
        print("Full Name:", fullName)
        print("Email:", email)
        print("Selected Avatar:", selectedAvatar)

        if email_exists_when_updating(employeeID, email):
            return jsonify({'message': 'Email already  registered'}), 400
        
        elif username_exists_when_updating(employeeID, username):
            return jsonify({'message': 'Username already registered'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE employee SET username=?, fullname=?, email=?, selectedAvatar=? WHERE employeeID=?", (username, fullName, email, selectedAvatar, employeeID))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Profile Updated Successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def insert_processing_summary(processing_id, employeeID, processing_time, processing_grade):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO processing_summary (processing_id, employeeID, processing_time, processing_grade) VALUES (?, ?, ?, ?)",
              (processing_id, employeeID, processing_time, processing_grade))
    conn.commit()
    conn.close()


@app.route("/predict", methods = ["POST"])
def predict():

    # for mobile application
    data = request.json
    
    defects = data['defects']
    employeeID = data.get('employeeID')
    processing_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
    SELECT COALESCE(MAX(CAST(SUBSTR(processing_id, 2) AS INTEGER)), 0) + 1 AS new_id FROM processing_summary
    ''')
    new_id = c.fetchone()[0]
    new_processing_id = 'P' + str(new_id).zfill(3)


    # To store one-hot values
    temp_length_total = []
    temp_width_total = []
    temp_height_total = []

    for i in range(1, 6):
        print("Defect: " + str(i))
        # Length Direction
        temp_length_single = [0, 0, 0, 0, 0]
        #loc_length = request.form.get("def"+str(i)+"_loc_len")
        loc_length = defects[i-1]["length"]
        print("Length:" + str(loc_length))

        if i == 1:
            if loc_length == "H":
                temp_length_single[0] = 1
            elif loc_length == "T":
                temp_length_single[1] = 1
            elif loc_length == "V":
                temp_length_single[2] = 1
            elif loc_length == "U":
                temp_length_single[3] = 1
            else:
                temp_length_single[4] = 1
        
        elif i == 2 or i == 3:
            if loc_length == "H":
                temp_length_single[0] = 1
            elif loc_length == "V":
                temp_length_single[1] = 1
            elif loc_length == "T":
                temp_length_single[2] = 1
            elif loc_length == "M":
                temp_length_single[3] = 1
            else:
                temp_length_single[4] = 1 
        
        elif i == 4:
            if loc_length == "H":
                temp_length_single[0] = 1
            elif loc_length == "M":
                temp_length_single[1] = 1
            elif loc_length == "V":
                temp_length_single[2] = 1
            elif loc_length == "U":
                temp_length_single[3] = 1
            else:
                temp_length_single[4] = 1 
        
        else:
            if loc_length == "H":
                temp_length_single[0] = 1
            elif loc_length == "U":
                temp_length_single[1] = 1
            elif loc_length == "V":
                temp_length_single[2] = 1
            elif loc_length == "M":
                temp_length_single[3] = 1
            else:
                temp_length_single[4] = 1 

        print("temp_length_single:")
        print(temp_length_single)
        temp_length_total.append(temp_length_single)
        print("temp_length_total:")
        print(temp_length_total)

        # Width Direction
        temp_width_single = [0, 0, 0, 0, 0, 0, 0]
        #loc_width = request.form.get("def"+str(i)+"_loc_width")
        loc_width = defects[i-1]["width"]
        print("Width:" + str(loc_width))

        if i == 1:
            if loc_width == "C":
                temp_width_single[0] = 1
            elif loc_width == "F":
                temp_width_single[1] = 1
            elif loc_width == "A":
                temp_width_single[2] = 1
            elif loc_width == "W":
                temp_width_single[3] = 1
            elif loc_width == "D":
                temp_width_single[4] = 1
            elif loc_width == "X":
                temp_width_single[5] = 1
            else:
                temp_width_single[6] = 1
        
        elif i == 2:
            if loc_width == "C":
                temp_width_single[0] = 1
            elif loc_width == "F":
                temp_width_single[1] = 1
            elif loc_width == "Y":
                temp_width_single[2] = 1
            elif loc_width == "A":
                temp_width_single[3] = 1
            elif loc_width == "D":
                temp_width_single[4] = 1
            elif loc_width == "W":
                temp_width_single[5] = 1
            else:
                temp_width_single[6] = 1
        
        elif i == 3:
            if loc_width == "A":
                temp_width_single[0] = 1
            elif loc_width == "C":
                temp_width_single[1] = 1
            elif loc_width == "F":
                temp_width_single[2] = 1
            elif loc_width == "D":
                temp_width_single[3] = 1
            elif loc_width == "X":
                temp_width_single[4] = 1
            elif loc_width == "W":
                temp_width_single[5] = 1
            else:
                temp_width_single[6] = 1
        
        elif i == 4:
            if loc_width == "F":
                temp_width_single[0] = 1
            elif loc_width == "A":
                temp_width_single[1] = 1
            elif loc_width == "D":
                temp_width_single[2] = 1
            elif loc_width == "C":
                temp_width_single[3] = 1
            elif loc_width == "W":
                temp_width_single[4] = 1
            elif loc_width == "Y":
                temp_width_single[5] = 1
            else:
                temp_width_single[6] = 1
        
        else:
            if loc_width == "F":
                temp_width_single[0] = 1
            elif loc_width == "C":
                temp_width_single[1] = 1
            elif loc_width == "A":
                temp_width_single[2] = 1
            elif loc_width == "D":
                temp_width_single[3] = 1
            elif loc_width == "Y":
                temp_width_single[4] = 1
            elif loc_width == "W":
                temp_width_single[5] = 1
            else:
                temp_width_single[6] = 1

        print("temp_width_single:")
        print(temp_width_single)
        temp_width_total.append(temp_width_single)
        print("temp_width_total:")
        print(temp_width_total)

        # Height Direction
        temp_height_single = [0, 0, 0]
        loc_height = defects[i-1]["height"]
        print("Height:" + str(loc_height))

        if i == 5:
            if loc_height == "T":
                temp_height_single[0] = 1
            elif loc_height == "D":
                temp_height_single[1] = 1
            else:
                temp_height_single[2] = 1
        else:
            if loc_height == "D":
                temp_height_single[0] = 1
            elif loc_height == "T":
                temp_height_single[1] = 1
            else:
                temp_height_single[2] = 1

        print("temp_height_single:")
        print(temp_height_single)
        temp_height_total.append(temp_height_single)
        print("temp_height_total:")
        print(temp_height_total)

    prediction_input = []
    for i in range(1, 6):
        prediction_input.append(float(defects[i-1]['rate']) / 2)
        prediction_input.append(float(defects[i-1]['area']) / 100)


    for i in range(0, 5):
        for j in temp_length_total[i]:
            prediction_input.append(j)

        for j in temp_width_total[i]:
            prediction_input.append(j)

        for j in temp_height_total[i]:
            prediction_input.append(j)


    features = np.array(prediction_input).reshape((1,85))
    #print(features)
    prediction = model.predict(features)
    prediction_y = prediction.argmax(axis=-1)

    # Convert int64 to a JSON-serializable type
    prediction_y_serializable = prediction_y.item()

    insert_processing_summary(new_processing_id, employeeID, processing_time,prediction_y_serializable+1)

    print(prediction_y_serializable+1)
    return jsonify({"prediction": prediction_y_serializable + 1})

@app.route('/processing_summary', methods=['GET'])
def get_processing_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT p.processing_id, p.processing_time, p.processing_grade, p.employeeID, e.username
        FROM processing_summary p
        INNER JOIN employee e ON p.employeeID = e.employeeID
    """)
    processing_summary_data = c.fetchall()
    conn.close()

    processing_summary_list = []
    for row in processing_summary_data:
        processing_summary_item = {
            'processing_id': row[0],
            'processing_time': row[1],
            'processing_grade': row[2],
            'employeeID': row[3],
            'username': row[4]  
        }
        processing_summary_list.append(processing_summary_item)

    return jsonify({'processing_summary': processing_summary_list})

@app.route('/dashboard_processing_summary', methods=['GET'])
def get_dashboard_processing_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT p.processing_grade
        FROM processing_summary p
    """)
    processing_summary_data = c.fetchall()
    conn.close()

    total_processing = len(processing_summary_data)
    grade_counts = {'1': 0, '2': 0, '3': 0, '4': 0}

    for row in processing_summary_data:
        grade = row[0]
        if grade == '1':
            grade_counts['1'] += 1
        elif grade == '2':
            grade_counts['2'] += 1
        elif grade == '3':
            grade_counts['3'] += 1
        elif grade == '4':
            grade_counts['4'] += 1

    return jsonify({'total_processing': total_processing, 'grade_counts': grade_counts})


def process_data():

    data = pd.read_excel(excel_file, header=0)

    data.drop(["TIME", "COILNO", "APNNO", "ISEVERHOLD",
           "onhold", "CUSTNO", "INSPECTIONCODE",
           "DEF_A", "DEF_B", "DEF_C", "DEF_D", "DEF_E",
           "DEF_F", "LOC_F", "RATE_F", "AREA_F",
          "DEF_G", "LOC_G", "RATE_G", "AREA_G",
          "DEF_H", "LOC_H", "RATE_H", "AREA_H",
          "DEF_I", "LOC_I", "RATE_I", "AREA_I",
          "DEF_J", "LOC_J", "RATE_J", "AREA_J",], axis=1, inplace=True)
    
    # Split LOCATION into LENGTH, WIDTH, and HEIGHT
    data[['LOC_A_LENGTH', 'LOC_A_WIDTH', 'LOC_A_HEIGHT']] = data['LOC_A'].str.split("", expand=True).drop([0,4], axis=1)
    data.drop("LOC_A", axis=1, inplace=True)
    data[['LOC_B_LENGTH', 'LOC_B_WIDTH', 'LOC_B_HEIGHT']] = data['LOC_B'].str.split("", expand=True).drop([0,4], axis=1)
    data.drop("LOC_B", axis=1, inplace=True)
    data[['LOC_C_LENGTH', 'LOC_C_WIDTH', 'LOC_C_HEIGHT']] = data['LOC_C'].str.split("", expand=True).drop([0,4], axis=1)
    data.drop("LOC_C", axis=1, inplace=True)
    data[['LOC_D_LENGTH', 'LOC_D_WIDTH', 'LOC_D_HEIGHT']] = data['LOC_D'].str.split("", expand=True).drop([0,4], axis=1)
    data.drop("LOC_D", axis=1, inplace=True)
    data[['LOC_E_LENGTH', 'LOC_E_WIDTH', 'LOC_E_HEIGHT']] = data['LOC_E'].str.split("", expand=True).drop([0,4], axis=1)
    data.drop("LOC_E", axis=1, inplace=True)

   # Remove rows with unexpected value
    data.drop(data[
        (data['LOC_A_LENGTH'] != "H") &
        (data['LOC_A_LENGTH'] != "U") &
        (data['LOC_A_LENGTH'] != "M") &
        (data['LOC_A_LENGTH'] != "V") &
        (data['LOC_A_LENGTH'] != "T") &
        (data['LOC_A_WIDTH'] != "W") &
        (data['LOC_A_WIDTH'] != "X") &
        (data['LOC_A_WIDTH'] != "C") &
        (data['LOC_A_WIDTH'] != "Y") &
        (data['LOC_A_WIDTH'] != "D") &
        (data['LOC_A_WIDTH'] != "A") &
        (data['LOC_A_WIDTH'] != "F") &
        (data['LOC_A_HEIGHT'] != "T") &
        (data['LOC_A_HEIGHT'] != "B") &
        (data['LOC_A_HEIGHT'] != "D") &
        (data['LOC_B_LENGTH'] != "H") &
        (data['LOC_B_LENGTH'] != "U") &
        (data['LOC_B_LENGTH'] != "M") &
        (data['LOC_B_LENGTH'] != "V") &
        (data['LOC_B_LENGTH'] != "T") &
        (data['LOC_B_WIDTH'] != "W") &
        (data['LOC_B_WIDTH'] != "X") &
        (data['LOC_B_WIDTH'] != "C") &
        (data['LOC_B_WIDTH'] != "Y") &
        (data['LOC_B_WIDTH'] != "D") &
        (data['LOC_B_WIDTH'] != "A") &
        (data['LOC_B_WIDTH'] != "F") &
        (data['LOC_B_HEIGHT'] != "T") &
        (data['LOC_B_HEIGHT'] != "B") &
        (data['LOC_B_HEIGHT'] != "D") &
        (data['LOC_C_LENGTH'] != "H") &
        (data['LOC_C_LENGTH'] != "U") &
        (data['LOC_C_LENGTH'] != "M") &
        (data['LOC_C_LENGTH'] != "V") &
        (data['LOC_C_LENGTH'] != "T") &
        (data['LOC_C_WIDTH'] != "W") &
        (data['LOC_C_WIDTH'] != "X") &
        (data['LOC_C_WIDTH'] != "C") &
        (data['LOC_C_WIDTH'] != "Y") &
        (data['LOC_C_WIDTH'] != "D") &
        (data['LOC_C_WIDTH'] != "A") &
        (data['LOC_C_WIDTH'] != "F") &
        (data['LOC_C_HEIGHT'] != "T") &
        (data['LOC_C_HEIGHT'] != "B") &
        (data['LOC_C_HEIGHT'] != "D") &
        (data['LOC_D_LENGTH'] != "H") &
        (data['LOC_D_LENGTH'] != "U") &
        (data['LOC_D_LENGTH'] != "M") &
        (data['LOC_D_LENGTH'] != "V") &
        (data['LOC_D_LENGTH'] != "T") &
        (data['LOC_D_WIDTH'] != "W") &
        (data['LOC_D_WIDTH'] != "X") &
        (data['LOC_D_WIDTH'] != "C") &
        (data['LOC_D_WIDTH'] != "Y") &
        (data['LOC_D_WIDTH'] != "D") &
        (data['LOC_D_WIDTH'] != "A") &
        (data['LOC_D_WIDTH'] != "F") &
        (data['LOC_D_HEIGHT'] != "T") &
        (data['LOC_D_HEIGHT'] != "B") &
        (data['LOC_D_HEIGHT'] != "D") &
        (data['LOC_E_LENGTH'] != "H") &
        (data['LOC_E_LENGTH'] != "U") &
        (data['LOC_E_LENGTH'] != "M") &
        (data['LOC_E_LENGTH'] != "V") &
        (data['LOC_E_LENGTH'] != "T") &
        (data['LOC_E_WIDTH'] != "W") &
        (data['LOC_E_WIDTH'] != "X") &
        (data['LOC_E_WIDTH'] != "C") &
        (data['LOC_E_WIDTH'] != "Y") &
        (data['LOC_E_WIDTH'] != "D") &
        (data['LOC_E_WIDTH'] != "A") &
        (data['LOC_E_WIDTH'] != "F") &
        (data['LOC_E_HEIGHT'] != "T") &
        (data['LOC_E_HEIGHT'] != "B") &
        (data['LOC_E_HEIGHT'] != "D")
    ].index, inplace = True)


   # Convert all letters to uppercase
    data['LOC_A_LENGTH'] = data['LOC_A_LENGTH'].str.upper()


    # drop row that contains null value
    data = data.dropna(axis=0)

    # drop rows that contain target value 5
    data.drop(data[data['INSPDISP'] == 5].index, inplace = True)

    # Preprocess label column (R --> 4)
    data.loc[data['INSPDISP'] == 'R', 'INSPDISP'] = 4

    # print(data)

    return data

def convert_excel_to_sqlite(DB_PATH, excel_info_table_name):
    # Read the Excel file into a pandas DataFrame
    data = process_data()
    
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    
    # Convert the DataFrame to an SQLite table
    data.to_sql(excel_info_table_name, conn, if_exists='replace', index=False)
    
    # Close the connection
    conn.close()

######################### so far no use ############################
def export_to_excel(data, output_file):
    # Write the DataFrame to an Excel file
    data.to_excel(output_file, index=False)
####################################################################

@app.route('/convert_data', methods=['GET'])
def convert_data():
    try:

        # Connect to SQLite database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Check if the table exists and delete it if it does
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{excel_info_table_name}'")
        if c.fetchone():
            c.execute(f'DROP TABLE {excel_info_table_name}')
            conn.commit()

        # Close the connection before conversion as it will open its own connection
        conn.close()

        # Call the function to convert Excel data to SQLite
        convert_excel_to_sqlite(DB_PATH, excel_info_table_name)
        
        ################################################################
         # Read the data from the SQLite table into a DataFrame
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f'SELECT * FROM {excel_info_table_name}', conn)
        conn.close()
        
        # Export the data to an Excel file
        export_to_excel(df, 'output_data.xlsx')
        ######################################################################
        return jsonify({'message': 'Data Converted Successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

################### so far no use ###############################################################################
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f'SELECT * FROM {excel_info_table_name}', conn)  
    
    return jsonify({'data': df.to_dict(orient='records')})
###################################################################################################################

@app.route('/total_records', methods=['GET'])
def get_total_records():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Fetch the total count of records
        query = f"SELECT COUNT(*) FROM {excel_info_table_name}"
        c.execute(query)
        total_count = c.fetchone()[0]
        
        conn.close()
        
        # Return the data and total count as JSON
        return jsonify({'total_count': total_count}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/total_by_grade_in_experts_prediction', methods=['GET'])
def get_total_by_grade():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Fetch the total count by grade
        query = f"SELECT INSPDISP, COUNT(*) FROM {excel_info_table_name} GROUP BY INSPDISP"
        c.execute(query)
        total_by_grade = c.fetchall()
        
        conn.close()
        
        # Convert result to dictionary for JSON response
        total_by_grade_dict = {INSPDISP: count for INSPDISP, count in total_by_grade}
        
        # Return the data and total count by grade as JSON
        return jsonify(total_by_grade_dict), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


######################### so far no use ###############################################################################
@app.route('/get_grades_count', methods=['GET'])
def get_grades():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f'SELECT INSPDISP, COUNT(*) AS total FROM {excel_info_table_name} GROUP BY INSPDISP', conn)
    conn.close()
    
    # Convert the DataFrame to a dictionary
    grades_dict = df.set_index('INSPDISP')['total'].to_dict()
    
    return jsonify(grades_dict)
####################################################################################################################

@app.route('/grade_count_by_month', methods=['GET'])
def get_grade_count_by_month():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f'SELECT * FROM {excel_info_table_name}', conn)
    
    # Convert DATE column to datetime format
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
    # Extract month and year from DATE column
    df['MONTH'] = df['DATE'].dt.month
    df['YEAR'] = df['DATE'].dt.year

    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'July', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    
    # Replace numeric month values with month names
    df['MONTH'] = df['MONTH'].map(month_names)

    # Group by month, year, and INSPDISP, then count occurrences
    grade_count_by_month = df.groupby(['YEAR', 'MONTH', 'INSPDISP']).size().reset_index(name='COUNT')
    
    # Convert DataFrame to dictionary
    grade_count_dict = {}
    for row in grade_count_by_month.itertuples(index=False):
        year = row.YEAR
        month = row.MONTH
        grade = row.INSPDISP
        count = row.COUNT
        key = f"{month} {year}"
        if key not in grade_count_dict:
            grade_count_dict[key] = {}
        grade_count_dict[key][grade] = count

    # Ensure all months have values for grades 1, 2, 3, and 4
    for month_dict in grade_count_dict.values():
        for grade in range(1, 5):
            if int(grade) not in month_dict:
                month_dict[int(grade)] = 0

    return jsonify(grade_count_dict)


@app.route('/AIPredictionByEmployee/<employeeID>', methods=['GET'])
def get_AIPrediction_by_employee(employeeID):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT p.processing_grade
        FROM processing_summary p
        WHERE p.employeeID = ?
    """, (employeeID,))
    processing_summary_data = c.fetchall()
    conn.close()

    total_processing = len(processing_summary_data)
    grade_counts = {'1': 0, '2': 0, '3': 0, '4': 0}

    for row in processing_summary_data:
        grade = row[0]
        if grade == '1':
            grade_counts['1'] += 1
        elif grade == '2':
            grade_counts['2'] += 1
        elif grade == '3':
            grade_counts['3'] += 1
        elif grade == '4':
            grade_counts['4'] += 1

    return jsonify({'total_processing': total_processing, 'grade_counts': grade_counts})

def get_total_processing_by_employee():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT employee.username, IFNULL(COUNT(processing_summary.employeeID), 0) 
        FROM employee
        LEFT JOIN processing_summary 
        ON employee.employeeID = processing_summary.employeeID 
        GROUP BY employee.employeeID
    """)
    total_processing = c.fetchall()
    conn.close()
    return total_processing

@app.route('/total_processing_for_each_employee', methods=['GET'])
def total_processing_by_employee():
    total_processing = get_total_processing_by_employee()
    result = [{'username': row[0], 'total_processing': row[1]} for row in total_processing]
    return jsonify({'total_processing_by_employee': result})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
