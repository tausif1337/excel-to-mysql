import pandas as pd
import mysql.connector
import numpy as np  # Import numpy for NaN handling

# MySQL Connection Details
mysql_config = {
    'host': 'localhost',
    'database': 'al-rukan-test-313937fb79',
    'user': 'root',
    'password': ''
}

# Excel file path
excel_file = 'customer.xlsx'

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

# Read Excel data and insert into corresponding MySQL tables
xls = pd.ExcelFile(excel_file)
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)
    table_name = sheet_name.replace(' ', '_').lower()  # Adjust table name if needed
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    
    # Generate column definitions from Excel columns
    for column in df.columns:
        column_name = column.replace(' ', '_').lower()  # Adjust column name if needed
        column_name = '`' + column_name + '`'  # Enclose column name in backticks
        column_type = 'VARCHAR(255)'  # Default to VARCHAR(255), adjust data type if needed
        create_table_query += f"{column_name} {column_type}, "
    
    create_table_query = create_table_query[:-2] + ")"  # Remove trailing comma and space
    cursor.execute(create_table_query)

    # Insert data into MySQL table
    for index, row in df.iterrows():
        # Replace NaN values with None (NULL in MySQL)
        row = [None if pd.isna(value) else value for value in row]
        
        # Insert row into MySQL table
        placeholders = ', '.join(['%s'] * len(row))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(insert_query, row)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully into MySQL tables.")
