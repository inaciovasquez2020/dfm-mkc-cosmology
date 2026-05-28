import subprocess
import sys

def test_act_dr6_baseline_lcdm_sacc_actual_value_binding_witness():
    subprocess.run(
        [sys.executable, "tools/verify_act_dr6_baseline_lcdm_sacc_actual_value_binding_witness.py"],
        check=True,
    )
