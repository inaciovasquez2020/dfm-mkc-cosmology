#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/lcdm_rejection_external_source_map_2026_05_22.json"
DOC = ROOT / "docs/status/LCDM_REJECTION_EXTERNAL_SOURCE_MAP_2026_05_22.md"

EXPECTED_SOURCE_IDS = {
    "KAMELI_BAGHRAM_2025_MODIFIED_INITIAL_POWER_SPECTRUM",
    "SHIMON_2026_SMALL_PATCH_HYPOTHESIS",
    "BULL_ET_AL_2016_BEYOND_LCDM_REVIEW",
}

EXPECTED_INTEGRATION_TARGETS = {
    "MULTIPROBE_LCDM_REJECTION_DATASET_REGISTRY",
    "DESI_DR2_CMB_SN_REJECTION_REPRODUCER",
    "GROWTH_SECTOR_HOLDOUT_COMPATIBILITY_TEST",
    "H0_DISTANCE_LADDER_SYSTEMATICS_PROFILE",
    "ALTERNATIVE_MODEL_STABILITY_SCORECARD",
}

REQUIRED_DOES_NOT_PROVE = {
    "Lambda-CDM failure",
    "six-parameter flat Lambda-CDM rejection",
    "DFM-MKC validation",
    "empirical discovery",
    "any Clay problem",
}

FORBIDDEN_PROMOTION_TOKENS = {
    "LCDM_DISPROVED",
    "LAMBDA_CDM_DISPROVED",
    "EXECUTED_LCDM_REJECTION",
    "DFM_MKC_VALIDATED",
    "EMPIRICAL_DISCOVERY_CLOSED",
}

def main():
    assert ARTIFACT.exists(), ARTIFACT
    assert DOC.exists(), DOC

    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "LCDM_REJECTION_EXTERNAL_SOURCE_MAP"
    assert data["status"] == "EXTERNAL_SOURCE_MAP_ONLY_NO_LCDM_REJECTION"
    assert data["required_next_object"] == "SOURCE_WEIGHTED_MULTIPROBE_LIKELIHOOD_EXECUTION_PLAN"

    source_ids = {source["id"] for source in data["sources"]}
    assert source_ids == EXPECTED_SOURCE_IDS

    integration_targets = set(data["integration_targets"])
    assert integration_targets == EXPECTED_INTEGRATION_TARGETS

    assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))
    assert "does not execute a likelihood" in data["boundary"]
    assert "reject Lambda-CDM" in data["boundary"]
    assert "validate DFM-MKC" in data["boundary"]
    assert "Clay problem" in data["boundary"]

    body = json.dumps(data, sort_keys=True)
    for token in FORBIDDEN_PROMOTION_TOKENS:
        assert token not in body

    for source in data["sources"]:
        assert source["claim_class"].endswith(("ONLY", "PRESSURE_ONLY"))
        assert "Lambda-CDM disproof" in source["not_usable_for"] or "current observational rejection of Lambda-CDM" in source["not_usable_for"] or "new empirical rejection" in source["not_usable_for"]

    doc_text = DOC.read_text()
    assert data["status"] in doc_text
    assert data["required_next_object"] in doc_text
    assert "Does not prove" in doc_text
    assert "Lambda-CDM failure" in doc_text
    assert "any Clay problem" in doc_text

    print("Lambda-CDM external source map verification OK.")
    print("Status: EXTERNAL_SOURCE_MAP_ONLY_NO_LCDM_REJECTION")
    print("Required next object: SOURCE_WEIGHTED_MULTIPROBE_LIKELIHOOD_EXECUTION_PLAN")

if __name__ == "__main__":
    main()
