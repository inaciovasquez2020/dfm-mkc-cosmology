import subprocess
import sys

def test_dfm_mkc_single_slot_promotion_gate_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_single_slot_promotion_gate.py"],
        check=True,
    )
