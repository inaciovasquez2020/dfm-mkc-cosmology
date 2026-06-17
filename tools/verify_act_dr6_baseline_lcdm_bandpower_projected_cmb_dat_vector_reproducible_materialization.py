import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_reproducible_materialization_2026_06_17.json")

data = json.loads(ART.read_text())

assert data["id"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_REPRODUCIBLE_MATERIALIZATION_2026_06_17"
assert data["status"] == "REPRODUCIBLE_MATERIALIZATION_NUMERIC_TOLERANCE_PASSED_RAW_BYTE_SHA_UNSTABLE_CANDIDATE_STILL_NOT_PROMOTED"
assert data["materializes_candidate"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_CANDIDATE_2026_06_17"
assert data["source_sacc_path"] == "data/act_dr6_cmbonly/dr6_data_cmbonly.fits"
assert data["source_theory_file"] == "dr6_lcdm_best_fits/cmb.dat"
assert data["source_theory_file_sha256"] == "8a83622627c48b925f01c8f14347f7a6877f11e87a4a7cedd086366af96f82b1"
assert data["ordering_certificate_id"] == "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_2026_05_25"

assert data["computed_shape"] == [135]
assert data["computed_finite"] is True
assert data["numeric_tolerance"] == 1e-9
assert data["max_abs_diff_against_candidate_samples"] <= data["numeric_tolerance"]

assert len(data["candidate_raw_byte_sha256"]) == 64
assert len(data["observed_raw_byte_sha256"]) == 64
assert data["raw_byte_sha256_match"] is False
assert len(data["canonical_decimal_sha256"]) == 64
int(data["canonical_decimal_sha256"], 16)
assert data["canonical_decimal_precision"] == ".12g"

assert data["projection_operation"] == "sum(window.weight * cmb.dat source column over ell values 2..8501, axis=0)"

assert len(data["blocks"]) == 3
assert data["blocks"][0]["data_type"] == "cl_00"
assert data["blocks"][0]["target_index_range"] == [0, 44]
assert data["blocks"][0]["source_col"] == 1
assert data["blocks"][1]["data_type"] == "cl_0e"
assert data["blocks"][1]["target_index_range"] == [45, 89]
assert data["blocks"][1]["source_col"] == 2
assert data["blocks"][2]["data_type"] == "cl_ee"
assert data["blocks"][2]["target_index_range"] == [90, 134]
assert data["blocks"][2]["source_col"] == 6

for block in data["blocks"]:
    assert block["computed_shape"] == [45]
    assert len(block["head"]) == 5
    assert len(block["tail"]) == 5
    assert block["max_abs_diff_against_candidate_head"] <= data["numeric_tolerance"]

assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
assert data["next_required_validation"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_OFFICIAL_CONVENTION_AUDIT"

for token in [
    "baseline LCDM prediction vector has been promoted",
    "baseline LCDM prediction vector is official",
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

print("ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_REPRODUCIBLE_MATERIALIZATION_OK")
