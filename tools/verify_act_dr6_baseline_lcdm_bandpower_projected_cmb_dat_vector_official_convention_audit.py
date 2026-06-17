
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_official_convention_audit_2026_06_17.json")
data = json.loads(ART.read_text())

assert data["id"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_OFFICIAL_CONVENTION_AUDIT_2026_06_17"
assert data["status"] == "OFFICIAL_CONVENTION_AUDIT_PARTIAL_PASS_FOREGROUND_COMPARISON_STILL_BLOCKED_CANDIDATE_NOT_PROMOTED"
assert data["audits_candidate"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_CANDIDATE_2026_06_17"
assert data["audits_materialization"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_REPRODUCIBLE_MATERIALIZATION_2026_06_17"

q = data["audit_questions"]
assert q["is_cmb_dat_dell_or_cell"]["answer"] == "D_ell"
assert q["is_cmb_dat_dell_or_cell"]["status"] == "PASSED"
assert "Dl_*" in q["is_cmb_dat_dell_or_cell"]["basis"]

assert q["are_tt_te_ee_columns_1_2_6_correct"]["answer"] is True
assert q["are_tt_te_ee_columns_1_2_6_correct"]["status"] == "PASSED"
assert "Dl_TT" in q["are_tt_te_ee_columns_1_2_6_correct"]["basis"]
assert "Dl_TE" in q["are_tt_te_ee_columns_1_2_6_correct"]["basis"]
assert "Dl_EE" in q["are_tt_te_ee_columns_1_2_6_correct"]["basis"]

assert q["are_sacc_windows_applied_to_dell_or_cell"]["status"] == "PASSED_FOR_CANDIDATE_NOT_PROMOTION"
assert q["is_foreground_or_cmb_only_convention_missing"]["answer"] is True
assert q["is_foreground_or_cmb_only_convention_missing"]["status"] == "BLOCKED"
assert "foreground" in q["is_foreground_or_cmb_only_convention_missing"]["basis"]

assert q["is_135_row_ordering_exact"]["status"] == "PASSED_FOR_CANDIDATE_NOT_PROMOTION"
assert "0..44" in q["is_135_row_ordering_exact"]["basis"]
assert "45..89" in q["is_135_row_ordering_exact"]["basis"]
assert "90..134" in q["is_135_row_ordering_exact"]["basis"]

assert "ACT_DR6_BASELINE_LCDM_CMB_ONLY_VS_CMB_AND_FOREGROUND_COMPARISON_BINDING_AUDIT" in data["remaining_blockers"]
assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
assert data["next_required_validation"] == "ACT_DR6_BASELINE_LCDM_CMB_ONLY_VS_CMB_AND_FOREGROUND_COMPARISON_BINDING_AUDIT"

for token in [
    "baseline LCDM prediction vector has been promoted",
    "baseline LCDM prediction vector is final official ACT comparison vector",
    "cmb.dat alone is the final official foreground-aware baseline comparison",
    "DFM-MKC prediction vector exists",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "gravity closure",
    "P vs NP",
    "any Clay problem",
]:
    assert token in data["does_not_prove"]

print("ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_OFFICIAL_CONVENTION_AUDIT_OK")
