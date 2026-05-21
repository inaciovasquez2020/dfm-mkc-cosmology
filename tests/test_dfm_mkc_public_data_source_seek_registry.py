import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_dfm_mkc_public_data_source_seek_registry_verifies():
    subprocess.run(
        ["python3", "tools/verify_dfm_mkc_public_data_source_seek_registry.py"],
        cwd=ROOT,
        check=True,
    )
