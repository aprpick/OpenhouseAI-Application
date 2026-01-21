import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== CRM + TRAFFIC MONTHLY AGGREGATION ===\n")

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

# Aggregate to monthly
crm_a_monthly = crm_a.groupby(['community', 'year', 'month']).size().reset_index(name='crm_lead_count')
print(f"  Aggregated to {len(crm_a_monthly)} community-months")

# Save
crm_a_monthly.to_csv('01_Data_Analytics/12A_crm_monthly.csv', index=False)
print(f"  ✓ Saved to 12A_crm_monthly.csv\n")

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

# Aggregate to monthly
crm_b_monthly = crm_b.groupby(['community', 'year', 'month']).size().reset_index(name='crm_lead_count')
print(f"  Aggregated to {len(crm_b_monthly)} community-months")

# Save
crm_b_monthly.to_csv('01_Data_Analytics/12B_crm_monthly.csv', index=False)
print(f"  ✓ Saved to 12B_crm_monthly.csv\n")

# ============================================================================
# TRAFFIC BUILDER A
# ============================================================================

print("Processing Traffic Builder A...")
traffic_a = pd.read_csv('01_Data_Analytics/10A_traffic_standardized.csv')
print(f"  Loaded: {len(traffic_a)} rows")

# Parse date
traffic_a['date'] = pd.to_datetime(traffic_a['date'], errors='coerce', utc=True).dt.tz_localize(None)
traffic_a['year'] = traffic_a['date'].dt.year
traffic_a['month'] = traffic_a['date'].dt.month

# Aggregate to monthly (sum sessions and users)
traffic_a_monthly = traffic_a.groupby(['community', 'year', 'month']).agg({
    'sessions': 'sum',
    'users': 'sum'
}).reset_index()
traffic_a_monthly.columns = ['community', 'year', 'month', 'web_traffic', 'unique_users']
print(f"  Aggregated to {len(traffic_a_monthly)} community-months")

# Save
traffic_a_monthly.to_csv('01_Data_Analytics/12A_traffic_monthly.csv', index=False)
print(f"  ✓ Saved to 12A_traffic_monthly.csv\n")

# ============================================================================
# TRAFFIC BUILDER B
# ============================================================================

print("Processing Traffic Builder B...")
traffic_b = pd.read_csv('01_Data_Analytics/10B_traffic_standardized.csv')
print(f"  Loaded: {len(traffic_b)} rows")

# Parse date
traffic_b['date'] = pd.to_datetime(traffic_b['date'], errors='coerce', utc=True).dt.tz_localize(None)
traffic_b['year'] = traffic_b['date'].dt.year
traffic_b['month'] = traffic_b['date'].dt.month

# Aggregate to monthly (sum sessions and users)
traffic_b_monthly = traffic_b.groupby(['community', 'year', 'month']).agg({
    'sessions': 'sum',
    'users': 'sum'
}).reset_index()
traffic_b_monthly.columns = ['community', 'year', 'month', 'web_traffic', 'unique_users']
print(f"  Aggregated to {len(traffic_b_monthly)} community-months")

# Save
traffic_b_monthly.to_csv('01_Data_Analytics/12B_traffic_monthly.csv', index=False)
print(f"  ✓ Saved to 12B_traffic_monthly.csv\n")

print("=== AGGREGATION COMPLETE ===")
print("\nCreated files:")
print("  - 12A_crm_monthly.csv")
print("  - 12B_crm_monthly.csv")
print("  - 12A_traffic_monthly.csv")
print("  - 12B_traffic_monthly.csv")