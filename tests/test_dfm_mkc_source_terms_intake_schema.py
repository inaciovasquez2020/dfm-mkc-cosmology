import subprocess
import sys

def test_dfm_mkc_source_terms_intake_schema_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_source_terms_intake_schema.py"],
        check=True,
    )
