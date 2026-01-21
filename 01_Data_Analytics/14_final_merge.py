import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== FINAL MERGE: SALES + TARGET + CRM + TRAFFIC ===\n")

# ============================================================================
# SIMPLE VERSION (using 12_ files)
# ============================================================================

print("Creating SIMPLE version...\n")

# Load sales + target base
sales_target = pd.read_csv('01_Data_Analytics/06_sales_target_combined.csv')
print(f"  Loaded sales+target: {len(sales_target)} rows")

# Load simple CRM monthly
crm_a_simple = pd.read_csv('01_Data_Analytics/12A_crm_monthly.csv')
crm_b_simple = pd.read_csv('01_Data_Analytics/12B_crm_monthly.csv')
crm_simple = pd.concat([crm_a_simple, crm_b_simple], ignore_index=True)
print(f"  Loaded CRM (simple): {len(crm_simple)} rows")

# Load simple traffic monthly
traffic_a_simple = pd.read_csv('01_Data_Analytics/12A_traffic_monthly.csv')
traffic_b_simple = pd.read_csv('01_Data_Analytics/12B_traffic_monthly.csv')
traffic_simple = pd.concat([traffic_a_simple, traffic_b_simple], ignore_index=True)
print(f"  Loaded traffic (simple): {len(traffic_simple)} rows")

# Merge CRM
final_simple = sales_target.merge(
    crm_simple,
    on=['community', 'year', 'month'],
    how='left'
)
print(f"  After CRM merge: {len(final_simple)} rows")

# Merge traffic
final_simple = final_simple.merge(
    traffic_simple,
    on=['community', 'year', 'month'],
    how='left'
)
print(f"  After traffic merge: {len(final_simple)} rows")

# Fill nulls with 0 for count metrics
final_simple['crm_lead_count'] = final_simple['crm_lead_count'].fillna(0).astype(int)
final_simple['web_traffic'] = final_simple['web_traffic'].fillna(0).astype(int)
final_simple['unique_users'] = final_simple['unique_users'].fillna(0).astype(int)

# Sort by date first, then builder/community
final_simple = final_simple.sort_values(['year', 'month', 'builder', 'community']).reset_index(drop=True)

# Save
final_simple.to_csv('01_Data_Analytics/14_final_report_simple.csv', index=False)
print(f"  ✓ Saved to 14_final_report_simple.csv")
print(f"  Shape: {final_simple.shape}\n")

# ============================================================================
# DETAILED VERSION (using 13_ files)
# ============================================================================

print("Creating DETAILED version...\n")

# Load sales + target base again
sales_target = pd.read_csv('01_Data_Analytics/06_sales_target_combined.csv')
print(f"  Loaded sales+target: {len(sales_target)} rows")

# Load detailed CRM monthly
crm_a_detailed = pd.read_csv('01_Data_Analytics/13A_crm_monthly_detailed.csv')
crm_b_detailed = pd.read_csv('01_Data_Analytics/13B_crm_monthly_detailed.csv')
crm_detailed = pd.concat([crm_a_detailed, crm_b_detailed], ignore_index=True)
print(f"  Loaded CRM (detailed): {len(crm_detailed)} rows, {len(crm_detailed.columns)} columns")

# Load detailed traffic monthly
traffic_a_detailed = pd.read_csv('01_Data_Analytics/13A_traffic_monthly_detailed.csv')
traffic_b_detailed = pd.read_csv('01_Data_Analytics/13B_traffic_monthly_detailed.csv')
traffic_detailed = pd.concat([traffic_a_detailed, traffic_b_detailed], ignore_index=True)
print(f"  Loaded traffic (detailed): {len(traffic_detailed)} rows")

# Merge CRM
final_detailed = sales_target.merge(
    crm_detailed,
    on=['community', 'year', 'month'],
    how='left'
)
print(f"  After CRM merge: {len(final_detailed)} rows, {len(final_detailed.columns)} columns")

# Merge traffic
final_detailed = final_detailed.merge(
    traffic_detailed,
    on=['community', 'year', 'month'],
    how='left'
)
print(f"  After traffic merge: {len(final_detailed)} rows, {len(final_detailed.columns)} columns")

# Fill nulls with 0 for all numeric columns
numeric_cols = final_detailed.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_cols:
    final_detailed[col] = final_detailed[col].fillna(0)

# Sort by date first, then builder/community
final_detailed = final_detailed.sort_values(['year', 'month', 'builder', 'community']).reset_index(drop=True)

# Save
final_detailed.to_csv('01_Data_Analytics/14_final_report_detailed.csv', index=False)
print(f"  ✓ Saved to 14_final_report_detailed.csv")
print(f"  Shape: {final_detailed.shape}\n")

# ============================================================================
# SUMMARY
# ============================================================================

print("=== MERGE COMPLETE ===\n")
print("Created files:")
print(f"  - 14_final_report_simple.csv ({final_simple.shape[0]} rows × {final_simple.shape[1]} columns)")
print(f"  - 14_final_report_detailed.csv ({final_detailed.shape[0]} rows × {final_detailed.shape[1]} columns)")

print("\nSimple report columns:")
print(f"  {', '.join(final_simple.columns.tolist())}")

print("\nDetailed report additional columns:")
detailed_extra = [col for col in final_detailed.columns if col not in final_simple.columns]
print(f"  {len(detailed_extra)} additional columns with source/status breakdowns")