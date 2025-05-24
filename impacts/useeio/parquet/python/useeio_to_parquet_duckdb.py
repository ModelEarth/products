import duckdb
import os
import json
import re

"""
Note schema design for demands data has been modified
The primary key is a combination of Sector Id and State
"""

# Directory paths
drive_path = '<useeio_path_data>'
parquet_base_path = '<base_path_for_parquet_files>'  


def createConnection():
    try:
        # DuckDB connection
        db = duckdb.connect()
        print("Connected to DuckDB")
        return db
    except Exception as e:
        print(e)


def createParquetFiles(db):
    """
    Create Parquet files for Factor, Sector, Indicator, and other data if they don't exist.
    """
    try:
        tables = ["Factor", "Sector", "Indicator", "RoUS_Consumption_Complete", "RoUS_Consumption_Domestic",
                  "RoUS_Production_Complete", "RoUS_Production_Domestic", "Consumption_Complete",
                  "Consumption_Domestic",
                  "Production_Complete", "Production_Domestic", "Matrix_M", "Matrix_N", "Matrix_x"]

        for table_name in tables:
            parquet_file_path = os.path.join(parquet_base_path, f"{table_name}.parquet")

            # If the Parquet file does not exist, create an empty Parquet file
            if not os.path.exists(parquet_file_path):
                db.execute(
                    f"CREATE TABLE {table_name} (Dummy VARCHAR)")
                db.execute(f"COPY {table_name} TO '{parquet_file_path}' (FORMAT PARQUET)")
                print(f"Parquet file created for table: {table_name}")

    except Exception as e:
        print(e)


def factorData(db):
    try:
        db.execute(
            f"CREATE TABLE Factor (FactorID INTEGER, FlowUUID VARCHAR, FactorName VARCHAR, Unit VARCHAR, Context VARCHAR)")

        factor_data = []
        flowId = 1
        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            flows_file = os.path.join(state_path, 'flows.json')

            if os.path.isfile(flows_file):
                with open(flows_file, 'r') as f:
                    flows_data = json.load(f)

                    # Collect data for Factor table
                    for flow in flows_data:
                        factor_id = flowId
                        flow_uuid = flow.get('uuid')
                        factor_name = flow.get('flowable')
                        unit = flow.get('unit')
                        context = flow.get('context')
                        factor_data.append((factor_id, flow_uuid, factor_name, unit, context))
                        flowId += 1

        # Write data to Parquet file
        parquet_file_path = os.path.join(parquet_base_path, "Factor.parquet")
        db.executemany("""
        INSERT INTO Factor (FactorID, FlowUUID, FactorName, Unit, Context)
        VALUES (?, ?, ?, ?, ?);
        """, factor_data)
        db.execute(f"COPY Factor TO '{parquet_file_path}' (FORMAT PARQUET)")

    except Exception as e:
        print(e)


def sectorData(db):
    try:
        db.execute(f"CREATE TABLE Sector (SectorID VARCHAR, SectorName VARCHAR)")
        sector_data = []
        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            sectors_file = os.path.join(state_path, 'sectors.json')

            if os.path.isfile(sectors_file):
                with open(sectors_file, 'r') as f:
                    sectors_data = json.load(f)

                    # Collect data for Sector table
                    for sector in sectors_data:
                        sector_id = sector.get('id')
                        sector_name = sector.get('name')
                        sector_data.append((sector_id, sector_name))

        unique_sector_data = list(set(sector_data))

        parquet_file_path = os.path.join(parquet_base_path, "Sector.parquet")

        db.executemany("""
        INSERT INTO Sector (SectorID, SectorName)
        VALUES (?, ?);
        """, unique_sector_data)
        db.execute(f"COPY Sector TO '{parquet_file_path}' (FORMAT PARQUET)")

    except Exception as e:
        print(e)


def indicatorData(db):
    try:
        db.execute("""
            DROP TABLE IF EXISTS Indicator;
        """)
        db.execute("""
                CREATE TABLE IF NOT EXISTS Indicator (
                    "Name" VARCHAR PRIMARY KEY,
                    Code VARCHAR,
                    Unit VARCHAR,
                    "Group" VARCHAR,
                    SimpleUnit VARCHAR,
                    SimpleName VARCHAR
                  );
                """)
        indicator_table = []
        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            indicator_path = os.path.join(state_path, 'indicators.json')

            if os.path.isfile(indicator_path):
                with open(indicator_path, 'r') as f:
                    indicators = json.load(f)

                    # Collect data for Indicator table
                    for indicator in indicators:
                        name = indicator.get('name')
                        code = indicator.get('code')
                        unit = indicator.get('unit')
                        group = indicator.get('group')
                        simpleunit = indicator.get('simpleunit')
                        simplename = indicator.get('simplename')
                        indicator_table.append((name, code, unit, group, simpleunit, simplename))

        unique_indicator_data = list(set(indicator_table))

        # Write data to Parquet file
        parquet_file_path = os.path.join(parquet_base_path, "Indicator.parquet")
        db.executemany("""
        INSERT INTO Indicator (Name, Code, Unit, "Group", SimpleUnit, SimpleName)
        VALUES (?, ?, ?, ?, ?, ?);
        """, unique_indicator_data)
        db.execute(f"COPY Indicator TO '{parquet_file_path}' (FORMAT PARQUET)")

    except Exception as e:
        print(e)


def demandsData(db):
    try:
        tables = ["RoUS_Consumption_Complete", "RoUS_Consumption_Domestic", "RoUS_Production_Complete",
                  "RoUS_Production_Domestic", "Consumption_Complete", "Consumption_Domestic", "Production_Complete",
                  "Production_Domestic"]

        db.execute("""
                DROP TABLE IF EXISTS RoUS_Consumption_Complete;
                CREATE TABLE IF NOT EXISTS RoUS_Consumption_Complete (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );

                DROP TABLE IF EXISTS RoUS_Consumption_Domestic;
                CREATE TABLE IF NOT EXISTS RoUS_Consumption_Domestic (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );

                DROP TABLE IF EXISTS RoUS_Production_Complete;
                CREATE TABLE IF NOT EXISTS RoUS_Production_Complete (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );

                DROP TABLE IF EXISTS RoUS_Production_Domestic;
                CREATE TABLE IF NOT EXISTS RoUS_Production_Domestic (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );

                DROP TABLE IF EXISTS Consumption_Complete;
                CREATE TABLE IF NOT EXISTS Consumption_Complete (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );

                DROP TABLE IF EXISTS Consumption_Domestic;
                CREATE TABLE IF NOT EXISTS Consumption_Domestic (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );

                DROP TABLE IF EXISTS Production_Complete;
                CREATE TABLE IF NOT EXISTS Production_Complete (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );

                DROP TABLE IF EXISTS Production_Domestic;
                CREATE TABLE IF NOT EXISTS Production_Domestic (
                    Sector VARCHAR,
                    Amount FLOAT DEFAULT 0,
                    State VARCHAR,
                    PRIMARY KEY (Sector, State)
                  );
                """)

        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            state = ""
            match = re.match(r'^([A-Z]{2})', state_folder)
            if match:
                state = match.group(1)

            flows_path = os.path.join(state_path, 'demands')
            iter = 0
            json_files = [file for file in os.listdir(flows_path) if file.endswith('.json')]

            for jsonFile in json_files:
                file_path = os.path.join(flows_path, jsonFile)
                table_name = tables[iter]
                iter += 1

                with open(file_path, 'r') as f:
                    data = json.load(f)
                    demand_data = [(entry.get('sector'), entry.get('amount'), state) for entry in data]

                    # Write data to Parquet file
                    parquet_file_path = os.path.join(parquet_base_path, f"{table_name}.parquet")

                    db.executemany(f"""
                    INSERT INTO "{table_name}" (Sector, Amount, State)
                    VALUES (?, ?, ?);
                    """, demand_data)
                    db.execute(f"COPY {table_name} TO '{parquet_file_path}' (FORMAT PARQUET)")

    except Exception as e:
        print(e)

def matrixMData(db):
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS Matrix_M (
          Sector FLOAT[],
          State VARCHAR
        );
        """)

        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            matrix_path = os.path.join(state_path, 'matrix/M.json')

            # Extract state code (first 2 characters of state folder)
            state = state_path.split('/')[-1][:2]
            print(f"Processing Matrix_M data for state: {state}")

            if os.path.isfile(matrix_path):
                with open(matrix_path, 'r') as f:
                    data = json.load(f)
                    for x in data:
                        db.execute("""
                          INSERT INTO Matrix_M (Sector, State)
                          VALUES (?, ?);
                        """, (x, state))

        # export it to Parquet
        parquet_file_path = os.path.join(parquet_base_path, "Matrix_M.parquet")
        db.execute(f"COPY Matrix_M TO '{parquet_file_path}' (FORMAT PARQUET)")

    except Exception as e:
        print(f"Error in matrixMData: {e}")


def matrixNData(db):
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS Matrix_N (
          Sector FLOAT[],
          State VARCHAR
        );
        """)

        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            matrix_path = os.path.join(state_path, 'matrix/N.json')

            state = state_path.split('/')[-1][:2]
            print(f"Processing Matrix_N data for state: {state}")

            if os.path.isfile(matrix_path):
                with open(matrix_path, 'r') as f:
                    data = json.load(f)
                    for x in data:
                        # Insert data into Matrix_N table
                        db.execute("""
                          INSERT INTO Matrix_N (Sector, State)
                          VALUES (?, ?);
                        """, (x, state))

        parquet_file_path = os.path.join(parquet_base_path, "Matrix_N.parquet")
        db.execute(f"COPY Matrix_N TO '{parquet_file_path}' (FORMAT PARQUET)")

    except Exception as e:
        print(f"Error in matrixNData: {e}")


def matrixxData(db):
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS Matrix_x (
          IndustryOutput DOUBLE[],
          State VARCHAR
        );
        """)

        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            matrix_path = os.path.join(state_path, 'matrix/x.json')

            state = state_path.split('/')[-1][:2]
            print(f"Processing Matrix_x data for state: {state}")

            if os.path.isfile(matrix_path):
                with open(matrix_path, 'r') as f:
                    data = json.load(f)
                    for x in data:
                        db.execute("""
                          INSERT INTO Matrix_x (IndustryOutput, State)
                          VALUES (?, ?);
                        """, (x, state))

        parquet_file_path = os.path.join(parquet_base_path, "Matrix_x.parquet")
        db.execute(f"COPY Matrix_x TO '{parquet_file_path}' (FORMAT PARQUET)")

    except Exception as e:
        print(f"Error in matrixxData: {e}")

def readFromParquetFiles(db):
    try:
        # Sample function to read from a parquet file
        read_path = os.path.join(parquet_base_path, 'Indicator.parquet')
        indicator_query = f"""
        SELECT * FROM READ_PARQUET("{read_path}");
        """
        indicator_data = db.execute(indicator_query).fetchall()
        for row in indicator_data:
            print(row)

    except Exception as e:
        print(e)


def call(db):
    try:
        # Create Parquet files and load data
        createParquetFiles(db)
        factorData(db)
        sectorData(db)
        indicatorData(db)
        demandsData(db)
        matrixxData(db)
        matrixNData(db)
        matrixMData(db)
        readFromParquetFiles(db)

    except Exception as e:
        print(e)


def main():
    db = createConnection()
    if db is None:
        exit(1)

    call(db)
    db.close()


if __name__ == "__main__":
    main()
