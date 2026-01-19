# OpenHouse.ai Application - Data Engineering Practice

Practice repository for OpenHouse.ai Data & Integration Engineer position.

## Project Structure

```
OpenhouseAI/
├── 01_Data_Analytics/
│   ├── 00_data_raw.csv          # Sample messy homebuilder data
│   ├── 01_data_explorer.py      # Data profiling & exploration
│   ├── 02_csv_cleaner.py        # Data cleaning pipeline
│   └── *_output/                # Generated reports (gitignored)
├── requirements.txt
└── README.md
```

## Scripts

### 01_data_explorer.py
Analyzes CSV files and generates comprehensive markdown reports.

**Features:**
- Classifies columns as: numerical, categorical, date, or text
- Detects data quality issues
- Provides type-specific statistics
- Outputs: `01.1_output.md`

**Usage:**
```bash
python 01_Data_Analytics/01_data_explorer.py
```

### 02_csv_cleaner.py
Cleans and standardizes messy data.

**Features:**
- Adds unique row IDs
- Flags/removes duplicates
- Standardizes dates and phone numbers
- Extracts numeric values from text
- Handles missing values
- Outputs: `02_data_clean.csv` (read-only)

**Usage:**
```bash
python 01_Data_Analytics/02_csv_cleaner.py
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate:
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Pipeline Philosophy

- **Raw data is sacred** - Original files never modified
- **Output CSVs are read-only** - Prevents accidental data corruption
- **Every transformation tracked** - Row IDs maintain lineage
- **Flexible for any dataset** - Not hardcoded to specific schemas

## About OpenHouse.ai

OpenHouse.ai is an AI-powered predictive analytics platform for homebuilders, helping them:
- Forecast sales demand
- Qualify leads with behavioral data
- Optimize construction timing

This project practices the core data engineering skills needed for their integration pipeline.

## Author

Adam Prpick | APEGA EIT  
Preparing for OpenHouse.ai Data & Integration Engineer position