from pathlib import Path
import importlib.util
import json
import subprocess
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_predicate_to_schema_validator_bridge_2026_05_21.json")
BRIDGE_MODULE = Path("tools/dfm_mkc_predicate_to_schema_validator_bridge.py")

def load_bridge():
    spec = importlib.util.spec_from_file_location("dfm_mkc_predicate_to_schema_validator_bridge", BRIDGE_MODULE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def valid_candidate():
    return {
        "data_vector": {
            "field": "data_vector",
            "source": "protocol_approved_data_vector_source",
            "kind": "one_dimensional_numeric_array",
            "nonempty": True,
            "finite_real_entries": True,
            "length_equals_mask_length": True,
            "length_equals_covariance_row_count": True,
            "freeze_lock_covered": True,
        },
        "covariance_matrix": {
            "field": "covariance_matrix",
            "source": "protocol_approved_covariance_source",
            "kind": "two_dimensional_numeric_matrix",
            "square": True,
            "finite_real_entries": True,
            "row_count_equals_data_vector_length": True,
            "column_count_equals_data_vector_length": True,
            "protocol_symmetric": True,
            "protocol_positive_semidefinite": True,
            "freeze_lock_covered": True,
        },
        "mask": {
            "field": "mask",
            "source": "protocol_approved_mask_source",
            "kind": "one_dimensional_boolean_array",
            "length_equals_data_vector_length": True,
            "has_active_entry": True,
            "masked_covariance_restriction_square": True,
            "freeze_lock_covered": True,
        },
        "likelihood_rule": {
            "field": "likelihood_rule",
            "rule_id": "protocol_likelihood_rule",
            "consumes": ("data_vector", "covariance_matrix", "mask"),
            "output_type": "protocol_likelihood_statistic",
            "frozen_by_protocol_hash": True,
        },
        "statistical_threshold": {
            "field": "statistical_threshold",
            "kind": "numeric_threshold",
            "finite": True,
            "comparison_direction": "<=",
            "frozen_by_protocol_hash": True,
        },
        "protocol_hash": {
            "field": "protocol_hash",
            "value": "frozen-protocol-hash-placeholder",
            "identifies_frozen_protocol_specification": True,
            "covers_required_material": True,
        },
        "actdr6_release_date": {
            "field": "actdr6_release_date",
            "iso_8601": True,
            "identifies_admitted_act_dr6_public_release_snapshot": True,
            "not_later_than_data_freeze_lock": True,
        },
        "data_freeze_lock": {
            "field": "data_freeze_lock",
            "identifies_frozen_admissible_payload": True,
            "records_timestamp_or_digest": True,
            "covers_required_fields": True,
        },
    }

def test_predicate_to_schema_validator_bridge_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_predicate_to_schema_validator_bridge.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DFM-MKC predicate-to-schema validator bridge verification OK." in result.stdout
    assert "PREDICATE_TO_SCHEMA_VALIDATOR_BRIDGE_ONLY_NO_AUTHENTIC_PAYLOAD_VALIDATION" in result.stdout

def test_bridge_accepts_complete_candidate_metadata():
    bridge = load_bridge()
    report = bridge.validate_candidate_metadata_schema(valid_candidate())
    assert report.accepted
    assert report.missing_fields == ()
    assert report.extra_fields == ()
    assert report.rejected_fields == ()

def test_bridge_rejects_missing_extra_and_failed_predicate_cases():
    bridge = load_bridge()

    missing = valid_candidate()
    missing.pop("mask")
    missing_report = bridge.validate_candidate_metadata_schema(missing)
    assert not missing_report.accepted
    assert "mask" in missing_report.missing_fields

    extra = valid_candidate()
    extra["unapproved_payload"] = {"field": "unapproved_payload"}
    extra_report = bridge.validate_candidate_metadata_schema(extra)
    assert not extra_report.accepted
    assert "unapproved_payload" in extra_report.extra_fields

    failed = valid_candidate()
    failed["data_vector"] = dict(failed["data_vector"])
    failed["data_vector"]["finite_real_entries"] = False
    failed_report = bridge.validate_candidate_metadata_schema(failed)
    assert not failed_report.accepted
    assert "data_vector" in failed_report.rejected_fields
    assert "all entries are finite real numbers" in failed_report.field_missing_predicates["data_vector"]

def test_artifact_preserves_boundary_and_nonclaims():
    data = json.loads(ARTIFACT.read_text())
    assert data["hard_blocker"] == "authentic ACT DR6 payload validation remains blocked"
    assert "validator bridge only" in data["boundary"]
    assert "does not validate authentic ACT DR6 payload bytes" in data["boundary"]
    assert "does not promote any empirical slot" in data["boundary"]
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
