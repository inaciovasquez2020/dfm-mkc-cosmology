#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_adapter_contract_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_candidate_shape_adapter_contract_2026_06_29.json")

for required in [
    Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_audit_2026_06_29.json"),
    Path("artifacts/external_validation/observed_desi_dr2_bao_numeric_order_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/frozen_dfm_mkc_prediction_vector_desi_order_2026_06_29.json"),
    Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json"),
]:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

data = json.loads(artifact_path.read_text())

if data.get("artifact") != "desi_dr2_bao_candidate_shape_adapter_contract":
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_candidate_shape_adapter_contract")

contract = data.get("repository_target_contract", {})
if contract.get("required_vector_length") != 36:
    raise SystemExit("MISSING_OBJECT := required_vector_length_36")
if contract.get("required_covariance_shape") != [36, 36]:
    raise SystemExit("MISSING_OBJECT := required_covariance_shape_36x36")
if contract.get("same_order_required") is not True:
    raise SystemExit("MISSING_OBJECT := same_order_required")

components = data.get("candidate_components", [])
if not components:
    raise SystemExit("MISSING_OBJECT := candidate_components")

component_ids = set()
computed_total = 0
for component in components:
    cid = component.get("component_id")
    if not cid or cid in component_ids:
        raise SystemExit("MISSING_OBJECT := unique_component_id")
    component_ids.add(cid)

    observable_length = component.get("observable_length")
    covariance_shape = component.get("covariance_shape")

    if not isinstance(observable_length, int) or observable_length <= 0:
        raise SystemExit(f"MISSING_OBJECT := positive_observable_length::{cid}")
    if covariance_shape != [observable_length, observable_length]:
        raise SystemExit(f"MISSING_OBJECT := covariance_shape_matches_observable_length::{cid}")
    if component.get("covariance_matches_component_observable_length") is not True:
        raise SystemExit(f"MISSING_OBJECT := covariance_matches_component_observable_length::{cid}")
    if not component.get("source_mean_sha256") or not component.get("source_covariance_sha256"):
        raise SystemExit(f"MISSING_OBJECT := source_sha256::{cid}")

    computed_total += observable_length

summary = data.get("candidate_shape_summary", {})
if summary.get("component_count") != len(components):
    raise SystemExit("MISSING_OBJECT := component_count")
if summary.get("total_component_observable_length") != computed_total:
    raise SystemExit("MISSING_OBJECT := total_component_observable_length")
if summary.get("all_component_covariances_match_component_length") is not True:
    raise SystemExit("MISSING_OBJECT := all_component_covariances_match_component_length")
if summary.get("exact_repository_36_pair_found") is not False:
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := exact_repository_36_pair_found")

if data.get("adapter_contract_status") != "shape_inventory_only_no_numeric_pin":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := numeric_pin")
if data.get("next_weakest_missing_object") != "DESI_DR2_BAO_candidate_shape_adapter_index_map_to_repository_36_order":
    raise SystemExit("MISSING_OBJECT := DESI_DR2_BAO_candidate_shape_adapter_index_map_to_repository_36_order")

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

for forbidden in [
    Path("public_data/desi_dr2/observed_bao_vector_36.csv"),
    Path("public_data/desi_dr2/observed_bao_covariance_36x36.csv"),
]:
    if forbidden.exists():
        raise SystemExit(f"CONDITIONAL := numeric_pin_exists::{forbidden}")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_observed_DESI_DR2_BAO_numeric_pin",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
}
if set(data.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

print("DESI_DR2_BAO_CANDIDATE_SHAPE_ADAPTER_CONTRACT_OK")
print(f"COMPONENT_COUNT := {len(components)}")
print(f"TOTAL_COMPONENT_OBSERVABLE_LENGTH := {computed_total}")
print("NEXT_MISSING_OBJECT := DESI_DR2_BAO_candidate_shape_adapter_index_map_to_repository_36_order")
