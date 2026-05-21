from pathlib import Path
import json
import subprocess
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_minimal_schema_validation_requirement_target_2026_05_21.json")

def test_minimal_schema_validation_requirement_target_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_minimal_schema_validation_requirement_target.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DFM-MKC minimal schema-validation requirement target verification OK." in result.stdout
    assert "REQUIREMENT_TARGET_ONLY_ACCEPTANCE_PREDICATES_NOT_IMPLEMENTED" in result.stdout

def test_required_acceptance_predicate_fields_are_exact():
    data = json.loads(ARTIFACT.read_text())
    target = data["minimal_schema_validation_requirement_target"]
    assert target["required_protocol_fields"] == [
        "data_vector",
        "covariance_matrix",
        "mask",
        "likelihood_rule",
        "statistical_threshold",
        "protocol_hash",
        "actdr6_release_date",
        "data_freeze_lock",
    ]
    assert set(target["acceptance_predicates"]) == set(target["required_protocol_fields"])

def test_boundary_preserves_no_evidence_and_no_promotion():
    data = json.loads(ARTIFACT.read_text())
    assert data["hard_blocker"] == "schema validation remains blocked"
    assert "acceptance predicates specified but not implemented as schema validation" in data["boundary"]
    assert "no evidence supplied" in data["boundary"]
    assert "no slot promoted" in data["boundary"]
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
