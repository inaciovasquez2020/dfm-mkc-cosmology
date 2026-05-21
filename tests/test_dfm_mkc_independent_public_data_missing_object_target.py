import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_independent_public_data_missing_object_target_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_independent_public_data_missing_object_target.py"],
        cwd=ROOT,
        check=True,
    )
