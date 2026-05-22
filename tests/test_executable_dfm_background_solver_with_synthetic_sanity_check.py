import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dfm_background_solver.py"
ARTIFACT = ROOT / "artifacts/repo_intake/executable_dfm_background_solver_synthetic_sanity_check_2026_05_22.json"
CSV = ROOT / "artifacts/results/dfm_background_solver_synthetic_sanity_check_2026_05_22.csv"

def test_solver_executes():
    result = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    assert data["status"] == "EXECUTABLE_SYNTHETIC_SANITY_CHECK_ONLY_NO_EMPIRICAL_VALIDATION"
    assert data["sanity"]["lambda_cdm_limit_passed"] is True

def test_solver_csv_shape():
    assert CSV.exists()
    with CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 601
    assert abs(float(rows[-1]["N"])) < 1e-12
    assert abs(float(rows[-1]["z"])) < 1e-12

def test_solver_boundaries():
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, stdout=ARTIFACT.open("w", encoding="utf-8"))
    data = json.loads(ARTIFACT.read_text())
    for boundary in [
        "DFM-MKC validation",
        "Lambda-CDM failure",
        "dark matter resolution",
        "dark energy resolution",
        "gravity closure",
        "empirical validation",
        "ACT validation",
        "DESI validation",
        "DES validation",
        "P vs NP",
        "any Clay problem",
    ]:
        assert boundary in data["does_not_prove"]
