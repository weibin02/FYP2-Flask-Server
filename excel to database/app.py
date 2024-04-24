from flask import Flask, request, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

# Define the path to your Excel file
excel_file = '2022 data raw.xlsx'

# Define the name of the SQLite database
db_file = 'excel_to_database.db'

# Define the name of the SQLite table
table_name = 'data'

# @app.route('/process', methods=['GET'])
def process_data():

    data = pd.read_excel(excel_file, header=0)

    data.drop(["DATE", "TIME", "COILNO", "APNNO", "ISEVERHOLD",
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

    print(data)

    return data


def convert_excel_to_sqlite(db_file, table_name):
    # Read the Excel file into a pandas DataFrame
    data = process_data()
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    
    # Convert the DataFrame to an SQLite table
    data.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Close the connection
    conn.close()


@app.route('/convert_data', methods=['GET'])
def convert_data():
    try:
        # Call the function to convert Excel data to SQLite
        convert_excel_to_sqlite(db_file, table_name)
        return jsonify({'message': 'Data converted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)  
    
    return jsonify({'data': df.to_dict(orient='records')})

   


@app.route('/total_records', methods=['GET'])
def get_total_records():
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # Fetch the total count of records
        c.execute("SELECT COUNT(*) FROM data")
        total_count = c.fetchone()[0]
        
        conn.close()
        
        # Return the data and total count as JSON
        return jsonify({'total_count': total_count}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
@app.route('/delete', methods=['GET'])
def delete():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("DELETE FROM data")
    conn.commit()
    conn.close()
    # Convert the list of tuples to a list of dictionaries
    return jsonify({'message': 'Data table deleted successfully'})


@app.route('/view_data', methods=['GET'])
def view_data():
    try:
        # Fetch data from SQLite database
        df, total_records = fetch_data_from_sqlite(db_file, table_name)
        # Convert DataFrame to JSON and return as response along with total records count
        return jsonify({'data': df.to_dict(orient='records'), 'total_records': total_records.tolist()})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
def fetch_data_from_sqlite(db_file, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    
    # Read data from the SQLite table into a pandas DataFrame
    df = pd.read_sql_query(f'SELECT * FROM {table_name} LIMIT 10', conn)  # Fetch only the first 10 records
    total_records = pd.read_sql_query(f'SELECT COUNT(*) FROM {table_name}', conn).iloc[0, 0]  # Get total count of records
    
    # Close the connection
    conn.close()
    
    return df, total_records

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
