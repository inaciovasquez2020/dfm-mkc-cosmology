import hashlib
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_sacc_actual_value_binding_witness_2026_05_28.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_SACC_ACTUAL_VALUE_BINDING_WITNESS_2026_05_28.md")

required_boundaries = [
    "baseline LCDM prediction vector",
    "DFM-MKC prediction vector",
    "likelihood execution",
    "empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "dark energy replacement",
    "gravity closure",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
actual = data["actual_values"]
payload = Path(actual["payload_path"])

assert data["status"] == "ACTUAL_VALUE_BINDING_WITNESS_ONLY_NO_NUMERICAL_VECTOR"
assert data["object"] == "ACTDR6BaselineLCDM_SACC_ToBestFitLabelBindingRule actual-value witness"

assert payload.exists()
payload_bytes = payload.read_bytes()
assert len(payload_bytes) == actual["payload_size_bytes"]
assert actual["payload_size_bytes"] > 0
assert hashlib.sha256(payload_bytes).hexdigest() == actual["payload_sha256"]
assert len(actual["payload_sha256"]) == 64
int(actual["payload_sha256"], 16)

assert actual["payload_sha256_hex_length"] == 64
assert actual["schema_pass_flag"] is True
assert actual["schema_pass_integer"] == 1
assert actual["baseline_lcdm_label"] == "ACT_DR6_CMBONLY_BASELINE_LCDM_BESTFIT"
assert actual["required_field_count"] == 5

for token in required_boundaries:
    assert token in data["does_not_prove"]
    assert token in doc

print("ACT_DR6_BASELINE_LCDM_SACC_ACTUAL_VALUE_BINDING_WITNESS_OK")
