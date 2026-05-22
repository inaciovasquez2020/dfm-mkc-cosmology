#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dfm_background_solver.py"
ARTIFACT = ROOT / "artifacts/repo_intake/executable_dfm_background_solver_synthetic_sanity_check_2026_05_22.json"
CSV = ROOT / "artifacts/results/dfm_background_solver_synthetic_sanity_check_2026_05_22.csv"
DOC = ROOT / "docs/status/EXECUTABLE_DFM_BACKGROUND_SOLVER_WITH_SYNTHETIC_SANITY_CHECK_2026_05_22.md"

STATUS = "EXECUTABLE_SYNTHETIC_SANITY_CHECK_ONLY_NO_EMPIRICAL_VALIDATION"
MODEL = "MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1"

BOUNDARIES = {
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
}

def require(ok: bool, msg: str) -> None:
    if not ok:
        raise SystemExit(msg)

def main() -> None:
    require(SCRIPT.exists(), f"Missing solver script: {SCRIPT}")

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    with ARTIFACT.open("w", encoding="utf-8") as f:
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, stdout=f)

    require(ARTIFACT.exists(), f"Missing artifact: {ARTIFACT}")
    require(CSV.exists(), f"Missing CSV: {CSV}")
    require(DOC.exists(), f"Missing doc: {DOC}")

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(data["status"] == STATUS, "Bad status")
    require(data["model"] == MODEL, "Bad model")
    require(data["sanity"]["lambda_cdm_limit_passed"] is True, "Lambda-CDM synthetic sanity check failed")
    require(set(data["does_not_prove"]) == BOUNDARIES, "Bad boundary set")

    with CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    require(len(rows) == 601, "Expected 601 solver rows")
    require(abs(float(rows[-1]["N"])) < 1e-12, "Final N must be zero")
    require(abs(float(rows[-1]["z"])) < 1e-12, "Final z must be zero")
    require(float(rows[-1]["H_dimensionless"]) > 0, "Final H must be positive")

    for boundary in BOUNDARIES:
        require(boundary in doc, f"Doc missing boundary: {boundary}")

    print("Executable DFM background solver synthetic sanity-check verification OK.")
    print(f"Status: {STATUS}")

if __name__ == "__main__":
    main()
