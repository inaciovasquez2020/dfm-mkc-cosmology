import subprocess
import sys

def test_dfm_mkc_single_slot_evidence_packet_template_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_single_slot_evidence_packet_template.py"],
        check=True,
    )
