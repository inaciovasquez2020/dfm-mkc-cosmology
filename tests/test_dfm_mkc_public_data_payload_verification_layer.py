import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_public_data_payload_verification_layer_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_public_data_payload_verification_layer.py"],
        cwd=ROOT,
        check=True,
    )
