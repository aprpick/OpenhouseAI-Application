"""
CSV Merger - Join multiple CSV files on common key
Merges 2-3 data sources into unified dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
import stat

# ============================================================================
# CONFIGURATION
# ============================================================================
# Input files
INPUT_FILE_1 = "00_data_raw_1.csv"  # Primary/left table
INPUT_FILE_2 = "00_data_raw_2.csv"  # Secondary table to merge
INPUT_FILE_3 = None         # Optional third file (set to None if only merging 2)

# Output
OUTPUT_FILE = "01.1_merged.csv"

# Join settings
JOIN_KEY = "customer_id"           # Column to join on (must exist in all files)
JOIN_TYPE = "left"                 # 'left', 'right', 'inner', or 'outer'
# left = keep all from file 1, add matching from file 2
# inner = only keep rows that match in both
# outer = keep everything from both files
# right = keep all from file 2, add matching from file 1
# ============================================================================

def make_read_only(filepath):
    """Make CSV file read-only to prevent accidental modification."""
    filepath = Path(filepath)
    if filepath.exists():
        current_permissions = stat.S_IMODE(os.lstat(filepath).st_mode)
        os.chmod(filepath, current_permissions & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
        print(f"  ✓ Set {filepath.name} to read-only")

def remove_read_only(filepath):
    """Remove read-only flag so file can be overwritten."""
    filepath = Path(filepath)
    if filepath.exists():
        current_permissions = stat.S_IMODE(os.lstat(filepath).st_mode)
        os.chmod(filepath, current_permissions | stat.S_IWUSR)

def load_csv(filepath, label):
    """Load CSV with error handling."""
    print(f"Loading {label}: {filepath}")
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='warn')
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding='latin-1', on_bad_lines='warn')
    except Exception:
        df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
    
    print(f"  → {len(df):,} rows × {len(df.columns)} columns")
    return df

def analyze_join_compatibility(df1, df2, join_key, label1="File 1", label2="File 2"):
    """Analyze how well two dataframes will join."""
    print(f"\nAnalyzing join compatibility: {label1} + {label2}")
    print("-" * 80)
    
    # Check if join key exists
    if join_key not in df1.columns:
        print(f"❌ ERROR: Join key '{join_key}' not found in {label1}")
        return False
    if join_key not in df2.columns:
        print(f"❌ ERROR: Join key '{join_key}' not found in {label2}")
        return False
    
    # Check for nulls in join key
    nulls1 = df1[join_key].isnull().sum()
    nulls2 = df2[join_key].isnull().sum()
    
    if nulls1 > 0:
        print(f"⚠️  {label1} has {nulls1} null values in join key")
    if nulls2 > 0:
        print(f"⚠️  {label2} has {nulls2} null values in join key")
    
    # Check for duplicates in join key
    dups1 = df1[join_key].duplicated().sum()
    dups2 = df2[join_key].duplicated().sum()
    
    if dups1 > 0:
        print(f"⚠️  {label1} has {dups1} duplicate values in join key (one-to-many)")
    if dups2 > 0:
        print(f"⚠️  {label2} has {dups2} duplicate values in join key (one-to-many)")
    
    # Overlap analysis
    values1 = set(df1[join_key].dropna())
    values2 = set(df2[join_key].dropna())
    
    overlap = len(values1 & values2)
    only_in_1 = len(values1 - values2)
    only_in_2 = len(values2 - values1)
    
    print(f"\nJoin key overlap:")
    print(f"  • In both files: {overlap:,} values")
    print(f"  • Only in {label1}: {only_in_1:,} values")
    print(f"  • Only in {label2}: {only_in_2:,} values")
    
    if overlap == 0:
        print(f"\n❌ WARNING: No overlapping values! Join will produce all nulls.")
        return False
    
    match_rate = (overlap / len(values1)) * 100 if len(values1) > 0 else 0
    print(f"  • Match rate: {match_rate:.1f}%")
    
    return True

def merge_files(df1, df2, join_key, join_type, label1="File 1", label2="File 2"):
    """Merge two dataframes."""
    print(f"\nMerging {label1} + {label2}...")
    print(f"  Join type: {join_type.upper()}")
    print(f"  Join key: '{join_key}'")
    
    # Perform merge
    merged = pd.merge(
        df1, df2,
        on=join_key,
        how=join_type,
        suffixes=('', '_dup')  # Add _dup to duplicate column names from file 2
    )
    
    print(f"  → Result: {len(merged):,} rows × {len(merged.columns)} columns")
    
    # Calculate match statistics
    if join_type == 'left':
        # Count how many from file 1 got matches from file 2
        # Check if any columns from file 2 exist (excluding join key)
        file2_cols = [col for col in df2.columns if col != join_key]
        if file2_cols:
            # Use first file2 column to check for matches
            matched = merged[file2_cols[0]].notna().sum()
            match_rate = (matched / len(merged)) * 100
            print(f"  → Matched: {matched:,} of {len(merged):,} rows ({match_rate:.1f}%)")
    
    return merged

def main():
    """Main execution."""
    print("=" * 80)
    print("CSV MERGER")
    print("=" * 80)
    print()
    
    # Load files
    print("LOADING FILES")
    print("-" * 80)
    
    if not Path(INPUT_FILE_1).exists():
        print(f"❌ ERROR: File not found: {INPUT_FILE_1}")
        sys.exit(1)
    
    if not Path(INPUT_FILE_2).exists():
        print(f"❌ ERROR: File not found: {INPUT_FILE_2}")
        sys.exit(1)
    
    df1 = load_csv(INPUT_FILE_1, "File 1 (Primary)")
    df2 = load_csv(INPUT_FILE_2, "File 2 (Secondary)")
    
    # Analyze compatibility
    if not analyze_join_compatibility(df1, df2, JOIN_KEY):
        print("\n❌ Cannot proceed with merge due to compatibility issues")
        sys.exit(1)
    
    # Merge file 1 + file 2
    merged = merge_files(df1, df2, JOIN_KEY, JOIN_TYPE, "File 1", "File 2")
    
    # If third file exists, merge it too
    if INPUT_FILE_3 and Path(INPUT_FILE_3).exists():
        print("\n" + "=" * 80)
        df3 = load_csv(INPUT_FILE_3, "File 3 (Additional)")
        
        if not analyze_join_compatibility(merged, df3, JOIN_KEY, "Merged so far", "File 3"):
            print("\n⚠️  Skipping File 3 due to compatibility issues")
        else:
            merged = merge_files(merged, df3, JOIN_KEY, JOIN_TYPE, "Merged", "File 3")
    
    # Save output
    print("\n" + "=" * 80)
    print("SAVING OUTPUT")
    print("-" * 80)
    
    output_path = Path(OUTPUT_FILE)
    remove_read_only(output_path)
    merged.to_csv(output_path, index=False)
    make_read_only(output_path)
    
    print(f"✓ Merged data saved to {output_path}")
    
    # Summary
    print("\n" + "=" * 80)
    print("MERGE SUMMARY")
    print("=" * 80)
    print(f"Input 1:  {len(df1):>8,} rows × {len(df1.columns):>3} columns")
    print(f"Input 2:  {len(df2):>8,} rows × {len(df2.columns):>3} columns")
    if INPUT_FILE_3 and Path(INPUT_FILE_3).exists():
        print(f"Input 3:  {len(df3):>8,} rows × {len(df3.columns):>3} columns")
    print(f"Output:   {len(merged):>8,} rows × {len(merged.columns):>3} columns")
    
    # Check for null columns (indicates no matches)
    null_cols = merged.columns[merged.isnull().all()].tolist()
    if null_cols:
        print(f"\n⚠️  Warning: {len(null_cols)} columns are entirely null (no matches):")
        for col in null_cols[:5]:  # Show first 5
            print(f"    - {col}")
    
    print("\n✓ MERGE COMPLETE")

if __name__ == "__main__":
    main()