
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_dfm_mkc_135_row_prediction_vector_candidate_target_2026_06_17.json")
data = json.loads(ART.read_text())

assert data["id"] == "ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR_CANDIDATE_TARGET_2026_06_17"
assert data["status"] == "TARGET_ONLY_DFM_VECTOR_NOT_YET_MATERIALIZED"
assert data["target_object"] == "ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR_CANDIDATE"
assert data["source_blocked_probe"] == "artifacts/dfm_mkc/act_dr6_dfm_vs_lcdm_internal_probe_blocked_no_dfm_vector_2026_06_17.json"

assert data["baseline_lcdm_reference"]["internal_lcdm_chi2"] == 153.61808801048306
assert data["required_shape"] == [135]

ordering = data["required_ordering"]
assert ordering["certificate"] == "artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json"
assert ordering["target_rows"][0]["range"] == [0, 44]
assert ordering["target_rows"][0]["data_type"] == "cl_00"
assert ordering["target_rows"][1]["range"] == [45, 89]
assert ordering["target_rows"][1]["data_type"] == "cl_0e"
assert ordering["target_rows"][2]["range"] == [90, 134]
assert ordering["target_rows"][2]["data_type"] == "cl_ee"

contract = data["required_numeric_contract"]
assert contract["shape"] == [135]
assert contract["all_finite"] is True
assert "chi2" in contract["comparison_metric"]

for required in [
    "DFM_MKC_PARAMETER_TO_CMB_OBSERVABLE_MAP",
    "DFM_MKC_ACT_DR6_CMBONLY_PARAMETER_POINT_OR_FIT_RULE",
    "DFM_MKC_UNBINNED_TT_TE_EE_THEORY_TABLE_OR_DIRECT_BANDPOWER_RULE",
    "DFM_MKC_ACT_DR6_BANDPOWER_WINDOW_PROJECTION_RULE_COMPATIBLE_WITH_LCDM_BASELINE",
    "DFM_MKC_135_ROW_VECTOR_NUMERIC_MATERIALIZATION",
    "DFM_MKC_VECTOR_CONVENTION_AUDIT",
]:
    assert required in data["required_model_source_objects"]

routes = {r["route"] for r in data["accepted_materialization_routes"]}
assert "unbinned_theory_to_bandpowers" in routes
assert "direct_bandpower_prediction" in routes

for field in [
    "id",
    "status",
    "source_model",
    "parameter_values_or_fit_rule",
    "projection_or_direct_bandpower_rule",
    "vector_shape",
    "vector_values",
    "finite",
    "numeric_digest",
    "ordering_certificate",
    "convention_audit",
    "does_not_prove",
]:
    assert field in data["minimum_candidate_artifact_fields"]

gate = data["comparison_gate_after_candidate_exists"]
assert gate["next_probe"] == "ACT_DR6_DFM_VS_LCDM_INTERNAL_CHI2_COMPARISON"
assert gate["better_than_lcdm_internal_condition"] == "dfm_mkc_chi2 < lcdm_chi2"
assert gate["claim_boundary"] == "internal numerical comparison only; not empirical validation"

assert data["current_resolution"] == "The missing object is now precisely specified, but not yet materialized."
assert data["next_required_validation"] == "ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR_CANDIDATE"

for token in [
    "ACT DR6 DFM-MKC 135-row prediction vector exists",
    "DFM-MKC is better than Lambda-CDM",
    "DFM-MKC is worse than Lambda-CDM",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "Lambda-CDM rejection",
    "dark matter resolution",
    "dark energy resolution",
    "gravity closure",
    "P vs NP",
    "any Clay problem",
]:
    assert token in data["does_not_prove"]

print("ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR_CANDIDATE_TARGET_OK")
