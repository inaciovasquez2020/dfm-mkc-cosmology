import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_dark_sector_closed_object_target_packet_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_DARK_SECTOR_CLOSED_OBJECT_TARGET_PACKET_2026_05_27.md")

def data():
    return json.loads(ART.read_text())

def test_status_is_target_packet_only():
    assert data()["status"] == "TARGET_PACKET_ONLY_OBJECTS_NOT_SUPPLIED"

def test_all_five_next_objects_are_targeted():
    ids = {target["id"] for target in data()["target_objects"]}
    assert ids == {
        "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1",
        "DFM_MKC_FIELD_EQUATIONS_V1",
        "DFM_MKC_MATTER_COUPLING_RULE_V1",
        "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
        "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
    }

def test_each_target_remains_missing_object_only():
    for target in data()["target_objects"]:
        assert target["status"] == "MISSING_OBJECT_TARGET_ONLY"
        assert target["required_contents"]
        assert target["acceptance_test"]

def test_packet_acceptance_rule_blocks_premature_validation_claims():
    rule = data()["packet_acceptance_rule"]
    assert rule["all_targets_must_be_supplied_before_validation_claim"] is True
    assert rule["no_single_target_promotes_empirical_status"] is True
    assert rule["requires_public_reproducible_code_before_experimental_claim"] is True
    assert rule["requires_blind_holdout_success_before_replacement_claim"] is True
    assert rule["requires_independent_reproduction_before_mainstream_replacement_claim"] is True

def test_boundary_blocks_overclaim():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC closed action functional" in blocked
    assert "DFM-MKC field equations" in blocked
    assert "DFM-MKC matter coupling law" in blocked
    assert "DFM-MKC linear perturbation system" in blocked
    assert "DFM-MKC ACT Planck DESI prediction vector" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "dark matter is a phase" in blocked
    assert "any Clay problem" in blocked

def test_doc_contains_targets_and_boundaries():
    text = DOC.read_text()
    assert "TARGET_PACKET_ONLY_OBJECTS_NOT_SUPPLIED" in text
    assert "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1" in text
    assert "DFM_MKC_FIELD_EQUATIONS_V1" in text
    assert "DFM_MKC_MATTER_COUPLING_RULE_V1" in text
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in text
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in text
    assert "Does not prove" in text
    assert "Dark matter replacement" in text
