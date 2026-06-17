import json
from pathlib import Path

PATH = Path("artifacts/repo_intake/dfm_mkc_current_source_numerical_vector_boundary_2026_06_17.json")
data = json.loads(PATH.read_text())

assert data["id"] == "DFM_MKC_CURRENT_SOURCE_NUMERICAL_VECTOR_BOUNDARY_2026_06_17"
assert data["status"] == "CURRENT_REPO_SOURCE_INSUFFICIENT_FOR_NUMERICAL_VECTOR"

can = set(data["current_repo_can_supply"])
for term in [
    "DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_V1_TARGET",
    "DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_ARTIFACT_SCHEMA",
    "ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR_CANDIDATE_TARGET",
    "ACT DR6 SACC projection pattern from the LCDM materializer",
]:
    assert term in can

cannot = set(data["current_repo_cannot_supply"])
for term in [
    "trusted executable DFM-MKC Boltzmann solver run",
    "trusted external DFM-MKC solver binding run",
    "finite DFM-MKC D_ell_TT array on ell=2..8501",
    "finite DFM-MKC D_ell_TE array on ell=2..8501",
    "finite DFM-MKC D_ell_EE array on ell=2..8501",
    "ACT DR6 DFM-MKC 135-row numerical prediction vector",
]:
    assert term in cannot

missing = data["required_missing_source_object"]
assert missing["id"] == "DFM_MKC_NUMERICAL_PREDICTION_VECTOR_RUN_V1"
assert missing["required_status"] == "HASH_LOCKED_FINITE_D_ELL_OUTPUTS_SUPPLIED_NO_ACT_PROJECTION"
assert missing["required_ell_contract"] == {"start": 2, "stop": 8501, "count": 8500, "step": 1}

for key in [
    "ell",
    "D_ell_TT",
    "D_ell_TE",
    "D_ell_EE",
    "input_hash_locks.parameter_block_sha256",
    "input_hash_locks.grid_block_sha256",
    "input_hash_locks.solver_environment_sha256",
    "input_hash_locks.solver_source_commit",
    "input_hash_locks.solver_config_sha256",
]:
    assert key in missing["required_fields"]

amd = data["amd_reuse_decision"]
assert amd["amd_files_found_in_repo"] is False
assert amd["amd_executable_vector_emitter_found_in_repo"] is False
assert "schema pattern" in amd["allowed_reuse"]
assert "projection pattern" in amd["allowed_reuse"]
assert "AMD numerical vector generation" in amd["disallowed_reuse"]

gate = data["act_projection_adaptation_gate"]
assert gate["existing_pattern_source"] == "tools/materialize_act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_reproducible_materialization.py"
assert gate["blocked_now"] is True

acceptance = data["acceptance_test_result"]
for key in [
    "current_source_boundary_recorded",
    "missing_numerical_source_identified",
    "amd_reuse_limited_to_schema_projection_pattern",
    "act_projection_adaptation_blocked",
]:
    assert acceptance[key] is True

for key in [
    "numerical_vector_supplied",
    "act_projection_materializer_adapted",
    "empirical_status_promoted",
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

print("DFM_MKC_CURRENT_SOURCE_NUMERICAL_VECTOR_BOUNDARY_OK")
