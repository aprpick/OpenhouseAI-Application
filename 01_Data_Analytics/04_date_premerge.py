import pandas as pd

print("=== PREPROCESSING: ADD DATE COLUMNS ===\n")

# ============================================================================
# SALES A
# ============================================================================

print("Processing 00A_sales_builder.csv...")
sales_a = pd.read_csv('01_Data_Analytics/00A_sales_builder.csv')

# Parse date and add columns
sales_a['date'] = pd.to_datetime(sales_a['sale_contract_date'], errors='coerce')
sales_a['year'] = sales_a['date'].dt.year
sales_a['month'] = sales_a['date'].dt.month
sales_a['day'] = sales_a['date'].dt.day

# Save new file
sales_a.to_csv('01_Data_Analytics/04A_sales_preprocessed.csv', index=False)
print(f"  ✓ Saved to 04A_sales_preprocessed.csv ({len(sales_a)} rows)\n")

# ============================================================================
# SALES B
# ============================================================================

print("Processing 00B_sales_builder.csv...")
sales_b = pd.read_csv('01_Data_Analytics/00B_sales_builder.csv')

# Parse date and add columns
sales_b['date'] = pd.to_datetime(sales_b['sale_contract_date'], errors='coerce')
sales_b['year'] = sales_b['date'].dt.year
sales_b['month'] = sales_b['date'].dt.month
sales_b['day'] = sales_b['date'].dt.day

# Save new file
sales_b.to_csv('01_Data_Analytics/04B_sales_preprocessed.csv', index=False)
print(f"  ✓ Saved to 04B_sales_preprocessed.csv ({len(sales_b)} rows)\n")

# ============================================================================
# TARGET A
# ============================================================================

print("Processing 00A_target_sales_builder.csv...")
target_a = pd.read_csv('01_Data_Analytics/00A_target_sales_builder.csv')

# Already has year and month, add day=1 for consistency
target_a['day'] = 1

# Save new file
target_a.to_csv('01_Data_Analytics/04A_target_preprocessed.csv', index=False)
print(f"  ✓ Saved to 04A_target_preprocessed.csv ({len(target_a)} rows)\n")

# ============================================================================
# TARGET B
# ============================================================================

print("Processing 00B_target_sales_builder.csv...")
target_b = pd.read_csv('01_Data_Analytics/00B_target_sales_builder.csv')

# Already has year and month, add day=1 for consistency
target_b['day'] = 1

# Save new file
target_b.to_csv('01_Data_Analytics/04B_target_preprocessed.csv', index=False)
print(f"  ✓ Saved to 04B_target_preprocessed.csv ({len(target_b)} rows)\n")

print("=== PREPROCESSING COMPLETE ===")
print("\nCreated new files:")
print("  - 04A_sales_preprocessed.csv")
print("  - 04B_sales_preprocessed.csv")
print("  - 04A_target_preprocessed.csv")
print("  - 04B_target_preprocessed.csv")