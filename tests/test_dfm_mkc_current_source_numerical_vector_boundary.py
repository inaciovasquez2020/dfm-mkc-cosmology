import subprocess
import sys

def test_dfm_mkc_current_source_numerical_vector_boundary():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_current_source_numerical_vector_boundary.py"],
        check=True,
    )
