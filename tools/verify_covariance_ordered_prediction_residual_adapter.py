#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

module_path = Path("numerics/prediction_adapter.py")
artifact_path = Path("artifacts/external_validation/covariance_ordered_prediction_residual_adapter_2026_06_29.json")
schema_path = Path("schemas/cosmology/covariance_ordered_prediction_residual_adapter_schema_2026_06_29.json")

for required in [
    module_path,
    artifact_path,
    schema_path,
    Path("h0_residuals.csv"),
    Path("s8_consistency.csv"),
]:
    if not required.exists():
        raise SystemExit(f"MISSING_OBJECT := {required}")

spec = importlib.util.spec_from_file_location("prediction_adapter", module_path)
if spec is None or spec.loader is None:
    raise SystemExit("MISSING_OBJECT := prediction_adapter_import_spec")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

adapter = module.CovarianceOrderedPredictionResidualAdapter()
cov = module.deterministic_covariance(adapter.block_dim)
witness = module.deterministic_rank_deficient_witness(adapter.block_dim)
result = adapter.map_external_residuals(cov, witness)

if result.get("adapter_id") != "covariance_ordered_prediction_residual_adapter":
    raise SystemExit("MISSING_OBJECT := adapter_id")
if result.get("claim_status") != "diagnostic_field_only_no_tensor_law":
    raise SystemExit("UNSUPPORTED_CLAIM_ENABLED := covariance_adapter")
if result.get("block_dim") != 36:
    raise SystemExit("MISSING_OBJECT := block_dim_36")

trace = result.get("finite_patch_trace")
if not isinstance(trace, float) or not math.isfinite(trace) or trace < 0.0:
    raise SystemExit("MISSING_OBJECT := finite_nonnegative_trace")

wrong_cov = np.eye(35, dtype=float)
try:
    adapter.map_external_residuals(wrong_cov, witness)
except ValueError:
    pass
else:
    raise SystemExit("MISSING_OBJECT := covariance_shape_guard")

nonsymmetric_cov = np.eye(36, dtype=float)
nonsymmetric_cov[0, 1] = 1.0
try:
    adapter.map_external_residuals(nonsymmetric_cov, witness)
except ValueError:
    pass
else:
    raise SystemExit("MISSING_OBJECT := covariance_symmetry_guard")

artifact = json.loads(artifact_path.read_text())
if artifact.get("csv_write_policy") != "no_mutation_of_h0_residuals_or_s8_consistency_by_verifier":
    raise SystemExit("MISSING_OBJECT := no_csv_mutation_policy")
if artifact.get("diagnostic_csv_field") != "adapter_diagnostic_trace":
    raise SystemExit("MISSING_OBJECT := adapter_diagnostic_trace_field")

required_boundaries = {
    "BOUNDARY := \u00ac current_repo_supports_LCDM_refutation_claim",
    "BOUNDARY := \u00ac current_repo_supports_DFM_MKC_cosmology_validation_claim",
    "BOUNDARY := \u00ac current_repo_supports_strict_w0wa_schema_constraint",
    "BOUNDARY := \u00ac current_repo_supports_chi_squared_likelihood_closure",
}
if set(artifact.get("claim_boundaries_preserved", [])) != required_boundaries:
    raise SystemExit("MISSING_OBJECT := claim_boundaries_preserved")

schema = json.loads(schema_path.read_text())
if schema["properties"]["adapter_id"]["const"] != "covariance_ordered_prediction_residual_adapter":
    raise SystemExit("MISSING_OBJECT := schema_adapter_id_const")
if schema["properties"]["claim_status"]["const"] != "diagnostic_field_only_no_tensor_law":
    raise SystemExit("MISSING_OBJECT := schema_claim_status_const")

for csv_path in [Path("h0_residuals.csv"), Path("s8_consistency.csv")]:
    with csv_path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
    if header is None:
        raise SystemExit(f"MISSING_OBJECT := {csv_path}_header")

print("COVARIANCE_ORDERED_PREDICTION_RESIDUAL_ADAPTER_OK")
print(f"ADAPTER_DIAGNOSTIC_TRACE := {trace:.17g}")
print("CLAIM_STATUS := diagnostic_field_only_no_tensor_law")
