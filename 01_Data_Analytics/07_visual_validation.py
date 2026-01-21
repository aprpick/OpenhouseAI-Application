import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

print("=== DATA VERIFICATION VISUALIZATION ===\n")

# Load pre-merge data
sales_a_raw = pd.read_csv('01_Data_Analytics/01A_sales_builder.csv')
sales_b_raw = pd.read_csv('01_Data_Analytics/01B_sales_builder.csv')

# Load post-merge data
combined = pd.read_csv('01_Data_Analytics/06_sales_target_combined.csv')

print("Loaded all files\n")

# ============================================================================
# PREPARE PRE-MERGE DATA
# ============================================================================

# Parse dates for raw sales
sales_a_raw['date'] = pd.to_datetime(sales_a_raw['sale_contract_date'], errors='coerce')
sales_a_raw['year'] = sales_a_raw['date'].dt.year
sales_a_raw['month'] = sales_a_raw['date'].dt.month

sales_b_raw['date'] = pd.to_datetime(sales_b_raw['sale_contract_date'], errors='coerce')
sales_b_raw['year'] = sales_b_raw['date'].dt.year
sales_b_raw['month'] = sales_b_raw['date'].dt.month

# Aggregate raw data to monthly by community
sales_a_monthly = sales_a_raw.groupby(['community_name', 'year', 'month']).agg({
    'home_id': 'count',
    'total_sale_price': 'sum'
}).reset_index()
sales_a_monthly.columns = ['community', 'year', 'month', 'sales_count', 'revenue']

sales_b_monthly = sales_b_raw.groupby(['community_name', 'year', 'month']).agg({
    'home_id': 'count',
    'total_sale_price': 'sum'
}).reset_index()
sales_b_monthly.columns = ['community', 'year', 'month', 'sales_count', 'revenue']

print("Aggregated pre-merge data to monthly\n")

# ============================================================================
# BUILDER A - SALES COUNT CHARTS
# ============================================================================

print("Creating Builder A sales count charts...\n")

a_communities = sales_a_monthly['community'].unique()
n_communities = len(a_communities)

fig, axes = plt.subplots(n_communities, 1, figsize=(12, 4*n_communities))
if n_communities == 1:
    axes = [axes]

for idx, community in enumerate(a_communities):
    # Pre-merge data
    pre = sales_a_monthly[sales_a_monthly['community'] == community].copy()
    pre['date'] = pd.to_datetime(pre['year'].astype(int).astype(str) + '-' + pre['month'].astype(int).astype(str) + '-01')
    
    # Post-merge data
    post = combined[(combined['builder'] == 'A') & (combined['community'] == community)].copy()
    post['date'] = pd.to_datetime(post['year'].astype(int).astype(str) + '-' + post['month'].astype(int).astype(str) + '-01')
    
    # Plot
    axes[idx].plot(pre['date'], pre['sales_count'], marker='o', label='Pre-merge (00A)', linewidth=2, color='blue')
    axes[idx].plot(post['date'], post['total_sales'], marker='s', label='Post-merge (06)', linewidth=2, linestyle='--', color='orange')
    axes[idx].set_title(f'Builder A - {community}: Sales Count', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Date')
    axes[idx].set_ylabel('Sales Count')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_Data_Analytics/07_verify_a_sales_count.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 07_verify_a_sales_count.png")

# ============================================================================
# BUILDER A - REVENUE CHARTS
# ============================================================================

print("Creating Builder A revenue charts...\n")

fig, axes = plt.subplots(n_communities, 1, figsize=(12, 4*n_communities))
if n_communities == 1:
    axes = [axes]

for idx, community in enumerate(a_communities):
    # Pre-merge data
    pre = sales_a_monthly[sales_a_monthly['community'] == community].copy()
    pre['date'] = pd.to_datetime(pre['year'].astype(int).astype(str) + '-' + pre['month'].astype(int).astype(str) + '-01')
    
    # Post-merge data
    post = combined[(combined['builder'] == 'A') & (combined['community'] == community)].copy()
    post['date'] = pd.to_datetime(post['year'].astype(int).astype(str) + '-' + post['month'].astype(int).astype(str) + '-01')
    
    # Plot
    axes[idx].plot(pre['date'], pre['revenue'], marker='o', label='Pre-merge (00A)', linewidth=2, color='blue')
    axes[idx].plot(post['date'], post['total_revenue'], marker='s', label='Post-merge (06)', linewidth=2, linestyle='--', color='orange')
    axes[idx].set_title(f'Builder A - {community}: Total Revenue', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Date')
    axes[idx].set_ylabel('Revenue ($)')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_Data_Analytics/07_verify_a_revenue.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 07_verify_a_revenue.png")

# ============================================================================
# BUILDER B - SALES COUNT CHARTS
# ============================================================================

print("Creating Builder B sales count charts...\n")

b_communities = sales_b_monthly['community'].unique()
n_communities = len(b_communities)

fig, axes = plt.subplots(n_communities, 1, figsize=(12, 4*n_communities))
if n_communities == 1:
    axes = [axes]

for idx, community in enumerate(b_communities):
    # Pre-merge data
    pre = sales_b_monthly[sales_b_monthly['community'] == community].copy()
    pre['date'] = pd.to_datetime(pre['year'].astype(int).astype(str) + '-' + pre['month'].astype(int).astype(str) + '-01')
    
    # Post-merge data
    post = combined[(combined['builder'] == 'B') & (combined['community'] == community)].copy()
    post['date'] = pd.to_datetime(post['year'].astype(int).astype(str) + '-' + post['month'].astype(int).astype(str) + '-01')
    
    # Plot
    axes[idx].plot(pre['date'], pre['sales_count'], marker='o', label='Pre-merge (00B)', linewidth=2, color='blue')
    axes[idx].plot(post['date'], post['total_sales'], marker='s', label='Post-merge (06)', linewidth=2, linestyle='--', color='orange')
    axes[idx].set_title(f'Builder B - {community}: Sales Count', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Date')
    axes[idx].set_ylabel('Sales Count')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_Data_Analytics/07_verify_b_sales_count.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 07_verify_b_sales_count.png")

# ============================================================================
# BUILDER B - REVENUE CHARTS
# ============================================================================

print("Creating Builder B revenue charts...\n")

fig, axes = plt.subplots(n_communities, 1, figsize=(12, 4*n_communities))
if n_communities == 1:
    axes = [axes]

for idx, community in enumerate(b_communities):
    # Pre-merge data
    pre = sales_b_monthly[sales_b_monthly['community'] == community].copy()
    pre['date'] = pd.to_datetime(pre['year'].astype(int).astype(str) + '-' + pre['month'].astype(int).astype(str) + '-01')
    
    # Post-merge data
    post = combined[(combined['builder'] == 'B') & (combined['community'] == community)].copy()
    post['date'] = pd.to_datetime(post['year'].astype(int).astype(str) + '-' + post['month'].astype(int).astype(str) + '-01')
    
    # Plot
    axes[idx].plot(pre['date'], pre['revenue'], marker='o', label='Pre-merge (00B)', linewidth=2, color='blue')
    axes[idx].plot(post['date'], post['total_revenue'], marker='s', label='Post-merge (06)', linewidth=2, linestyle='--', color='orange')
    axes[idx].set_title(f'Builder B - {community}: Total Revenue', fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Date')
    axes[idx].set_ylabel('Revenue ($)')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_Data_Analytics/07_verify_b_revenue.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 07_verify_b_revenue.png")

print("\n=== VERIFICATION COMPLETE ===")
print("\nGenerated files:")
print("  - 07_verify_a_sales_count.png")
print("  - 07_verify_a_revenue.png")
print("  - 07_verify_b_sales_count.png")
print("  - 07_verify_b_revenue.png")
print("\nIf pre and post lines overlap, data was preserved correctly.")