import requests
import yaml
import pandas as pd
import psycopg2
from supabase import create_client, Client
from io import StringIO
import psycopg2.extras

# Function to load YAML configuration file
def load_yaml(file_path_or_url, is_url=True):
    if is_url:
        try:
            response = requests.get(file_path_or_url)
            response.raise_for_status()
            config = yaml.safe_load(response.text)
        except Exception as e:
            print(f"Failed to load the YAML file from URL: {e}")
            exit(1)
    else:
        try:
            with open(file_path_or_url, 'r') as file:
                config = yaml.safe_load(file)
        except Exception as e:
            print(f"Failed to load the YAML file from local path: {e}")
            exit(1)
    return config

# Supabase credentials - HIMANSHU'S LOGIN
supabase_url = "https://ivlbvaqjjklzallpvjvi.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2bGJ2YXFqamtsemFsbHB2anZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTgyNDIzNzcsImV4cCI6MjAzMzgxODM3N30.GWAujC6YvjoDUF45ZAUDmR2Vu2ZCyyxwbe-zkJWIUFU"
supabase: Client = create_client(supabase_url, supabase_key)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres.ivlbvaqjjklzallpvjvi",
    password="Himanshu@123",
    host="aws-0-us-east-1.pooler.supabase.com",
    port="6543"
)
cur = conn.cursor()

# Helper function to map pandas dtypes to SQL types compatible with PostgreSQL
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    else:
        return "TEXT"

# Function to convert column names to CamelCase without underscores
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].capitalize() + ''.join(x.title() for x in components[1:])

# Ask user to choose between loading data from URL or local file path
load_from_url = input("Do you want to load data from URL? (yes/no): ").strip().lower() == "yes"

if load_from_url:
    createDatabaseYaml = "https://raw.githubusercontent.com/ModelEarth/profile/main/impacts/exiobase/US-source/create-database.yaml"
    sourcePath = "https://raw.githubusercontent.com/ModelEarth/profile/main/impacts/exiobase/US-source/2020/"
else:
    createDatabaseYaml = input("Enter the path to your local create-database.yaml: ").strip()
    sourcePath = input("Enter the path to your local CSV files directory: ").strip()
    sourcePath = sourcePath + "\\"

# Load the YAML configuration file
config = load_yaml(createDatabaseYaml, is_url=load_from_url)

# Ask user for the value to replace 'XX' in table names
xx_value = input("Enter the value to replace 'XX' in table names: ").strip()

# Process each table in the YAML configuration
for table_name, table_config in config.items():
    # Replace 'XX' in the table name with the user-specified value
    if 'XX' in table_name:
        table_name = table_name.replace('XX', xx_value)

    csv_file = table_config['source']
    csv_url = sourcePath + csv_file
    print(f"Loading: {csv_url}")

    try:
        if load_from_url:
            response = requests.get(csv_url)
            response.raise_for_status()
            csv_content = StringIO(response.text)
        else:
            csv_content = open(csv_url, 'r')
        
        df = pd.read_csv(csv_content)
    except Exception as e:
        print(f"Failed to load CSV file from URL {csv_url}: {e}")
        continue  # Skip this file and move to the next one

    columns_map = table_config.get('columns', {})
    omit_columns = table_config.get('omit', [])

    # Drop omitted columns
    df.drop(columns=omit_columns, errors='ignore', inplace=True)

    # Rename columns as per the YAML configuration
    df.rename(columns=columns_map, inplace=True)

    # Generate new column names for remaining columns
    new_columns = {}
    for col in df.columns:
        if col not in columns_map.values():
            new_columns[col] = to_camel_case(col)
    df.rename(columns=new_columns, inplace=True)

    # Exclude 'Year' column if not explicitly included in columns_map
    if 'Year' not in columns_map.values() and 'Year' in df.columns:
        df.drop(columns=['Year'], inplace=True)

    # Check if the table already exists
    cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');")
    table_exists = cur.fetchone()[0]

    if table_exists:
        action = input(f"Table '{table_name}' already exists. Do you want to delete existing data or append to it? (delete/append): ").strip().lower()
        if action == "delete":
            cur.execute(f"TRUNCATE TABLE \"{table_name}\";")
            conn.commit()

    # Create table in Supabase if it doesn't exist
    columns_with_types = ", ".join([f'"{col}" {map_dtype(df[col].dtype)}' for col in df.columns])
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS "{table_name}" (
        {columns_with_types}
    );
    """
    print(f"Creating table with query: {create_table_query}")  # Print the query for debugging
    try:
        cur.execute(create_table_query)
        conn.commit()
    except Exception as e:
        print(f"Failed to create table {table_name}: {e}")
        continue  # Skip this table and move to the next one

    # Insert data in batches of 10000 rows
    batch_size = 10000
    rows = [tuple(x) for x in df.to_numpy()]
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f'INSERT INTO "{table_name}" VALUES ({placeholders})'

    try:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            psycopg2.extras.execute_batch(cur, insert_query, batch)
            conn.commit()
    except Exception as e:
        print(f"Failed to insert data into table {table_name}: {e}")
        conn.rollback()

# Close the PostgreSQL connection
cur.close()
conn.close()
