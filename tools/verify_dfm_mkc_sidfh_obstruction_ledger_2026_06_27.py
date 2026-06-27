#!/usr/bin/env python3
import json
from pathlib import Path

data = json.loads(Path("artifacts/repo_intake/dfm_mkc_sidfh_obstruction_ledger_2026_06_27.json").read_text())

assert data["id"] == "DFM_MKC_SIDFH_OBSTRUCTION_LEDGER_2026_06_27"
assert data["object_type"] == "bounded obstruction ledger for DFM-MKC/SIDFH phase-front sector"
assert len(data["depends_on"]) == 4
assert data["ranked_gaps"][0]["rank"] == 1
assert "same-metric same-stress winding counterexample" in data["ranked_gaps"][0]["gap"]
assert "dark matter is explained" in data["does_not_prove"]
assert "any Clay problem" in data["does_not_prove"]

print("DFM_MKC_SIDFH_OBSTRUCTION_LEDGER_2026_06_27_OK")
