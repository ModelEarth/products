[Profile Panels](../../../) and [Trade Flow](../../../../profile/trade/)

# DuckDB from .csv files

Also see our [Supabase from .csv files page](../../sql/supabase) and [TO DO List](../../../impacts/)

View our [Javascript for DuckDB](tables.html) - TO DO: Debug Javascript

## ### Overview

The `duckdb-db-loader.py` script is designed to load data from CSV files into a DuckDB database. It provides flexibility in loading data from both URLs and local files, dynamically creating tables in DuckDB based on input data columns, and allowing users to choose whether to append new data to an existing table or replace it.

Table migrations and column names are configured in `create-database.yaml`.

\### Requirements

\- Python 3.x

\- DuckDB

\- pandas

\### Usage

1\. Clone or download the repository to your local machine.

2\. Install the required Python libraries using pip:

\`\`\`bash

pip install duckdb pandas

\`\`\`

3\. Run the script:

\`\`\`bash

python [duckdb-db-loader.py](http://duckdb-db-loader.py)

\`\`\`

4\. Follow the prompts:

- Choose whether to load data from a URL or a local file.

- Provide the URL or the path to the local CSV file.

- If the table already exists in the DuckDB database, choose whether to delete existing data and add new data or append new data to the existing table.

\### Script Breakdown

1\. **Loading Data**

- The script prompts the user to choose between loading data from a URL or a local file.

- Data is loaded into a pandas DataFrame using `pd.read_csv()`.

2\. **Dynamically Creating the DuckDB Table**

- The script infers column types from the DataFrame and creates the DuckDB table using a `CREATE TABLE` statement.

- Column types are inferred as INTEGER, DOUBLE, or VARCHAR.

3\. **Handling Existing Tables**

- If the table already exists, the script prompts the user to choose whether to delete existing data and add new data or append new data to the existing data.

4\. **Loading Data into DuckDB**

- The script uses an `INSERT INTO` statement to load data into the DuckDB table.

- It either appends new data to the existing table or replaces existing data.

5\. **Verification**

- The script verifies the number of rows loaded into the DuckDB table and displays the count.

\### Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

**Note:** When loading local CSV files, provide paths using slashes (\`/\`) rather than backslashes (\`\\\`).

\### Additional Overview

This Python script loads data from CSV files into a DuckDB database based on configurations provided in a YAML file. It supports dynamic column mapping and data manipulation before insertion into DuckDB tables.

\### Features

\- Loads data from CSV files into DuckDB tables.

\- Supports configuration through a YAML file for specifying data sources and table mappings.

\- Allows users to choose between loading data from URLs or local file paths.

\- Provides options to delete existing data or append to it when tables already exist in the DuckDB database.

\### Prerequisites

\- Python 3.6 or higher installed.

\- Required Python packages:

- `requests`

- `yaml`

- `pandas`

- `duckdb`

\### Setup

1\. Install required Python packages using pip:

\`\`\`bash

pip install requests yaml pandas duckdb

\`\`\`

2\. Download and install DuckDB from the DuckDB website.

3\. Prepare Data and Configuration:

- Ensure your CSV files are accessible either via URLs or locally.

- Prepare a `create-database.yaml` file specifying the source and configuration of your CSV files.

\### Usage

1\. Navigate to the directory containing the script and run:

\`\`\`bash

python duckdb_data\_[loader.py](http://loader.py)

\`\`\`

2\. Follow the prompts:

- Choose whether to load data from URLs or local file paths.

- Provide paths or URLs as required.

- Follow prompts to delete existing data or append to it for existing DuckDB tables.

3\. Monitor Progress:

- The script will output status messages indicating the loading and transformation of data, as well as any errors encountered.

\### YAML Configuration (\`create-database.yaml\`)

\- Modify to specify:

- `source`: CSV file names or URLs.

- `columns`: Column mappings for renaming.

- `omit`: Columns to omit from CSV files.