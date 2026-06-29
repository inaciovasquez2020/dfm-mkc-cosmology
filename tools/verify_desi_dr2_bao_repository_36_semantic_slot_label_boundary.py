#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_repository_36_semantic_slot_label_boundary_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_repository_36_semantic_slot_label_boundary_2026_06_29.json")

for required in [
    Path("artifacts/external_validation/desi_dr2_bao_repository_36_slot_manifest_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_candidate_index_map_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_adapter_contract_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_audit_2026_06_29.json"),
    Path("artifacts/external_validation/observed_desi_dr2_bao_numeric_order_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/frozen_dfm_mkc_prediction_vector_desi_order_2026_06_29.json"),
    Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json"),
]:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

data = json.loads(artifact_path.read_text())

if data.get("artifact") != "desi_dr2_bao_repository_36_semantic_slot_label_boundary":
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_repository_36_semantic_slot_label_boundary")

target = data.get("repository_target_order", {})
if target.get("required_vector_length") != 36:
    raise SystemExit("MISSING_OBJECT := required_vector_length_36")
if target.get("required_covariance_shape") != [36, 36]:
    raise SystemExit("MISSING_OBJECT := required_covariance_shape_36x36")
if target.get("same_order_required") is not True:
    raise SystemExit("MISSING_OBJECT := same_order_required")

contract = data.get("semantic_slot_label_contract", {})
requirements = contract.get("slot_label_requirements", [])

if contract.get("slot_count") != 36:
    raise SystemExit("MISSING_OBJECT := slot_count_36")
if contract.get("resolved_slot_label_count") != 0:
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := resolved_slot_label_count")
if contract.get("unresolved_slot_label_count") != 36:
    raise SystemExit("MISSING_OBJECT := unresolved_slot_label_count_36")
if len(requirements) != 36:
    raise SystemExit("MISSING_OBJECT := 36_slot_label_requirements")

required_fields = {
    "observable_family",
    "redshift_or_effective_redshift",
    "observable_quantity",
    "tracer_or_sample",
    "source_component_id",
    "source_component_offset",
    "source_mean_file",
    "source_covariance_file",
}

seen = set()
for expected_idx, req in enumerate(requirements):
    idx = req.get("repository_slot_index")
    if idx != expected_idx:
        raise SystemExit(f"MISSING_OBJECT := contiguous_repository_slot_index::{expected_idx}")
    if idx in seen:
        raise SystemExit("MISSING_OBJECT := unique_repository_slot_index")
    seen.add(idx)

    if set(req.get("required_semantic_fields", [])) != required_fields:
        raise SystemExit(f"MISSING_OBJECT := required_semantic_fields::{idx}")
    if req.get("semantic_label_status") != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := semantic_label_status::{idx}")
    if req.get("semantic_label_value") != "unresolved":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := semantic_label_value::{idx}")
    if req.get("source_mapping_status") != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := source_mapping_status::{idx}")
    if req.get("source_mapping_value") != "unresolved":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := source_mapping_value::{idx}")
    if req.get("no_invented_label_allowed") is not True:
        raise SystemExit(f"MISSING_OBJECT := no_invented_label_allowed::{idx}")

status = data.get("status", {})
expected_blocked = [
    "semantic_slot_labels",
    "source_authority_for_labels",
    "candidate_to_repository_index_map",
    "observed_numeric_pin",
    "chi_squared_likelihood_closure",
]
for key in expected_blocked:
    if status.get(key) != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {key}")

for key in [
    "no_invented_slot_labels",
    "no_padding_or_duplication_allowed",
]:
    if status.get(key) is not True:
        raise SystemExit(f"MISSING_OBJECT := {key}")

blocked = set(data.get("blocked_objects", []))
required_blocked = {
    "DESI_DR2_BAO_repository_36_semantic_slot_labels",
    "DESI_DR2_BAO_authoritative_slot_label_source",
    "DESI_DR2_BAO_candidate_to_repository_36_semantic_index_map",
    "public_data/desi_dr2/observed_bao_vector_36.csv",
    "public_data/desi_dr2/observed_bao_covariance_36x36.csv",
    "covariance_bound_chi_squared_likelihood_verifier",
}
if blocked != required_blocked:
    raise SystemExit("MISSING_OBJECT := complete_blocked_objects")

for forbidden in [
    Path("public_data/desi_dr2/observed_bao_vector_36.csv"),
    Path("public_data/desi_dr2/observed_bao_covariance_36x36.csv"),
]:
    if forbidden.exists():
        raise SystemExit(f"CONDITIONAL := numeric_pin_exists::{forbidden}")

if data.get("next_weakest_missing_object") != "DESI_DR2_BAO_authoritative_slot_label_source":
    raise SystemExit("MISSING_OBJECT := DESI_DR2_BAO_authoritative_slot_label_source")

claims = data.get("claim_status", {})
required_claims = {
    "observed_numeric_pin",
    "chi_squared_likelihood_closure",
    "LCDM_refutation_claim",
    "DFM_MKC_cosmology_validation_claim",
    "strict_w0wa_schema_constraint",
}
if set(claims) != required_claims:
    raise SystemExit("MISSING_OBJECT := complete_claim_status")
for claim, value in claims.items():
    if value != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {claim}")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_observed_DESI_DR2_BAO_numeric_pin",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
}
if set(data.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

print("DESI_DR2_BAO_REPOSITORY_36_SEMANTIC_SLOT_LABEL_BOUNDARY_OK")
print("REPOSITORY_SLOT_COUNT := 36")
print("RESOLVED_SLOT_LABEL_COUNT := 0")
print("UNRESOLVED_SLOT_LABEL_COUNT := 36")
print("NEXT_MISSING_OBJECT := DESI_DR2_BAO_authoritative_slot_label_source")
