
import subprocess
import sys

def test_act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_official_convention_audit():
    subprocess.run(
        [sys.executable, "tools/verify_act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_official_convention_audit.py"],
        check=True,
    )
