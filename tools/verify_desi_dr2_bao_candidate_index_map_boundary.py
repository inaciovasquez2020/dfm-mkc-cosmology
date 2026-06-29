#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_candidate_index_map_boundary_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_candidate_index_map_boundary_2026_06_29.json")

for required in [
    Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_adapter_contract_2026_06_29.json"),
    Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_audit_2026_06_29.json"),
    Path("artifacts/external_validation/observed_desi_dr2_bao_numeric_order_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/frozen_dfm_mkc_prediction_vector_desi_order_2026_06_29.json"),
    Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json"),
]:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

data = json.loads(artifact_path.read_text())

if data.get("artifact") != "desi_dr2_bao_candidate_index_map_boundary":
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_candidate_index_map_boundary")

source = data.get("candidate_source_order", {})
segments = source.get("source_order_segments", [])

if source.get("component_count") != 8:
    raise SystemExit("MISSING_OBJECT := source_component_count_8")
if source.get("total_observable_length") != 26:
    raise SystemExit("MISSING_OBJECT := source_observable_length_26")
if len(segments) != 8:
    raise SystemExit("MISSING_OBJECT := source_order_segments_8")

expected_start = 0
seen = set()
computed_total = 0
for segment in segments:
    cid = segment.get("component_id")
    if not cid or cid in seen:
        raise SystemExit("MISSING_OBJECT := unique_component_id")
    seen.add(cid)

    start = segment.get("source_offset_start_in_candidate_26_order")
    stop = segment.get("source_offset_stop_exclusive_in_candidate_26_order")
    length = segment.get("observable_length")

    if start != expected_start:
        raise SystemExit(f"MISSING_OBJECT := contiguous_source_start::{cid}")
    if stop != start + length:
        raise SystemExit(f"MISSING_OBJECT := contiguous_source_stop::{cid}")
    if not isinstance(length, int) or length <= 0:
        raise SystemExit(f"MISSING_OBJECT := positive_observable_length::{cid}")
    if not segment.get("source_mean_sha256") or not segment.get("source_covariance_sha256"):
        raise SystemExit(f"MISSING_OBJECT := source_hashes::{cid}")

    expected_start = stop
    computed_total += length

if computed_total != 26 or expected_start != 26:
    raise SystemExit("MISSING_OBJECT := contiguous_candidate_26_order")

target = data.get("repository_target_order", {})
if target.get("required_vector_length") != 36:
    raise SystemExit("MISSING_OBJECT := repository_required_vector_length_36")
if target.get("required_covariance_shape") != [36, 36]:
    raise SystemExit("MISSING_OBJECT := repository_required_covariance_shape_36x36")
if target.get("same_order_required") is not True:
    raise SystemExit("MISSING_OBJECT := same_order_required")

index_status = data.get("index_map_status", {})
if index_status.get("candidate_to_repository_36_index_map") != "blocked":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := candidate_to_repository_36_index_map")
if index_status.get("candidate_source_length") != 26:
    raise SystemExit("MISSING_OBJECT := candidate_source_length_26")
if index_status.get("repository_target_length") != 36:
    raise SystemExit("MISSING_OBJECT := repository_target_length_36")
if index_status.get("length_gap") != 10:
    raise SystemExit("MISSING_OBJECT := length_gap_10")
if index_status.get("no_padding_or_duplication_allowed") is not True:
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := padding_or_duplication")
if index_status.get("no_semantic_observable_slot_manifest") is not True:
    raise SystemExit("MISSING_OBJECT := no_semantic_observable_slot_manifest")
if index_status.get("no_numeric_pin") is not True:
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := numeric_pin")

blocked = set(data.get("blocked_objects", []))
required_blocked = {
    "public_data/desi_dr2/observed_bao_vector_36.csv",
    "public_data/desi_dr2/observed_bao_covariance_36x36.csv",
    "DESI_DR2_BAO_candidate_to_repository_36_semantic_index_map",
    "DESI_DR2_BAO_repository_36_observable_slot_manifest",
}
if blocked != required_blocked:
    raise SystemExit("MISSING_OBJECT := complete_blocked_objects")

for forbidden in [
    Path("public_data/desi_dr2/observed_bao_vector_36.csv"),
    Path("public_data/desi_dr2/observed_bao_covariance_36x36.csv"),
]:
    if forbidden.exists():
        raise SystemExit(f"CONDITIONAL := numeric_pin_exists::{forbidden}")

if data.get("next_weakest_missing_object") != "DESI_DR2_BAO_repository_36_observable_slot_manifest":
    raise SystemExit("MISSING_OBJECT := DESI_DR2_BAO_repository_36_observable_slot_manifest")

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
for claim, status in claims.items():
    if status != "blocked":
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

print("DESI_DR2_BAO_CANDIDATE_INDEX_MAP_BOUNDARY_OK")
print("SOURCE_COMPONENT_COUNT := 8")
print("SOURCE_OBSERVABLE_LENGTH := 26")
print("REPOSITORY_TARGET_LENGTH := 36")
print("LENGTH_GAP := 10")
print("NEXT_MISSING_OBJECT := DESI_DR2_BAO_repository_36_observable_slot_manifest")
