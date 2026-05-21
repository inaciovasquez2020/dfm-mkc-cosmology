import subprocess
import sys

def test_dfm_mkc_frozen_prediction_vector_intake_schema_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_frozen_prediction_vector_intake_schema.py"],
        check=True,
    )
