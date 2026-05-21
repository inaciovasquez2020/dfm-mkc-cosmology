import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_independent_empirical_validation_intake_schema_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_independent_empirical_validation_intake_schema.py"],
        cwd=ROOT,
        check=True,
    )
