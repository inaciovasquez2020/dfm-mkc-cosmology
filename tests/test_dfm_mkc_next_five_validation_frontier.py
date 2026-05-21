from pathlib import Path
import json
import subprocess
import sys

OBJECTS = [
    "authentic_payload_schema_validation_blocker_certificate",
    "authentic_payload_validation_target",
    "payload_field_binding_requirement_surface",
    "payload_digest_freeze_lock_target",
    "schema_validation_execution_gate",
]

def test_next_five_validation_frontier_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_next_five_validation_frontier.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DFM-MKC next five validation frontier verification OK." in result.stdout
    assert "Objects verified: 5" in result.stdout

def test_all_five_artifacts_exist_and_preserve_predecessor():
    for index, slug in enumerate(OBJECTS, start=1):
        path = Path(f"artifacts/repo_intake/dfm_mkc_{slug}_2026_05_21.json")
        assert path.exists()
        data = json.loads(path.read_text())
        assert data["object_index"] == index
        assert data["predecessor"]["pull_request"] == 103
        assert data["predecessor"]["merge_commit"] == "11a518b"
        assert data["predecessor"]["status"] == "PREDICATE_TO_SCHEMA_VALIDATOR_BRIDGE_ONLY_NO_AUTHENTIC_PAYLOAD_VALIDATION"

def test_required_protocol_fields_are_preserved_in_all_objects():
    expected = [
        "data_vector",
        "covariance_matrix",
        "mask",
        "likelihood_rule",
        "statistical_threshold",
        "protocol_hash",
        "actdr6_release_date",
        "data_freeze_lock",
    ]
    for slug in OBJECTS:
        data = json.loads(Path(f"artifacts/repo_intake/dfm_mkc_{slug}_2026_05_21.json").read_text())
        assert data["required_fields"] == expected

def test_boundaries_and_nonclaims_are_preserved_in_all_objects():
    for slug in OBJECTS:
        data = json.loads(Path(f"artifacts/repo_intake/dfm_mkc_{slug}_2026_05_21.json").read_text())
        assert "frontier object only" in data["boundary"]
        assert "does not validate authentic ACT DR6 payload bytes" in data["boundary"]
        assert "does not extract a numerical data vector" in data["boundary"]
        assert "does not extract a covariance matrix" in data["boundary"]
        assert "does not execute the likelihood" in data["boundary"]
        assert "does not supply evidence" in data["boundary"]
        assert "does not promote any empirical slot" in data["boundary"]
        assert "DFM-MKC" in data["does_not_prove"]
        assert "Lambda-CDM failure" in data["does_not_prove"]
        assert "ACT/DES holdout survival" in data["does_not_prove"]
        assert "independent empirical validation" in data["does_not_prove"]
        assert "any Clay problem" in data["does_not_prove"]
