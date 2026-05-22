#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/lcdm_popular_critique_source_map_2026_05_22.json"
DOC = ROOT / "docs/status/LCDM_POPULAR_CRITIQUE_SOURCE_MAP_2026_05_22.md"

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
    "ALTERNATIVE_MODEL_VALIDATED"
}

def main():
    assert ARTIFACT.exists(), ARTIFACT
    assert DOC.exists(), DOC
    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "LCDM_POPULAR_CRITIQUE_SOURCE_MAP"
    assert data["status"] == "POPULAR_CRITIQUE_SOURCE_ONLY_NO_LCDM_REJECTION"
    assert data["required_next_object"] == "POPULAR_CRITIQUE_CLAIM_EXTRACTION_AND_EVIDENCE_AUDIT"
    assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))
    assert "does not execute a likelihood" in data["boundary"]
    assert "reject Lambda-CDM" in data["boundary"]
    assert "validate DFM-MKC" in data["boundary"]
    assert "Clay problem" in data["boundary"]

    sources = data["sources"]
    assert len(sources) == 1
    source = sources[0]
    assert source["id"] == "KRIGER_2026_BANKRUPT_COSMOLOGY_MEDIUM"
    assert source["claim_class"] == "POPULAR_POLEMICAL_CRITIQUE_ONLY"
    assert "peer-reviewed empirical evidence" in source["not_usable_for"]
    assert "executed multiprobe likelihood" in source["not_usable_for"]

    body = json.dumps(data, sort_keys=True)
    for token in FORBIDDEN_PROMOTION_TOKENS:
        assert token not in body, token

    text = DOC.read_text()
    assert data["status"] in text
    assert data["required_next_object"] in text
    assert "Does not prove" in text
    assert "Lambda-CDM failure" in text
    assert "any Clay problem" in text

    print("Lambda-CDM popular critique source map verification OK.")
    print("Status: POPULAR_CRITIQUE_SOURCE_ONLY_NO_LCDM_REJECTION")
    print("Required next object: POPULAR_CRITIQUE_CLAIM_EXTRACTION_AND_EVIDENCE_AUDIT")

if __name__ == "__main__":
    main()
