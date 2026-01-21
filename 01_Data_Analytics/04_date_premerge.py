import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== PREPROCESSING: ADD DATE COLUMNS ===\n")

# ============================================================================
# SALES A
# ============================================================================

print("Processing 01A_sales_builder.csv...")
sales_a = pd.read_csv('01_Data_Analytics/01A_sales_builder.csv')

# Parse date with multiple format attempts
def parse_date_flexible(date_str):
    """Try multiple date formats to parse"""
    if pd.isna(date_str):
        return pd.NaT
    
    date_str = str(date_str).strip()
    
    # Try common formats
    formats = [
        '%Y-%m-%d',      # 2025-03-12
        '%m/%d/%Y',      # 03/12/2025
        '%d/%m/%Y',      # 12/03/2025
        '%Y/%m/%d',      # 2025/03/12
        '%d-%m-%Y',      # 12-03-2025
        '%m-%d-%Y',      # 03-12-2025
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    
    # Fallback: let pandas infer
    try:
        return pd.to_datetime(date_str, dayfirst=False)
    except:
        return pd.NaT

sales_a['date'] = sales_a['sale_contract_date'].apply(parse_date_flexible)
sales_a['year'] = sales_a['date'].dt.year
sales_a['month'] = sales_a['date'].dt.month
sales_a['day'] = sales_a['date'].dt.day

# Report parsing failures
failed = sales_a['date'].isna().sum()
if failed > 0:
    print(f"  WARNING: Failed to parse {failed} dates")
    print(sales_a[sales_a['date'].isna()][['home_id', 'sale_contract_date']].head())

# Save new file
sales_a.to_csv('01_Data_Analytics/04A_sales_preprocessed.csv', index=False)
print(f"  ✓ Saved to 04A_sales_preprocessed.csv ({len(sales_a)} rows)\n")

# ============================================================================
# SALES B
# ============================================================================

print("Processing 01B_sales_builder.csv...")
sales_b = pd.read_csv('01_Data_Analytics/01B_sales_builder.csv')

sales_b['date'] = sales_b['sale_contract_date'].apply(parse_date_flexible)
sales_b['year'] = sales_b['date'].dt.year
sales_b['month'] = sales_b['date'].dt.month
sales_b['day'] = sales_b['date'].dt.day

# Report parsing failures
failed = sales_b['date'].isna().sum()
if failed > 0:
    print(f"  WARNING: Failed to parse {failed} dates")
    print(sales_b[sales_b['date'].isna()][['home_id', 'sale_contract_date']].head())

# Save new file
sales_b.to_csv('01_Data_Analytics/04B_sales_preprocessed.csv', index=False)
print(f"  ✓ Saved to 04B_sales_preprocessed.csv ({len(sales_b)} rows)\n")

# ============================================================================
# TARGET A
# ============================================================================

print("Processing 01A_target_sales_builder.csv...")
target_a = pd.read_csv('01_Data_Analytics/01A_target_sales_builder.csv')

# Already has year and month, add day=1 for consistency
target_a['day'] = 1

# Save new file
target_a.to_csv('01_Data_Analytics/04A_target_preprocessed.csv', index=False)
print(f"  ✓ Saved to 04A_target_preprocessed.csv ({len(target_a)} rows)\n")

# ============================================================================
# TARGET B
# ============================================================================

print("Processing 01B_target_sales_builder.csv...")
target_b = pd.read_csv('01_Data_Analytics/01B_target_sales_builder.csv')

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