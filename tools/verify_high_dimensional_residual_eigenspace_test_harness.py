#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/high_dimensional_residual_eigenspace_test_harness_2026_05_25.json")
DOC = Path("docs/status/HIGH_DIMENSIONAL_RESIDUAL_EIGENSPACE_TEST_HARNESS_2026_05_25.md")
TOOL = Path("tools/run_high_dimensional_residual_eigenspace_test.py")

REQUIRED_OBJECTS = {
    "HIGH_DIMENSIONAL_RESIDUAL_EIGENSPACE_SYNTHETIC_TEST_HARNESS",
    "RESIDUAL_COVARIANCE_EIGENSPECTRUM_DIAGNOSTIC",
    "TOP_EIGENSPACE_PROJECTION_DIAGNOSTIC",
    "BOUNDARY_COVARIANCE_SYNTHETIC_FAILURE_CASE",
}

REQUIRED_BOUNDARIES = {
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "dark matter resolution",
    "dark energy resolution",
    "ACT validation",
    "DES validation",
    "CMB validation",
    "BAO validation",
    "independent empirical replication",
    "gravity closure",
    "Chronos proof input",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

def main() -> None:
    assert ART.exists(), ART
    assert DOC.exists(), DOC
    assert TOOL.exists(), TOOL

    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["id"] == "HIGH_DIMENSIONAL_RESIDUAL_EIGENSPACE_TEST_HARNESS_2026_05_25"
    assert data["status"] == "SYNTHETIC_HARNESS_ONLY_NO_EMPIRICAL_EVIDENCE"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"

    object_ids = {obj["id"] for obj in data["objects_added"]}
    assert REQUIRED_OBJECTS <= object_ids

    boundaries = set(data["does_not_prove"])
    assert REQUIRED_BOUNDARIES <= boundaries

    for token in REQUIRED_OBJECTS | REQUIRED_BOUNDARIES:
        assert token in doc, token

    assert "SYNTHETIC_HARNESS_ONLY_NO_EMPIRICAL_EVIDENCE" in doc
    assert "HYPOTHESIS_ONLY" in doc

    result = subprocess.run(
        ["python3", str(TOOL), "--seed", "145", "--top-k", "3"],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert payload["status"] == "SYNTHETIC_HARNESS_ONLY_NO_EMPIRICAL_EVIDENCE"
    assert payload["dimension"] == 12
    assert payload["baseline_rank"] == 12
    assert payload["candidate_rank"] == 12
    assert payload["singular_failure_rank"] < 12
    assert payload["boundary_guard_passed"] is True
    assert payload["synthetic_singular_boundary_guard_passed"] is False
    assert payload["top_eigenspace_projection_distance"] >= 0.0
    assert payload["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"

    print("HIGH_DIMENSIONAL_RESIDUAL_EIGENSPACE_TEST_HARNESS_OK")

if __name__ == "__main__":
    main()
