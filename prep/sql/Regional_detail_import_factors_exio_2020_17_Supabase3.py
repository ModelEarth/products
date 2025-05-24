import psycopg2
import pandas as pd
import os

# Database connection details
host = 'aws-0-us-west-1.pooler.supabase.com'
database = 'postgres'
user = 'postgres.dxgxrduioffmwbwikliq'
password = 'ModelEarth@Exiobase'
port = '5432'

# Function to map pandas dtypes to SQL types
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    else:
        return 'TEXT'

# Prompt user for data source
data_source = input("Do you want to load data from a URL or a local file? (Enter 'url' or 'file'): ").strip().lower()
if data_source == 'url':
    csv_url = input("Please enter the URL: ").strip()
    print("Reading the CSV file from the URL...")
    data = pd.read_csv(csv_url)
elif data_source == 'file':
    csv_file_path = input("Please enter the file path: ").strip()
    print("Reading the CSV file from the local file...")
    data = pd.read_csv(csv_file_path)
else:
    print("Invalid input. Please enter 'url' or 'file'.")
    exit()

print("CSV file read successfully.")

# Connect to the Supabase database
print("Connecting to the database...")
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)
cur = conn.cursor()
print("Connected to the database.")

# Check if table exists
cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sectorimport_flow');")
table_exists = cur.fetchone()[0]

if table_exists:
    data_handling = input("The table 'SectorImport_Flow' exists. Do you want to delete existing data before adding new data or append new data to the existing data? (Enter 'delete' or 'append'): ").strip().lower()
    if data_handling == 'delete':
        print("Deleting existing data...")
        cur.execute("DELETE FROM SectorImport_Flow;")
        conn.commit()
        print("Existing data deleted.")
    elif data_handling == 'append':
        print("Appending new data to existing data.")
    else:
        print("Invalid input. Please enter 'delete' or 'append'.")
        cur.close()
        conn.close()
        exit()
else:
    print("Table 'SectorImport_Flow' does not exist. It will be created.")

# Generate SQL create table statement
columns = data.columns
dtypes = data.dtypes
column_defs = ', '.join([f'{col} {map_dtype(dtype)}' for col, dtype in zip(columns, dtypes)])

create_table_query = f'''
CREATE TABLE IF NOT EXISTS SectorImport_Flow (
    {column_defs}
);
'''

# Create the table if it does not exist
if not table_exists:
    print("Creating the table...")
    cur.execute(create_table_query)
    conn.commit()
    print("Table created successfully.")

# Batch insert data into the table
batch_size = 1000
num_rows = len(data)
print(f"Inserting {num_rows} rows into the table...")
for start in range(0, num_rows, batch_size):
    end = min(start + batch_size, num_rows)
    batch = data.iloc[start:end]

    placeholders = ', '.join(['%s'] * len(batch.columns))
    insert_query = f'''
    INSERT INTO SectorImport_Flow ({', '.join(columns)}) VALUES ({placeholders})
    '''
    try:
        cur.executemany(insert_query, batch.values)
        conn.commit()
        print(f"Inserted rows {start} to {end}")
    except Exception as e:
        print(f"Error inserting rows {start} to {end}: {e}")
        conn.rollback()

cur.close()
conn.close()
print("Data insertion completed.")