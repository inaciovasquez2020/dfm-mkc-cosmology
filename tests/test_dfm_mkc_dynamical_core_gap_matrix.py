import subprocess
import sys

def test_dfm_mkc_dynamical_core_gap_matrix_verifies():
    subprocess.run(
        [sys.executable, "tools/build_dfm_mkc_dynamical_core_gap_matrix.py"],
        check=True,
    )
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_dynamical_core_gap_matrix.py"],
        check=True,
    )
