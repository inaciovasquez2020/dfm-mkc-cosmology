import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/status/act_dr6_release_hash_boundary_receipt.json"

assert ARTIFACT.exists(), "missing ACT DR6 release hash boundary receipt"

data = json.loads(ARTIFACT.read_text())

assert data["object"] == "ACT_DR6_RELEASE_HASH_BOUNDARY_RECEIPT"
assert data["status"] == "EXTERNAL_DIGEST_NOT_SUPPLIED"
assert data["scope"] == "BOUNDARY_RECEIPT_ONLY"
assert "no independent release digest supplied" in data["non_claims"]
assert "no likelihood execution performed" in data["non_claims"]

print("ACT_DR6_RELEASE_HASH_BOUNDARY_RECEIPT_OK")
