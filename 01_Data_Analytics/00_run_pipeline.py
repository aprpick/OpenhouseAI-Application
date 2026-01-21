"""
Pipeline Runner - Execute data processing pipeline in order
Runs all scripts in sequence with error handling.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# PIPELINE CONFIGURATION - Edit this list to add/remove/reorder scripts
# ============================================================================
PIPELINE_STEPS = [
    {
        'name': 'Merge Data Sources',
        'script': '01_merger.py',
        'description': 'Combine multiple CSV files into one'
    },
    {
        'name': 'Sample Dataset',
        'script': '02_data_sampler.py',
        'description': 'Extract random sample for testing'
    },
    {
        'name': 'Explore Data',
        'script': '03_data_explorer.py',
        'description': 'Generate data profiling report'
    },
    # Add more steps here as needed:
    # {
    #     'name': 'Clean Data',
    #     'script': '04_cleaner.py',
    #     'description': 'Standardize and clean dataset'
    # },
]

# Options
STOP_ON_ERROR = True  # Set to False to continue even if a step fails
# ============================================================================

def run_script(script_path, step_name):
    """
    Run a Python script and capture output.
    
    Args:
        script_path: Path to script
        step_name: Name of the step (for logging)
        
    Returns:
        bool: True if successful, False if failed
    """
    print(f"\n{'='*80}")
    print(f"RUNNING: {step_name}")
    print(f"Script: {script_path}")
    print(f"{'='*80}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,  # Show output in real-time
            text=True,
            check=True
        )
        
        print(f"\n✓ {step_name} completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {step_name} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ {step_name} failed: {str(e)}")
        return False

def main():
    """Execute the pipeline."""
    start_time = datetime.now()
    
    print("=" * 80)
    print("DATA PROCESSING PIPELINE")
    print("=" * 80)
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total steps: {len(PIPELINE_STEPS)}")
    print()
    
    results = []
    
    for i, step in enumerate(PIPELINE_STEPS, 1):
        print(f"\n[Step {i}/{len(PIPELINE_STEPS)}] {step['name']}")
        print(f"Description: {step['description']}")
        
        script_path = Path(step['script'])
        
        # Check if script exists
        if not script_path.exists():
            print(f"⚠️  Warning: Script not found: {script_path}")
            results.append({
                'step': step['name'],
                'status': 'SKIPPED',
                'reason': 'Script not found'
            })
            
            if STOP_ON_ERROR:
                print(f"\n❌ Pipeline stopped (STOP_ON_ERROR = True)")
                break
            else:
                print(f"Continuing to next step...")
                continue
        
        # Run the script
        success = run_script(script_path, step['name'])
        
        results.append({
            'step': step['name'],
            'status': 'SUCCESS' if success else 'FAILED'
        })
        
        if not success and STOP_ON_ERROR:
            print(f"\n❌ Pipeline stopped due to error (STOP_ON_ERROR = True)")
            break
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("PIPELINE SUMMARY")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        status_symbol = "✓" if result['status'] == 'SUCCESS' else "❌" if result['status'] == 'FAILED' else "⊘"
        print(f"{i}. {status_symbol} {result['step']}: {result['status']}")
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    failed_count = sum(1 for r in results if r['status'] == 'FAILED')
    skipped_count = sum(1 for r in results if r['status'] == 'SKIPPED')
    
    print(f"\nResults: {success_count} succeeded, {failed_count} failed, {skipped_count} skipped")
    print(f"Duration: {duration.total_seconds():.2f} seconds")
    print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_count == 0 and skipped_count == 0:
        print("\n✓ PIPELINE COMPLETED SUCCESSFULLY")
        return 0
    else:
        print(f"\n⚠️  PIPELINE COMPLETED WITH ISSUES")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)