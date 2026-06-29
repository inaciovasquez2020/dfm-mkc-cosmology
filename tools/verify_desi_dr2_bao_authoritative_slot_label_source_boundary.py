#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_authoritative_slot_label_source_boundary_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_authoritative_slot_label_source_boundary_2026_06_29.json")

for required in [
    Path("artifacts/external_validation/desi_dr2_bao_repository_36_semantic_slot_label_boundary_2026_06_29.json"),
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

if data.get("artifact") != "desi_dr2_bao_authoritative_slot_label_source_boundary":
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_authoritative_slot_label_source_boundary")

candidate = data.get("candidate_source_authority", {})
sources = candidate.get("candidate_sources", [])
if candidate.get("component_count") != 8:
    raise SystemExit("MISSING_OBJECT := candidate_component_count_8")
if candidate.get("candidate_numeric_row_count") != 26:
    raise SystemExit("MISSING_OBJECT := candidate_numeric_row_count_26")
if candidate.get("candidate_row_count_authority") != "candidate_shape_adapter_contract_observable_length":
    raise SystemExit("MISSING_OBJECT := candidate_row_count_authority")
if len(sources) != 8:
    raise SystemExit("MISSING_OBJECT := 8_candidate_sources")

seen = set()
computed_rows = 0
for source in sources:
    cid = source.get("component_id")
    if not cid or cid in seen:
        raise SystemExit("MISSING_OBJECT := unique_component_id")
    seen.add(cid)

    if not source.get("source_mean_file") or not source.get("source_covariance_file"):
        raise SystemExit(f"MISSING_OBJECT := source_files::{cid}")
    if not source.get("source_mean_sha256") or not source.get("source_covariance_sha256"):
        raise SystemExit(f"MISSING_OBJECT := source_sha256::{cid}")

    row_count = source.get("candidate_numeric_row_count")
    if not isinstance(row_count, int) or row_count <= 0:
        raise SystemExit(f"MISSING_OBJECT := positive_candidate_numeric_row_count::{cid}")
    computed_rows += row_count

    if source.get("candidate_row_count_authority") != "candidate_shape_adapter_contract_observable_length":
        raise SystemExit(f"MISSING_OBJECT := candidate_row_count_authority::{cid}")
    if source.get("authority_status_for_candidate_component") != "source_file_header_observed":
        raise SystemExit(f"MISSING_OBJECT := source_file_header_observed::{cid}")
    if source.get("authority_status_for_repository_36_slot") != "insufficient_without_repository_36_slot_manifest_mapping":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := repository_36_slot_authority::{cid}")

if computed_rows != 26:
    raise SystemExit("MISSING_OBJECT := computed_candidate_numeric_row_count_26")

status = data.get("repository_36_slot_authority_status", {})
if status.get("required_repository_slot_count") != 36:
    raise SystemExit("MISSING_OBJECT := required_repository_slot_count_36")
if status.get("resolved_repository_slot_label_count") != 0:
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := resolved_repository_slot_label_count")
if status.get("unresolved_repository_slot_label_count") != 36:
    raise SystemExit("MISSING_OBJECT := unresolved_repository_slot_label_count_36")
if status.get("candidate_source_rows_available") != 26:
    raise SystemExit("MISSING_OBJECT := candidate_source_rows_available_26")
if status.get("repository_36_authoritative_slot_label_source") != "blocked":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := repository_36_authoritative_slot_label_source")
for key in ["no_invented_labels", "no_padding_or_duplication_allowed", "no_numeric_pin"]:
    if status.get(key) is not True:
        raise SystemExit(f"MISSING_OBJECT := {key}")

blocked = set(data.get("blocked_objects", []))
required_blocked = {
    "DESI_DR2_BAO_repository_36_authoritative_slot_label_source",
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

if data.get("next_weakest_missing_object") != "DESI_DR2_BAO_repository_36_authoritative_slot_label_source":
    raise SystemExit("MISSING_OBJECT := DESI_DR2_BAO_repository_36_authoritative_slot_label_source")

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

print("DESI_DR2_BAO_AUTHORITATIVE_SLOT_LABEL_SOURCE_BOUNDARY_OK")
print("CANDIDATE_COMPONENT_COUNT := 8")
print("CANDIDATE_NUMERIC_ROW_COUNT := 26")
print("RESOLVED_REPOSITORY_SLOT_LABEL_COUNT := 0")
print("NEXT_MISSING_OBJECT := DESI_DR2_BAO_repository_36_authoritative_slot_label_source")
