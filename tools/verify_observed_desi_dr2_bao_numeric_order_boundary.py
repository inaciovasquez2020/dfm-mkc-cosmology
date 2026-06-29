#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact_path = Path("artifacts/external_validation/observed_desi_dr2_bao_numeric_order_boundary_2026_06_29.json")
required_existing = [
    artifact_path,
    Path("artifacts/external_validation/desi_dr2_bao_input_packet_2026_06_29.json"),
    Path("artifacts/external_validation/frozen_dfm_mkc_prediction_vector_desi_order_2026_06_29.json"),
    Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json"),
    Path("tools/verify_frozen_dfm_mkc_prediction_vector_desi_order.py"),
    Path("tools/verify_covariance_ordered_prediction_residual_adapter.py"),
]
for required in required_existing:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

data = json.loads(artifact_path.read_text())

if data.get("status") != "blocked_missing_observed_numeric_vector_and_covariance":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := observed_desi_numeric_order_boundary")

contract = data.get("required_order_contract", {})
if contract.get("block_dim") != 36:
    raise SystemExit("MISSING_OBJECT := block_dim_36")
if contract.get("vector_length") != 36:
    raise SystemExit("MISSING_OBJECT := vector_length_36")
if contract.get("covariance_shape") != [36, 36]:
    raise SystemExit("MISSING_OBJECT := covariance_shape_36x36")
if contract.get("same_order_required") is not True:
    raise SystemExit("MISSING_OBJECT := same_order_required")

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

required_numeric = data.get("required_numeric_objects", {})
vector = Path(required_numeric.get("observed_data_vector_csv", ""))
covariance = Path(required_numeric.get("observed_covariance_matrix_csv", ""))

if vector.exists() or covariance.exists():
    raise SystemExit("CONDITIONAL := numeric DESI files exist; replace this boundary with a shape-and-sha256 verifier")

expected_missing = "public_data/desi_dr2/observed_bao_vector_36.csv_and_public_data/desi_dr2/observed_bao_covariance_36x36.csv"
if data.get("weakest_missing_object") != expected_missing:
    raise SystemExit("MISSING_OBJECT := weakest_missing_object")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
}
if set(data.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

print("OBSERVED_DESI_DR2_BAO_NUMERIC_ORDER_BOUNDARY_OK")
print("MISSING_OBJECT := public_data/desi_dr2/observed_bao_vector_36.csv")
print("MISSING_OBJECT := public_data/desi_dr2/observed_bao_covariance_36x36.csv")
print("CLAIM_STATUS := blocked_until_real_numeric_vector_and_covariance_are_pinned")
