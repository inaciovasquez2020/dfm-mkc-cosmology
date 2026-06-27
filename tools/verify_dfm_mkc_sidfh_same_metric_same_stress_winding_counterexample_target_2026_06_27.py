#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("artifacts/repo_intake/dfm_mkc_sidfh_same_metric_same_stress_winding_counterexample_target_2026_06_27.json")
data = json.loads(path.read_text())

def require(cond, msg):
    if not cond:
        raise SystemExit(msg)

require(data["id"] == "DFM_MKC_SIDFH_SAME_METRIC_SAME_STRESS_WINDING_COUNTEREXAMPLE_TARGET_2026_06_27", "bad id")
require(data["depends_on"] == "DFM_MKC_SIDFH_PHASE_FRONT_CHARGE_REDUCIBILITY_TEST_2026_06_27", "bad dependency")
blob = json.dumps(data, sort_keys=True)
for item in [
    "same Lorentzian metric g",
    "same DFM-MKC stress-energy tensor T_DFM_MKC",
    "same dark_front(t)",
    "same closed loop gamma subset dark_front(t)"
]:
    require(item in data["candidate_counterexample"]["shared_requirements"], f"missing shared requirement: {item}")
require("!=" in data["candidate_counterexample"]["separation_requirement"], "missing separation requirement")
require("theta is periodic modulo 2pi" in data["mathematical_mechanism_to_test"], "missing periodic mechanism")
require("global winding may not be determined" in blob, "missing winding mechanism")
require("wall-strengthening theorem" in data["reduction_outcome"], "missing reduction outcome")
require("nonmetric DFM-MKC/SIDFH residual" in data["nonreduction_outcome"], "missing nonreduction outcome")
require("Does not claim the counterexample exists." in data["guardrails"], "missing existence guard")
require("Does not claim new physics." in data["guardrails"], "missing new-physics guard")
print("DFM_MKC_SIDFH_SAME_METRIC_SAME_STRESS_WINDING_COUNTEREXAMPLE_TARGET_2026_06_27_OK")
