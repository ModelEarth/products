import pandas as pd
import json
import os

data = "2022-NAICS-Codes-listed-numerically-2-Digit-through-6-Digit.xlsx"

# Load the Excel file
df = pd.read_excel(data)

# Clean column names: remove leading/trailing spaces and multiple spaces
df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

# Define the output directory: Inside 'Trade/Naics/'
output_dir = os.path.abspath(os.path.join(os.getcwd(), "../../Trade/naics"))

# Create the directory if it doesn’t exist
os.makedirs(output_dir, exist_ok=True)

# Find actual column names dynamically
naics_code_col = [col for col in df.columns if "NAICS US Code" in col][0]
naics_title_col = [col for col in df.columns if "NAICS US Title" in col][0]
description_col = [col for col in df.columns if "Description" in col][0]

# Define dictionaries for different NAICS lengths
naics_data = {2: [], 3: [], 4: [], 5: [], 6: []}

for _, row in df.iterrows():
    naics_code = str(row[naics_code_col]).strip()
    naics_title = str(row[naics_title_col]).strip().rstrip("T")
    
    description = str(row[description_col]).strip()
    
    # Remove leading zeros if "T" was present
    if row[naics_title_col].endswith("T"):
        naics_code = naics_code.lstrip("0")
    
    naics_length = len(naics_code)
    if naics_length in naics_data:
        naics_data[naics_length].append({
            "code": naics_code,
            "title": naics_title,
            "description": description
        })

# Save each NAICS level to a separate JSON file in 'Trade/Naics'
for length, entries in naics_data.items():
    file_name = f"Naics Code Length {length}.json"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w") as f:
        json.dump(entries, f, indent=4)

print(f"JSON files successfully created in: {output_dir}")
