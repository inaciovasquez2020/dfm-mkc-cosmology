#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

REQUIRED_FIELDS = (
    "data_vector",
    "covariance_matrix",
    "mask",
    "likelihood_rule",
    "statistical_threshold",
    "protocol_hash",
    "actdr6_release_date",
    "data_freeze_lock",
)

STATUS = "PREDICATE_IMPLEMENTATION_SURFACE_ONLY_NO_PAYLOAD_VALIDATION"

@dataclass(frozen=True)
class PredicateResult:
    field: str
    accepted: bool
    missing_predicates: tuple[str, ...]

def _truthy(record: dict[str, Any], key: str) -> bool:
    return bool(record.get(key, False))

def _has_nonempty_string(record: dict[str, Any], key: str) -> bool:
    value = record.get(key)
    return isinstance(value, str) and bool(value.strip())

def _accepted_source(record: dict[str, Any], expected: str) -> bool:
    return record.get("source") == expected

def _all(record: dict[str, Any], checks: dict[str, Callable[[dict[str, Any]], bool]]) -> PredicateResult:
    missing = tuple(name for name, check in checks.items() if not check(record))
    return PredicateResult(
        field=str(record.get("field", "<missing-field-name>")),
        accepted=not missing,
        missing_predicates=missing,
    )

def accept_data_vector(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "data_vector",
        "field is bound to the protocol-approved data-vector source": lambda r: _accepted_source(r, "protocol_approved_data_vector_source"),
        "value is a one-dimensional numeric array": lambda r: r.get("kind") == "one_dimensional_numeric_array",
        "array is nonempty": lambda r: _truthy(r, "nonempty"),
        "all entries are finite real numbers": lambda r: _truthy(r, "finite_real_entries"),
        "length equals mask length": lambda r: _truthy(r, "length_equals_mask_length"),
        "length equals covariance_matrix row count": lambda r: _truthy(r, "length_equals_covariance_row_count"),
        "value is covered by data_freeze_lock": lambda r: _truthy(r, "freeze_lock_covered"),
    })

def accept_covariance_matrix(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "covariance_matrix",
        "field is bound to the protocol-approved covariance source": lambda r: _accepted_source(r, "protocol_approved_covariance_source"),
        "value is a two-dimensional numeric matrix": lambda r: r.get("kind") == "two_dimensional_numeric_matrix",
        "matrix is square": lambda r: _truthy(r, "square"),
        "all entries are finite real numbers": lambda r: _truthy(r, "finite_real_entries"),
        "row count equals data_vector length": lambda r: _truthy(r, "row_count_equals_data_vector_length"),
        "column count equals data_vector length": lambda r: _truthy(r, "column_count_equals_data_vector_length"),
        "matrix satisfies the protocol symmetry predicate": lambda r: _truthy(r, "protocol_symmetric"),
        "matrix satisfies the protocol positive-semidefinite predicate": lambda r: _truthy(r, "protocol_positive_semidefinite"),
        "value is covered by data_freeze_lock": lambda r: _truthy(r, "freeze_lock_covered"),
    })

def accept_mask(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "mask",
        "field is bound to the protocol-approved mask source": lambda r: _accepted_source(r, "protocol_approved_mask_source"),
        "value is a one-dimensional boolean or zero-one array": lambda r: r.get("kind") in {"one_dimensional_boolean_array", "one_dimensional_zero_one_array"},
        "length equals data_vector length": lambda r: _truthy(r, "length_equals_data_vector_length"),
        "at least one entry is active": lambda r: _truthy(r, "has_active_entry"),
        "masked covariance restriction remains square": lambda r: _truthy(r, "masked_covariance_restriction_square"),
        "value is covered by data_freeze_lock": lambda r: _truthy(r, "freeze_lock_covered"),
    })

def accept_likelihood_rule(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "likelihood_rule",
        "field identifies the exact protocol likelihood rule": lambda r: _has_nonempty_string(r, "rule_id"),
        "rule consumes data_vector, covariance_matrix, and mask": lambda r: tuple(r.get("consumes", ())) == ("data_vector", "covariance_matrix", "mask"),
        "rule output type is the protocol likelihood statistic": lambda r: r.get("output_type") == "protocol_likelihood_statistic",
        "rule version is frozen by protocol_hash": lambda r: _truthy(r, "frozen_by_protocol_hash"),
    })

def accept_statistical_threshold(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "statistical_threshold",
        "threshold is numeric": lambda r: r.get("kind") == "numeric_threshold",
        "threshold is finite": lambda r: _truthy(r, "finite"),
        "threshold comparison direction is specified": lambda r: r.get("comparison_direction") in {"<", "<=", ">", ">="},
        "threshold is frozen by protocol_hash": lambda r: _truthy(r, "frozen_by_protocol_hash"),
    })

def accept_protocol_hash(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "protocol_hash",
        "hash is a nonempty string": lambda r: _has_nonempty_string(r, "value"),
        "hash identifies the frozen protocol specification": lambda r: _truthy(r, "identifies_frozen_protocol_specification"),
        "hash covers field keys, field sources, acceptance predicates, likelihood_rule, statistical_threshold, and data_freeze_lock": lambda r: _truthy(r, "covers_required_material"),
    })

def accept_actdr6_release_date(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "actdr6_release_date",
        "date is ISO-8601 formatted": lambda r: _truthy(r, "iso_8601"),
        "date identifies the ACT DR6 public-release snapshot admitted by the protocol": lambda r: _truthy(r, "identifies_admitted_act_dr6_public_release_snapshot"),
        "date is not later than data_freeze_lock timestamp": lambda r: _truthy(r, "not_later_than_data_freeze_lock"),
    })

def accept_data_freeze_lock(record: dict[str, Any]) -> PredicateResult:
    return _all(record, {
        "field is present": lambda r: r.get("field") == "data_freeze_lock",
        "lock identifies the frozen admissible payload": lambda r: _truthy(r, "identifies_frozen_admissible_payload"),
        "lock records timestamp or immutable content digest": lambda r: _truthy(r, "records_timestamp_or_digest"),
        "lock covers data_vector, covariance_matrix, mask, likelihood_rule, statistical_threshold, protocol_hash, and actdr6_release_date": lambda r: _truthy(r, "covers_required_fields"),
    })

ACCEPTANCE_PREDICATES = {
    "data_vector": accept_data_vector,
    "covariance_matrix": accept_covariance_matrix,
    "mask": accept_mask,
    "likelihood_rule": accept_likelihood_rule,
    "statistical_threshold": accept_statistical_threshold,
    "protocol_hash": accept_protocol_hash,
    "actdr6_release_date": accept_actdr6_release_date,
    "data_freeze_lock": accept_data_freeze_lock,
}

def evaluate_candidate_field_map(candidate: dict[str, dict[str, Any]]) -> dict[str, PredicateResult]:
    return {field: ACCEPTANCE_PREDICATES[field](candidate.get(field, {})) for field in REQUIRED_FIELDS}

def candidate_accepted(candidate: dict[str, dict[str, Any]]) -> bool:
    return all(result.accepted for result in evaluate_candidate_field_map(candidate).values())
