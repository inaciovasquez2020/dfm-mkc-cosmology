#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("artifacts/repo_intake/dfm_mkc_sidfh_phase_winding_test_variable_2026_06_27.json")
data = json.loads(path.read_text())

def require(cond, msg):
    if not cond:
        raise SystemExit(msg)

require(data["id"] == "DFM_MKC_SIDFH_PHASE_WINDING_TEST_VARIABLE_2026_06_27", "bad id")
require(data["variable"]["name"] == "n_wind_gamma", "bad variable name")
blob = json.dumps(data, sort_keys=True)
require("(1 / 2pi) integral_gamma dtheta" in blob, "missing winding definition")
require("integer winding number" in blob, "missing integer domain")
require("same Lorentzian metric g" in blob, "missing same metric condition")
require("same DFM-MKC stress-energy tensor T_DFM_MKC" in blob, "missing same stress condition")
require("!=" in data["test_condition"]["separation"], "missing separation condition")
require("Does not claim new physics." in data["guardrails"], "missing new-physics guard")
print("DFM_MKC_SIDFH_PHASE_WINDING_TEST_VARIABLE_2026_06_27_OK")
