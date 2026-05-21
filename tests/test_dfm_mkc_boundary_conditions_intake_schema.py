import subprocess
import sys

def test_dfm_mkc_boundary_conditions_intake_schema_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_boundary_conditions_intake_schema.py"],
        check=True,
    )
