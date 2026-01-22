# OpenHouse.ai Data Integration Pipeline

**Technical Assessment Submission - Data & Integration Engineer**

## Overview

This pipeline integrates homebuilder data from multiple sources (sales CSVs, target files, CRM API, web traffic API) into monthly community-level reports for business analysis.

**Output:** `14_final_report_simple.csv` - Monthly sales, targets, CRM leads, and web traffic aggregated by builder and community.

## Quick Start

### Prerequisites

```bash
python 3.11+
pip install requirements.txt
```

### Run the Full Pipeline

```bash
cd "/01_Data_Analytics"
python 01_Data_Analytics/00_run_pipeline.py
```

This master script executes all 9 steps in sequence and handles errors gracefully.

## Project Structure

```
project_root/
├── 01_Data_Analytics/
│   ├── 00_raw_data/              # Place raw data files here
│   │   ├── sales_builder_a.csv
│   │   ├── sales_builder_b.csv
│   │   ├── target_sales_builder_a.xlsx
│   │   └── target_sales_builder_b.csv
│   ├── 00_run_pipeline.py        # Master pipeline executor
│   ├── 01_xlsx_to_csv...py       # Step 1: Convert & standardize
│   ├── 02_API_download.py        # Step 2: Fetch API data
│   ├── 04_date_premerge.py       # Step 3: Add date columns
│   ├── 05_sales_date_monthly.py  # Step 4: Aggregate sales
│   ├── 06_merge_A+B.py           # Step 5: Combine builders
│   ├── 10_API_community_fix.py   # Step 6: Standardize API
│   ├── 12_API_to_monthly...py    # Step 7: Aggregate API
│   ├── 13_API_monthly...py       # Step 8: Detailed API agg
│   ├── 14_final_merge.py         # Step 9: Final merge
│   └── 14_final_report_simple.csv # FINAL OUTPUT
└── README.md
```

## Pipeline Steps

### Step 1: Convert & Standardize Raw Files

**Script:** `01_xlsx_to_csv+date_fix+name_fix.py`

* Converts Excel to CSV
* Standardizes date formats to `YYYY-MM-DD`
* Standardizes community names (removes variations)
* Handles special semicolon-delimited Excel format for Builder A targets

**Outputs:** `01A_sales_builder.csv`, `01B_sales_builder.csv`, `01A_target_sales_builder.csv`, `01B_target_sales_builder.csv`

### Step 2: Download API Data

**Script:** `02_API_download.py`

* Fetches CRM leads from API (6214 Builder A, 6314 Builder B)
* Fetches web traffic from API (3405 records each)
* Saves to CSV for processing

**Outputs:** `02A_api_crm_builder.csv`, `02B_api_crm_builder.csv`, `02A_api_traffic_builder.csv`, `02B_api_traffic_builder.csv`

### Step 3: Add Date Columns

**Script:** `04_date_premerge.py`

* Parses dates with flexible format handling
* Adds `year`, `month`, `day` columns to sales files
* Logs any failed date parsing

**Outputs:** `04A_sales_preprocessed.csv`, `04B_sales_preprocessed.csv`, `04A_target_preprocessed.csv`, `04B_target_preprocessed.csv`

### Step 4: Aggregate Sales to Monthly

**Script:** `05_sales_date_monthly.py`

* Groups sales by community, year, month
* Counts total sales and breaks down by type (spec/build/model)
* Sums revenue and sqft
* Merges with targets, calculates variance

**Outputs:** `05A_sales_target_merged.csv`, `05B_sales_target_merged.csv`

### Step 5: Combine Builders

**Script:** `06_merge_A+B.py`

* Concatenates Builder A and B into single dataset
* Adds `builder` column to distinguish

**Output:** `06_sales_target_combined.csv`

### Step 6: Standardize API Data

**Script:** `10_API_community_fix.py`

* Standardizes community names in CRM and traffic data
* Filters out unknown communities (Stonegate Heights, Conner Heights)

**Outputs:** `10A_crm_standardized.csv`, `10B_crm_standardized.csv`, `10A_traffic_standardized.csv`, `10B_traffic_standardized.csv`

### Step 7: Aggregate API to Monthly (Simple)

**Script:** `12_API_to_monthly_crm_simple.py`

* Aggregates CRM to monthly lead counts
* Aggregates traffic to monthly session totals

**Outputs:** `12A_crm_monthly.csv`, `12B_crm_monthly.csv`, `12A_traffic_monthly.csv`, `12B_traffic_monthly.csv`

### Step 8: Aggregate API to Monthly (Detailed)

**Script:** `13_API_monthly_crm_detailed.py`

* Includes breakdowns by source (PAID_SEARCH, ORGANIC_SEARCH, etc.)
* Includes breakdowns by status (NEW_LEAD, IN_PROGRESS, etc.)

**Outputs:** `13A_crm_monthly_detailed.csv`, `13B_crm_monthly_detailed.csv`, etc.

### Step 9: Final Merge

**Script:** `14_final_merge.py`

* Merges sales+targets with CRM and traffic data
* Creates both simple and detailed versions
* Fills missing values appropriately
* Sorts by date, builder, community

**Outputs:**

* `14_final_report_simple.csv` (main deliverable)
* `14_final_report_detailed.csv` (with source/status breakdowns)

## Output Schema

### Final Report (Simple Version)

| Column         | Description                        | Type   |
| -------------- | ---------------------------------- | ------ |
| community      | Community name (standardized)      | string |
| year           | Year                               | int    |
| month          | Month (1-12)                       | int    |
| total_sales    | Number of homes sold               | int    |
| total_revenue  | Sum of sale prices                 | float  |
| total_sqft     | Sum of square footage              | float  |
| spec_sales     | Count of spec homes sold           | int    |
| build_sales    | Count of build-to-order homes sold | int    |
| model_sales    | Count of model homes sold          | int    |
| sales_target   | Monthly sales target               | int    |
| variance       | actual_sales - target_sales        | int    |
| builder        | 'A' or 'B'                         | string |
| crm_lead_count | Number of CRM leads created        | int    |
| web_traffic    | Total website sessions             | int    |
| unique_users   | Unique website visitors            | int    |

**Row count:** 279 (8 communities × ~35 months average)

## Data Quality Features

### Date Standardization

* Handles 6+ date formats: `YYYY-MM-DD`, `MM/DD/YYYY`, `DD-MM-YYYY`, etc.
* Reports any failed parsing with diagnostic output
* **Result:** 0 sales lost due to date issues (validated)

### Community Name Standardization

Maps all variations to canonical names:

**Builder A (4 communities):**

* Fairview Estates (combines: Fairview Est., FairviewEstates, Fairview Estates (FVE), Fairview Estates - Phase 2)
* Cedar Creek
* Glenview Meadows
* Riverbend Townhomes

**Builder B (4 communities):**

* Maplewood Heights (combines: Maplewood-Heights, Maplewood Heights - Phase 2)
* Oakridge Villas
* Sunset Pines
* Willow Creek Meadows

### Data Validation

* **Sales preservation:** 738 total sales (410 Builder A + 328 Builder B) fully preserved
* **Zero data loss:** Aggregation validated to maintain all records
* **Diagnostic scripts:** `07_visual_validation.py`, `08_summary_validation.py` create charts and reports

## Validation Scripts (Optional)

### Visual Validation

```bash
python 01_Data_Analytics/07_visual_validation.py
```

Creates charts comparing pre-merge vs post-merge data to verify no information loss.

### Summary Validation

```bash
python 01_Data_Analytics/08_summary_validation.py
```

Generates markdown report with totals comparison and detected issues.

### CRM/Traffic Check

```bash
python 01_Data_Analytics/09_CRM+traffic_check.py
```

Analyzes API data quality before standardization.

## Configuration

### API Credentials

Located in `02_API_download.py`:

```python
API_BASE = "https://builder-api-875175326233.us-central1.run.app/builder-api"
API_KEY = "bapi_sk_c8f9a2b7e4d1c5a3f6b9d2e7a1c4b8f5"
```

### File Paths

All paths are relative to project root. **Changing the parent folder name will not break the pipeline.**

## Known Issues & Design Decisions

### Date Range Mismatch

* **Sales:** 2023-2025 (historical + current)
* **Targets:** 2025-2026 (future forecasts only)
* **CRM/Traffic:** 2024-2025 (recent activity)

**Decision:** Report includes ALL months where any data exists. Months without targets show blank `sales_target` and `variance`.

### Unknown Communities

Traffic data contains 2 communities not in sales/targets:

* Stonegate Heights (Builder A)
* Conner Heights (Builder B)

**Decision:** Filtered out in Step 6 as they have no sales targets.

### CRM Rating Field

Builder B CRM has 1,170 records with blank `rating` field.

**Decision:** Kept as-is (represents "not yet rated" status).

## Troubleshooting

### Unicode Errors

If you see `'charmap' codec can't encode character` errors:

* Ensure all scripts have `sys.stdout.reconfigure(encoding='utf-8')` at the top
* Run from terminal that supports UTF-8 (not Windows Command Prompt)

### File Not Found

* Ensure you're running from project root directory
* Check that `01_Data_Analytics/00_raw_data/` contains all source files

### API Connection Failures

* Verify API key is valid
* Check network allows connections to Google Cloud Run
* API may have rate limits (built-in 10-second timeout)

## Performance

* **Total runtime:** ~30-60 seconds (depends on API speed)
* **Memory usage:** <500MB
* **Output size:** ~50KB (simple), ~200KB (detailed)

## Testing

Run validation after pipeline:

```bash
python 01_Data_Analytics/08_summary_validation.py
```

Check that "Pre-merge sales" = "Post-merge sales" (should both be 738).

## Contact

Adam Prpick, Aprpick@gmail.com

---

**Last Updated:** 2026-01-21

**Pipeline Version:** 1.0

**Total Scripts:** 15 (9 core pipeline + 6 validation/diagnostic)
