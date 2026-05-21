import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_payload_extraction_classifier_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_payload_extraction_classifier.py"],
        cwd=ROOT,
        check=True,
    )
