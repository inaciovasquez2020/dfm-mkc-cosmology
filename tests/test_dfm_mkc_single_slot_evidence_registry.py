import subprocess
import sys

def test_dfm_mkc_single_slot_evidence_registry_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_single_slot_evidence_registry.py"],
        check=True,
    )
