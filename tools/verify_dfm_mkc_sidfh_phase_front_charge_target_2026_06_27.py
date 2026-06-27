#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("artifacts/repo_intake/dfm_mkc_sidfh_phase_front_charge_target_2026_06_27.json")
data = json.loads(path.read_text())

def require(cond, msg):
    if not cond:
        raise SystemExit(msg)

require(data["id"] == "DFM_MKC_SIDFH_PHASE_FRONT_CHARGE_TARGET_2026_06_27", "bad id")
require(data["status"] == "candidate_nonmetric_object_only", "bad status")
blob = json.dumps(data, sort_keys=True)
require("theta : M -> R / 2pi Z" in blob, "missing periodic theta")
require("PhaseFrontCharge" in blob, "missing PhaseFrontCharge")
require("integral_gamma dtheta" in blob, "missing charge integral")
require("Does not claim new physics." in data["guardrails"], "missing new-physics guard")
require("Does not claim PhaseFrontCharge is independent." in data["guardrails"], "missing independence guard")
require("wall-strengthening reduction" in blob, "missing reduction outcome")
require("candidate nonmetric SIDFH residual" in blob, "missing nonreduction outcome")
print("DFM_MKC_SIDFH_PHASE_FRONT_CHARGE_TARGET_2026_06_27_OK")
