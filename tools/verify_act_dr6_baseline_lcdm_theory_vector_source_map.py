#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_theory_vector_source_map_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE_MAP_2026_05_25.md")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
GATE = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_execution_gate_2026_05_25.json")

REQUIRED_SOURCES = {
    "ACT_DR6_ACT_LITE_LIKELIHOOD",
    "ACT_DR6_PARAMETERS_AND_RUN_SETTINGS",
    "NASA_LAMBDA_ACT_DR6_COBAYA_CHAINS",
}

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "checked NPZ baseline vector artifact exists",
    "baseline LCDM prediction vector is correct",
    "DFM-MKC prediction vector exists",
    "DFM-MKC prediction vector is correct",
    "ACT DR6 residual eigenspace empirical comparison has been run",
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
    assert ART.exists(), ART
    assert DOC.exists(), DOC
    assert ORDER.exists(), ORDER
    assert GATE.exists(), GATE

    data = json.loads(ART.read_text())
    order = json.loads(ORDER.read_text())
    doc = DOC.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE_MAP_2026_05_25"
    assert data["status"] == "OFFICIAL_COBAYA_CAMB_SOURCE_MAP_ONLY_NO_VECTOR_ARTIFACT_FOUND"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["standalone_official_row_aligned_npz_vector_found"] is False
    assert data["trusted_source_route_found"] is True
    assert data["minimal_next_object"]["id"] == "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS"
    assert data["minimal_next_object"]["status"] == "MISSING"
    assert data["allowed_next_status"] == "BASELINE_LCDM_OFFICIAL_SOURCE_ROUTE_FOUND_VECTOR_STILL_MISSING"
    assert data["still_missing_objects_after_this_source_map"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_SOURCES <= set(data["official_sources_found"])
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for source in REQUIRED_SOURCES:
        assert source in doc, source

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE_MAP",
            "OFFICIAL_COBAYA_CAMB_SOURCE_MAP_ONLY_NO_VECTOR_ARTIFACT_FOUND",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS",
            "BASELINE_LCDM_OFFICIAL_SOURCE_ROUTE_FOUND_VECTOR_STILL_MISSING",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE_MAP_OK")

if __name__ == "__main__":
    main()
