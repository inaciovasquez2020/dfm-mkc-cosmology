#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("artifacts/repo_intake/dfm_mkc_sidfh_phase_front_charge_reducibility_test_2026_06_27.json")
data = json.loads(path.read_text())

def require(cond, msg):
    if not cond:
        raise SystemExit(msg)

require(data["id"] == "DFM_MKC_SIDFH_PHASE_FRONT_CHARGE_REDUCIBILITY_TEST_2026_06_27", "bad id")
require(data["depends_on"] == "DFM_MKC_SIDFH_PHASE_FRONT_CHARGE_TARGET_2026_06_27", "bad dependency")
blob = json.dumps(data, sort_keys=True)
require("PhaseFrontCharge(t,gamma)" in blob, "missing tested object")
require("uniquely determined" in data["reducibility_question"], "missing reducibility question")
for item in ["same g", "same T_DFM_MKC", "same dark_front(t)", "same gamma"]:
    require(item in data["counterexample_shape"]["same_data_requirements"], f"missing {item}")
require("!=" in data["counterexample_shape"]["separation_requirement"], "missing separation requirement")
require("wall-strengthening reduction" in data["reduction_outcome"], "missing reduction outcome")
require("nonmetric DFM-MKC/SIDFH residual" in data["nonreduction_outcome"], "missing nonreduction outcome")
require("Does not claim new physics." in data["guardrails"], "missing new-physics guard")
require("Does not claim independence." in data["guardrails"], "missing independence guard")
print("DFM_MKC_SIDFH_PHASE_FRONT_CHARGE_REDUCIBILITY_TEST_2026_06_27_OK")
