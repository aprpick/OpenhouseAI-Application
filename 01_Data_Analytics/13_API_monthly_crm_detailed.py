import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== CRM + TRAFFIC DETAILED MONTHLY AGGREGATION ===\n")

# ============================================================================
# CRM BUILDER A
# ============================================================================

print("Processing CRM Builder A...")
crm_a = pd.read_csv('01_Data_Analytics/10A_crm_standardized.csv')
print(f"  Loaded: {len(crm_a)} rows")

# Parse date
date_col = 'createdate' if 'createdate' in crm_a.columns else 'create_at'
crm_a['date'] = pd.to_datetime(crm_a[date_col], errors='coerce', utc=True).dt.tz_localize(None)
crm_a['year'] = crm_a['date'].dt.year
crm_a['month'] = crm_a['date'].dt.month

# Total leads
crm_a_total = crm_a.groupby(['community', 'year', 'month']).size().reset_index(name='crm_lead_count')

# Leads by source (pivot)
source_col = 'hs_analytics_source' if 'hs_analytics_source' in crm_a.columns else 'sourcetype'
crm_a_by_source = crm_a.groupby(['community', 'year', 'month', source_col]).size().reset_index(name='count')
crm_a_source_pivot = crm_a_by_source.pivot_table(
    index=['community', 'year', 'month'],
    columns=source_col,
    values='count',
    fill_value=0
).reset_index()
# Flatten column names and add prefix
crm_a_source_pivot.columns = ['community', 'year', 'month'] + [f'source_{col}' for col in crm_a_source_pivot.columns[3:]]

# Leads by status (pivot)
status_col = 'hs_lead_status' if 'hs_lead_status' in crm_a.columns else 'rating'
crm_a_by_status = crm_a.groupby(['community', 'year', 'month', status_col]).size().reset_index(name='count')
crm_a_status_pivot = crm_a_by_status.pivot_table(
    index=['community', 'year', 'month'],
    columns=status_col,
    values='count',
    fill_value=0
).reset_index()
# Flatten column names and add prefix
crm_a_status_pivot.columns = ['community', 'year', 'month'] + [f'status_{col}' for col in crm_a_status_pivot.columns[3:]]

# Merge all together
crm_a_monthly = crm_a_total.merge(crm_a_source_pivot, on=['community', 'year', 'month'], how='left')
crm_a_monthly = crm_a_monthly.merge(crm_a_status_pivot, on=['community', 'year', 'month'], how='left')

print(f"  Aggregated to {len(crm_a_monthly)} community-months")
print(f"  Columns: {len(crm_a_monthly.columns)}")

# Save
crm_a_monthly.to_csv('01_Data_Analytics/13A_crm_monthly_detailed.csv', index=False)
print(f"  ✓ Saved to 13A_crm_monthly_detailed.csv\n")

# ============================================================================
# CRM BUILDER B
# ============================================================================

print("Processing CRM Builder B...")
crm_b = pd.read_csv('01_Data_Analytics/10B_crm_standardized.csv')
print(f"  Loaded: {len(crm_b)} rows")

# Parse date
date_col = 'createdate' if 'createdate' in crm_b.columns else 'create_at'
crm_b['date'] = pd.to_datetime(crm_b[date_col], errors='coerce', utc=True).dt.tz_localize(None)
crm_b['year'] = crm_b['date'].dt.year
crm_b['month'] = crm_b['date'].dt.month

# Total leads
crm_b_total = crm_b.groupby(['community', 'year', 'month']).size().reset_index(name='crm_lead_count')

# Leads by source
source_col = 'hs_analytics_source' if 'hs_analytics_source' in crm_b.columns else 'sourcetype'
crm_b_by_source = crm_b.groupby(['community', 'year', 'month', source_col]).size().reset_index(name='count')
crm_b_source_pivot = crm_b_by_source.pivot_table(
    index=['community', 'year', 'month'],
    columns=source_col,
    values='count',
    fill_value=0
).reset_index()
crm_b_source_pivot.columns = ['community', 'year', 'month'] + [f'source_{col}' for col in crm_b_source_pivot.columns[3:]]

# Leads by status
status_col = 'hs_lead_status' if 'hs_lead_status' in crm_b.columns else 'rating'
crm_b_by_status = crm_b.groupby(['community', 'year', 'month', status_col]).size().reset_index(name='count')
crm_b_status_pivot = crm_b_by_status.pivot_table(
    index=['community', 'year', 'month'],
    columns=status_col,
    values='count',
    fill_value=0
).reset_index()
crm_b_status_pivot.columns = ['community', 'year', 'month'] + [f'status_{col}' for col in crm_b_status_pivot.columns[3:]]

# Merge all together
crm_b_monthly = crm_b_total.merge(crm_b_source_pivot, on=['community', 'year', 'month'], how='left')
crm_b_monthly = crm_b_monthly.merge(crm_b_status_pivot, on=['community', 'year', 'month'], how='left')

print(f"  Aggregated to {len(crm_b_monthly)} community-months")
print(f"  Columns: {len(crm_b_monthly.columns)}")

# Save
crm_b_monthly.to_csv('01_Data_Analytics/13B_crm_monthly_detailed.csv', index=False)
print(f"  ✓ Saved to 13B_crm_monthly_detailed.csv\n")

# ============================================================================
# TRAFFIC (same as simple version - no breakdowns)
# ============================================================================

print("Processing Traffic Builder A...")
traffic_a = pd.read_csv('01_Data_Analytics/10A_traffic_standardized.csv')
print(f"  Loaded: {len(traffic_a)} rows")

traffic_a['date'] = pd.to_datetime(traffic_a['date'], errors='coerce', utc=True).dt.tz_localize(None)
traffic_a['year'] = traffic_a['date'].dt.year
traffic_a['month'] = traffic_a['date'].dt.month

traffic_a_monthly = traffic_a.groupby(['community', 'year', 'month']).agg({
    'sessions': 'sum',
    'users': 'sum'
}).reset_index()
traffic_a_monthly.columns = ['community', 'year', 'month', 'web_traffic', 'unique_users']
print(f"  Aggregated to {len(traffic_a_monthly)} community-months")

traffic_a_monthly.to_csv('01_Data_Analytics/13A_traffic_monthly_detailed.csv', index=False)
print(f"  ✓ Saved to 13A_traffic_monthly_detailed.csv\n")

print("Processing Traffic Builder B...")
traffic_b = pd.read_csv('01_Data_Analytics/10B_traffic_standardized.csv')
print(f"  Loaded: {len(traffic_b)} rows")

traffic_b['date'] = pd.to_datetime(traffic_b['date'], errors='coerce', utc=True).dt.tz_localize(None)
traffic_b['year'] = traffic_b['date'].dt.year
traffic_b['month'] = traffic_b['date'].dt.month

traffic_b_monthly = traffic_b.groupby(['community', 'year', 'month']).agg({
    'sessions': 'sum',
    'users': 'sum'
}).reset_index()
traffic_b_monthly.columns = ['community', 'year', 'month', 'web_traffic', 'unique_users']
print(f"  Aggregated to {len(traffic_b_monthly)} community-months")

traffic_b_monthly.to_csv('01_Data_Analytics/13B_traffic_monthly_detailed.csv', index=False)
print(f"  ✓ Saved to 13B_traffic_monthly_detailed.csv\n")

print("=== DETAILED AGGREGATION COMPLETE ===")
print("\nCreated files:")
print("  - 13A_crm_monthly_detailed.csv")
print("  - 13B_crm_monthly_detailed.csv")
print("  - 13A_traffic_monthly_detailed.csv")
print("  - 13B_traffic_monthly_detailed.csv")