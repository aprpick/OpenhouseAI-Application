"""
Data Explorer - Analyze CSV and generate markdown report
Creates comprehensive data profile for any CSV file.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================
INPUT_FILE = "00_data_raw.csv"
OUTPUT_FILE = "01.1_output.md"

# Thresholds
CATEGORICAL_THRESHOLD = 30  # Max unique values to be considered categorical
# ============================================================================

def classify_column_type(series):
    """
    Classify column as: numerical, categorical, date, or text.
    
    Args:
        series: pandas Series
        
    Returns:
        str: 'numerical', 'categorical', 'date', or 'text'
    """
    # Check if numerical
    if pd.api.types.is_numeric_dtype(series):
        return 'numerical'
    
    # Check if date - try to parse non-null values
    non_null = series.dropna()
    if len(non_null) > 0:
        # Sample up to 20 values
        sample = non_null.head(min(20, len(non_null)))
        try:
            parsed = pd.to_datetime(sample, errors='coerce')
            # If >50% successfully parse as dates, it's a date column
            success_rate = parsed.notna().sum() / len(sample)
            if success_rate > 0.5:
                return 'date'
        except:
            pass
    
    # Check if categorical (few unique values)
    unique_count = series.nunique()
    if unique_count < CATEGORICAL_THRESHOLD:
        return 'categorical'
    
    # Everything else is text
    return 'text'

def analyze_csv(filepath):
    """
    Analyze CSV file and return comprehensive report data.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        dict: Analysis results
    """
    print(f"Analyzing {filepath}...")
    
    # Load data
    try:
        df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='warn')
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding='latin-1', on_bad_lines='warn')
    except Exception:
        df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
    
    # Basic stats
    file_size = Path(filepath).stat().st_size
    
    results = {
        'filename': Path(filepath).name,
        'rows': len(df),
        'columns': len(df.columns),
        'file_size': file_size,
        'file_size_mb': file_size / (1024 * 1024),
        'column_details': []
    }
    
    # Analyze each column
    print(f"Analyzing {len(df.columns)} columns...")
    for col in df.columns:
        col_info = analyze_column(df[col])
        results['column_details'].append(col_info)
    
    return results

def analyze_column(series):
    """
    Analyze a single column and return detailed stats.
    
    Args:
        series: pandas Series
        
    Returns:
        dict: Column analysis
    """
    col_type = classify_column_type(series)
    
    info = {
        'name': series.name,
        'type': col_type,
        'dtype': str(series.dtype),
        'missing': series.isnull().sum(),
        'missing_pct': (series.isnull().sum() / len(series)) * 100,
        'unique': series.nunique()
    }
    
    # Type-specific analysis
    if col_type == 'numerical':
        info.update(analyze_numerical(series))
    elif col_type == 'categorical':
        info.update(analyze_categorical(series))
    elif col_type == 'date':
        info.update(analyze_date(series))
    else:  # text
        info.update(analyze_text(series))
    
    # Check for type mismatches (non-matching values)
    info['type_issues'] = check_type_consistency(series, col_type)
    
    return info

def analyze_numerical(series):
    """Analyze numerical column."""
    return {
        'min': series.min(),
        'max': series.max(),
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std()
    }

def analyze_categorical(series):
    """Analyze categorical column."""
    value_counts = series.value_counts()
    
    return {
        'unique_values': series.nunique(),
        'most_common': value_counts.head(5).to_dict(),
        'rarest': value_counts.tail(5).to_dict()
    }

def analyze_date(series):
    """Analyze date column."""
    # Parse all dates
    dates = pd.to_datetime(series, errors='coerce')
    valid_dates = dates.dropna()
    unparseable = (dates.isnull() & series.notnull()).sum()
    
    if len(valid_dates) > 0:
        return {
            'earliest': str(valid_dates.min().date()),
            'latest': str(valid_dates.max().date()),
            'unparseable': unparseable,
            'date_formats': series.dropna().sample(min(3, len(series.dropna()))).tolist()
        }
    else:
        # No valid dates found
        return {
            'unparseable': len(series.dropna()),
            'sample_values': series.dropna().sample(min(5, len(series.dropna()))).tolist()
        }

def analyze_text(series):
    """Analyze text column."""
    sample_size = min(5, len(series.dropna()))
    samples = series.dropna().sample(sample_size).tolist() if sample_size > 0 else []
    
    return {
        'sample_values': samples,
        'avg_length': series.astype(str).str.len().mean()
    }

def check_type_consistency(series, expected_type):
    """Check if all values match expected type."""
    issues = []
    
    if expected_type == 'numerical':
        # Check if any non-numeric when it should be numeric
        non_numeric = pd.to_numeric(series, errors='coerce').isnull() & series.notnull()
        if non_numeric.any():
            bad_values = series[non_numeric].unique()[:3]  # Show up to 3 examples
            issues.append(f"Non-numeric values found: {list(bad_values)}")
    
    return issues

def generate_markdown(results, output_path):
    """
    Generate markdown report from analysis results.
    
    Args:
        results: Analysis results dict
        output_path: Where to save markdown file
    """
    print(f"Generating markdown report...")
    
    lines = []
    
    # Header
    lines.append(f"# Data Exploration Report")
    lines.append(f"")
    lines.append(f"**File:** `{results['filename']}`")
    lines.append(f"")
    
    # Basic Statistics
    lines.append(f"## Basic Statistics")
    lines.append(f"")
    lines.append(f"- **Rows:** {results['rows']:,}")
    lines.append(f"- **Columns:** {results['columns']}")
    lines.append(f"- **File Size:** {results['file_size']:,} bytes ({results['file_size_mb']:.2f} MB)")
    lines.append(f"")
    
    # Column Summary Table
    lines.append(f"## Column Summary")
    lines.append(f"")
    lines.append(f"| Column | Type | Missing | Unique |")
    lines.append(f"|--------|------|---------|--------|")
    
    for col in results['column_details']:
        lines.append(f"| {col['name']} | {col['type']} | {col['missing']} ({col['missing_pct']:.1f}%) | {col['unique']} |")
    
    lines.append(f"")
    
    # Detailed Column Analysis
    lines.append(f"## Detailed Column Analysis")
    lines.append(f"")
    
    for col in results['column_details']:
        lines.append(f"### {col['name']}")
        lines.append(f"")
        lines.append(f"**Type:** {col['type']} (`{col['dtype']}`)")
        lines.append(f"")
        lines.append(f"**Missing Values:** {col['missing']} ({col['missing_pct']:.1f}%)")
        lines.append(f"")
        
        # Type-specific details
        if col['type'] == 'numerical':
            lines.append(f"**Statistics:**")
            lines.append(f"- Min: {col['min']:.2f}")
            lines.append(f"- Max: {col['max']:.2f}")
            lines.append(f"- Mean: {col['mean']:.2f}")
            lines.append(f"- Median: {col['median']:.2f}")
            lines.append(f"- Std Dev: {col['std']:.2f}")
        
        elif col['type'] == 'categorical':
            lines.append(f"**Unique Values:** {col['unique_values']}")
            lines.append(f"")
            lines.append(f"**Most Common:**")
            for value, count in col['most_common'].items():
                lines.append(f"- `{value}`: {count} ({count/results['rows']*100:.1f}%)")
            
            lines.append(f"")
            lines.append(f"**Rarest:**")
            for value, count in col['rarest'].items():
                lines.append(f"- `{value}`: {count} ({count/results['rows']*100:.1f}%)")
        
        elif col['type'] == 'date':
            if 'earliest' in col:
                lines.append(f"**Date Range:**")
                lines.append(f"- Earliest: `{col['earliest']}`")
                lines.append(f"- Latest: `{col['latest']}`")
                if col['unparseable'] > 0:
                    lines.append(f"- ⚠️ Unparseable dates: {col['unparseable']}")
                
                lines.append(f"")
                lines.append(f"**Sample Formats:**")
                for val in col.get('date_formats', []):
                    lines.append(f"- `{val}`")
            else:
                lines.append(f"**⚠️ No valid dates found**")
                lines.append(f"- Unparseable: {col['unparseable']}")
                lines.append(f"")
                lines.append(f"**Sample Values:**")
                for val in col.get('sample_values', []):
                    lines.append(f"- `{val}`")
        
        else:  # text
            lines.append(f"**Average Length:** {col['avg_length']:.1f} characters")
            lines.append(f"")
            lines.append(f"**Sample Values:**")
            for val in col['sample_values']:
                display_val = str(val)[:50]  # Truncate long strings
                if len(str(val)) > 50:
                    display_val += "..."
                lines.append(f"- `{display_val}`")
        
        # Type issues
        if col['type_issues']:
            lines.append(f"")
            lines.append(f"**⚠️ Data Quality Issues:**")
            for issue in col['type_issues']:
                lines.append(f"- {issue}")
        
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Report saved to {output_path}")

def main():
    """Main execution."""
    print("=" * 80)
    print("DATA EXPLORER")
    print("=" * 80)
    print()
    
    # Check if file exists
    if not Path(INPUT_FILE).exists():
        print(f"❌ ERROR: File not found: {INPUT_FILE}")
        sys.exit(1)
    
    # Analyze
    results = analyze_csv(INPUT_FILE)
    
    # Generate markdown
    generate_markdown(results, OUTPUT_FILE)
    
    print()
    print("=" * 80)
    print("✓ ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"Report: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()