#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_repository_36_slot_manifest_boundary_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_repository_36_slot_manifest_boundary_2026_06_29.json")

for required in [
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

if data.get("artifact") != "desi_dr2_bao_repository_36_observable_slot_manifest_boundary":
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_repository_36_observable_slot_manifest_boundary")

target = data.get("repository_target_order", {})
if target.get("required_vector_length") != 36:
    raise SystemExit("MISSING_OBJECT := required_vector_length_36")
if target.get("required_covariance_shape") != [36, 36]:
    raise SystemExit("MISSING_OBJECT := required_covariance_shape_36x36")
if target.get("same_order_required") is not True:
    raise SystemExit("MISSING_OBJECT := same_order_required")

manifest = data.get("repository_36_slot_manifest", {})
slots = manifest.get("slots", [])
if manifest.get("slot_count") != 36:
    raise SystemExit("MISSING_OBJECT := slot_count_36")
if manifest.get("slot_semantics_status") != "unresolved":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := resolved_slot_semantics")
if len(slots) != 36:
    raise SystemExit("MISSING_OBJECT := 36_repository_slots")

seen = set()
for expected_index, slot in enumerate(slots):
    idx = slot.get("repository_slot_index")
    if idx != expected_index:
        raise SystemExit(f"MISSING_OBJECT := contiguous_repository_slot_index::{expected_index}")
    if idx in seen:
        raise SystemExit("MISSING_OBJECT := unique_repository_slot_index")
    seen.add(idx)

    for key in [
        "semantic_observable_label",
        "source_component_id",
        "source_component_offset",
        "source_mean_file",
        "source_covariance_file",
    ]:
        if slot.get(key) != "unresolved":
            raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := resolved_{key}::{idx}")

    if slot.get("status") != "blocked_until_semantic_slot_label_and_source_mapping_are_supplied":
        raise SystemExit(f"MISSING_OBJECT := blocked_slot_status::{idx}")

context = data.get("candidate_source_context", {})
if context.get("candidate_component_count") != 8:
    raise SystemExit("MISSING_OBJECT := candidate_component_count_8")
if context.get("candidate_observable_length") != 26:
    raise SystemExit("MISSING_OBJECT := candidate_observable_length_26")
if context.get("repository_target_length") != 36:
    raise SystemExit("MISSING_OBJECT := repository_target_length_36")
if context.get("length_gap") != 10:
    raise SystemExit("MISSING_OBJECT := length_gap_10")
if context.get("candidate_to_repository_index_map_status") != "blocked":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := candidate_to_repository_index_map")

status = data.get("manifest_status", {})
expected_status = {
    "semantic_slot_labels": "blocked",
    "candidate_source_mapping": "blocked",
    "numeric_pin": "blocked",
}
for key, expected in expected_status.items():
    if status.get(key) != expected:
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {key}")

for key in [
    "no_padding_or_duplication_allowed",
    "no_invented_observable_labels",
    "no_chi_squared_likelihood_closure",
]:
    if status.get(key) is not True:
        raise SystemExit(f"MISSING_OBJECT := {key}")

blocked = set(data.get("blocked_objects", []))
required_blocked = {
    "DESI_DR2_BAO_repository_36_semantic_slot_labels",
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

if data.get("next_weakest_missing_object") != "DESI_DR2_BAO_repository_36_semantic_slot_labels":
    raise SystemExit("MISSING_OBJECT := DESI_DR2_BAO_repository_36_semantic_slot_labels")

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

print("DESI_DR2_BAO_REPOSITORY_36_SLOT_MANIFEST_BOUNDARY_OK")
print("REPOSITORY_SLOT_COUNT := 36")
print("SLOT_SEMANTICS_STATUS := unresolved")
print("CANDIDATE_SOURCE_LENGTH := 26")
print("REPOSITORY_TARGET_LENGTH := 36")
print("NEXT_MISSING_OBJECT := DESI_DR2_BAO_repository_36_semantic_slot_labels")
