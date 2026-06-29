#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/desi_dr2_bao_candidate_shape_audit_2026_06_29.json")
if not artifact_path.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_candidate_shape_audit_2026_06_29.json")

for required in [
    Path("artifacts/external_validation/observed_desi_dr2_bao_numeric_order_boundary_2026_06_29.json"),
    Path("artifacts/external_validation/frozen_dfm_mkc_prediction_vector_desi_order_2026_06_29.json"),
    Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json"),
    Path("tools/verify_observed_desi_dr2_bao_numeric_order_boundary.py"),
]:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

data = json.loads(artifact_path.read_text())

if data.get("first_authoritative_failure") != "MISSING_OBJECT := exact_DESI_DR2_BAO_36_vector_and_36x36_covariance_pair":
    raise SystemExit("MISSING_OBJECT := first_authoritative_failure")

if data.get("status") != "blocked_exact_36_pair_not_found_in_candidate_repository_layout":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := desi_dr2_numeric_pin")

expected_missing = "DESI_DR2_BAO_candidate_shape_adapter_from_available_blocks_to_repository_36_order"
if data.get("weakest_missing_object") != expected_missing:
    raise SystemExit("MISSING_OBJECT := DESI_DR2_BAO_candidate_shape_adapter_from_available_blocks_to_repository_36_order")

blocked = set(data.get("blocked_pin_targets", []))
if blocked != {
    "public_data/desi_dr2/observed_bao_vector_36.csv",
    "public_data/desi_dr2/observed_bao_covariance_36x36.csv",
}:
    raise SystemExit("MISSING_OBJECT := blocked_pin_targets")

for target in blocked:
    if Path(target).exists():
        raise SystemExit(f"CONDITIONAL := {target}")

claims = data.get("claim_status", {})
required_claims = {
    "chi_squared_likelihood_closure",
    "LCDM_refutation_claim",
    "DFM_MKC_cosmology_validation_claim",
    "strict_w0wa_schema_constraint",
}
if set(claims) != required_claims:
    raise SystemExit("MISSING_OBJECT := complete_claim_status_map")
for claim, status in claims.items():
    if status != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {claim}")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
}
if set(data.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

print("DESI_DR2_BAO_CANDIDATE_SHAPE_AUDIT_OK")
print("MISSING_OBJECT := exact_DESI_DR2_BAO_36_vector_and_36x36_covariance_pair")
print("NEXT_MISSING_OBJECT := DESI_DR2_BAO_candidate_shape_adapter_from_available_blocks_to_repository_36_order")
