import subprocess
import sys
from datetime import datetime

print("="*80)
print("OPENHOUSE.AI DATA PIPELINE - MASTER SCRIPT")
print("="*80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Define pipeline steps in order
pipeline_steps = [
    ("Step 1: Convert raw files + fix dates/names", "01_Data_Analytics/01_xlsx_to_csv+date_fix+name_fix.py"),
    ("Step 2: Download API data", "01_Data_Analytics/02_API_download.py"),
    ("Step 3: Add date columns", "01_Data_Analytics/04_date_premerge.py"),
    ("Step 4: Aggregate sales to monthly", "01_Data_Analytics/05_sales_date_monthly.py"),
    ("Step 5: Combine Builder A + B", "01_Data_Analytics/06_merge_A+B.py"),
    ("Step 6: Standardize API data", "01_Data_Analytics/10_API_community_fix.py"),
    ("Step 7: Aggregate API to monthly simple", "01_Data_Analytics/12_API_to_monthly_crm_simple.py"),
    ("Step 8: Aggregate API to monthly detailed", "01_Data_Analytics/13_API_monthly_crm_detailed.py"),
    ("Step 9: Final merge", "01_Data_Analytics/14_final_merge.py"),
]

failed_steps = []
completed_steps = []

for step_num, (description, script_path) in enumerate(pipeline_steps, 1):
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}")
    print(f"Running: {script_path}\n")
    
    try:
        # Run the script and wait for completion
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Print output
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        print(f"\n✓ Step {step_num} completed successfully")
        completed_steps.append(description)
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Step {step_num} FAILED")
        print(f"Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        failed_steps.append((description, str(e)))
        
        # Ask user if they want to continue
        print("\n" + "="*80)
        response = input("Step failed. Continue to next step? (y/n): ")
        if response.lower() != 'y':
            print("\nPipeline aborted by user.")
            break

# Final summary
print("\n" + "="*80)
print("PIPELINE SUMMARY")
print("="*80)
print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print(f"Completed steps: {len(completed_steps)}/{len(pipeline_steps)}")
for step in completed_steps:
    print(f"  ✓ {step}")

if failed_steps:
    print(f"\nFailed steps: {len(failed_steps)}")
    for step, error in failed_steps:
        print(f"  ✗ {step}")
        print(f"    Error: {error}")
else:
    print("\n✓ ALL STEPS COMPLETED SUCCESSFULLY")

print("\n" + "="*80)
print("Output file: 01_Data_Analytics/14_final_report_simple.csv")
print("="*80)