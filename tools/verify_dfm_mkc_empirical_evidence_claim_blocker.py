#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_empirical_evidence_claim_blocker_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_EMPIRICAL_EVIDENCE_CLAIM_BLOCKER_2026_05_21.md"

EXPECTED_STATUS = "EMPIRICAL_EVIDENCE_CLAIM_BLOCKED_NO_EXECUTED_COMPARISON"

EXPECTED_MISSING = {
    "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL",
    "DFM_PARAMETER_MAP",
    "DFM_OBSERVABLE_PREDICTION_RULES",
    "DFM_FROZEN_PREDICTION_VECTOR",
    "DFM_LIKELIHOOD_RULE",
    "DFM_HOLDOUT_SPLIT",
    "DFM_VS_LAMBDA_CDM_COMPARISON",
    "INDEPENDENT_VALIDATION",
}

EXPECTED_TARGETS = {
    "DFM_MKC_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_TARGET",
    "DFM_MKC_PARAMETER_MAP_TARGET",
    "DFM_MKC_OBSERVABLE_PREDICTION_RULES_TARGET",
    "DFM_MKC_FROZEN_PREDICTION_VECTOR_TARGET",
    "DFM_MKC_LIKELIHOOD_RULE_TARGET",
    "DFM_MKC_HOLDOUT_SPLIT_TARGET",
    "DFM_MKC_VS_LAMBDA_CDM_COMPARISON_TARGET",
}

EXPECTED_BLOCKED_CLAIMS = {
    "DFM has empirical evidence",
    "DFM beats Lambda-CDM",
    "Lambda-CDM is empirically disproved",
    "CDM is replaced by DFM",
    "DFM resolves dark energy",
    "DFM resolves dark matter",
    "DFM gives final cosmology closure",
}

EXPECTED_BOUNDARY = [
    "Blocker certificate only.",
    "Does not supply empirical evidence.",
    "Does not execute DFM-vs-Lambda-CDM comparison.",
    "Does not execute holdout evaluation.",
    "Does not supply independent validation.",
    "Does not supply DFM metrics.",
    "Does not supply Lambda-CDM metrics.",
    "Does not compute delta chi-square.",
    "Does not compute delta AIC.",
    "Does not compute delta BIC.",
    "Does not prove DFM.",
    "Does not disprove Lambda-CDM.",
    "Does not replace CDM.",
    "Does not claim final cosmology closure.",
]

EXPECTED_DOES_NOT_PROVE = {
    "DFM",
    "Lambda-CDM failure",
    "CDM replacement",
    "dark-energy resolution",
    "dark-matter resolution",
    "final cosmology closure",
    "Nobel-level physical discovery",
    "any Clay problem",
}

def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    return json.loads(path.read_text())

def verify_artifact(data: dict) -> None:
    assert data["artifact"] == "DFM_MKC_EMPIRICAL_EVIDENCE_CLAIM_BLOCKER"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "blocker_certificate_only"
    assert data["empirical_evidence_claim_admissible"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["comparison_executed"] is False
    assert data["holdout_evaluation_executed"] is False
    assert data["independent_validation_supplied"] is False
    assert data["dfm_metrics_supplied"] is False
    assert data["lambda_cdm_metrics_supplied"] is False
    assert data["model_comparison_metrics_supplied"] is False
    assert data["root_blocker"] == "NO_EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON"

    assert EXPECTED_MISSING <= set(data["blocking_missing_objects"])
    assert EXPECTED_TARGETS <= set(data["upstream_registered_targets"])

    blocked_claims = {item["claim"] for item in data["blocked_claims"]}
    assert EXPECTED_BLOCKED_CLAIMS <= blocked_claims
    for item in data["blocked_claims"]:
        assert item["status"] == "blocked"

    boundary = "\n".join(data["boundary"])
    for token in EXPECTED_BOUNDARY:
        assert token in boundary

    assert EXPECTED_DOES_NOT_PROVE <= set(data["does_not_prove"])

def verify_doc() -> None:
    if not DOC.exists():
        raise SystemExit(f"missing status doc: {DOC}")
    doc = DOC.read_text()
    assert EXPECTED_STATUS in doc
    assert "NO_EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC empirical evidence claim blocker verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
