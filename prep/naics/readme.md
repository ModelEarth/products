# NAICS Data Processing and Export to JSON

### Naics_Data_ Processing.py: 
This Python script processes an Excel file(2022-NAICS-Codes-listed-numerically-2-Digit-through-6-Digit.xlsx) containing NAICS data (codes, titles, and descriptions), categorizes the data by the length of the NAICS codes, and exports it into separate JSON files to Prep/trade/Naics.

### Input file : 
2022-NAICS-Codes-listed-numerically-2-Digit-through-6-Digit.xlsx.

source: https://www.naics.com/search/
2125 rows


### Output files: (in trade repository)
1. Naics Code Length 2.json - 17 rows
2. Naics Code Length 3.json - 96 rows
3. Naics Code Length 4.json - 308 rows
4. Naics Code Length 5.json - 692 rows
5. Naics Code Length 2.json - 1012 rows


## Requirements

- Python 3.x
- `pandas` library
- `openpyxl` (for reading `.xlsx` files)

You can install the required dependencies using pip.

