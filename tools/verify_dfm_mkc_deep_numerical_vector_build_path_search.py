import json
from pathlib import Path

PATH = Path("artifacts/repo_intake/dfm_mkc_deep_numerical_vector_build_path_search_2026_06_17.json")
data = json.loads(PATH.read_text())

assert data["id"] == "DFM_MKC_DEEP_NUMERICAL_VECTOR_BUILD_PATH_SEARCH_2026_06_17"
assert data["object_type"] == "bounded deep local search record for a DFM-MKC numerical vector build path"

policy = data["search_policy"]
assert policy["max_file_bytes"] == 1000000
assert policy["max_github_files"] == 12000
assert "replace unbounded full GITHUB text scan" in policy["repair"]

contract = data["required_vector_contract"]
assert contract["ell"] == {"start": 2, "stop": 8501, "count": 8500, "step": 1}
for key in ["ell", "D_ell_TT", "D_ell_TE", "D_ell_EE"]:
    assert key in contract["required_fields"]

for key in [
    "parameter_block_sha256",
    "grid_block_sha256",
    "solver_environment_sha256",
    "solver_source_commit",
    "solver_config_sha256",
]:
    assert key in contract["required_hash_locks"]

for scope in ["repo_search_summary", "github_search_summary"]:
    summary = data[scope]
    for key in [
        "files_scanned",
        "amd_files",
        "strong_vector_emitters",
        "spectrum_emitters",
        "external_or_solver_candidates",
        "hash_locked_candidates",
        "admissible_build_paths",
    ]:
        assert key in summary
        assert isinstance(summary[key], int)

for key in [
    "repo_candidates",
    "github_candidates",
    "admissible_repo_build_paths",
    "admissible_github_build_paths",
]:
    assert key in data

acceptance = data["acceptance_test_result"]
for key in [
    "deep_search_recorded",
    "required_contract_recorded",
    "repo_scanned",
    "github_tree_scanned",
    "amd_path_checked",
]:
    assert acceptance[key] is True

for key in [
    "numerical_vector_supplied",
    "act_projection_materializer_adapted",
    "empirical_status_promoted",
]:
    assert acceptance[key] is False

assert acceptance["admissible_build_path_found"] is False
assert acceptance["false_positive_lcdm_mapping_trial_rejected"] is True
assert data["admissible_repo_build_paths"] == []
assert data["admissible_github_build_paths"] == []
assert data["status"] == "NO_ADMISSIBLE_DFM_MKC_OR_AMD_BUILD_PATH_FOUND_REUSE_SCHEMA_PROJECTION_PATTERN_ONLY"
assert "reuse only LCDM projection/schema/hash-lock/verifier pattern" in data["decision"]

false_positive_paths = {row["path"] for row in data["false_positive_admissible_paths"]}
assert "tools/materialize_act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial.py" in false_positive_paths

for term in [
    "DFM-MKC numerical integration run",
    "DFM-MKC numerical prediction vector",
    "ACT DR6 DFM-MKC 135-row prediction vector",
    "AMD executable vector emitter exists",
    "DFM-MKC empirical validation",
    "P vs NP",
    "any Clay problem",
]:
    assert term in data["does_not_prove"]

print("DFM_MKC_DEEP_NUMERICAL_VECTOR_BUILD_PATH_SEARCH_OK")
