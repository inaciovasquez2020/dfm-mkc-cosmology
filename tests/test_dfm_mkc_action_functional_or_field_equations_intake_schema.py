import subprocess
import sys

def test_dfm_mkc_action_functional_or_field_equations_intake_schema_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_action_functional_or_field_equations_intake_schema.py"],
        check=True,
    )
