#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_full_remaining_claim_blocker_rollup_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_full_remaining_claim_blocker_rollup_2026_06_29.json")

required_inputs = [
    Path("artifacts/external_validation/desi_dr2_bao_authoritative_slot_label_source_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_repository_36_semantic_slot_label_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_repository_36_slot_manifest_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_candidate_index_map_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_adapter_contract_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_audit_2026_06_29.json"),
    Path("artifacts/external_validation/observed_desi_dr2_bao_numeric_order_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/frozen_dfm_mkc_prediction_vector_desi_order_2026_06_29.json"),
    Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json"),
    Path("artifacts/external_validation/cosmology_claim_strength_internal_2026_06_29.json"),
    Path("artifacts/external_validation/cosmology_claim_readiness_gate_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_input_packet_2026_06_29.json"),
]
for required in required_inputs:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

data = json.loads(artifact_path.read_text())

if data.get("artifact") != "desi_dr2_bao_full_remaining_claim_blocker_rollup":
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_full_remaining_claim_blocker_rollup")

expected_completed = {
    "DESI_DR2_BAO_INPUT_PACKET_OK",
    "COSMOLOGY_CLAIM_READINESS_GATE_OK",
    "COSMOLOGY_CLAIM_STRENGTH_INTERNAL_OK",
    "COVARIANCE_ORDERED_PREDICTION_RESIDUAL_ADAPTER_OK",
    "FROZEN_DFM_MKC_PREDICTION_VECTOR_DESI_ORDER_OK",
    "OBSERVED_DESI_DR2_BAO_NUMERIC_ORDER_BOUNDARY_OK",
    "DESI_DR2_BAO_CANDIDATE_SHAPE_AUDIT_OK",
    "DESI_DR2_BAO_CANDIDATE_SHAPE_ADAPTER_CONTRACT_OK",
    "DESI_DR2_BAO_CANDIDATE_INDEX_MAP_BOUNDARY_OK",
    "DESI_DR2_BAO_REPOSITORY_36_SLOT_MANIFEST_BOUNDARY_OK",
    "DESI_DR2_BAO_REPOSITORY_36_SEMANTIC_SLOT_LABEL_BOUNDARY_OK",
    "DESI_DR2_BAO_AUTHORITATIVE_SLOT_LABEL_SOURCE_BOUNDARY_OK",
}
if set(data.get("completed_support_objects", [])) != expected_completed:
    raise SystemExit("MISSING_OBJECT := completed_support_objects")

remaining = data.get("remaining_objects", [])
if data.get("remaining_object_count") != 13 or len(remaining) != 13:
    raise SystemExit("MISSING_OBJECT := remaining_object_count_13")

expected_remaining = {
    "DESI_DR2_BAO_repository_36_authoritative_slot_label_source": "still_missing",
    "DESI_DR2_BAO_repository_36_semantic_slot_labels": "unresolved",
    "DESI_DR2_BAO_candidate_to_repository_36_semantic_index_map": "blocked",
    "exact_DESI_DR2_BAO_36_vector_and_36x36_covariance_pair": "missing",
    "public_data/desi_dr2/observed_bao_vector_36.csv": "missing",
    "public_data/desi_dr2/observed_bao_covariance_36x36.csv": "missing",
    "observed_DESI_DR2_BAO_numeric_data_vector_and_covariance_matrix_with_same_order": "missing",
    "non-diagnostic_DFM_MKC_prediction_vector_bound_to_same_36_order": "not_done",
    "covariance_bound_chi_squared_likelihood_verifier": "missing",
    "preregistered_decision_rule": "missing",
    "strict_w0wa_schema_constraint": "blocked",
    "LCDM_refutation_claim": "blocked",
    "DFM_MKC_cosmology_validation_claim": "blocked",
}

seen = {}
for item in remaining:
    obj = item.get("object")
    status = item.get("status")
    ordinal = item.get("ordinal")
    if obj in seen:
        raise SystemExit(f"MISSING_OBJECT := unique_remaining_object::{obj}")
    seen[obj] = item
    if obj not in expected_remaining:
        raise SystemExit(f"UNEXPECTED_OBJECT := {obj}")
    if status != expected_remaining[obj]:
        raise SystemExit(f"UNSUPPORTED_STATUS := {obj}::{status}")
    if not isinstance(ordinal, int) or ordinal < 1 or ordinal > 13:
        raise SystemExit(f"MISSING_OBJECT := ordinal_1_to_13::{obj}")

if set(seen) != set(expected_remaining):
    missing = sorted(set(expected_remaining) - set(seen))
    raise SystemExit(f"MISSING_OBJECT := complete_remaining_object_set::{missing}")

expected_ordinals = list(range(1, 14))
actual_ordinals = [item.get("ordinal") for item in remaining]
if actual_ordinals != expected_ordinals:
    raise SystemExit("MISSING_OBJECT := contiguous_ordinals_1_to_13")

for object_name in [
    "public_data/desi_dr2/observed_bao_vector_36.csv",
    "public_data/desi_dr2/observed_bao_covariance_36x36.csv",
]:
    path = Path(object_name)
    if path.exists():
        raise SystemExit(f"CONDITIONAL := forbidden_placeholder_numeric_file_exists::{object_name}")

for missing_file in data.get("missing_files", []):
    if Path(missing_file).exists():
        raise SystemExit(f"CONDITIONAL := missing_file_now_exists::{missing_file}")

forbidden = data.get("forbidden_side_effects", {})
for key in [
    "must_not_invent_repository_36_slot_labels",
    "must_not_pad_or_duplicate_26_candidate_rows_to_36",
    "must_not_create_placeholder_observed_vector",
    "must_not_create_placeholder_observed_covariance",
    "must_not_enable_lcdm_refutation_claim",
    "must_not_enable_dfm_mkc_cosmology_validation_claim",
]:
    if forbidden.get(key) is not True:
        raise SystemExit(f"MISSING_OBJECT := forbidden_side_effect::{key}")

blocked_claims = data.get("blocked_claims", {})
expected_blocked_claims = {
    "observed_numeric_pin",
    "chi_squared_likelihood_closure",
    "strict_w0wa_schema_constraint",
    "LCDM_refutation_claim",
    "DFM_MKC_cosmology_validation_claim",
}
if set(blocked_claims) != expected_blocked_claims:
    raise SystemExit("MISSING_OBJECT := complete_blocked_claims")
for claim, status in blocked_claims.items():
    if status != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {claim}")

if data.get("next_weakest_missing_object") != "DESI_DR2_BAO_repository_36_authoritative_slot_label_source_search_audit":
    raise SystemExit("MISSING_OBJECT := DESI_DR2_BAO_repository_36_authoritative_slot_label_source_search_audit")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_observed_DESI_DR2_BAO_numeric_pin",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
}
if set(data.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

print("DESI_DR2_BAO_FULL_REMAINING_CLAIM_BLOCKER_ROLLUP_OK")
print("REMAINING_OBJECT_COUNT := 13")
print("BLOCKED_CLAIM_COUNT := 5")
print("NEXT_MISSING_OBJECT := DESI_DR2_BAO_repository_36_authoritative_slot_label_source_search_audit")
