import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_downloaded_public_payload_manifest_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_downloaded_public_payload_manifest.py"],
        cwd=ROOT,
        check=True,
    )
