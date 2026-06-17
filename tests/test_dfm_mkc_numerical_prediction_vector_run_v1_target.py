import subprocess
import sys

def test_dfm_mkc_numerical_prediction_vector_run_v1_target():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_numerical_prediction_vector_run_v1_target.py"],
        check=True,
    )
