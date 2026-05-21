import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_act_des_holdout_survival_intake_schema_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_act_des_holdout_survival_intake_schema.py"],
        cwd=ROOT,
        check=True,
    )
