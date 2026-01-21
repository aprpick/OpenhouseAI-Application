import pandas as pd
from datetime import datetime

print("=== SUMMARY VALIDATION ===\n")

# Load pre-merge data
sales_a_raw = pd.read_csv('01_Data_Analytics/01A_sales_builder.csv')
sales_b_raw = pd.read_csv('01_Data_Analytics/01B_sales_builder.csv')

# Load post-merge data
combined = pd.read_csv('01_Data_Analytics/06_sales_target_combined.csv')

print("Loaded all files\n")

# ============================================================================
# PREPARE DATA
# ============================================================================

# Parse dates
sales_a_raw['date'] = pd.to_datetime(sales_a_raw['sale_contract_date'], errors='coerce')
sales_b_raw['date'] = pd.to_datetime(sales_b_raw['sale_contract_date'], errors='coerce')

# ============================================================================
# BUILDER A SUMMARY
# ============================================================================

# Pre-merge totals by community
a_pre_totals = sales_a_raw.groupby('community_name').agg({
    'home_id': 'count',
    'total_sale_price': 'sum',
    'date': ['min', 'max']
}).reset_index()
a_pre_totals.columns = ['community', 'sales_count', 'total_revenue', 'date_min', 'date_max']

# Post-merge totals by community
a_post_totals = combined[combined['builder'] == 'A'].groupby('community').agg({
    'total_sales': 'sum',
    'total_revenue': 'sum'
}).reset_index()
a_post_totals.columns = ['community', 'sales_count', 'total_revenue']

# ============================================================================
# BUILDER B SUMMARY
# ============================================================================

# Pre-merge totals by community
b_pre_totals = sales_b_raw.groupby('community_name').agg({
    'home_id': 'count',
    'total_sale_price': 'sum',
    'date': ['min', 'max']
}).reset_index()
b_pre_totals.columns = ['community', 'sales_count', 'total_revenue', 'date_min', 'date_max']

# Post-merge totals by community
b_post_totals = combined[combined['builder'] == 'B'].groupby('community').agg({
    'total_sales': 'sum',
    'total_revenue': 'sum'
}).reset_index()
b_post_totals.columns = ['community', 'sales_count', 'total_revenue']

# ============================================================================
# DETECT COMMUNITY NAME VARIATIONS
# ============================================================================

def find_variations(communities):
    """Find similar community names that might be variations"""
    variations = []
    seen = set()
    
    for comm in communities:
        base = comm.lower().replace('-', '').replace(' ', '').replace('phase', '').replace('2', '').replace('1', '')
        if base in seen:
            variations.append(comm)
        seen.add(base)
    
    return variations

a_variations = find_variations(sales_a_raw['community_name'].unique())
b_variations = find_variations(sales_b_raw['community_name'].unique())

# ============================================================================
# CREATE MARKDOWN REPORT
# ============================================================================

output = []
output.append("# Summary Validation Report\n")
output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Builder A
output.append("## Builder A\n")
output.append("### Pre-Merge Totals (01A_sales_builder.csv)\n")
output.append("| Community | Sales Count | Total Revenue | Date Range |")
output.append("|-----------|-------------|---------------|------------|")
for _, row in a_pre_totals.iterrows():
    date_range = f"{row['date_min'].strftime('%Y-%m-%d')} to {row['date_max'].strftime('%Y-%m-%d')}" if pd.notna(row['date_min']) else "N/A"
    output.append(f"| {row['community']} | {row['sales_count']} | ${row['total_revenue']:,.0f} | {date_range} |")

output.append("\n### Post-Merge Totals (06_sales_target_combined.csv)\n")
output.append("| Community | Sales Count | Total Revenue |")
output.append("|-----------|-------------|---------------|")
for _, row in a_post_totals.iterrows():
    output.append(f"| {row['community']} | {row['sales_count']} | ${row['total_revenue']:,.0f} |")

output.append("\n### Comparison\n")
a_pre_total_sales = a_pre_totals['sales_count'].sum()
a_post_total_sales = a_post_totals['sales_count'].sum()
a_pre_total_rev = a_pre_totals['total_revenue'].sum()
a_post_total_rev = a_post_totals['total_revenue'].sum()

output.append(f"**Total Sales:**")
output.append(f"- Pre-merge: {a_pre_total_sales}")
output.append(f"- Post-merge: {a_post_total_sales}")
output.append(f"- Difference: {a_post_total_sales - a_pre_total_sales}")

output.append(f"\n**Total Revenue:**")
output.append(f"- Pre-merge: ${a_pre_total_rev:,.0f}")
output.append(f"- Post-merge: ${a_post_total_rev:,.0f}")
output.append(f"- Difference: ${a_post_total_rev - a_pre_total_rev:,.0f}")

if a_variations:
    output.append(f"\n**Community Name Variations Detected:**")
    for var in a_variations:
        output.append(f"- {var}")

# Builder B
output.append("\n## Builder B\n")
output.append("### Pre-Merge Totals (01B_sales_builder.csv)\n")
output.append("| Community | Sales Count | Total Revenue | Date Range |")
output.append("|-----------|-------------|---------------|------------|")
for _, row in b_pre_totals.iterrows():
    date_range = f"{row['date_min'].strftime('%Y-%m-%d')} to {row['date_max'].strftime('%Y-%m-%d')}" if pd.notna(row['date_min']) else "N/A"
    output.append(f"| {row['community']} | {row['sales_count']} | ${row['total_revenue']:,.0f} | {date_range} |")

output.append("\n### Post-Merge Totals (06_sales_target_combined.csv)\n")
output.append("| Community | Sales Count | Total Revenue |")
output.append("|-----------|-------------|---------------|")
for _, row in b_post_totals.iterrows():
    output.append(f"| {row['community']} | {row['sales_count']} | ${row['total_revenue']:,.0f} |")

output.append("\n### Comparison\n")
b_pre_total_sales = b_pre_totals['sales_count'].sum()
b_post_total_sales = b_post_totals['sales_count'].sum()
b_pre_total_rev = b_pre_totals['total_revenue'].sum()
b_post_total_rev = b_post_totals['total_revenue'].sum()

output.append(f"**Total Sales:**")
output.append(f"- Pre-merge: {b_pre_total_sales}")
output.append(f"- Post-merge: {b_post_total_sales}")
output.append(f"- Difference: {b_post_total_sales - b_pre_total_sales}")

output.append(f"\n**Total Revenue:**")
output.append(f"- Pre-merge: ${b_pre_total_rev:,.0f}")
output.append(f"- Post-merge: ${b_post_total_rev:,.0f}")
output.append(f"- Difference: ${b_post_total_rev - b_pre_total_rev:,.0f}")

if b_variations:
    output.append(f"\n**Community Name Variations Detected:**")
    for var in b_variations:
        output.append(f"- {var}")

# Overall summary
output.append("\n## Overall Summary\n")
output.append(f"**Combined Totals:**")
output.append(f"- Pre-merge sales: {a_pre_total_sales + b_pre_total_sales}")
output.append(f"- Post-merge sales: {a_post_total_sales + b_post_total_sales}")
output.append(f"- Match: {'YES' if (a_pre_total_sales + b_pre_total_sales) == (a_post_total_sales + b_post_total_sales) else 'NO'}")

output.append(f"\n**Unique Communities:**")
output.append(f"- Builder A pre-merge: {len(a_pre_totals)}")
output.append(f"- Builder A post-merge: {len(a_post_totals)}")
output.append(f"- Builder B pre-merge: {len(b_pre_totals)}")
output.append(f"- Builder B post-merge: {len(b_post_totals)}")

# Save markdown
with open('01_Data_Analytics/08_summary_validation.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('\n'.join(output))
print("\n✓ Saved to: 08_summary_validation.md")
print("\n=== VALIDATION COMPLETE ===")