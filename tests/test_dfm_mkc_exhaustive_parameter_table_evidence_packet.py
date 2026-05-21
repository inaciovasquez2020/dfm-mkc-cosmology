import subprocess
import sys

def test_dfm_mkc_exhaustive_parameter_table_evidence_packet_verifies():
    subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_exhaustive_parameter_table_evidence_packet.py"],
        check=True,
    )
