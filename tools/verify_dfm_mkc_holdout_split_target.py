#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_holdout_split_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_HOLDOUT_SPLIT_TARGET_2026_05_21.md"

EXPECTED_STATUS = "HOLDOUT_SPLIT_TARGET_ONLY_NOT_SUPPLIED"

EXPECTED_UPSTREAM = {
    "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL",
    "DFM_PARAMETER_MAP",
    "DFM_OBSERVABLE_PREDICTION_RULES",
    "DFM_FROZEN_PREDICTION_VECTOR",
    "DFM_LIKELIHOOD_RULE",
    "DFM_EXTERNAL_DATA_MANIFEST",
}

EXPECTED_FIELDS = {
    "split_identifier",
    "split_timestamp",
    "source_commit",
    "registered_data_manifest_reference",
    "frozen_prediction_vector_reference",
    "likelihood_rule_reference",
    "training_data_sources",
    "validation_data_sources",
    "holdout_data_sources",
    "blind_data_sources",
    "data_access_status",
    "pre_unblinding_allowed_operations",
    "post_unblinding_forbidden_operations",
    "parameter_freeze_reference",
    "prediction_freeze_reference",
    "likelihood_freeze_reference",
    "no_post_hoc_tuning_certificate",
    "failure_thresholds",
    "model_comparison_metrics",
    "reproduction_command",
}

EXPECTED_PROBES = {
    "CMB_TT_TE_EE",
    "CMB_LENSING",
    "BAO_DISTANCES",
    "SNIA_DISTANCES",
    "WEAK_LENSING_AND_CLUSTERING",
    "CLUSTER_ABUNDANCE",
}

EXPECTED_DOWNSTREAM = {
    "DFM_HOLDOUT_SPLIT_EXECUTION",
    "DFM_VS_LAMBDA_CDM_COMPARISON",
    "DFM_EMPIRICAL_EVIDENCE_CLAIM",
    "DFM_CDM_REPLACEMENT_CLAIM",
}

EXPECTED_BOUNDARY = [
    "Target schema only.",
    "Does not assign training data.",
    "Does not assign validation data.",
    "Does not assign blind holdout data.",
    "Does not execute holdout evaluation.",
    "Does not supply DFM field equations.",
    "Does not supply DFM action functional.",
    "Does not supply DFM parameter map.",
    "Does not supply DFM observable prediction rules.",
    "Does not supply frozen DFM prediction values.",
    "Does not supply likelihood equations.",
    "Does not execute any likelihood.",
    "Does not produce empirical evidence.",
    "Does not prove DFM.",
    "Does not disprove Lambda-CDM.",
    "Does not replace CDM.",
]

EXPECTED_DOES_NOT_PROVE = {
    "DFM",
    "Lambda-CDM failure",
    "CDM replacement",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
}

def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    return json.loads(path.read_text())

def verify_artifact(data: dict) -> None:
    assert data["artifact"] == "DFM_MKC_HOLDOUT_SPLIT_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["holdout_split_supplied"] is False
    assert data["holdout_execution_supplied"] is False
    assert data["training_split_supplied"] is False
    assert data["validation_split_supplied"] is False
    assert data["test_split_supplied"] is False
    assert data["blind_protocol_supplied"] is False
    assert data["no_post_hoc_tuning_certificate_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["root_blocker"] == "DFM_HOLDOUT_SPLIT_NOT_SUPPLIED"

    assert EXPECTED_UPSTREAM <= set(data["upstream_required_objects"])
    assert EXPECTED_FIELDS <= set(data["required_holdout_split_fields"])
    assert EXPECTED_PROBES == set(data["required_probe_coverage"].keys())

    for role in data["candidate_data_source_roles"].values():
        assert role["status"] == "blocked_no_holdout_split"

    for probe in data["required_probe_coverage"].values():
        assert probe["status"] == "blocked_no_holdout_assignment"

    assert EXPECTED_DOWNSTREAM <= set(data["downstream_blocked_objects"])

    boundary = "\n".join(data["boundary"])
    for token in EXPECTED_BOUNDARY:
        assert token in boundary

    assert EXPECTED_DOES_NOT_PROVE <= set(data["does_not_prove"])

def verify_doc() -> None:
    if not DOC.exists():
        raise SystemExit(f"missing status doc: {DOC}")
    doc = DOC.read_text()
    assert EXPECTED_STATUS in doc
    assert "DFM_HOLDOUT_SPLIT_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC holdout split target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
