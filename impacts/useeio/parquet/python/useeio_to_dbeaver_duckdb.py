import duckdb
import os
import json
import re

"""
Install DBeaver in system - https://dbeaver.io/download/ 
Setup DuckDB database - https://duckdb.org/docs/guides/sql_editors/dbeaver.html 
Do not use :memory: as path as it is instance based

Matrix Data information - 
Matrix M - flows x sector
           each state has 1581 factors/flows with 146 individual sectors, so total size of matrix - 50 (states) x 1581 (factors) x 146 (sectors)
           
Matrix N - indicators x sector
           each state has 16 indicators with 146 individual sectors, so total size of matrix - 50 (states) x 16 (indicators) x 146 (sectors)

"""

file_path = '<your_file_path>'
db_path = '<your_db_path_in_dbeaver>'

def createConnection():
    try:
        db = duckdb.connect(db_path)
        print("Connected to DuckDB")
        return db
    except Exception as e:
        print(e)

def factorData(db):
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS Factor (
            FactorID VARCHAR PRIMARY KEY,
            FlowUUID VARCHAR,
            FactorName VARCHAR,
            Unit VARCHAR,
            Context VARCHAR
        );
        """)

        flow_data = []
        flowId = 1

        for state_folder in os.listdir(path):
            state_path = os.path.join(path, state_folder)
            if not os.path.isdir(state_path):
                continue
            flows_file = os.path.join(state_path, 'flows.json')

            if os.path.isfile(flows_file):
                # Read and parse the sectors.json file
                with open(flows_file, 'r') as f:
                    flows_data = json.load(f)

                    # Insert data into in-memory DuckDB
                    for flow in flows_data:
                        factor_id = flowId
                        flow_uuid = flow.get('uuid')
                        factor_name = flow.get('flowable')
                        unit = flow.get('unit')
                        context = flow.get('context')
                        flow_data.append((factor_id, flow_uuid, factor_name, unit, context))
                        flowId += 1


        db.executemany("""
        INSERT INTO Factor (FactorID, FlowUUID, FactorName, Unit, Context)
        VALUES (?, ?, ?, ?, ?);
        """, flow_data)
    except Exception as e:
        print(e)

def sectorData(db):
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS Sector (
            SectorID VARCHAR PRIMARY KEY,
            SectorName VARCHAR
        );
        """)
        sector_data = []
        for state_folder in os.listdir(drive_path):
            state_path = os.path.join(drive_path, state_folder)
            if not os.path.isdir(state_path):
                continue
            sectors_file = os.path.join(state_path, 'sectors.json')

            if os.path.isfile(sectors_file):
                # Read and parse the sectors.json file
                with open(sectors_file, 'r') as f:
                    sectors_data = json.load(f)

                    # Insert data into in-memory DuckDB
                    for sector in sectors_data:
                        sector_id = sector.get('id')
                        sector_name = sector.get('name')
                        sector_data.append((sector_id, sector_name))

        unique_sector_data = list(set(sector_data))
        db.executemany("""
        INSERT INTO Sector (SectorID, SectorName)
        VALUES (?, ?);
        """, unique_sector_data)

    except Exception as e:
        print(e)

def indicatorData(db):
    try:
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
            # print(indicator_file)

            if os.path.isfile(flows_file):
                # Read and parse the sectors.json file
                with open(indicator_path, 'r') as f:
                    indicators = json.load(f)

                    # Insert data into in-memory DuckDB
                    for indicator in indicators:
                        name = indicator.get('name')
                        code = indicator.get('code')
                        unit = indicator.get('unit')
                        group = indicator.get('group')
                        simpleunit = indicator.get('simpleunit')
                        simplename = indicator.get('simplename')
                        indicator_table.append((name, code, unit, group, simpleunit, simplename))

        unique_indicator_data = list(set(indicator_table))

        db.executemany("""
        INSERT INTO Indicator (Name, Code, Unit, "Group", SimpleUnit, SimpleName)
        VALUES (?, ?, ?, ?, ?, ?);
        """, unique_indicator_data)

    except Exception as e:
        print(e)


def demandsData(db):
    try:
        db.execute("""
        CREATE TABLE IF NOT EXISTS RoUS_Consumption_Complete (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );

        CREATE TABLE IF NOT EXISTS RoUS_Consumption_Domestic (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );

        CREATE TABLE IF NOT EXISTS RoUS_Production_Complete (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );

        CREATE TABLE IF NOT EXISTS RoUS_Production_Domestic (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );

        CREATE TABLE IF NOT EXISTS Consumption_Complete (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );

        CREATE TABLE IF NOT EXISTS Consumption_Domestic (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );

        CREATE TABLE IF NOT EXISTS Production_Complete (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );

        CREATE TABLE IF NOT EXISTS Production_Domestic (
            Sector VARCHAR PRIMARY KEY,
            Amount FLOAT DEFAULT 0,
            State VARCHAR
          );
        """)

        tables = ["RoUS_Consumption_Complete", "RoUS_Consumption_Domestic", "RoUS_Production_Complete",
                  "RoUS_Production_Domestic", "Consumption_Complete", "Consumption_Domestic", "Production_Complete",
                  "Production_Domestic"]

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
            # print(flows_path, state)

            json_files = [file for file in os.listdir(flows_path) if file.endswith('.json')]
            # print(json_files)

            for jsonFile in json_files:
                file_path = os.path.join(flows_path, jsonFile)
                table_name = tables[iter]
                iter += 1

                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for entry in data:
                        sector = entry.get('sector')
                        amount = entry.get('amount')
                        db.execute(f"""
                    INSERT OR REPLACE INTO "{table_name}" (Sector, Amount, State)
                    VALUES (?, ?, ?);
                    """, (sector, amount, state))


    except Exception as e:
        print(e)


def dataSourcesData(db):
    try:
        db.execute("""
          CREATE TABLE IF NOT EXISTS Data_Sources (
            Id INTEGER PRIMARY KEY,
            Title VARCHAR,
            Author VARCHAR,
            DataYear DATE,
            Url VARCHAR,
            "Primary" BOOLEAN
          );
        """)
        # No data available right now

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

            state = state_path.split('/')[-1][:2]
            #print(state)

            with open(matrix_path, 'r') as f:
                data = json.load(f)
                for x in data:
                    db.execute("""
                  INSERT INTO Matrix_M (Sector, State)
                  VALUES (?, ?);
                  """, (x, state))

    except Exception as e:
        print(e)


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
            # print(state)

            with open(matrix_path, 'r') as f:
                data = json.load(f)
                for x in data:
                    db.execute("""
                  INSERT INTO Matrix_N (Sector, State)
                  VALUES (?, ?);
                  """, (x, state))



    except Exception as e:
        print(e)


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
            # print(state)

            with open(matrix_path, 'r') as f:
                data = json.load(f)
                # print(data)
                for x in data:
                    con.execute("""
                  INSERT INTO Matrix_x (IndustryOutput, State)
                  VALUES (?, ?);
                  """, (x, state))

    except Exception as e:
        print(e)

def call(db):
    try:
        factorData(db)
        sectorDate(db)
        indicatorData(db)
        dataSourcesData(db)
        demandsData(db)
        matrixMData(db)
        matrixNData(db)
        matrixxData(db)

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
