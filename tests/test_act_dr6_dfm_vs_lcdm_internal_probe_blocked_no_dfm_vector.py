
import subprocess
import sys

def test_act_dr6_dfm_vs_lcdm_internal_probe_blocked_no_dfm_vector():
    subprocess.run(
        [sys.executable, "tools/verify_act_dr6_dfm_vs_lcdm_internal_probe_blocked_no_dfm_vector.py"],
        check=True,
    )
