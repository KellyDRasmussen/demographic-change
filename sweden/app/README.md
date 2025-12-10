# Swedish Demographic Change Explorer

An interactive visualization tool showing how Sweden's working-age population (18-67) has changed between 2014-2024, broken down by demographic background.

## Purpose

This tool counters simplistic "replacement" narratives by showing the nuanced reality of demographic change across Swedish kommuner. It demonstrates that different municipalities show different patterns of growth, stability, and change across various demographic categories.

## Features

- **Interactive map** of all 311 Swedish kommuner
- **4 demographic categories:**
  - Born overseas
  - Born in Sweden, both parents born overseas
  - Born in Sweden, one parent born overseas
  - Born in Sweden, both parents born in Sweden
- **Two view modes:**
  - Current snapshot (2024) - shows percentage of population by category
  - Change over time (2014-2024) - shows how demographics have shifted
- **Aggregation options** - combine categories to see broader "foreign background" groupings
- **Two change metrics:**
  - Percentage points change (e.g., from 15% to 25% = +10 pp)
  - Relative percent change (e.g., from 15% to 25% = +67%)
- **Statistics dashboard** with national totals and top/bottom kommuner

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Process the raw data (if needed)
python3 process_data.py

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Data

- **Source:** Statistics Sweden (SCB) - Table TAB4824
- **Population:** Working age (18-67 years)
- **Time period:** 2014-2024
- **Geography:** All 311 Swedish kommuner

## Files

- `app.py` - Main Streamlit application
- `process_data.py` - Data processing script
- `TAB4824_sv.csv` - Raw data from SCB (472MB)
- `processed_demographics.csv` - Cleaned, processed data
- `swedish_municipalities.geojson` - Municipal boundaries
- `requirements.txt` - Python dependencies

## Usage Examples

### View current foreign-born population percentage
1. Select "Current Snapshot (2024)"
2. Choose "Born overseas" from the dropdown
3. Explore the map - darker colors indicate higher percentages

### See change in mixed-background population
1. Select "Change Over Time (2014-2024)"
2. Choose "One parent born overseas (born in Sweden)"
3. Select "Percentage points" to see absolute change
4. Red areas show decrease, blue areas show increase

### Compare broader "foreign background" category
1. Check "Show aggregated view"
2. Select multiple categories (e.g., all except "Both parents born in Sweden")
3. Toggle between snapshot and change views

## License

[![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
