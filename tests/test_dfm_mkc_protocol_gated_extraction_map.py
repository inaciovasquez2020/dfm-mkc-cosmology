import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_protocol_gated_extraction_map_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_protocol_gated_extraction_map.py"],
        cwd=ROOT,
        check=True,
    )
