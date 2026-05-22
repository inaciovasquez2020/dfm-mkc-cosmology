#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/bound_external_nuisance_prior_sources_and_covariance_policy_records_2026_05_22.json"
DOC = ROOT / "docs/status/BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS_2026_05_22.md"

OBJECT = "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS"
STATUS = "BOUND_SOURCE_RECORD_TARGET_MATERIALIZED_RECORDS_NOT_BOUND"
NEXT = "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS"

def main() -> None:
    if not ARTIFACT.exists():
        raise SystemExit(f"missing artifact: {ARTIFACT}")
    if not DOC.exists():
        raise SystemExit(f"missing status doc: {DOC}")

    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["object"] == OBJECT
    assert data["status"] == STATUS
    assert data["required_next_object"] == NEXT
    assert data["upstream_required_object"] == "EXTERNAL_NUISANCE_PRIOR_SOURCE_TABLE_AND_CROSS_COVARIANCE_POLICY_VALUES"

    required_fields = set(data["required_bound_record_fields"])
    for field in [
        "probe",
        "nuisance_parameter",
        "external_source_identifier",
        "external_source_locator",
        "source_release_or_version",
        "source_digest_sha256",
        "schema_field_path",
        "prior_family",
        "prior_value_or_distribution",
        "cross_covariance_policy",
        "cross_probe_dependency_scope",
        "compatibility_role",
        "certification_status",
    ]:
        assert field in required_fields

    probes = {row["probe"] for row in data["probe_record_targets"]}
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

    for row in data["probe_record_targets"]:
        assert row["record_status"] == "target_only_record_not_supplied"

    for phrase in [
        "likelihood execution",
        "Lambda-CDM rejection",
        "alternative-model validation",
        "DFM-MKC validation",
        "empirical validation",
        "any Clay problem",
    ]:
        assert phrase in data["does_not_prove"]
        assert phrase in doc

    assert STATUS in doc
    assert NEXT in doc
    assert "target surface only" in doc

    print("Bound external nuisance-prior source and covariance-policy records verification OK.")
    print(f"Status: {STATUS}")
    print(f"Required next object: {NEXT}")

if __name__ == "__main__":
    main()
