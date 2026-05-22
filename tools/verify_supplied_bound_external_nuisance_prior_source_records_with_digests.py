#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/supplied_bound_external_nuisance_prior_source_records_with_digests_2026_05_22.json"
DOC = ROOT / "docs/status/SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS_2026_05_22.md"

OBJECT = "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS"
STATUS = "SUPPLIED_BOUND_RECORD_TARGET_MATERIALIZED_RECORD_PAYLOADS_NOT_SUPPLIED"
NEXT = "REAL_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_DIGESTS_SCHEMA_PATHS_AND_POLICY_VALUES"

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["object"] == OBJECT
    assert data["status"] == STATUS
    assert data["required_next_object"] == NEXT
    assert data["upstream_required_object"] == "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS"

    fields = set(data["record_schema"]["required_fields"])
    for field in [
        "external_source_identifier",
        "external_source_locator",
        "source_release_or_version",
        "source_digest_sha256",
        "schema_field_path",
        "prior_value_or_distribution",
        "cross_covariance_policy",
        "cross_probe_dependency_scope",
        "certification_status",
    ]:
        assert field in fields

    probes = {row["probe"]: row for row in data["required_probe_records"]}
    for probe in [
        "ACT_DR6",
        "Planck_2018",
        "PantheonPlusSH0ES",
        "DESI_DR2_BAO",
        "DES_Y6",
        "GrowthSector",
        "H0DistanceLadder",
    ]:
        assert probe in probes
        assert probes[probe]["record_status"] == "payload_not_supplied"

    for item in [
        "complete certified multiprobe manifest",
        "likelihood execution",
        "DFM-MKC versus Lambda-CDM comparison",
        "Lambda-CDM rejection",
        "DFM-MKC validation",
        "empirical validation",
        "any Clay problem",
    ]:
        assert item in data["does_not_prove"]
        assert item in doc

    assert STATUS in doc
    assert NEXT in doc
    print("Supplied bound external nuisance-prior source records with digests verification OK.")
    print(f"Status: {STATUS}")
    print(f"Required next object: {NEXT}")

if __name__ == "__main__":
    main()
