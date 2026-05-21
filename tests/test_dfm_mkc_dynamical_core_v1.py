import subprocess
import sys

def test_dfm_mkc_dynamical_core_v1_scaffold_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_dynamical_core_v1.py"],
        check=True,
    )
