import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("=== DATA INTEGRITY CHECK: PRE vs POST MERGE ===\n")

# Load pre-merge data
sales_a = pd.read_csv('01_Data_Analytics/00A_sales_builder.csv')
sales_b = pd.read_csv('01_Data_Analytics/00B_sales_builder.csv')
crm_a = pd.read_csv('01_Data_Analytics/02A_api_crm_builder.csv')
crm_b = pd.read_csv('01_Data_Analytics/02B_api_crm_builder.csv')
traffic_a = pd.read_csv('01_Data_Analytics/02A_api_traffic_builder.csv')
traffic_b = pd.read_csv('01_Data_Analytics/02B_api_traffic_builder.csv')

# Load post-merge data
merged = pd.read_csv('01_Data_Analytics/04_result_merger.csv')

print("Loaded all files\n")

# ============================================================================
# PREPARE PRE-MERGE DATA
# ============================================================================

# Parse dates and aggregate pre-merge sales to monthly
sales_a['date'] = pd.to_datetime(sales_a['sale_contract_date'], errors='coerce')
sales_a['year'] = sales_a['date'].dt.year
sales_a['month'] = sales_a['date'].dt.month
sales_a_monthly = sales_a.groupby(['year', 'month']).size().reset_index(name='sales_count')

sales_b['date'] = pd.to_datetime(sales_b['sale_contract_date'], errors='coerce')
sales_b['year'] = sales_b['date'].dt.year
sales_b['month'] = sales_b['date'].dt.month
sales_b_monthly = sales_b.groupby(['year', 'month']).size().reset_index(name='sales_count')

# Parse and aggregate CRM to monthly
if 'createdate' in crm_a.columns:
    crm_a['date'] = pd.to_datetime(crm_a['createdate'], errors='coerce', utc=True).dt.tz_localize(None)
elif 'create_at' in crm_a.columns:
    crm_a['date'] = pd.to_datetime(crm_a['create_at'], errors='coerce', utc=True).dt.tz_localize(None)
crm_a['year'] = crm_a['date'].dt.year
crm_a['month'] = crm_a['date'].dt.month
crm_a_monthly = crm_a.groupby(['year', 'month']).size().reset_index(name='crm_count')

if 'createdate' in crm_b.columns:
    crm_b['date'] = pd.to_datetime(crm_b['createdate'], errors='coerce', utc=True).dt.tz_localize(None)
elif 'create_at' in crm_b.columns:
    crm_b['date'] = pd.to_datetime(crm_b['create_at'], errors='coerce', utc=True).dt.tz_localize(None)
crm_b['year'] = crm_b['date'].dt.year
crm_b['month'] = crm_b['date'].dt.month
crm_b_monthly = crm_b.groupby(['year', 'month']).size().reset_index(name='crm_count')

# Parse and aggregate traffic to monthly
traffic_a['date'] = pd.to_datetime(traffic_a['date'], errors='coerce', utc=True).dt.tz_localize(None)
traffic_a['year'] = traffic_a['date'].dt.year
traffic_a['month'] = traffic_a['date'].dt.month
traffic_a_monthly = traffic_a.groupby(['year', 'month'])['sessions'].sum().reset_index(name='traffic_sum')

traffic_b['date'] = pd.to_datetime(traffic_b['date'], errors='coerce', utc=True).dt.tz_localize(None)
traffic_b['year'] = traffic_b['date'].dt.year
traffic_b['month'] = traffic_b['date'].dt.month
traffic_b_monthly = traffic_b.groupby(['year', 'month'])['sessions'].sum().reset_index(name='traffic_sum')

print("Aggregated pre-merge data to monthly\n")

# ============================================================================
# PREPARE POST-MERGE DATA
# ============================================================================

merged_a = merged[merged['builder'] == 'A'].groupby(['year', 'month']).agg({
    'actual_sales': 'sum',
    'crm_lead_count': 'sum',
    'web_traffic': 'sum'
}).reset_index()

merged_b = merged[merged['builder'] == 'B'].groupby(['year', 'month']).agg({
    'actual_sales': 'sum',
    'crm_lead_count': 'sum',
    'web_traffic': 'sum'
}).reset_index()

print("Aggregated post-merge data\n")

# ============================================================================
# CHART 1: SALES COMPARISON
# ============================================================================

print("Creating Chart: Sales Comparison...\n")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Builder A
sales_a_monthly = sales_a_monthly.dropna(subset=['year', 'month'])
sales_a_monthly['date'] = pd.to_datetime(sales_a_monthly['year'].astype(int).astype(str) + '-' + sales_a_monthly['month'].astype(int).astype(str) + '-01')
merged_a['date'] = pd.to_datetime(merged_a['year'].astype(int).astype(str) + '-' + merged_a['month'].astype(int).astype(str) + '-01')

ax1.plot(sales_a_monthly['date'], sales_a_monthly['sales_count'], marker='o', label='Pre-Merge (00A_sales)', linewidth=2)
ax1.plot(merged_a['date'], merged_a['actual_sales'], marker='s', label='Post-Merge (actual_sales)', linewidth=2, linestyle='--')
ax1.set_title('Builder A: Sales Count Comparison (Pre vs Post Merge)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Sales Count')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Builder B
sales_b_monthly = sales_b_monthly.dropna(subset=['year', 'month'])
sales_b_monthly['date'] = pd.to_datetime(sales_b_monthly['year'].astype(int).astype(str) + '-' + sales_b_monthly['month'].astype(int).astype(str) + '-01')
merged_b['date'] = pd.to_datetime(merged_b['year'].astype(int).astype(str) + '-' + merged_b['month'].astype(int).astype(str) + '-01')

ax2.plot(sales_b_monthly['date'], sales_b_monthly['sales_count'], marker='o', label='Pre-Merge (00B_sales)', linewidth=2)
ax2.plot(merged_b['date'], merged_b['actual_sales'], marker='s', label='Post-Merge (actual_sales)', linewidth=2, linestyle='--')
ax2.set_title('Builder B: Sales Count Comparison (Pre vs Post Merge)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Date')
ax2.set_ylabel('Sales Count')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_Data_Analytics/integrity_check_sales.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: integrity_check_sales.png")

# ============================================================================
# CHART 2: CRM & TRAFFIC COMPARISON
# ============================================================================

print("Creating Chart: CRM & Traffic Comparison...\n")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Builder A - CRM
crm_a_monthly = crm_a_monthly.dropna(subset=['year', 'month'])
crm_a_monthly['date'] = pd.to_datetime(crm_a_monthly['year'].astype(int).astype(str) + '-' + crm_a_monthly['month'].astype(int).astype(str) + '-01')
axes[0,0].plot(crm_a_monthly['date'], crm_a_monthly['crm_count'], marker='o', label='Pre-Merge CRM', linewidth=2)
axes[0,0].plot(merged_a['date'], merged_a['crm_lead_count'], marker='s', label='Post-Merge CRM', linewidth=2, linestyle='--')
axes[0,0].set_title('Builder A: CRM Leads', fontsize=12, fontweight='bold')
axes[0,0].set_xlabel('Date')
axes[0,0].set_ylabel('Lead Count')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# Builder A - Traffic
traffic_a_monthly = traffic_a_monthly.dropna(subset=['year', 'month'])
traffic_a_monthly['date'] = pd.to_datetime(traffic_a_monthly['year'].astype(int).astype(str) + '-' + traffic_a_monthly['month'].astype(int).astype(str) + '-01')
axes[0,1].plot(traffic_a_monthly['date'], traffic_a_monthly['traffic_sum'], marker='o', label='Pre-Merge Traffic', linewidth=2)
axes[0,1].plot(merged_a['date'], merged_a['web_traffic'], marker='s', label='Post-Merge Traffic', linewidth=2, linestyle='--')
axes[0,1].set_title('Builder A: Web Traffic', fontsize=12, fontweight='bold')
axes[0,1].set_xlabel('Date')
axes[0,1].set_ylabel('Sessions')
axes[0,1].legend()
axes[0,1].grid(True, alpha=0.3)

# Builder B - CRM
crm_b_monthly = crm_b_monthly.dropna(subset=['year', 'month'])
crm_b_monthly['date'] = pd.to_datetime(crm_b_monthly['year'].astype(int).astype(str) + '-' + crm_b_monthly['month'].astype(int).astype(str) + '-01')
axes[1,0].plot(crm_b_monthly['date'], crm_b_monthly['crm_count'], marker='o', label='Pre-Merge CRM', linewidth=2)
axes[1,0].plot(merged_b['date'], merged_b['crm_lead_count'], marker='s', label='Post-Merge CRM', linewidth=2, linestyle='--')
axes[1,0].set_title('Builder B: CRM Leads', fontsize=12, fontweight='bold')
axes[1,0].set_xlabel('Date')
axes[1,0].set_ylabel('Lead Count')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# Builder B - Traffic
traffic_b_monthly = traffic_b_monthly.dropna(subset=['year', 'month'])
traffic_b_monthly['date'] = pd.to_datetime(traffic_b_monthly['year'].astype(int).astype(str) + '-' + traffic_b_monthly['month'].astype(int).astype(str) + '-01')
axes[1,1].plot(traffic_b_monthly['date'], traffic_b_monthly['traffic_sum'], marker='o', label='Pre-Merge Traffic', linewidth=2)
axes[1,1].plot(merged_b['date'], merged_b['web_traffic'], marker='s', label='Post-Merge Traffic', linewidth=2, linestyle='--')
axes[1,1].set_title('Builder B: Web Traffic', fontsize=12, fontweight='bold')
axes[1,1].set_xlabel('Date')
axes[1,1].set_ylabel('Sessions')
axes[1,1].legend()
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_Data_Analytics/integrity_check_crm_traffic.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: integrity_check_crm_traffic.png")

# ============================================================================
# SUMMARY COMPARISON
# ============================================================================

print("\n=== SUMMARY COMPARISON ===\n")

print("Builder A:")
print(f"  Sales - Pre-merge total: {sales_a_monthly['sales_count'].sum()}")
print(f"  Sales - Post-merge total: {merged_a['actual_sales'].sum()}")
print(f"  CRM - Pre-merge total: {crm_a_monthly['crm_count'].sum()}")
print(f"  CRM - Post-merge total: {merged_a['crm_lead_count'].sum()}")
print(f"  Traffic - Pre-merge total: {traffic_a_monthly['traffic_sum'].sum()}")
print(f"  Traffic - Post-merge total: {merged_a['web_traffic'].sum()}")

print("\nBuilder B:")
print(f"  Sales - Pre-merge total: {sales_b_monthly['sales_count'].sum()}")
print(f"  Sales - Post-merge total: {merged_b['actual_sales'].sum()}")
print(f"  CRM - Pre-merge total: {crm_b_monthly['crm_count'].sum()}")
print(f"  CRM - Post-merge total: {merged_b['crm_lead_count'].sum()}")
print(f"  Traffic - Pre-merge total: {traffic_b_monthly['traffic_sum'].sum()}")
print(f"  Traffic - Post-merge total: {merged_b['web_traffic'].sum()}")

print("\n=== INTEGRITY CHECK COMPLETE ===")
print("\nIf pre and post totals match, the merge preserved data correctly.")
print("Check the charts to see if the lines overlap.")