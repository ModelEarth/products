[Profile Panels](../../../) and [Trade Flow](../../../../profile/trade/)

# DuckDB Parquet

## Parquet files from USEEIO json (forerunner to Exiobase pull)

View our [Parquet using WASM javascript from USEEIO data](../../../impacts/useeio/parquet) and [in GitHub repo](https://github.com/ModelEarth/profile/tree/main/impacts/useeio/parquet) - dev by Satyabrat
<!-- When readme added: [DuckDB parquet files from USEEIO](../../../impacts/useeio) -->
[Another DuckDB parquet via Javascript](parquet-sample.html) - These are slow due to WASM speed in browser. Json is quicker.

<!-- these 2 also reside on trade page -->
[NEW - Parquet To Github](https://colab.research.google.com/drive/1Pqpdebj4rY06E6NAgqJskgt-G4HBHPUZ?usp=sharing)
[NEW - Colab to Github](https://colab.research.google.com/drive/1mnZKBypCBlVLXiCuSpGj0JZf4NZzNR7h?usp=sharing)



## Prior Notes

View our DuckDB parquet tables in [ObservableHQ Dashboard](https://observablehq.com/d/2898d01446cefef1) and [Static Framework](/data-commons/dist/innovation/)  

We shifted away from starting from the merged US Economy .csv files created with the US EPA script. Our newer work pulls from the international exiobase data (which includes Comtrade) using Colabs to push to Github.

Our prior 8.4MB **US-2020-17schema.duckdb** output resides in [profile/impacts/exiobase/US-source](https://github.com/ModelEarth/profile/tree/main/impacts/exiobase/US-source). 
We're moving it into the 2020 subfolder and adding parquet files there also.

Also see our [Supabase from .csv files page](../../sql/supabase), the resulting upcoming [Impact Charts](../../../impacts/) and our [Related Projects TO DO List](../../../prep/)

<!--
View our [Failed Javascript attempt for DuckDB](tables.html) - TO DO: Debug Javascript or start fresh. (We could use functions from [built Observable](/data-commons/dist/innovation/))
-->

The <!-- Loren couldn't find load_data.py, so he's guessing duckdb-db-loader.py is the new name. -->[duckdb-db-loader2.py](https://github.com/ModelEarth/profile/blob/main/prep/sql/duckdb/)  script is designed to load data from a CSV file into a DuckDB database. It provides flexibility in loading data from both a URL and a local file, dynamically creating a table in [DuckDB](https://duckdb.org/docs/api/r.html) based on the columns of the input data, and allowing users to choose whether to append new data to an existing table or replace existing data. The user is prompted to either enter a URL for a YAML file or provide the path to a locally stored YAML file. This YAML file serves as a reference, allowing users to map file names to the desired table names, and to determine which columns to omit or retain. Using this information, a new table will be created with the specified table name, including only the retained columns and excluding those listed for omission.

Table migrations and column names are set in [create-database.yaml](https://github.com/ModelEarth/profile/blob/main/impacts/exiobase/US-source/create-database.yaml)


## Requirements
- Python 3.6 or higher installed. Required Python packages:
- requests: For making HTTP requests to download files from URLs.
- yaml: For loading and parsing YAML files.
- duckdb: For interacting with DuckDB databases
- pandas: For data manipulation and analysis.



### Download DuckDB:
Download and install DuckDB from DuckDB website.


### Prepare Data and Configuration:
Ensure your CSV files are accessible either via URLs or locally.
Prepare a create-database.yaml file specifying the source and configuration of your CSV files.


### Usage
1. Clone or download the repository to your local machine.
2. Install the required Python libraries (`duckdb` and `pandas`) using pip:
   ```sh
   pip install duckdb pandas requests pyyaml
   ```
3. Run the script duckdb-db-loader.py:
   ```sh
   python duckdb-db-loader.py
   ```
4. Follow the prompts:
   - Choose whether to load data from a URL or a local file.
   - Provide the URL or the path to the local CSV file.
   - If the table already exists in the DuckDB database, choose whether to delete existing data and add new data, or append new data to the existing data.


### Script Breakdown

## 1. Loading Data
- The script prompts the user to choose between loading data from a URL or a local file.
- Depending on the user's choice, the script loads the data into a pandas DataFrame using `pd.read_csv()` from either the provided URL or the local file path.

## 2. Dynamically Creating the DuckDB Table
- The script dynamically infers the column types from the DataFrame and creates the DuckDB table using a `CREATE TABLE` statement.
- Column types are inferred as INTEGER, DOUBLE, or VARCHAR based on the data types in the DataFrame.

## 3. Handling Existing Tables
- If the table already exists in the DuckDB database, the script prompts the user to choose whether to delete existing data and add new data, or append new data to the existing data.

## 4. Loading Data into DuckDB
- The script loads the data into the DuckDB table using an `INSERT INTO` statement.
- Depending on the user's choice, it either appends the new data to the existing table or replaces existing data with the new data.

## 5. Verification
- After loading the data, the script verifies the number of rows loaded into the DuckDB table and displays the count to the user.

### Monitor Progress:
The script will output status messages indicating the loading and transformation of data, as well as any errors encountered.

### YAML Configuration (create-database.yaml):
Modify the YAML file to specify the following:
source: CSV file names or URLs.
columns: Column mappings for renaming.
omit: Columns to omit from CSV files.


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

---

** When loading local CSV files, provide paths using slashes (/) rather than backslashes (\\).
