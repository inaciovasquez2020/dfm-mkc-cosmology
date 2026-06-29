#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_repository_36_authoritative_slot_label_source_search_audit_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_repository_36_authoritative_slot_label_source_search_audit_2026_06_29.json")

required_inputs = [
    Path("artifacts/external_validation/desi_dr2_bao_full_remaining_claim_blocker_rollup_2026_06_29.json"),
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

if data.get("artifact") != "desi_dr2_bao_repository_36_authoritative_slot_label_source_search_audit":
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_repository_36_authoritative_slot_label_source_search_audit")

if data.get("input_rollup") != "desi_dr2_bao_full_remaining_claim_blocker_rollup_2026_06_29":
    raise SystemExit("MISSING_OBJECT := input_rollup")
if data.get("input_source_boundary") != "desi_dr2_bao_authoritative_slot_label_source_boundary_2026_06_29":
    raise SystemExit("MISSING_OBJECT := input_source_boundary")

if data.get("search_scope_count") != 3:
    raise SystemExit("MISSING_OBJECT := search_scope_count_3")
scopes = data.get("search_scopes", [])
if len(scopes) != 3:
    raise SystemExit("MISSING_OBJECT := three_search_scopes")
scope_ids = {s.get("scope_id") for s in scopes}
required_scope_ids = {
    "current_repository_external_validation_artifacts",
    "current_repository_public_data_desi_dr2_if_present",
    "CobayaSampler_bao_data_desi_bao_dr2",
}
if scope_ids != required_scope_ids:
    raise SystemExit("MISSING_OBJECT := required_search_scopes")

inventory = data.get("candidate_source_inventory", {})
if inventory.get("candidate_component_count") != 8:
    raise SystemExit("MISSING_OBJECT := candidate_component_count_8")
if inventory.get("candidate_numeric_row_count") != 26:
    raise SystemExit("MISSING_OBJECT := candidate_numeric_row_count_26")
if inventory.get("required_candidate_source_file_count") != 16:
    raise SystemExit("MISSING_OBJECT := required_candidate_source_file_count_16")
if inventory.get("candidate_source_files_all_present_in_search_clone") is not True:
    raise SystemExit("MISSING_OBJECT := candidate_source_files_all_present_in_search_clone")

result = data.get("authoritative_36_slot_label_source_search_result", {})
if result.get("status") != "not_found":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := authoritative_36_slot_label_source_found")
if result.get("accepted_authoritative_source_count") != 0:
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := accepted_authoritative_source_count")
if result.get("candidate_rows_available") != 26:
    raise SystemExit("MISSING_OBJECT := candidate_rows_available_26")
if result.get("repository_slots_required") != 36:
    raise SystemExit("MISSING_OBJECT := repository_slots_required_36")
if result.get("resolved_repository_slot_label_count") != 0:
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := resolved_repository_slot_label_count")
if result.get("unresolved_repository_slot_label_count") != 36:
    raise SystemExit("MISSING_OBJECT := unresolved_repository_slot_label_count_36")

expected_blockers = {
    "DESI_DR2_BAO_repository_36_authoritative_slot_label_source",
    "DESI_DR2_BAO_repository_36_semantic_slot_labels",
    "DESI_DR2_BAO_candidate_to_repository_36_semantic_index_map",
    "exact_DESI_DR2_BAO_36_vector_and_36x36_covariance_pair",
    "public_data/desi_dr2/observed_bao_vector_36.csv",
    "public_data/desi_dr2/observed_bao_covariance_36x36.csv",
    "observed_DESI_DR2_BAO_numeric_data_vector_and_covariance_matrix_with_same_order",
    "non-diagnostic_DFM_MKC_prediction_vector_bound_to_same_36_order",
    "covariance_bound_chi_squared_likelihood_verifier",
    "preregistered_decision_rule",
    "strict_w0wa_schema_constraint",
    "LCDM_refutation_claim",
    "DFM_MKC_cosmology_validation_claim",
}
if set(data.get("preserved_blockers", [])) != expected_blockers:
    raise SystemExit("MISSING_OBJECT := preserved_13_blockers")

for forbidden_path in [
    Path("public_data/desi_dr2/observed_bao_vector_36.csv"),
    Path("public_data/desi_dr2/observed_bao_covariance_36x36.csv"),
]:
    if forbidden_path.exists():
        raise SystemExit(f"CONDITIONAL := forbidden_numeric_file_exists::{forbidden_path}")

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

claims = data.get("claim_status", {})
expected_claims = {
    "observed_numeric_pin",
    "chi_squared_likelihood_closure",
    "strict_w0wa_schema_constraint",
    "LCDM_refutation_claim",
    "DFM_MKC_cosmology_validation_claim",
}
if set(claims) != expected_claims:
    raise SystemExit("MISSING_OBJECT := complete_claim_status")
for claim, status in claims.items():
    if status != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {claim}")

if data.get("next_weakest_missing_object") != "external_authoritative_DESI_DR2_BAO_36_slot_label_source_or_repository_target_order_revision":
    raise SystemExit("MISSING_OBJECT := external_authoritative_DESI_DR2_BAO_36_slot_label_source_or_repository_target_order_revision")

stop = data.get("good_stopping_point", {})
if stop.get("status") != "yes_after_merge_and_main_push_ci_success":
    raise SystemExit("MISSING_OBJECT := good_stopping_point")
if "external authoritative data/schema input" not in stop.get("reason", ""):
    raise SystemExit("MISSING_OBJECT := stopping_reason_external_input")

print("DESI_DR2_BAO_REPOSITORY_36_AUTHORITATIVE_SLOT_LABEL_SOURCE_SEARCH_AUDIT_OK")
print("SEARCH_SCOPE_COUNT := 3")
print("CANDIDATE_COMPONENT_COUNT := 8")
print("CANDIDATE_NUMERIC_ROW_COUNT := 26")
print("ACCEPTED_AUTHORITATIVE_SOURCE_COUNT := 0")
print("NEXT_MISSING_OBJECT := external_authoritative_DESI_DR2_BAO_36_slot_label_source_or_repository_target_order_revision")
print("GOOD_STOPPING_POINT := after_merge_and_main_push_ci_success")
