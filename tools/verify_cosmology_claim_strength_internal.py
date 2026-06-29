#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

artifact = Path("artifacts/external_validation/cosmology_claim_strength_internal_2026_06_29.json")
if not artifact.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/cosmology_claim_strength_internal_2026_06_29.json")

required_files = [
    "artifacts/external_validation/desi_dr2_bao_input_packet_2026_06_29.json",
    "artifacts/external_validation/cosmology_claim_readiness_gate_2026_06_29.json",
    "tools/verify_desi_dr2_bao_input_packet.py",
    "tools/verify_cosmology_claim_readiness_gate.py",
    "h0_residuals.csv",
    "s8_consistency.csv",
    "likelihoods/bao_chi2.py",
    "likelihoods/sn_chi2.py",
    "schemas/cosmology/desi_dr2_bao_model_comparison_output_schema_2026_05_24.json",
]
for name in required_files:
    if not Path(name).exists():
        raise SystemExit(f"MISSING_OBJECT := {name}")

data = json.loads(artifact.read_text())

expected_order = [
    "chi_squared_likelihood_closure",
    "strict_w0wa_schema_constraint",
    "LCDM_refutation_claim",
    "DFM_MKC_cosmology_validation_claim",
]
actual_order = [item.get("claim") for item in data.get("claim_strength_order", [])]
if actual_order != expected_order:
    raise SystemExit("CLAIM_STRENGTH_ORDER_MISMATCH")

for item in data["claim_strength_order"]:
    if item["claim"] == "chi_squared_likelihood_closure":
        if item["status"] != "strongest_blocked_claim":
            raise SystemExit("MISSING_OBJECT := strongest_blocked_claim_marker")
        if item["weakest_missing_object"] != "covariance_ordered_prediction_residual_adapter":
            raise SystemExit("MISSING_OBJECT := covariance_ordered_prediction_residual_adapter")
    elif item["status"] not in {"blocked", "weakest_blocked_claim"}:
        raise SystemExit(f"UNSUPPORTED_CLAIM_ENABLED := {item['claim']}")

supported = data.get("strongest_current_admissible_claim", {})
if supported.get("status") != "supported":
    raise SystemExit("MISSING_OBJECT := strongest_current_admissible_claim")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
}
if set(data.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

print("COSMOLOGY_CLAIM_STRENGTH_INTERNAL_OK")
print("STRONGEST_BLOCKED_CLAIM := chi_squared_likelihood_closure")
print("STRONGEST_ADMISSIBLE_CLAIM := ci_enforced_DESI_DR2_BAO_input_packet_plus_claim_readiness_gate")
