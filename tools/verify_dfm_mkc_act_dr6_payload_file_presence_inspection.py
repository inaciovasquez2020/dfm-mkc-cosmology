#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_act_dr6_payload_file_presence_inspection_2026_05_21.json")
STATUS_DOC = Path("docs/status/DFM_MKC_ACT_DR6_PAYLOAD_FILE_PRESENCE_INSPECTION_2026_05_21.md")

PAYLOAD_CANDIDATES = [
    Path("artifacts/public_payloads/act_lite_numeric_like_extracted_2026_05_21/DR6-ACT-lite-main__act_dr6_cmbonly__data__act_dr6_cmb_sacc.fits"),
    Path("artifacts/public_payloads/act_dr6_act_lite_main_2026_05_21.zip"),
]

REQUIRED_BOUNDARIES = [
    "payload file-presence inspection only",
    "does not extract a numerical data vector",
    "does not extract a covariance matrix",
    "does not bind protocol fields to FITS HDUs",
    "does not execute the likelihood",
    "does not compute residuals",
    "does not supply empirical evidence",
    "does not promote any empirical slot",
]

REQUIRED_NONCLAIMS = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical inspection",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing artifact: {ARTIFACT}")
    if not STATUS_DOC.exists():
        fail(f"missing status doc: {STATUS_DOC}")

    data = json.loads(ARTIFACT.read_text())
    text = STATUS_DOC.read_text()

    if data.get("status") != "ACT_DR6_PAYLOAD_FILE_PRESENCE_INSPECTED_NO_SCHEMA_VALIDATION":
        fail("unexpected status")
    if data.get("predecessor", {}).get("pull_request") != 104:
        fail("missing predecessor PR #104")
    if data.get("predecessor", {}).get("merge_commit") != "920c260":
        fail("missing predecessor merge commit 920c260")

    payload = data.get("inspected_payload", {})
    payload_path = Path(payload.get("path", ""))

    if payload_path not in PAYLOAD_CANDIDATES:
        fail(f"unexpected payload path: {payload_path}")
    if not payload_path.exists():
        fail(f"payload file does not exist: {payload_path}")
    if not payload_path.is_file():
        fail(f"payload path is not a file: {payload_path}")
    if payload_path.stat().st_size <= 0:
        fail(f"payload file is empty: {payload_path}")

    digest = sha256_file(payload_path)
    if payload.get("sha256") != digest:
        fail("payload sha256 mismatch")
    if payload.get("size_bytes") != payload_path.stat().st_size:
        fail("payload size mismatch")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in data.get("boundary", []):
            fail(f"missing artifact boundary: {boundary}")
        if boundary not in text:
            fail(f"missing status boundary: {boundary}")

    for nonclaim in REQUIRED_NONCLAIMS:
        if nonclaim not in data.get("does_not_prove", []):
            fail(f"missing artifact nonclaim: {nonclaim}")
        if nonclaim not in text:
            fail(f"missing status nonclaim: {nonclaim}")

    print("DFM-MKC ACT DR6 payload file-presence inspection verification OK.")
    print(f"Status: {data['status']}")
    print(f"Payload: {payload_path}")
    print(f"sha256: {digest}")

if __name__ == "__main__":
    main()
