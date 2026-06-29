#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

artifact = Path("artifacts/external_validation/desi_dr2_bao_input_packet_2026_06_29.json")
if not artifact.exists():
    raise SystemExit("MISSING_OBJECT := artifacts/external_validation/desi_dr2_bao_input_packet_2026_06_29.json")

data = json.loads(artifact.read_text())

required_boundary = {
    "no_lcdm_refutation_claim",
    "no_dfm_mkc_cosmology_validation_claim",
    "no_strict_w0wa_schema_constraint",
    "no_chi_squared_likelihood_claim",
}
if not required_boundary.issubset(set(data.get("boundary", []))):
    raise SystemExit("MISSING_OBJECT := boundary_nonclaim_guard")

for key in ("h0_residuals_csv", "s8_consistency_csv"):
    p = Path(data["repository_targets"][key])
    if not p.exists():
        raise SystemExit(f"MISSING_OBJECT := {p}")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

files = data.get("files", [])
if not files:
    raise SystemExit("MISSING_OBJECT := desi_dr2_bao_input_files")

for item in files:
    p = Path(item["path"])
    if not p.exists():
        raise SystemExit(f"MISSING_OBJECT := {p}")
    if sha256(p) != item["sha256"]:
        raise SystemExit(f"SHA256_MISMATCH := {p}")

print("DESI_DR2_BAO_INPUT_PACKET_OK")
