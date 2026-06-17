import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_bandpower_projected_cmb_dat_vector_candidate_2026_06_17.json")

required_boundaries = [
    "baseline LCDM prediction vector has been promoted",
    "baseline LCDM prediction vector is official",
    "baseline LCDM prediction vector is physically correct",
    "DFM-MKC prediction vector exists",
    "DFM-MKC prediction vector is correct",
    "ACT DR6 residual eigenspace empirical comparison has been run",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

data = json.loads(ART.read_text())

assert data["id"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_CANDIDATE_2026_06_17"
assert data["status"] == "CANDIDATE_ONLY_NOT_PROMOTED"
assert data["candidate_object"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_CANDIDATE"
assert data["source_sacc_path"] == "data/act_dr6_cmbonly/dr6_data_cmbonly.fits"
assert data["source_theory_file"] == "dr6_lcdm_best_fits/cmb.dat"
assert data["source_theory_parent_payload_sha256"] == "f63d900ac986bd5b5bd3f523556e42b7b4743c13a81547697675432590514992"
assert data["source_theory_file_sha256"] == "8a83622627c48b925f01c8f14347f7a6877f11e87a4a7cedd086366af96f82b1"
assert data["ordering_certificate_id"] == "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_2026_05_25"

assert data["sacc_row_count"] == 135
assert data["candidate_shape"] == [135]
assert data["candidate_finite"] is True
assert len(data["candidate_sha256_input_only_not_artifact"]) == 64
int(data["candidate_sha256_input_only_not_artifact"], 16)

rule = data["projection_rule"]
assert rule["window_weight_shape"] == [8500, 45]
assert "window.weight.T @ cmb_dat" in rule["operation"]
assert rule["blocks"][0]["target_index_range"] == [0, 44]
assert rule["blocks"][0]["data_type"] == "cl_00"
assert rule["blocks"][0]["source_col"] == 1
assert rule["blocks"][1]["target_index_range"] == [45, 89]
assert rule["blocks"][1]["data_type"] == "cl_0e"
assert rule["blocks"][1]["source_col"] == 2
assert rule["blocks"][2]["target_index_range"] == [90, 134]
assert rule["blocks"][2]["data_type"] == "cl_ee"
assert rule["blocks"][2]["source_col"] == 6

assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
assert data["next_required_validation"] == "ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_REPRODUCIBLE_MATERIALIZATION"

for token in required_boundaries:
    assert token in data["does_not_prove"]

print("ACT_DR6_BASELINE_LCDM_BANDPOWER_PROJECTED_CMB_DAT_VECTOR_CANDIDATE_OK")
