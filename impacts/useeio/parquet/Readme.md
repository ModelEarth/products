[DuckDB Prep](../../../prep/sql/duckdb/)

# Reading Parquet Files with DuckDB-WASM and JavaScript  

These files provide examples of reading Parquet files using DuckDB-WASM and JavaScript.  

DuckDB parquet files can be [displayed using javascript WASM](indicator.html), but load times are slow.  
NEW: So we're also focused on outputting [json files from exiobase trade data](../../json/). 

DBeaver provides [CloudBeaver](https://dbeaver.com/docs/cloudbeaver/) for web-based database management, allowing multiple users to collaborate on database operations.

## Examples  

- **Indicators Table**: The first example demonstrates reading the **Indicators** table, which contains 16 entries.  
- **Sector & Production Complete Amount**: The second example combines data from two tables—**Sector** and **Production Complete Amount**—based on a selected state.  

### Parquet Javascript Exmples

1. [Indicators (total 16) table](indicator.html)

2. [Combines Sector and Production Complete Amount](SectorvsProductionComplete.html) using a selected State

3. [Join Example Using Sector](JoinExampleUsingSector.html)

## To do
Use a Constant Js file to store all constant values (like State's code) and Parquet file's urls instead of hard-coding in the static files.

[View related python in the GitHub repo](https://github.com/ModelEarth/profile/tree/main/impacts/useeio/parquet) - dev by Satyabrat