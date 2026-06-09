from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/status/dfm_mkc_bounded_repo_sync_2026_06_09.json"
DOC = ROOT / "docs/status/DFM_MKC_BOUNDED_REPO_SYNC_2026_06_09.md"
VERIFY = ROOT / "tools/verify_dfm_mkc_bounded_repo_sync.py"

def test_dfm_mkc_bounded_repo_sync_artifact():
    data = json.loads(ART.read_text())
    assert data["status"] == "DFM_MKC_BOUNDED_REPO_SYNC_ONLY"
    assert data["next_admissible_object"] == "Stop"
    assert len(data["synced_objects"]) == 3
    assert "Lambda_CDM_failure_claim" in data["dfm_mkc_claims_not_made"]
    assert "Clay_problem_closure" in data["dfm_mkc_claims_not_made"]

def test_dfm_mkc_bounded_repo_sync_doc_boundary():
    text = DOC.read_text()
    assert "DFM_MKC_BOUNDED_REPO_SYNC_ONLY" in text
    assert "repository_native_bounded_status_certificate" in text
    assert "concreteAnalyticPackageNextBuildStopLockCertificate" in text
    assert "URF_TEXTBOOK_BOUNDED_STATUS_SYNC_2026_06_09" in text
    assert "This sync does not add" in text
    assert "P vs NP" in text

def test_dfm_mkc_bounded_repo_sync_verifier():
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "DFM_MKC_BOUNDED_REPO_SYNC_OK" in result.stdout
