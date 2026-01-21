import pandas as pd
from datetime import datetime

files = {
    'Sales A': '01_Data_Analytics/01A_sales_builder.csv',
    'Sales B': '01_Data_Analytics/01B_sales_builder.csv',
    'Target A': '01_Data_Analytics/01A_target_sales_builder.csv',
    'Target B': '01_Data_Analytics/01B_target_sales_builder.csv',
    'CRM A': '01_Data_Analytics/02A_api_crm_builder.csv',
    'CRM B': '01_Data_Analytics/02B_api_crm_builder.csv',
    'Traffic A': '01_Data_Analytics/02A_api_traffic_builder.csv',
    'Traffic B': '01_Data_Analytics/02B_api_traffic_builder.csv',
}

output = []
output.append("# Date Range Analysis\n")
output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

for name, file in files.items():
    output.append(f"\n## {name}")
    output.append(f"**File:** `{file}`\n")
    
    try:
        df = pd.read_csv(file)
        output.append(f"**Rows:** {len(df)}")
        output.append(f"**Columns:** {list(df.columns)}\n")
        
        # Find date columns
        date_cols = []
        for col in df.columns:
            if 'date' in col.lower() or 'create' in col.lower():
                date_cols.append(col)
        
        if 'year' in df.columns and 'month' in df.columns:
            # Target files have year/month
            min_year = df['year'].min()
            max_year = df['year'].max()
            min_month = df[df['year'] == min_year]['month'].min()
            max_month = df[df['year'] == max_year]['month'].max()
            output.append(f"**Date Range:** {min_year}-{min_month:02d} to {max_year}-{max_month:02d}")
        elif date_cols:
            # Has date column
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                min_date = df[col].min()
                max_date = df[col].max()
                output.append(f"**{col}:** {min_date} to {max_date}")
        else:
            output.append("**No date columns found**")
        
        output.append("")
        
    except Exception as e:
        output.append(f"**Error:** {e}\n")

# Overlap analysis
output.append("\n## Date Overlap Analysis\n")

date_ranges = {}
for name, file in files.items():
    try:
        df = pd.read_csv(file)
        
        if 'year' in df.columns and 'month' in df.columns:
            min_date = pd.to_datetime(f"{df['year'].min()}-{df[df['year'] == df['year'].min()]['month'].min():02d}-01")
            max_date = pd.to_datetime(f"{df['year'].max()}-{df[df['year'] == df['year'].max()]['month'].max():02d}-01")
            date_ranges[name] = (min_date, max_date)
        else:
            for col in df.columns:
                if 'date' in col.lower() or 'create' in col.lower():
                    df[col] = pd.to_datetime(df[col], errors='coerce', utc=True).dt.tz_localize(None)
                    date_ranges[name] = (df[col].min(), df[col].max())
                    break
    except:
        pass

if date_ranges:
    # Split by builder
    a_ranges = {k: v for k, v in date_ranges.items() if ' A' in k}
    b_ranges = {k: v for k, v in date_ranges.items() if ' B' in k}
    
    # Check Builder A overlap
    if a_ranges:
        output.append("### Builder A Files\n")
        a_min = min([d[0] for d in a_ranges.values()])
        a_max = max([d[1] for d in a_ranges.values()])
        output.append(f"**Overall Range:** {a_min.strftime('%Y-%m-%d')} to {a_max.strftime('%Y-%m-%d')}\n")
        
        all_a_start_same = len(set([d[0] for d in a_ranges.values()])) == 1
        all_a_end_same = len(set([d[1] for d in a_ranges.values()])) == 1
        
        if all_a_start_same and all_a_end_same:
            output.append("** 100% Overlap ** - All Builder A files cover exact same date range\n")
        else:
            output.append("** Partial Overlap ** - Builder A files cover different date ranges:\n")
            for name, (start, end) in a_ranges.items():
                output.append(f"- **{name}:** {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
            output.append("")
    
    # Check Builder B overlap
    if b_ranges:
        output.append("### Builder B Files\n")
        b_min = min([d[0] for d in b_ranges.values()])
        b_max = max([d[1] for d in b_ranges.values()])
        output.append(f"**Overall Range:** {b_min.strftime('%Y-%m-%d')} to {b_max.strftime('%Y-%m-%d')}\n")
        
        all_b_start_same = len(set([d[0] for d in b_ranges.values()])) == 1
        all_b_end_same = len(set([d[1] for d in b_ranges.values()])) == 1
        
        if all_b_start_same and all_b_end_same:
            output.append("** 100% Overlap ** - All Builder B files cover exact same date range\n")
        else:
            output.append("** Partial Overlap ** - Builder B files cover different date ranges:\n")
            for name, (start, end) in b_ranges.items():
                output.append(f"- **{name}:** {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")

# Write to file
with open('01_Data_Analytics/03_date_ranges.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('\n'.join(output))
print("\n✓ Saved to: 01_Data_Analytics/03_date_ranges.md")