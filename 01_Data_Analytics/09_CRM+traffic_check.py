import pandas as pd
from datetime import datetime

print("=== CRM + TRAFFIC DATA CHECK ===\n")

# Load data
crm_a = pd.read_csv('01_Data_Analytics/02A_api_crm_builder.csv')
crm_b = pd.read_csv('01_Data_Analytics/02B_api_crm_builder.csv')
traffic_a = pd.read_csv('01_Data_Analytics/02A_api_traffic_builder.csv')
traffic_b = pd.read_csv('01_Data_Analytics/02B_api_traffic_builder.csv')

print(f"Loaded CRM A: {len(crm_a)} rows")
print(f"Loaded CRM B: {len(crm_b)} rows")
print(f"Loaded Traffic A: {len(traffic_a)} rows")
print(f"Loaded Traffic B: {len(traffic_b)} rows\n")

# ============================================================================
# CREATE MARKDOWN REPORT
# ============================================================================

output = []
output.append("# CRM + Traffic Data Quality Check\n")
output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# CRM BUILDER A
# ============================================================================

output.append("## CRM - Builder A\n")
output.append(f"**Total Records:** {len(crm_a)}\n")
output.append(f"**Columns:** {', '.join(crm_a.columns.tolist())}\n")

# Date column
date_col = None
for col in ['createdate', 'create_at', 'date']:
    if col in crm_a.columns:
        date_col = col
        break

if date_col:
    output.append(f"**Date Column:** `{date_col}`")
    
    # Sample dates
    output.append(f"\n**Sample Dates:**")
    for date in crm_a[date_col].head(5):
        output.append(f"- {date}")
    
    # Try parsing
    crm_a['parsed_date'] = pd.to_datetime(crm_a[date_col], errors='coerce', utc=True)
    failed = crm_a['parsed_date'].isna().sum()
    output.append(f"\n**Date Parsing:**")
    output.append(f"- Successfully parsed: {len(crm_a) - failed}")
    output.append(f"- Failed to parse: {failed}")
    
    if failed > 0:
        output.append(f"\n**Failed Dates:**")
        for date in crm_a[crm_a['parsed_date'].isna()][date_col].head(5):
            output.append(f"- {date}")
    
    # Date range
    if failed < len(crm_a):
        output.append(f"\n**Date Range:**")
        output.append(f"- Min: {crm_a['parsed_date'].min()}")
        output.append(f"- Max: {crm_a['parsed_date'].max()}")

# Community names
if 'community' in crm_a.columns:
    output.append(f"\n**Unique Communities:** {crm_a['community'].nunique()}")
    output.append(f"\n**Community Names:**")
    for comm in sorted(crm_a['community'].unique()):
        count = len(crm_a[crm_a['community'] == comm])
        output.append(f"- {comm} ({count} records)")

# Categorical features
categorical_cols = []
for col in crm_a.columns:
    if col not in [date_col, 'community'] and crm_a[col].dtype == 'object':
        categorical_cols.append(col)

if categorical_cols:
    output.append(f"\n**Categorical Features:**")
    for col in categorical_cols:
        unique_vals = crm_a[col].nunique()
        output.append(f"\n*{col}* ({unique_vals} unique values):")
        for val in crm_a[col].value_counts().head(10).index:
            count = crm_a[col].value_counts()[val]
            output.append(f"- {val}: {count}")

# ============================================================================
# CRM BUILDER B
# ============================================================================

output.append("\n## CRM - Builder B\n")
output.append(f"**Total Records:** {len(crm_b)}\n")
output.append(f"**Columns:** {', '.join(crm_b.columns.tolist())}\n")

# Date column
date_col = None
for col in ['createdate', 'create_at', 'date']:
    if col in crm_b.columns:
        date_col = col
        break

if date_col:
    output.append(f"**Date Column:** `{date_col}`")
    
    # Sample dates
    output.append(f"\n**Sample Dates:**")
    for date in crm_b[date_col].head(5):
        output.append(f"- {date}")
    
    # Try parsing
    crm_b['parsed_date'] = pd.to_datetime(crm_b[date_col], errors='coerce', utc=True)
    failed = crm_b['parsed_date'].isna().sum()
    output.append(f"\n**Date Parsing:**")
    output.append(f"- Successfully parsed: {len(crm_b) - failed}")
    output.append(f"- Failed to parse: {failed}")
    
    if failed > 0:
        output.append(f"\n**Failed Dates:**")
        for date in crm_b[crm_b['parsed_date'].isna()][date_col].head(5):
            output.append(f"- {date}")
    
    # Date range
    if failed < len(crm_b):
        output.append(f"\n**Date Range:**")
        output.append(f"- Min: {crm_b['parsed_date'].min()}")
        output.append(f"- Max: {crm_b['parsed_date'].max()}")

# Community names
if 'community' in crm_b.columns:
    output.append(f"\n**Unique Communities:** {crm_b['community'].nunique()}")
    output.append(f"\n**Community Names:**")
    for comm in sorted(crm_b['community'].unique()):
        count = len(crm_b[crm_b['community'] == comm])
        output.append(f"- {comm} ({count} records)")

# Categorical features
categorical_cols = []
for col in crm_b.columns:
    if col not in [date_col, 'community'] and crm_b[col].dtype == 'object':
        categorical_cols.append(col)

if categorical_cols:
    output.append(f"\n**Categorical Features:**")
    for col in categorical_cols:
        unique_vals = crm_b[col].nunique()
        output.append(f"\n*{col}* ({unique_vals} unique values):")
        for val in crm_b[col].value_counts().head(10).index:
            count = crm_b[col].value_counts()[val]
            output.append(f"- {val}: {count}")

# ============================================================================
# TRAFFIC BUILDER A
# ============================================================================

output.append("\n## Web Traffic - Builder A\n")
output.append(f"**Total Records:** {len(traffic_a)}\n")
output.append(f"**Columns:** {', '.join(traffic_a.columns.tolist())}\n")

# Date column
if 'date' in traffic_a.columns:
    output.append(f"**Date Column:** `date`")
    
    # Sample dates
    output.append(f"\n**Sample Dates:**")
    for date in traffic_a['date'].head(5):
        output.append(f"- {date}")
    
    # Try parsing
    traffic_a['parsed_date'] = pd.to_datetime(traffic_a['date'], errors='coerce', utc=True)
    failed = traffic_a['parsed_date'].isna().sum()
    output.append(f"\n**Date Parsing:**")
    output.append(f"- Successfully parsed: {len(traffic_a) - failed}")
    output.append(f"- Failed to parse: {failed}")
    
    # Date range
    if failed < len(traffic_a):
        output.append(f"\n**Date Range:**")
        output.append(f"- Min: {traffic_a['parsed_date'].min()}")
        output.append(f"- Max: {traffic_a['parsed_date'].max()}")

# Community names
if 'community' in traffic_a.columns:
    output.append(f"\n**Unique Communities:** {traffic_a['community'].nunique()}")
    output.append(f"\n**Community Names:**")
    for comm in sorted(traffic_a['community'].unique()):
        count = len(traffic_a[traffic_a['community'] == comm])
        output.append(f"- {comm} ({count} records)")

# ============================================================================
# TRAFFIC BUILDER B
# ============================================================================

output.append("\n## Web Traffic - Builder B\n")
output.append(f"**Total Records:** {len(traffic_b)}\n")
output.append(f"**Columns:** {', '.join(traffic_b.columns.tolist())}\n")

# Date column
if 'date' in traffic_b.columns:
    output.append(f"**Date Column:** `date`")
    
    # Sample dates
    output.append(f"\n**Sample Dates:**")
    for date in traffic_b['date'].head(5):
        output.append(f"- {date}")
    
    # Try parsing
    traffic_b['parsed_date'] = pd.to_datetime(traffic_b['date'], errors='coerce', utc=True)
    failed = traffic_b['parsed_date'].isna().sum()
    output.append(f"\n**Date Parsing:**")
    output.append(f"- Successfully parsed: {len(traffic_b) - failed}")
    output.append(f"- Failed to parse: {failed}")
    
    # Date range
    if failed < len(traffic_b):
        output.append(f"\n**Date Range:**")
        output.append(f"- Min: {traffic_b['parsed_date'].min()}")
        output.append(f"- Max: {traffic_b['parsed_date'].max()}")

# Community names
if 'community' in traffic_b.columns:
    output.append(f"\n**Unique Communities:** {traffic_b['community'].nunique()}")
    output.append(f"\n**Community Names:**")
    for comm in sorted(traffic_b['community'].unique()):
        count = len(traffic_b[traffic_b['community'] == comm])
        output.append(f"- {comm} ({count} records)")

# Save markdown
with open('01_Data_Analytics/09_crm_traffic_check.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('\n'.join(output))
print("\n✓ Saved to: 09_crm_traffic_check.md")
print("\n=== CHECK COMPLETE ===")