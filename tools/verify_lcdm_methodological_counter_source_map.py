#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/lcdm_methodological_counter_source_map_2026_05_22.json"
DOC = ROOT / "docs/status/LCDM_METHODOLOGICAL_COUNTER_SOURCE_MAP_2026_05_22.md"

REQUIRED_DOES_NOT_PROVE = {
    "Lambda-CDM correctness",
    "Lambda-CDM failure",
    "six-parameter flat Lambda-CDM rejection",
    "DFM-MKC validation",
    "empirical discovery",
    "any Clay problem"
}

FORBIDDEN_PROMOTION_TOKENS = {
    "LCDM_PROVED_FINAL",
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
    assert data["id"] == "LCDM_METHODOLOGICAL_COUNTER_SOURCE_MAP"
    assert data["status"] == "METHODOLOGICAL_COUNTER_SOURCE_ONLY_NO_LCDM_REJECTION"
    assert data["required_next_object"] == "METHODOLOGICAL_CLAIM_EXTRACTION_AND_FALSIFICATION_CRITERION_AUDIT"
    assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))

    assert "does not execute a likelihood" in data["boundary"]
    assert "prove Lambda-CDM final" in data["boundary"]
    assert "reject Lambda-CDM" in data["boundary"]
    assert "validate DFM-MKC" in data["boundary"]
    assert "Clay problem" in data["boundary"]

    sources = data["sources"]
    assert len(sources) == 1
    source = sources[0]
    assert source["id"] == "BLANCHARD_2025_FALLACIES_OF_LCDM_FALSIFICATIONS"
    assert source["doi"] == "10.5772/intechopen.1010549"
    assert source["claim_class"] == "PEER_REVIEWED_METHODOLOGICAL_COUNTER_SOURCE_ONLY"
    assert "falsification-criterion audit" in source["usable_for"]
    assert "executed multiprobe likelihood" in source["not_usable_for"]
    assert "proof that Lambda-CDM is final" in source["not_usable_for"]

    body = json.dumps(data, sort_keys=True)
    for token in FORBIDDEN_PROMOTION_TOKENS:
        assert token not in body, token

    text = DOC.read_text()
    assert data["status"] in text
    assert data["required_next_object"] in text
    assert "Does not prove" in text
    assert "Lambda-CDM correctness" in text
    assert "Lambda-CDM failure" in text
    assert "any Clay problem" in text

    print("Lambda-CDM methodological counter-source map verification OK.")
    print("Status: METHODOLOGICAL_COUNTER_SOURCE_ONLY_NO_LCDM_REJECTION")
    print("Required next object: METHODOLOGICAL_CLAIM_EXTRACTION_AND_FALSIFICATION_CRITERION_AUDIT")

if __name__ == "__main__":
    main()
