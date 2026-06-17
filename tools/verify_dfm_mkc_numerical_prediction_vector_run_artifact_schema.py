import json
from pathlib import Path

PATH = Path("artifacts/repo_intake/dfm_mkc_numerical_prediction_vector_run_artifact_schema_2026_06_17.json")
TARGET = Path("artifacts/repo_intake/dfm_mkc_numerical_prediction_vector_run_v1_target_2026_06_17.json")

data = json.loads(PATH.read_text())
target = json.loads(TARGET.read_text())

assert data["id"] == "DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_ARTIFACT_SCHEMA"
assert data["status"] == "RUN_ARTIFACT_SCHEMA_SUPPLIED_NO_NUMERICAL_VECTOR"
assert data["schema_target"] == "DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_V1"
assert target["id"] == "DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_V1_TARGET"

required_top = set(data["required_top_level_fields"])
for key in [
    "id",
    "date",
    "status",
    "program",
    "source_target_id",
    "input_hash_locks",
    "solver_provenance",
    "ell",
    "D_ell_TT",
    "D_ell_TE",
    "D_ell_EE",
    "diagnostics",
    "act_projection_compatibility",
    "does_not_prove",
]:
    assert key in required_top

assert data["required_status"] == "HASH_LOCKED_FINITE_D_ELL_OUTPUTS_SUPPLIED_NO_ACT_PROJECTION"

locks = data["input_hash_locks_schema"]["required_fields"]
for key in [
    "parameter_block_sha256",
    "grid_block_sha256",
    "solver_environment_sha256",
    "solver_source_commit",
    "solver_config_sha256",
]:
    assert key in locks
    assert key in data["input_hash_locks_schema"]["field_contract"]

prov = data["solver_provenance_schema"]
for key in [
    "solver_route",
    "solver_name",
    "solver_version",
    "source_commit",
    "environment_lock_path",
    "run_command",
    "run_timestamp_utc",
]:
    assert key in prov["required_fields"]

assert prov["allowed_solver_routes"] == [
    "first_party_solver",
    "trusted_external_solver_binding",
]

arrays = data["output_array_schema"]
assert arrays["ell"]["shape"] == [8500]
assert arrays["ell"]["exact_values"] == {"start": 2, "stop": 8501, "step": 1}

for key in ["D_ell_TT", "D_ell_TE", "D_ell_EE"]:
    assert arrays[key]["dtype"] == "float64"
    assert arrays[key]["shape"] == [8500]
    assert arrays[key]["finite"] is True
    assert arrays[key]["units"] == "microK^2"

diag = data["diagnostics_schema"]
for key in [
    "finite_output_check",
    "ell_grid_check",
    "hash_lock_check",
    "constraint_residual_summary",
    "grid_convergence_summary",
    "output_digest_sha256",
]:
    assert key in diag["required_fields"]

compat = data["act_projection_compatibility_schema"]["required_values"]
assert compat["source_sacc_path"] == "data/act_dr6_cmbonly/dr6_data_cmbonly.fits"
assert compat["ell_min"] == 2
assert compat["ell_max"] == 8501
assert compat["ell_count"] == 8500
assert compat["compatible_with_existing_lcdm_projection_materializer"] is True
assert compat["act_projection_performed"] is False

acceptance = data["acceptance_test_result"]
for key in [
    "schema_declared",
    "input_hash_lock_schema_declared",
    "solver_provenance_schema_declared",
    "ell_schema_declared",
    "D_ell_TT_schema_declared",
    "D_ell_TE_schema_declared",
    "D_ell_EE_schema_declared",
    "act_projection_compatibility_schema_declared",
]:
    assert acceptance[key] is True

for key in [
    "numerical_vector_supplied",
    "act_projection_materializer_adapted",
    "act_projection_performed",
    "dfm_mkc_empirical_status_promoted",
]:
    assert acceptance[key] is False

for term in [
    "DFM-MKC numerical integration run",
    "DFM-MKC numerical prediction vector",
    "ACT DR6 DFM-MKC 135-row prediction vector",
    "ACT projection materializer adaptation",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "P vs NP",
    "any Clay problem",
]:
    assert term in data["does_not_prove"]

print("DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_ARTIFACT_SCHEMA_OK")
