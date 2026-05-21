#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_unfixed_2026_05_21.json")
STATUS_DOC = Path("docs/status/DFM_MKC_ACTDR6_NUMERICAL_DATA_UNFIXED_2026_05_21.md")

EXPECTED_STATUS = "ACTDR6_NUMERICAL_DATA_UNFIXED_EXTRACTED_FROM_AUTHENTIC_PAYLOAD"
EXPECTED_PAYLOAD_SHA256 = "9506da7b482c10b60571c5a3805fc392853d50f81244485754566d21b85219ad"
EXPECTED_LENGTH = 127
EXPECTED_BLOCK_LENGTHS = {
    "data:cl_00": 45,
    "data:cl_0e": 40,
    "data:cl_ee": 42,
}

REQUIRED_BOUNDARY = [
    "numerical data extraction only",
    "uses ACT-lite SACC FITS payload already present locally",
    "data vector extracted from value columns of data:cl_00, data:cl_0e, and data:cl_ee",
    "covariance matrix extracted from covariance image HDU",
    "mask inferred as all-active because no explicit mask HDU is present",
    "does not bind a DFM-MKC likelihood rule",
    "does not execute the likelihood",
    "does not compute residuals",
    "does not supply empirical evidence",
    "does not promote any empirical slot",
]

REQUIRED_NONCLAIMS = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing artifact: {ARTIFACT}")
    if not STATUS_DOC.exists():
        fail(f"missing status doc: {STATUS_DOC}")

    data = json.loads(ARTIFACT.read_text())
    status_text = STATUS_DOC.read_text()

    if data.get("status") != EXPECTED_STATUS:
        fail("unexpected status")

    if data["payload"]["sha256"] != EXPECTED_PAYLOAD_SHA256:
        fail("payload sha256 mismatch")

    vector = data["data_vector"]["values"]
    covariance = data["covariance_matrix"]["values"]
    mask = data["mask"]["values"]

    if data["data_vector"]["length"] != EXPECTED_LENGTH:
        fail("wrong data vector length")
    if len(vector) != EXPECTED_LENGTH:
        fail("wrong data vector value count")
    if data["covariance_matrix"]["shape"] != [EXPECTED_LENGTH, EXPECTED_LENGTH]:
        fail("wrong covariance shape")
    if len(covariance) != EXPECTED_LENGTH:
        fail("wrong covariance row count")
    if any(len(row) != EXPECTED_LENGTH for row in covariance):
        fail("wrong covariance column count")
    if data["mask"]["length"] != EXPECTED_LENGTH:
        fail("wrong mask length")
    if mask != [True] * EXPECTED_LENGTH:
        fail("mask is not all-active")

    block_lengths = {block["hdu"]: block["length"] for block in data["data_blocks"]}
    if block_lengths != EXPECTED_BLOCK_LENGTHS:
        fail(f"wrong block lengths: {block_lengths}")

    for boundary in REQUIRED_BOUNDARY:
        if boundary not in data["boundary"]:
            fail(f"missing artifact boundary: {boundary}")
        if boundary not in status_text:
            fail(f"missing status boundary: {boundary}")

    for nonclaim in REQUIRED_NONCLAIMS:
        if nonclaim not in data["does_not_prove"]:
            fail(f"missing artifact nonclaim: {nonclaim}")
        if nonclaim not in status_text:
            fail(f"missing status nonclaim: {nonclaim}")

    print("DFM-MKC ACTDR6 numerical data unfixed verifier OK.")
    print(f"Status: {EXPECTED_STATUS}")
    print(f"Data length: {EXPECTED_LENGTH}")
    print("Covariance shape: 127 x 127")

if __name__ == "__main__":
    main()
