
import subprocess
import sys

def test_act_dr6_dfm_mkc_135_row_prediction_vector_candidate_target():
    subprocess.run(
        [sys.executable, "tools/verify_act_dr6_dfm_mkc_135_row_prediction_vector_candidate_target.py"],
        check=True,
    )
