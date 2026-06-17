import json
from pathlib import Path

PATH = Path("artifacts/repo_intake/dfm_mkc_numerical_prediction_vector_run_v1_target_2026_06_17.json")

data = json.loads(PATH.read_text())

assert data["id"] == "DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_V1_TARGET"
assert data["status"] == "NUMERICAL_PREDICTION_VECTOR_RUN_TARGET_SUPPLIED_NO_NUMERICAL_RUN"

locks = data["required_input_hash_locks"]
for key in [
    "parameter_block_sha256",
    "grid_block_sha256",
    "solver_environment_sha256",
    "solver_source_commit",
    "solver_config_sha256",
]:
    assert key in locks
    assert locks[key]["required"] is True

outputs = data["required_output_fields"]
for key in ["ell", "D_ell_TT", "D_ell_TE", "D_ell_EE"]:
    assert key in outputs

assert outputs["ell"]["shape"] == [8500]
assert outputs["ell"]["required_min"] == 2
assert outputs["ell"]["required_max"] == 8501
assert outputs["ell"]["required_step"] == 1

for key in ["D_ell_TT", "D_ell_TE", "D_ell_EE"]:
    assert outputs[key]["dtype"] == "float64"
    assert outputs[key]["shape"] == [8500]
    assert outputs[key]["finite"] is True

compat = data["act_projection_compatibility"]
assert compat["source_sacc_path"] == "data/act_dr6_cmbonly/dr6_data_cmbonly.fits"
assert compat["required_ell_grid"] == {"start": 2, "stop": 8501, "count": 8500, "step": 1}
assert compat["projected_vector_shape"] == [135]

order = compat["required_output_order"]
assert order[0]["data_type"] == "cl_00"
assert order[0]["source_field"] == "D_ell_TT"
assert order[0]["target_index_range"] == [0, 44]
assert order[1]["data_type"] == "cl_0e"
assert order[1]["source_field"] == "D_ell_TE"
assert order[1]["target_index_range"] == [45, 89]
assert order[2]["data_type"] == "cl_ee"
assert order[2]["source_field"] == "D_ell_EE"
assert order[2]["target_index_range"] == [90, 134]

acceptance = data["acceptance_test_result"]
for key in [
    "target_declared",
    "input_hash_lock_requirements_declared",
    "required_output_fields_declared",
    "act_projection_compatibility_declared",
    "accepted_materialization_routes_declared",
]:
    assert acceptance[key] is True

for key in [
    "numerical_integration_run",
    "prediction_vector_computed",
    "act_projection_materializer_adapted",
    "dfm_mkc_empirical_status_promoted",
]:
    assert acceptance[key] is False

for term in [
    "DFM-MKC numerical integration run",
    "DFM-MKC numerical prediction vector",
    "ACT DR6 DFM-MKC 135-row prediction vector",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "P vs NP",
    "any Clay problem",
]:
    assert term in data["does_not_prove"]

print("DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_V1_TARGET_OK")
