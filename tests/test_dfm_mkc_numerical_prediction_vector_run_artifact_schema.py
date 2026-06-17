import subprocess
import sys

def test_dfm_mkc_numerical_prediction_vector_run_artifact_schema():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_numerical_prediction_vector_run_artifact_schema.py"],
        check=True,
    )
