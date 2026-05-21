import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_act_lite_numeric_like_extraction_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_act_lite_numeric_like_extraction.py"],
        cwd=ROOT,
        check=True,
    )
