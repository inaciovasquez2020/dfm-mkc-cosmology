import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/covariance_spectral_validation_source_map_2026_05_25.json")
DOC = Path("docs/status/COVARIANCE_SPECTRAL_VALIDATION_SOURCE_MAP_2026_05_25.md")

def test_covariance_spectral_validation_source_map_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_covariance_spectral_validation_source_map.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "COVARIANCE_SPECTRAL_VALIDATION_SOURCE_MAP_OK" in result.stdout

def test_physical_phase_claims_remain_hypothesis_only():
    data = json.loads(ART.read_text())
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]

def test_empirical_promotion_requires_covariance_and_spectral_diagnostics():
    data = json.loads(ART.read_text())
    reqs = set(data["promotion_requirements"])
    assert "Authentic covariance matrix supplied" in reqs
    assert "Residual covariance diagnostic reported" in reqs
    assert "Residual eigenspectrum diagnostic reported" in reqs
    assert "Residual eigenspace diagnostic reported" in reqs
    assert "Boundary covariance failure guard passed" in reqs

def test_status_doc_contains_no_overclaim_boundaries():
    text = DOC.read_text()
    assert "SOURCE_MAP_AND_REQUIREMENT_LAYER_ONLY" in text
    assert "HYPOTHESIS_ONLY" in text
    assert "This is not a physical dark-matter mechanism" in text
    assert "DFM-MKC empirical validation" in text
    assert "Lambda-CDM failure" in text
    assert "dark matter resolution" in text
