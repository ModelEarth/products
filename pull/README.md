About Script and Workflow

Documentation at: [model.earth/products/](http://model.earth/products/)

## Scripts Overview

### `product-footprints.py`
Main script for fetching EPD data from BuildingTransparency.org API and saving as YAML files organized by country and category.

### `analyze_emissions_data.py`
Analyzes all downloaded EPD YAML files to document emissions-related fields and impact data availability.

**Product Count:** Currently analyzes **184,614 products**:
- **US:** 149,325 products
- **India (IN):** 211 products  
- **Other countries:** 35,078 products (Great Britain, Germany, Netherlands, Canada, Mexico, China)

**Processing Performance:** 
- Estimated processing time: **~15.8 minutes per 100,000 files**
- For all 184,614 products: approximately **29 minutes**

The script scans the `products-data` directory and generates a comprehensive report documenting:
- GWP (Global Warming Potential) fields and coverage
- Other LCIA impact categories (Ozone depletion, Acidification, Eutrophication, etc.)
- Resource use indicators (Primary energy, Water use, Waste generation)
- Coverage breakdown by country and category

**Usage:**
```bash
python3 analyze_emissions_data.py
```

### `calculate_transportation_impact.py`
Utility module for calculating transportation impacts and adjusting GWP values based on actual vs. default transportation distances.

**Functions:**
- `calculate_transportation_impact(distance_km, load_kg, emission_factor)` - Calculates transportation impact in kgCO2e for a given distance and load
- `get_default_transportation_impact(epd)` - Extracts default transportation distance and mass from EPD and calculates default impact
- `calculate_adjusted_gwp(epd, actual_distance_km)` - Calculates adjusted GWP based on actual transportation distance, returning a dict with:
  - `base_gwp` - Original GWP value
  - `default_transport_impact` - Impact using category default distance
  - `actual_transport_impact` - Impact using user-provided distance
  - `adjusted_gwp` - Final GWP adjusted for actual transportation
  - `savings` - CO2e savings from reduced distance
  - `percentage_reduction` - Percentage reduction in total GWP

**Usage:**
```python
from calculate_transportation_impact import calculate_adjusted_gwp
import yaml

# Load an EPD
with open('epd.yaml', 'r') as f:
    epd = yaml.safe_load(f)

# Calculate adjusted GWP for 500 km distance
result = calculate_adjusted_gwp(epd, 500)
print(f"Adjusted GWP: {result['adjusted_gwp']:.2f} kgCO2e")
print(f"Savings: {result['savings']:.2f} kgCO2e ({result['percentage_reduction']:.1f}% reduction)")
```

**Formula:** Transportation Impact = Distance (km) × Load (kg) × Emission Factor (0.062 kgCO2e/ton-km) ÷ 1000

See [README.md](../README.md#transportation-impacts) for detailed documentation on transportation impact calculations.