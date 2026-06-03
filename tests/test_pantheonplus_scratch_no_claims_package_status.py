import subprocess
import sys

def test_pantheonplus_scratch_no_claims_package_status_verifier():
    subprocess.check_call([
        sys.executable,
        "tools/verify_pantheonplus_scratch_no_claims_package_status.py",
    ])
