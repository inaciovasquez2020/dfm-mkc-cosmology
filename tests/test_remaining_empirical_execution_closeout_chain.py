import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/remaining_empirical_execution_closeout_chain_2026_05_22.json"
DOC = ROOT / "docs/status/REMAINING_EMPIRICAL_EXECUTION_CLOSEOUT_CHAIN_2026_05_22.md"

def test_closeout_chain_exists():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "REMAINING_EMPIRICAL_EXECUTION_CLOSEOUT_CHAIN"
    assert data["status"] == "TERMINAL_CLOSEOUT_CHAIN_MATERIALIZED_EXECUTION_BLOCKED_BY_MISSING_REAL_PAYLOADS"
    assert data["finish_for_day_status"] == "structural_closeout_complete_empirical_execution_not_started"

def test_all_remaining_steps_are_recorded():
    data = json.loads(ARTIFACT.read_text())
    objects = [step["object"] for step in data["closeout_steps"]]
    assert "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS" in objects
    assert "ACTUAL_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS" in objects
    assert "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS" in objects
    assert "ACTUAL_LIKELIHOOD_EXECUTION" in objects
    assert "ACTUAL_DFM_MKC_VS_LAMBDA_CDM_COMPARISON" in objects
    assert "OUT_OF_SAMPLE_REJECTION_OR_VALIDATION_CERTIFICATE" in objects

def test_execution_is_blocked_by_missing_payloads():
    data = json.loads(ARTIFACT.read_text())
    missing = set(data["terminal_missing_payloads"])
    assert "SHA-256 digests" in missing
    assert "schema field paths" in missing
    assert "cross-covariance policy records" in missing
    assert "real data paths" in missing
    assert "executed likelihood outputs" in missing

def test_no_final_empirical_claim():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    for phrase in [
        "likelihood execution",
        "DFM-MKC versus Lambda-CDM comparison",
        "Lambda-CDM rejection",
        "DFM-MKC validation",
        "empirical validation",
        "any Clay problem",
    ]:
        assert phrase in data["does_not_prove"]
        assert phrase in doc
