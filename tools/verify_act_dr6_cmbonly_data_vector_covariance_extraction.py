#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_cmbonly_data_vector_covariance_extraction_2026_05_25.json")
TOOL = Path("tools/extract_act_dr6_cmbonly_data_vector_covariance.py")
DOC = Path("docs/status/ACT_DR6_CMBONLY_DATA_VECTOR_COVARIANCE_EXTRACTION_2026_05_25.md")

REQUIRED_BOUNDARIES = {
    "ACT DR6 empirical comparison has been run",
    "baseline LCDM prediction vector has been extracted",
    "DFM-MKC prediction vector exists",
    "residual eigenspace empirical comparison has been run",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "ACT validation of DFM-MKC",
    "CMB validation of DFM-MKC",
    "independent empirical replication",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

def main() -> None:
    subprocess.run(["python3", str(TOOL)], check=True)

    assert ART.exists(), ART
    assert DOC.exists(), DOC

    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["id"] == "ACT_DR6_CMBONLY_DATA_VECTOR_COVARIANCE_EXTRACTION_2026_05_25"
    assert data["status"] == "SCHEMA_LEVEL_EXTRACTION_ONLY_NO_EMPIRICAL_COMPARISON"
    assert data["hdu_count"] >= 1
    assert data["numeric_candidate_count"] >= 1
    assert data["data_vector_status"] == "CANDIDATE_ARRAYS_IDENTIFIED_NOT_PROMOTED"
    assert data["covariance_matrix_status"] == "CANDIDATE_ARRAYS_IDENTIFIED_NOT_PROMOTED"
    assert data["dfm_mkc_prediction_vector_status"] == "NOT_AVAILABLE_NO_DFM_MKC_ACT_SOLVER_BOUND"
    assert data["residual_eigenspace_empirical_run_status"] == "NOT_RUN"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in REQUIRED_BOUNDARIES | {
        "SCHEMA_LEVEL_EXTRACTION_ONLY_NO_EMPIRICAL_COMPARISON",
        "HYPOTHESIS_ONLY",
    }:
        assert token in doc, token

    print("ACT_DR6_CMBONLY_DATA_VECTOR_COVARIANCE_EXTRACTION_VERIFIED")


if __name__ == "__main__":
    main()
