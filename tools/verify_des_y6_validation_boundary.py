from pathlib import Path
import json

freeze = json.loads(Path("config/dfm_mkc_parameter_freeze.json").read_text())
manifest = json.loads(Path("data/des_y6/AUTHENTIC_INPUT_MANIFEST.json").read_text())
status = Path("docs/status/DFM_MKC_DES_Y6_VALIDATION_STATUS_2026_05_11.md").read_text()

assert freeze["status"] == "PARAMETER_RULES_FROZEN_BEFORE_DES_Y6_COMPARISON"
assert manifest["status"] == "AWAITING_AUTHENTIC_DES_Y6_MACHINE_READABLE_INPUT"

required_boundary = [
    "No final cosmological truth",
    "No DFM-MKC over Lambda-CDM theorem",
    "No theorem-level URF cosmology closure",
    "No empirical superiority claim before authentic DES Y6 input and baseline comparison",
]

for phrase in required_boundary:
    assert phrase in status

forbidden = [
    "DFM-MKC proves final cosmological truth",
    "DFM-MKC unconditionally beats Lambda-CDM",
    "URF cosmology closure is proved",
]

positive_claim_surface = status

for phrase in forbidden:
    assert phrase not in positive_claim_surface

print("DFM-MKC DES Y6 validation boundary verified.")
