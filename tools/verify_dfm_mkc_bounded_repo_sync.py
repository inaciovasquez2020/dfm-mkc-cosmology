#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/status/dfm_mkc_bounded_repo_sync_2026_06_09.json"
DOC = ROOT / "docs/status/DFM_MKC_BOUNDED_REPO_SYNC_2026_06_09.md"

REQUIRED_CLOSED_OBJECTS = {
    "repository_native_bounded_status_certificate",
    "concreteAnalyticPackageNextBuildStopLockCertificate",
    "URF_TEXTBOOK_BOUNDED_STATUS_SYNC_2026_06_09",
}

REQUIRED_NONCLAIMS = {
    "new_DFM_MKC_prediction_vector",
    "ACT_DES_Planck_DESI_validation_result",
    "Lambda_CDM_failure_claim",
    "dark_matter_resolution_claim",
    "dark_energy_resolution_claim",
    "gravity_closure_claim",
    "Chronos_RR",
    "H4_FGL",
    "P_vs_NP",
    "Clay_problem_closure",
}

def main() -> int:
    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["status"] == "DFM_MKC_BOUNDED_REPO_SYNC_ONLY"
    assert data["next_admissible_object"] == "Stop"

    objects = {entry["closed_object"] for entry in data["synced_objects"]}
    assert REQUIRED_CLOSED_OBJECTS <= objects

    nonclaims = set(data["dfm_mkc_claims_not_made"])
    assert REQUIRED_NONCLAIMS <= nonclaims

    assert "This sync does not add" in doc
    assert "Lambda-CDM failure claim" in doc
    assert "any Clay-problem closure" in doc

    print("DFM_MKC_BOUNDED_REPO_SYNC_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
