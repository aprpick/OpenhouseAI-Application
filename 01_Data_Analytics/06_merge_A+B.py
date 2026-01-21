import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== COMBINING BUILDER A + B ===\n")

# Load both builder files
merged_a = pd.read_csv('01_Data_Analytics/05A_sales_target_merged.csv')
merged_b = pd.read_csv('01_Data_Analytics/05B_sales_target_merged.csv')

print(f"Builder A: {len(merged_a)} rows")
print(f"Builder B: {len(merged_b)} rows")

# Combine
combined = pd.concat([merged_a, merged_b], ignore_index=True)

# Sort by builder, community, year, month
combined = combined.sort_values(['builder', 'community', 'year', 'month']).reset_index(drop=True)

print(f"\nCombined: {len(combined)} rows")

# Save
combined.to_csv('01_Data_Analytics/06_sales_target_combined.csv', index=False)
print(f"\n✓ Saved to 06_sales_target_combined.csv")

print("\n=== COMBINE COMPLETE ===")