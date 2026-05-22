import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/bound_external_nuisance_prior_sources_and_covariance_policy_records_2026_05_22.json"
DOC = ROOT / "docs/status/BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS_2026_05_22.md"

def test_bound_external_nuisance_record_target_exists():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS"
    assert data["status"] == "BOUND_SOURCE_RECORD_TARGET_MATERIALIZED_RECORDS_NOT_BOUND"
    assert data["required_next_object"] == "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS"

def test_required_bound_fields_are_explicit():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_bound_record_fields"])
    assert "external_source_identifier" in fields
    assert "external_source_locator" in fields
    assert "source_release_or_version" in fields
    assert "source_digest_sha256" in fields
    assert "schema_field_path" in fields
    assert "cross_covariance_policy" in fields
    assert "cross_probe_dependency_scope" in fields
    assert "certification_status" in fields

def test_probe_record_targets_remain_target_only():
    data = json.loads(ARTIFACT.read_text())
    probes = {row["probe"]: row for row in data["probe_record_targets"]}
    assert "ACT_DR6" in probes
    assert "Planck_2018" in probes
    assert "PantheonPlusSH0ES" in probes
    assert "DESI_DR2_BAO" in probes
    assert "DES_Y6" in probes
    assert "GrowthSector" in probes
    assert "H0DistanceLadder" in probes
    assert all(row["record_status"] == "target_only_record_not_supplied" for row in probes.values())

def test_no_empirical_or_claim_promotion():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    for phrase in [
        "complete certified multiprobe manifest",
        "likelihood execution",
        "Lambda-CDM rejection",
        "alternative-model validation",
        "DFM-MKC validation",
        "empirical validation",
        "any Clay problem",
    ]:
        assert phrase in data["does_not_prove"]
        assert phrase in doc
