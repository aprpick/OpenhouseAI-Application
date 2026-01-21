import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== CRM + TRAFFIC DATA STANDARDIZATION ===\n")

# Community name standardization function
def standardize_community(name):
    """Standardize community name variations"""
    if pd.isna(name):
        return name
    
    name = str(name).strip()
    name_lower = name.lower()
    
    # Cedar Creek variations
    if 'cedar' in name_lower and 'creek' in name_lower:
        return 'Cedar Creek'
    
    # Fairview Estates variations
    if 'fairview' in name_lower:
        return 'Fairview Estates'
    
    # Glenview Meadows variations
    if 'glenview' in name_lower:
        return 'Glenview Meadows'
    
    # Riverbend Townhomes variations
    if 'riverbend' in name_lower:
        return 'Riverbend Townhomes'
    
    # Maplewood Heights variations
    if 'maplewood' in name_lower:
        return 'Maplewood Heights'
    
    # Oakridge Villas variations
    if 'oakridge' in name_lower:
        return 'Oakridge Villas'
    
    # Sunset Pines variations
    if 'sunset' in name_lower:
        return 'Sunset Pines'
    
    # Willow Creek Meadows variations
    if 'willow' in name_lower and 'creek' in name_lower:
        return 'Willow Creek Meadows'
    
    # Unknown communities - flag them
    print(f"  WARNING: Unknown community name: {name}")
    return name

# ============================================================================
# CRM BUILDER A
# ============================================================================

print("Processing CRM Builder A...")
crm_a = pd.read_csv('01_Data_Analytics/02A_api_crm_builder.csv')
print(f"  Loaded: {len(crm_a)} rows")

# Standardize community names
crm_a['community'] = crm_a['community'].apply(standardize_community)

# Save
crm_a.to_csv('01_Data_Analytics/10A_crm_standardized.csv', index=False)
print(f"  ✓ Saved to 10A_crm_standardized.csv")
print(f"  Communities after standardization: {sorted(crm_a['community'].unique())}\n")

# ============================================================================
# CRM BUILDER B
# ============================================================================

print("Processing CRM Builder B...")
crm_b = pd.read_csv('01_Data_Analytics/02B_api_crm_builder.csv')
print(f"  Loaded: {len(crm_b)} rows")

# Standardize community names
crm_b['community'] = crm_b['community'].apply(standardize_community)

# Save
crm_b.to_csv('01_Data_Analytics/10B_crm_standardized.csv', index=False)
print(f"  ✓ Saved to 10B_crm_standardized.csv")
print(f"  Communities after standardization: {sorted(crm_b['community'].unique())}\n")

# ============================================================================
# TRAFFIC BUILDER A
# ============================================================================

print("Processing Traffic Builder A...")
traffic_a = pd.read_csv('01_Data_Analytics/02A_api_traffic_builder.csv')
print(f"  Loaded: {len(traffic_a)} rows")

# Standardize community names
traffic_a['community'] = traffic_a['community'].apply(standardize_community)

# Drop unknown communities
unknown_communities = ['Stonegate Heights - New Homes']
before_count = len(traffic_a)
traffic_a = traffic_a[~traffic_a['community'].isin(unknown_communities)]
dropped = before_count - len(traffic_a)
if dropped > 0:
    print(f"  Dropped {dropped} records from unknown communities: {unknown_communities}")

# Save
traffic_a.to_csv('01_Data_Analytics/10A_traffic_standardized.csv', index=False)
print(f"  ✓ Saved to 10A_traffic_standardized.csv")
print(f"  Communities after standardization: {sorted(traffic_a['community'].unique())}\n")

# ============================================================================
# TRAFFIC BUILDER B
# ============================================================================

print("Processing Traffic Builder B...")
traffic_b = pd.read_csv('01_Data_Analytics/02B_api_traffic_builder.csv')
print(f"  Loaded: {len(traffic_b)} rows")

# Standardize community names
traffic_b['community'] = traffic_b['community'].apply(standardize_community)

# Drop unknown communities
unknown_communities = ['Conner Heights - New Homes']
before_count = len(traffic_b)
traffic_b = traffic_b[~traffic_b['community'].isin(unknown_communities)]
dropped = before_count - len(traffic_b)
if dropped > 0:
    print(f"  Dropped {dropped} records from unknown communities: {unknown_communities}")

# Save
traffic_b.to_csv('01_Data_Analytics/10B_traffic_standardized.csv', index=False)
print(f"  ✓ Saved to 10B_traffic_standardized.csv")
print(f"  Communities after standardization: {sorted(traffic_b['community'].unique())}\n")

print("=== STANDARDIZATION COMPLETE ===")
print("\nCreated files:")
print("  - 10A_crm_standardized.csv")
print("  - 10B_crm_standardized.csv")
print("  - 10A_traffic_standardized.csv")
print("  - 10B_traffic_standardized.csv")