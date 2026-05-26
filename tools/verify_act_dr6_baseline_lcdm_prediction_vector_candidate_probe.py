#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_2026_05_25.json")
RESULT = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_result.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE_2026_05_25.md")
PROBE = Path("tools/probe_act_dr6_baseline_lcdm_prediction_vector_candidates.py")
HARNESS_ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_cobaya_run_output_binding_harness_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "baseline LCDM prediction vector is official",
    "baseline LCDM prediction vector is physically correct",
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
    assert RESULT.exists(), RESULT
    assert DOC.exists(), DOC
    assert PROBE.exists(), PROBE
    assert HARNESS_ART.exists(), HARNESS_ART
    assert ORDER.exists(), ORDER

    data = json.loads(ART.read_text())
    result = json.loads(RESULT.read_text())
    order = json.loads(ORDER.read_text())
    doc = DOC.read_text()
    probe_text = PROBE.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE_2026_05_25"
    assert data["status"] == "CANDIDATE_PROBE_ONLY_BASELINE_VECTOR_NOT_PROMOTED"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["object_added"]["id"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE"
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["probe_result_status"] == result["status"]
    assert data["matching_candidate_count"] == result["matching_candidate_count"]
    assert data["still_missing_objects_after_this_probe"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in [
        "discover_files",
        "inspect_candidate",
        "bind_first_match",
        "MATCHING_CANDIDATE_FOUND_AND_BOUND",
        "NO_MATCHING_BASELINE_LCDM_VECTOR_CANDIDATE_FOUND",
    ]:
        assert token in probe_text, token

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE",
            "CANDIDATE_PROBE_ONLY_BASELINE_VECTOR_NOT_PROMOTED",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE_OK")

if __name__ == "__main__":
    main()
