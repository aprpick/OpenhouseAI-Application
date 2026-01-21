import pandas as pd
import os
from pathlib import Path

raw_dir = Path('01_Data_Analytics/00_raw_data')
output_dir = Path('01_Data_Analytics')

print("=== FILE CONVERTER & RENAMER ===\n")

# Mapping of original names to new names
rename_map = {
    'sales_builder_a.csv': '00A_sales_builder.csv',
    'sales_builder_a.xlsx': '00A_sales_builder.csv',
    'target_sales_builder_a.csv': '00A_target_sales_builder.csv',
    'target_sales_builder_a.xlsx': '00A_target_sales_builder.csv',
    'sales_builder_b.csv': '00B_sales_builder.csv',
    'sales_builder_b.xlsx': '00B_sales_builder.csv',
    'target_sales_builder_b.csv': '00B_target_sales_builder.csv',
    'target_sales_builder_b.xlsx': '00B_target_sales_builder.csv',
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
        
        df.to_csv(output_path, index=False)
        print(f"  ✓ Converted and saved to: {new_name}\n")
    
    # Handle csv -> csv (just copy with new name)
    elif file.suffix == '.csv':
        df = pd.read_csv(file)
        df.to_csv(output_path, index=False)
        print(f"  ✓ Renamed and saved to: {new_name}\n")
    
    else:
        print(f"  ⚠ Unknown file type, skipping\n")

print("=== CONVERSION COMPLETE ===")
print("\nOutput files in 01_Data_Analytics/:")
for file in sorted(output_dir.glob('00*.csv')):
    print(f"  ✓ {file.name}")