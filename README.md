```
# OpenHouse.ai Data Engineering Assessment

## 📋 Project Overview
This repository contains a modular data processing pipeline designed to integrate disparate data sources for homebuilder analytics. It harmonizes Sales, Targets, CRM Leads, and Web Traffic data from two different builders (Builder A and Builder B) into a unified dataset ready for ML forecasting.

## 🚀 Quick Start
To set up the environment and run the full pipeline, execute the following commands in your terminal:

### 1. Install Dependencies
Ensure you have Python installed, then install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Run the Pipeline

**Execute the master orchestration script. This will run all steps in sequence (Ingestion → Cleaning → Merging → Validation).**

**code**Bash

```
python 01_Data_Analytics/00_run_pipeline.py
```

---

## 📂 Pipeline Architecture

**The solution is orchestrated by** **00_run_pipeline.py**, which executes the following modular steps:

### 1. Ingestion & Standardization

* **01_xlsx_to_csv+date_fix+name_fix.py**: The "Heavy Lifter." It ingests raw CSV and Excel files (handling specific semicolon-delimited formats), standardizes date formats to ISO 8601 (**YYYY-MM-DD**), and normalizes Community Names (e.g., mapping "Fairview" variations to "Fairview Estates").

### 2. API Integration (CRM & Traffic)

* **02_API_download.py**: Connects to the external Builder API to fetch raw CRM leads and Website Traffic data for both builders.
* **10_API_community_fix.py**: Performs entity resolution on the API data, cleaning mismatched community names (e.g., removing " - New Homes" suffixes) so they align with Sales data.

### 3. Aggregation & Feature Engineering

* **04_date_premerge.py**: Parses dates into **Year**, **Month**, and **Day** **features to enable accurate joining.**
* **05_sales_date_monthly.py**: Aggregates transactional sales data to a monthly grain, calculates revenue totals, and merges them with Sales Targets to calculate variance.
* **12_API_to_monthly_crm_simple.py**: Aggregates API data to a simple monthly count (Leads/Sessions per community).
* **13_API_monthly_crm_detailed.py**: Performs advanced aggregation, pivoting CRM data to create features for Lead Source (e.g., **source_social_media**) and Lead Status (e.g., **status_qualified**).

### 4. Merging

* **06_merge_A+B.py**: Unifies the datasets from Builder A and Builder B into a single schema.
* **14_final_merge.py**: The final step. Joins the Sales/Target data with the CRM/Traffic data to produce the final output CSVs.

### 5. Quality Assurance

* **03_data_dates_ranges.py**: Checks date ranges for overlap.
* **07_visual_validation.py**: Generates time-series plots to visually confirm data trends were preserved during merging.
* **08_summary_validation.py**: Automated integrity check. Calculates total sales/revenue before and after processing to ensure 0% data loss. Generates **08_summary_validation.md**.
* **09_ & 10_**: Check on API data to find duplicates, misnamed data or inconsistent date fomats.

---

## 📊 Output Files

**The pipeline generates two key reports in the** **01_Data_Analytics/** **folder:**

* **14_final_report_simple.csv**

  * **Description:** **High-level monthly aggregation suitable for executive reporting.**
  * **Key Columns:** **community**, **year**, **month**, **total_sales**, **sales_target**, **variance**, **crm_lead_count**, **web_traffic**.
* **14_final_report_detailed.csv**

  * **Description:** **Granular dataset including CRM lead sources and status breakdowns.**
  * **Key Features:** **Useful for ML models needing specific lead attribution (e.g.,** **source_social_media**, **status_qualified**).
