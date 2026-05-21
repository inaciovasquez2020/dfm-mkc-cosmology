#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_predicate_to_schema_validator_bridge_2026_05_21.json")
STATUS_DOC = Path("docs/status/DFM_MKC_PREDICATE_TO_SCHEMA_VALIDATOR_BRIDGE_2026_05_21.md")
BRIDGE_MODULE = Path("tools/dfm_mkc_predicate_to_schema_validator_bridge.py")

REQUIRED_FIELDS = [
    "data_vector",
    "covariance_matrix",
    "mask",
    "likelihood_rule",
    "statistical_threshold",
    "protocol_hash",
    "actdr6_release_date",
    "data_freeze_lock",
]

REQUIRED_BOUNDARIES = [
    "validator bridge only",
    "validates candidate metadata against implemented acceptance predicates",
    "does not validate authentic ACT DR6 payload bytes",
    "does not extract a numerical data vector",
    "does not extract a covariance matrix",
    "does not execute the likelihood",
    "does not supply evidence",
    "does not promote any empirical slot",
]

REQUIRED_NONCLAIMS = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

def load_bridge():
    spec = importlib.util.spec_from_file_location("dfm_mkc_predicate_to_schema_validator_bridge", BRIDGE_MODULE)
    if spec is None or spec.loader is None:
        fail("could not load bridge module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def valid_candidate() -> dict[str, dict[str, object]]:
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

def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing artifact: {ARTIFACT}")
    if not STATUS_DOC.exists():
        fail(f"missing status doc: {STATUS_DOC}")
    if not BRIDGE_MODULE.exists():
        fail(f"missing bridge module: {BRIDGE_MODULE}")

    artifact = json.loads(ARTIFACT.read_text())
    status_text = STATUS_DOC.read_text()
    bridge = load_bridge()

    if artifact.get("status") != "PREDICATE_TO_SCHEMA_VALIDATOR_BRIDGE_ONLY_NO_AUTHENTIC_PAYLOAD_VALIDATION":
        fail("unexpected artifact status")
    if artifact.get("hard_blocker") != "authentic ACT DR6 payload validation remains blocked":
        fail("hard blocker changed")
    if list(bridge.REQUIRED_FIELDS) != REQUIRED_FIELDS:
        fail("bridge required fields mismatch")

    accepted_report = bridge.validate_candidate_metadata_schema(valid_candidate())
    if not accepted_report.accepted:
        fail("valid candidate metadata was not accepted")

    missing_candidate = valid_candidate()
    missing_candidate.pop("mask")
    missing_report = bridge.validate_candidate_metadata_schema(missing_candidate)
    if missing_report.accepted:
        fail("candidate with missing field was accepted")
    if "mask" not in missing_report.missing_fields:
        fail("missing mask was not reported")

    extra_candidate = valid_candidate()
    extra_candidate["unapproved_payload"] = {"field": "unapproved_payload"}
    extra_report = bridge.validate_candidate_metadata_schema(extra_candidate)
    if extra_report.accepted:
        fail("candidate with extra field was accepted")
    if "unapproved_payload" not in extra_report.extra_fields:
        fail("extra field was not reported")

    invalid_candidate = valid_candidate()
    invalid_candidate["data_vector"] = dict(invalid_candidate["data_vector"])
    invalid_candidate["data_vector"]["finite_real_entries"] = False
    invalid_report = bridge.validate_candidate_metadata_schema(invalid_candidate)
    if invalid_report.accepted:
        fail("candidate with failed predicate was accepted")
    if "data_vector" not in invalid_report.rejected_fields:
        fail("rejected data_vector was not reported")
    if "all entries are finite real numbers" not in invalid_report.field_missing_predicates["data_vector"]:
        fail("failed finite-real predicate was not reported")

    for field in REQUIRED_FIELDS:
        if field not in artifact.get("validated_fields", []):
            fail(f"missing validated field in artifact: {field}")
        if field not in status_text:
            fail(f"missing field in status doc: {field}")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in artifact.get("boundary", []):
            fail(f"missing artifact boundary: {boundary}")
        if boundary not in status_text:
            fail(f"missing status boundary: {boundary}")

    for nonclaim in REQUIRED_NONCLAIMS:
        if nonclaim not in artifact.get("does_not_prove", []):
            fail(f"missing artifact nonclaim: {nonclaim}")
        if nonclaim not in status_text:
            fail(f"missing status nonclaim: {nonclaim}")

    print("DFM-MKC predicate-to-schema validator bridge verification OK.")
    print(f"Status: {artifact['status']}")
    print(f"Validated fields: {', '.join(REQUIRED_FIELDS)}")

if __name__ == "__main__":
    main()
