#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact = Path("artifacts/external_validation/cosmology_claim_readiness_gate_2026_06_29.json")
if not artifact.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/cosmology_claim_readiness_gate_2026_06_29.json")

data = json.loads(artifact.read_text())

required_claims = {
    "lcdm_refutation_claim",
    "dfm_mkc_cosmology_validation_claim",
    "strict_w0wa_schema_constraint",
    "chi_squared_likelihood_closure",
}
claim_status = data.get("claim_status", {})
if set(claim_status) != required_claims:
    raise SystemExit("MISSING_OBJECT := complete_claim_status_map")

for claim, status in claim_status.items():
    if status != "blocked":
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {claim}")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
}
if set(data.get("blocked_claim_boundaries", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := blocked_claim_boundaries")

required_prerequisites = {
    "frozen_prediction_vector",
    "observed_data_packet",
    "covariance_bound_likelihood",
    "preregistered_decision_rule",
}
if set(data.get("required_prerequisites", [])) != required_prerequisites:
    raise SystemExit("MISSING_OBJECT := claim_prerequisite_set")

if data.get("weakest_missing_object") != "covariance_ordered_prediction_residual_adapter":
    raise SystemExit("MISSING_OBJECT := weakest_missing_object")

if data.get("admissible_next_target") != "frozen_prediction_vector":
    raise SystemExit("MISSING_OBJECT := admissible_next_target")

print("COSMOLOGY_CLAIM_READINESS_GATE_OK")
