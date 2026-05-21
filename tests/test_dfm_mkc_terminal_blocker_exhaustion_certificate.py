import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_terminal_blocker_exhaustion_certificate_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_terminal_blocker_exhaustion_certificate.py"],
        cwd=ROOT,
        check=True,
    )
