import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/supplied_bound_external_nuisance_prior_source_records_with_digests_2026_05_22.json"
DOC = ROOT / "docs/status/SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS_2026_05_22.md"

def test_supplied_bound_record_target_exists():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS"
    assert data["status"] == "SUPPLIED_BOUND_RECORD_TARGET_MATERIALIZED_RECORD_PAYLOADS_NOT_SUPPLIED"
    assert data["required_next_object"] == "REAL_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_DIGESTS_SCHEMA_PATHS_AND_POLICY_VALUES"

def test_required_payload_schema_is_explicit():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["record_schema"]["required_fields"])
    assert "source_digest_sha256" in fields
    assert "schema_field_path" in fields
    assert "cross_covariance_policy" in fields
    assert "cross_probe_dependency_scope" in fields

def test_all_probe_payloads_remain_unsupplied():
    data = json.loads(ARTIFACT.read_text())
    assert len(data["required_probe_records"]) == 7
    assert all(row["record_status"] == "payload_not_supplied" for row in data["required_probe_records"])

def test_no_claim_promotion():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    for phrase in [
        "likelihood execution",
        "DFM-MKC versus Lambda-CDM comparison",
        "Lambda-CDM rejection",
        "DFM-MKC validation",
        "empirical validation",
        "any Clay problem",
    ]:
        assert phrase in data["does_not_prove"]
        assert phrase in doc
