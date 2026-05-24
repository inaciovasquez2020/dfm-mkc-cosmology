#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/cosmology/esgb_scalar_dark_sector_comparator_source_2026_05_24.json")
DOC = Path("docs/status/ESGB_SCALAR_DARK_SECTOR_COMPARATOR_SOURCE_2026_05_24.md")

REQUIRED_JSON_TOP_LEVEL = [
    "record_id",
    "status",
    "strand",
    "primary_source",
    "admissible_use",
    "validated_content_summary",
    "negative_use_lock",
    "additional_source_classification",
    "chronos_boundary",
]

REQUIRED_ADMISSIBLE_USE = [
    "comparator model",
    "dark-sector scalar-field interaction reference",
    "Gauss-Bonnet modified-gravity benchmark",
    "future-data / Roman high-redshift discriminator reference",
]

REQUIRED_NEGATIVE_LOCK = [
    "not Chronos proof input",
    "not evidence for R1",
    "not evidence for R2",
    "not evidence for R3",
    "not evidence for NON_FACTORISATION",
    "not evidence for Chronos-RR",
    "not evidence for H4.1/FGL",
    "not evidence for P vs NP",
    "not theorem-level proof input",
]

REQUIRED_BOUNDARY_TOKENS = [
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
]

def main() -> None:
    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    for key in REQUIRED_JSON_TOP_LEVEL:
        assert key in data, key

    assert data["record_id"] == "ESGB_SCALAR_DARK_SECTOR_COMPARATOR_2507_05207_V3"
    assert data["status"] == "EXTERNAL_COMPARATOR_SOURCE_RECORD_ONLY"
    assert data["strand"] == "DFM-MKC / cosmology"
    assert data["primary_source"]["arxiv_id"] == "2507.05207v3"
    assert data["primary_source"]["source_url"] == "https://arxiv.org/html/2507.05207v3"

    for token in REQUIRED_ADMISSIBLE_USE:
        assert token in data["admissible_use"], token
        assert token in doc, token

    for token in REQUIRED_NEGATIVE_LOCK:
        assert token in data["negative_use_lock"], token
        assert token in doc, token

    for token in REQUIRED_BOUNDARY_TOKENS:
        assert token in doc, token

    classifications = "\n".join(item["classification"] for item in data["additional_source_classification"])
    assert "low-trust/speculative external hypothesis source only; not proof evidence" in classifications
    assert "not dark-sector scalar-field cosmology comparator" in classifications
    assert "not dark-sector scalar-field comparator" in classifications

    print("ESGB_SCALAR_DARK_SECTOR_COMPARATOR_SOURCE_RECORD_OK")

if __name__ == "__main__":
    main()
