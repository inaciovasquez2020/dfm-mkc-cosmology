import subprocess
import sys
from pathlib import Path


def test_des_y6_real_data_materialization_frontier():
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, "tools/verify_des_y6_real_data_materialization_frontier.py"],
        cwd=repo,
        check=True,
    )
