import pandas as pd
import os
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')

raw_dir = Path('01_Data_Analytics/00_raw_data')
output_dir = Path('01_Data_Analytics')

print("=== FILE CONVERTER & RENAMER ===\n")

# Date standardization function
def standardize_date(date_str):
    """Convert any date format to YYYY-MM-DD"""
    if pd.isna(date_str):
        return date_str
    
    date_str = str(date_str).strip()
    
    # Try multiple formats
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
            parsed = pd.to_datetime(date_str, format=fmt)
            return parsed.strftime('%Y-%m-%d')
        except:
            continue
    
    # Fallback: let pandas infer
    try:
        parsed = pd.to_datetime(date_str, dayfirst=False)
        return parsed.strftime('%Y-%m-%d')
    except:
        print(f"    WARNING: Could not parse date: {date_str}")
        return date_str

# Community name standardization function
def standardize_community(name):
    """Standardize community name variations"""
    if pd.isna(name):
        return name
    
    name = str(name).strip()
    
    # Fairview variations -> Fairview Estates
    if any(x in name.lower() for x in ['fairview']):
        return 'Fairview Estates'
    
    # Maplewood variations -> Maplewood Heights
    if any(x in name.lower() for x in ['maplewood']):
        return 'Maplewood Heights'
    
    # Return as-is for others
    return name

# Mapping of original names to new names
rename_map = {
    'sales_builder_a.csv': '01A_sales_builder.csv',
    'sales_builder_a.xlsx': '01A_sales_builder.csv',
    'target_sales_builder_a.csv': '01A_target_sales_builder.csv',
    'target_sales_builder_a.xlsx': '01A_target_sales_builder.csv',
    'sales_builder_b.csv': '01B_sales_builder.csv',
    'sales_builder_b.xlsx': '01B_sales_builder.csv',
    'target_sales_builder_b.csv': '01B_target_sales_builder.csv',
    'target_sales_builder_b.xlsx': '01B_target_sales_builder.csv',
}

# Process each file in raw_data
for file in raw_dir.glob('*'):
    if file.name.startswith('.'):
        continue
    
    print(f"Processing: {file.name}")
    
    # Get new name
    new_name = rename_map.get(file.name)
    if not new_name:
        print(f"  ⚠ No mapping found, skipping\n")
        continue
    
    output_path = output_dir / new_name
    
    # Handle xlsx -> csv conversion
    if file.suffix == '.xlsx':
        print(f"  Converting Excel to CSV...")
        
        # Check if it's the semicolon-delimited target file
        if 'target' in file.name.lower() and 'builder_a' in file.name.lower():
            print(f"  Special handling for Builder A targets (semicolon-delimited)")
            
            # Read and parse semicolon-delimited Excel
            df_raw = pd.read_excel(file, header=None)
            df_split = df_raw[0].str.split(';', expand=True)
            
            # Row 2 is header, data starts at row 3
            header_row = df_split.iloc[2].tolist()
            data_rows = df_split.iloc[3:].reset_index(drop=True)
            data_rows.columns = header_row
            
            # Convert to long format
            result = []
            for idx, row in data_rows.iterrows():
                community = row['Subdivision']
                
                months_2025 = ['Jan-25', 'Feb-25', 'Mar-25', 'Apr-25', 'May-25', 'Jun-25',
                               'Jul-25', 'Aug-25', 'Sep-25', 'Oct-25', 'Nov-25', 'Dec-25']
                months_2026 = ['Jan-26', 'Feb-26', 'Mar-26', 'Apr-26', 'May-26', 'Jun-26',
                               'Jul-26', 'Aug-26', 'Sep-26', 'Oct-26', 'Nov-26', 'Dec-26']
                
                for month_col in months_2025 + months_2026:
                    if month_col in row.index:
                        value = row[month_col]
                        month_name, year_short = month_col.split('-')
                        year = 2000 + int(year_short)
                        month_num = pd.to_datetime(month_name, format='%b').month
                        
                        result.append({
                            'community': community,
                            'year': year,
                            'month': month_num,
                            'sales_target': int(value) if pd.notna(value) and value != '' else 0
                        })
            
            df = pd.DataFrame(result)
        else:
            # Regular Excel file
            df = pd.read_excel(file)
            
            # Standardize dates if this is a sales file
            if 'sale_contract_date' in df.columns:
                print(f"  Standardizing dates...")
                df['sale_contract_date'] = df['sale_contract_date'].apply(standardize_date)
        
        df.to_csv(output_path, index=False)
        print(f"  ✓ Converted and saved to: {new_name}\n")
    
    # Handle csv -> csv (just copy with new name, but standardize dates)
    elif file.suffix == '.csv':
        df = pd.read_csv(file)
        
        # Standardize dates if this is a sales file
        if 'sale_contract_date' in df.columns:
            print(f"  Standardizing dates...")
            df['sale_contract_date'] = df['sale_contract_date'].apply(standardize_date)
        
        # Standardize community names if column exists
        if 'community_name' in df.columns:
            print(f"  Standardizing community names...")
            df['community_name'] = df['community_name'].apply(standardize_community)
        elif 'community' in df.columns:
            print(f"  Standardizing community names...")
            df['community'] = df['community'].apply(standardize_community)
        
        # Standardize community names if column exists
        if 'community_name' in df.columns:
            print(f"  Standardizing community names...")
            df['community_name'] = df['community_name'].apply(standardize_community)
        elif 'community' in df.columns:
            print(f"  Standardizing community names...")
            df['community'] = df['community'].apply(standardize_community)
        
        df.to_csv(output_path, index=False)
        print(f"  ✓ Renamed and saved to: {new_name}\n")
    
    else:
        print(f"  ⚠ Unknown file type, skipping\n")

print("=== CONVERSION COMPLETE ===")
print("\nOutput files in 01_Data_Analytics/:")
for file in sorted(output_dir.glob('00*.csv')):
    print(f"  ✓ {file.name}")