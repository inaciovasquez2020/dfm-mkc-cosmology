import subprocess
import sys

def test_dfm_mkc_full_closure_blocker_certificate_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_full_closure_blocker_certificate.py"],
        check=True,
    )
