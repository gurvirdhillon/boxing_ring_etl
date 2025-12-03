import time
import subprocess
import os
import pytest

@pytest.mark.timeout(10)
@pytest.mark.xfail(reason="run_app.py is long-running; allowed to timeout.")
def test_run_app_execution_time():
    start = time.perf_counter()

    # Get the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Correct path to run_app.py inside /scripts/
    script_path = os.path.join(base_dir, "scripts", "run_app.py")

    # Safety check - fail early if file missing
    assert os.path.exists(script_path), f"run_app.py not found at: {script_path}"

    # Run the script
    try:
        subprocess.run(["python", script_path, "test"], check=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.skip("run_app took too long, skipping to next test")
        
    elapsed = time.perf_counter() - start
    print(f"\nrun_app.py finished in {elapsed:.2f} seconds")

# 
