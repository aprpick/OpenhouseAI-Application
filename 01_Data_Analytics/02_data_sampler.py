"""
CSV Sampler - Extract random sample from large CSV
Takes N random rows for testing/validation purposes.
"""

import pandas as pd
from pathlib import Path
import sys
import os
import stat

# ============================================================================
# CONFIGURATION
# ============================================================================
INPUT_FILE = "01.1_merged.csv"
OUTPUT_FILE = "02.1_sample.csv"
SAMPLE_SIZE = 1000              # Number of random rows to extract
RANDOM_SEED = 42                # Set seed for reproducible sampling (or None for random)
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

def sample_csv(input_path, output_path, n_samples, random_seed):
    """
    Extract random sample from CSV.
    
    Args:
        input_path: Path to input CSV
        output_path: Path to output CSV
        n_samples: Number of rows to sample
        random_seed: Random seed for reproducibility
    """
    print("=" * 80)
    print("CSV SAMPLER")
    print("=" * 80)
    print()
    
    # Load data
    print(f"Loading: {input_path}")
    try:
        df = pd.read_csv(input_path, encoding='utf-8', on_bad_lines='warn')
    except UnicodeDecodeError:
        df = pd.read_csv(input_path, encoding='latin-1', on_bad_lines='warn')
    except Exception:
        df = pd.read_csv(input_path, encoding='utf-8', on_bad_lines='skip')
    
    print(f"  → Loaded {len(df):,} rows × {len(df.columns)} columns")
    
    # Adjust sample size if larger than dataset
    actual_sample_size = min(n_samples, len(df))
    
    if actual_sample_size < n_samples:
        print(f"\n⚠️  Requested {n_samples:,} samples but only {len(df):,} rows available")
        print(f"  → Sampling all {len(df):,} rows instead")
    
    # Sample
    print(f"\nSampling {actual_sample_size:,} random rows...")
    if random_seed is not None:
        print(f"  → Using random seed: {random_seed} (reproducible)")
        sampled = df.sample(n=actual_sample_size, random_state=random_seed)
    else:
        print(f"  → No seed specified (different results each run)")
        sampled = df.sample(n=actual_sample_size)
    
    # Save
    print(f"\nSaving sample to: {output_path}")
    output_path = Path(output_path)
    remove_read_only(output_path)
    sampled.to_csv(output_path, index=False)
    make_read_only(output_path)
    
    print(f"  ✓ Saved {len(sampled):,} rows")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original:  {len(df):>8,} rows")
    print(f"Sample:    {len(sampled):>8,} rows ({len(sampled)/len(df)*100:.1f}%)")
    print(f"Columns:   {len(sampled.columns):>8}")
    
    print("\n✓ SAMPLING COMPLETE")

def main():
    """Main execution."""
    # Check if file exists
    if not Path(INPUT_FILE).exists():
        print(f"❌ ERROR: File not found: {INPUT_FILE}")
        print(f"\nMake sure to run the merger script first to create {INPUT_FILE}")
        sys.exit(1)
    
    # Run sampling
    sample_csv(INPUT_FILE, OUTPUT_FILE, SAMPLE_SIZE, RANDOM_SEED)

if __name__ == "__main__":
    main()