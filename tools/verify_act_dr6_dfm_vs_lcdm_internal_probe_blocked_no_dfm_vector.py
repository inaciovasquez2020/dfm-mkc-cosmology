
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_dfm_vs_lcdm_internal_probe_blocked_no_dfm_vector_2026_06_17.json")
data = json.loads(ART.read_text())

assert data["id"] == "ACT_DR6_DFM_VS_LCDM_INTERNAL_PROBE_BLOCKED_NO_DFM_VECTOR_2026_06_17"
assert data["status"] == "INTERNAL_PROBE_BLOCKED_NO_ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR"
assert data["probe_type"] == "internal_nonclaiming_chi2_probe"
assert data["observed_data_vector_shape"] == [135]
assert data["covariance_shape"] == [135, 135]
assert data["lcdm_baseline_candidate_available"] is True
assert abs(data["lcdm_baseline_candidate_chi2"] - 153.61808801048306) < 1e-9
assert data["dfm_mkc_vector_candidates_found"] == 0
assert data["dfm_mkc_chi2"] is None
assert data["comparison_result"] == "NOT_COMPUTABLE"
assert data["missing_object"] == "ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR_CANDIDATE"
assert data["next_required_validation"] == "ACT_DR6_DFM_MKC_135_ROW_PREDICTION_VECTOR_CANDIDATE"

for token in [
    "DFM-MKC is better than Lambda-CDM",
    "DFM-MKC is worse than Lambda-CDM",
    "DFM-MKC prediction vector exists",
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

print("ACT_DR6_DFM_VS_LCDM_INTERNAL_PROBE_BLOCKED_NO_DFM_VECTOR_OK")
