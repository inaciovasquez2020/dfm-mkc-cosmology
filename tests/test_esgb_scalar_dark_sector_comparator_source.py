import json
import subprocess
from pathlib import Path

ART = Path("artifacts/cosmology/esgb_scalar_dark_sector_comparator_source_2026_05_24.json")
DOC = Path("docs/status/ESGB_SCALAR_DARK_SECTOR_COMPARATOR_SOURCE_2026_05_24.md")

def test_esgb_comparator_record_is_external_only():
    data = json.loads(ART.read_text())
    assert data["status"] == "EXTERNAL_COMPARATOR_SOURCE_RECORD_ONLY"
    assert data["strand"] == "DFM-MKC / cosmology"
    assert data["primary_source"]["arxiv_id"] == "2507.05207v3"
    assert data["primary_source"]["source_classification"] == "external comparator model"

def test_esgb_comparator_record_negative_use_lock():
    text = DOC.read_text()
    for token in [
        "not Chronos proof input",
        "not evidence for R1",
        "not evidence for R2",
        "not evidence for R3",
        "not evidence for NON_FACTORISATION",
        "not evidence for Chronos-RR",
        "not evidence for H4.1/FGL",
        "not evidence for P vs NP",
        "not theorem-level proof input",
    ]:
        assert token in text

def test_esgb_comparator_record_boundary():
    text = DOC.read_text()
    for token in [
        "does not prove DFM-MKC",
        "does not execute a likelihood",
        "does not reject Lambda-CDM",
        "does not validate an alternative cosmology",
        "does not provide Chronos evidence",
        "does not prove R1/R2/R3",
        "does not prove NON_FACTORISATION",
        "does not prove Chronos-RR",
        "does not prove H4.1/FGL",
        "does not prove P vs NP",
        "does not prove any Clay problem",
    ]:
        assert token in text

def test_esgb_comparator_verifier_passes():
    out = subprocess.check_output(
        ["python3", "tools/verify_esgb_scalar_dark_sector_comparator_source.py"],
        text=True,
    )
    assert "ESGB_SCALAR_DARK_SECTOR_COMPARATOR_SOURCE_RECORD_OK" in out
