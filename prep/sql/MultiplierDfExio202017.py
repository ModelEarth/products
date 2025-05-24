## 5. Multiplier_df_exio_2020_17sch.csv

import duckdb
import pandas as pd

def load_data_from_url(url):
    # Read the CSV file into a pandas DataFrame from the URL
    df = pd.read_csv(url)
    return df

def load_data_from_local(file_path):
    # Read the CSV file into a pandas DataFrame from the local file
    df = pd.read_csv(file_path)
    return df

def create_table_if_not_exists(con, df, table_name):
    # Generate SQL CREATE TABLE statement dynamically
    columns = df.columns
    column_types = []

    # Infer column types from the DataFrame
    for column in columns:
        if pd.api.types.is_integer_dtype(df[column]):
            column_type = 'INTEGER'
        elif pd.api.types.is_float_dtype(df[column]):
            column_type = 'DOUBLE'
        else:
            column_type = 'VARCHAR'
        column_types.append(f'"{column}" {column_type}')

    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(column_types)})'

    # Create the SQL table if it does not exist
    con.execute(create_table_query)

def load_data_to_table(con, df, table_name, append):
    # Register the DataFrame as a DuckDB relation
    con.register('df', df)
    
    if append:
        # Insert the DataFrame into the DuckDB table
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    else:
        # Delete existing data and insert the new data
        con.execute(f"DELETE FROM {table_name}")
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")

    print("Data loaded successfully!")

# User inputs
user_choice = input("Do you want to load data from a URL or a local file? (Enter 'url' or 'local'): ").strip().lower()
if user_choice == 'url':
    csv_url = input("Please enter the URL to the CSV file: ").strip()
    df = load_data_from_url(csv_url)
elif user_choice == 'local':
    csv_file_path = input("Please enter the path to the local CSV file: ").strip()
    df = load_data_from_local(csv_file_path)
else:
    raise ValueError("Invalid choice! Please enter 'url' or 'local'.")

# Drop the "year" column if it exists
if 'year' in df.columns:
    df = df.drop(columns=['year'])

# Define the DuckDB database path and table name
database_path = r"C:\Users\sahil\Downloads\EEIO_2020_2017schema_US.db"
table_name = 'MultiplierDfExio202017'

# Connect to (or create) the DuckDB database
con = duckdb.connect(database_path)

# Check if the table exists
table_exists = con.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='{table_name.lower()}'").fetchone()[0]

if table_exists:
    append_choice = input(f"The table '{table_name}' already exists. Do you want to delete existing data and add new data, or append new data to the existing data? (Enter 'delete' or 'append'): ").strip().lower()
    if append_choice == 'delete':
        append = False
    elif append_choice == 'append':
        append = True
    else:
        raise ValueError("Invalid choice! Please enter 'delete' or 'append'.")
else:
    # Create the table if it does not exist
    create_table_if_not_exists(con, df, table_name)
    append = True

# Create the table if it does not exist and load data
create_table_if_not_exists(con, df, table_name)
load_data_to_table(con, df, table_name, append)

# Verify the data load
row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
print(f"Number of rows in the table '{table_name}': {row_count}")

# Close the connection
con.close()
