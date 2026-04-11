import csv
import os
import subprocess
import sys
from pathlib import Path

def test_model_comparison_generates_expected_rows():
    repo = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo)
    subprocess.run(
        [sys.executable, str(repo / "src/analysis/model_comparison.py")],
        cwd=repo,
        env=env,
        check=True,
    )
    out = repo / "artifacts/results/model_comparison.csv"
    rows = list(csv.DictReader(out.open()))
    assert [r["model"] for r in rows] == ["LCDM", "wCDM", "curved_LCDM", "DFM_MKC"]
    assert all(r["status"] == "example" for r in rows)
    assert all(r["logL"] != "" for r in rows)
    assert all(r["AIC"] != "" for r in rows)
    assert all(r["BIC"] != "" for r in rows)
