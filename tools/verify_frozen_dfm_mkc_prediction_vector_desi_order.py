#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path

artifact = Path("artifacts/external_validation/frozen_dfm_mkc_prediction_vector_desi_order_2026_06_29.json")
desi_packet = Path("artifacts/external_validation/desi_dr2_bao_input_packet_2026_06_29.json")
adapter_artifact = Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json")

for required in [
    artifact,
    desi_packet,
    adapter_artifact,
    Path("tools/verify_covariance_ordered_prediction_residual_adapter.py"),
    Path("h0_residuals.csv"),
    Path("s8_consistency.csv"),
]:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

data = json.loads(artifact.read_text())
desi = json.loads(desi_packet.read_text())
adapter = json.loads(adapter_artifact.read_text())

if data.get("status") != "diagnostic_prediction_vector_frozen_not_empirical_validation":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := frozen_prediction_vector")

if data.get("adapter_id") != "covariance_ordered_prediction_residual_adapter":
    raise SystemExit("MISSING_OBJECT := adapter_id_binding")

if data.get("source_packet") != "desi_dr2_bao_input_packet_2026_06_29":
    raise SystemExit("MISSING_OBJECT := desi_source_packet_binding")

if adapter.get("block_dim") != 36:
    raise SystemExit("MISSING_OBJECT := adapter_block_dim_36")

binding = data.get("covariance_order_binding", {})
if binding.get("block_dim") != 36:
    raise SystemExit("MISSING_OBJECT := prediction_vector_block_dim_36")
if binding.get("order_index_base") != 0:
    raise SystemExit("MISSING_OBJECT := zero_based_order_binding")
if binding.get("covariance_binding_status") != "bound_to_adapter_block_dimension_only":
    raise SystemExit("MISSING_OBJECT := covariance_binding_status")

vector = data.get("prediction_vector")
if not isinstance(vector, list) or len(vector) != 36:
    raise SystemExit("MISSING_OBJECT := 36_entry_prediction_vector")
if not all(isinstance(x, (int, float)) and math.isfinite(float(x)) for x in vector):
    raise SystemExit("MISSING_OBJECT := finite_prediction_vector")
if any(float(x) != 0.0 for x in vector):
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := nonzero_physical_prediction_vector")

if data.get("prediction_vector_semantics") != "zero_baseline_frozen_diagnostic_seed_only":
    raise SystemExit("MISSING_OBJECT := diagnostic_prediction_vector_semantics")

if not desi.get("files"):
    raise SystemExit("MISSING_OBJECT := desi_packet_files")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
}
if set(data.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

next_missing = data.get("strengthened_claim_path", {}).get("next_weakest_missing_object")
if next_missing != "observed_DESI_DR2_BAO_numeric_data_vector_and_covariance_matrix_with_same_order":
    raise SystemExit("MISSING_OBJECT := next_weakest_missing_object")

print("FROZEN_DFM_MKC_PREDICTION_VECTOR_DESI_ORDER_OK")
print("VECTOR_LENGTH := 36")
print("CLAIM_STATUS := diagnostic_prediction_vector_frozen_not_empirical_validation")
print("NEXT_MISSING_OBJECT := observed_DESI_DR2_BAO_numeric_data_vector_and_covariance_matrix_with_same_order")
