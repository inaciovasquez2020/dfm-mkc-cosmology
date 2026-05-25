#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/covariance_spectral_validation_source_map_2026_05_25.json")
DOC = Path("docs/status/COVARIANCE_SPECTRAL_VALIDATION_SOURCE_MAP_2026_05_25.md")

REQUIRED_OBJECTS = {
    "COVARIANCE_SPECTRAL_VALIDATION_SOURCE_MAP",
    "HIGH_DIMENSIONAL_RESIDUAL_EIGENSPACE_TEST_TARGET",
    "BOUNDARY_COVARIANCE_ESTIMATE_FAILURE_GUARD",
    "DFM_MKC_COMPARATOR_COVARIANCE_DIAGNOSTIC_REQUIREMENT",
}

REQUIRED_BOUNDARIES = {
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "ACT validation",
    "DES validation",
    "CMB validation",
    "BAO validation",
    "independent empirical replication",
    "gravity closure",
    "Chronos proof input",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

REQUIRED_PROMOTION_REQUIREMENTS = {
    "Authentic data vector supplied",
    "Authentic covariance matrix supplied",
    "Covariance matrix schema validated",
    "Covariance matrix positive semidefinite or justified regularized substitute certified",
    "Baseline Lambda-CDM comparator executed",
    "DFM-MKC comparator executed",
    "Residual covariance diagnostic reported",
    "Residual eigenspectrum diagnostic reported",
    "Residual eigenspace diagnostic reported",
    "Boundary covariance failure guard passed",
    "Independent reproduction command supplied",
}

def main() -> None:
    assert ART.exists(), ART
    assert DOC.exists(), DOC

    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["id"] == "COVARIANCE_SPECTRAL_VALIDATION_SOURCE_MAP_2026_05_25"
    assert data["status"] == "SOURCE_MAP_AND_REQUIREMENT_LAYER_ONLY"
    assert data["program"] == "DFM_MKC_DARK_SECTOR_VALIDATION"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"

    object_ids = {obj["id"] for obj in data["objects_added"]}
    assert REQUIRED_OBJECTS <= object_ids

    promotion_requirements = set(data["promotion_requirements"])
    assert REQUIRED_PROMOTION_REQUIREMENTS <= promotion_requirements

    boundaries = set(data["does_not_prove"])
    assert REQUIRED_BOUNDARIES <= boundaries

    source_labels = "\n".join(src["label"] for src in data["source_map"])
    assert "Generalized linear spectral statistics" in source_labels
    assert "Covariance Estimation" in source_labels
    assert "Non-boundary covariance matrix estimation" in source_labels
    assert "Symmetry volume 18 issue 2" in source_labels

    for token in REQUIRED_OBJECTS:
        assert token in doc, token

    assert "HYPOTHESIS_ONLY" in doc
    assert "SOURCE_MAP_AND_REQUIREMENT_LAYER_ONLY" in doc

    for token in REQUIRED_BOUNDARIES:
        assert token in doc, token

    print("COVARIANCE_SPECTRAL_VALIDATION_SOURCE_MAP_OK")

if __name__ == "__main__":
    main()
