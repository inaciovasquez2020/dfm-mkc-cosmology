import csv
import os
import subprocess
import sys
from pathlib import Path

def test_real_data_table_writer_marks_synthetic_placeholder_data():
    repo = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo)
    subprocess.run(
        [sys.executable, str(repo / "src/analysis/write_model_comparison_table.py")],
        cwd=repo,
        env=env,
        check=True,
    )
    rows = list(csv.DictReader((repo / "artifacts/results/model_comparison_real_data.csv").open()))
    assert len(rows) == 4
    assert all(r["status"] == "synthetic_placeholder_data" for r in rows)
