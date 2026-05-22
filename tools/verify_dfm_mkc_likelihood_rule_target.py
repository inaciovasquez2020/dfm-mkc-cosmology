#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_likelihood_rule_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_LIKELIHOOD_RULE_TARGET_2026_05_21.md"

EXPECTED_STATUS = "LIKELIHOOD_RULE_TARGET_ONLY_NOT_SUPPLIED"

EXPECTED_UPSTREAM = {
    "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL",
    "DFM_PARAMETER_MAP",
    "DFM_OBSERVABLE_PREDICTION_RULES",
    "DFM_FROZEN_PREDICTION_VECTOR",
    "DFM_EXTERNAL_DATA_MANIFEST",
}

EXPECTED_FIELDS = {
    "likelihood_identifier",
    "data_vector_reference",
    "frozen_prediction_vector_reference",
    "covariance_matrix_reference",
    "inverse_covariance_rule",
    "residual_vector_definition",
    "probe_likelihood_blocks",
    "joint_likelihood_composition_rule",
    "nuisance_parameter_handling",
    "prior_application_rule",
    "scale_cut_rule",
    "masking_rule",
    "calibration_systematics_rule",
    "cross_probe_covariance_rule",
    "chi_square_definition",
    "log_likelihood_definition",
    "model_comparison_metrics",
    "lambda_cdm_baseline_reference",
    "holdout_execution_rule",
    "failure_thresholds",
    "reproduction_command",
}

EXPECTED_CHANNELS = {
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
    "Does not supply DFM field equations.",
    "Does not supply DFM action functional.",
    "Does not supply DFM parameter map.",
    "Does not supply DFM observable prediction rules.",
    "Does not supply frozen DFM prediction values.",
    "Does not supply likelihood equations.",
    "Does not supply covariance matrices.",
    "Does not supply probe likelihoods.",
    "Does not supply joint likelihood.",
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
    assert data["artifact"] == "DFM_MKC_LIKELIHOOD_RULE_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["likelihood_rule_supplied"] is False
    assert data["joint_likelihood_supplied"] is False
    assert data["probe_likelihoods_supplied"] is False
    assert data["covariance_rule_supplied"] is False
    assert data["model_comparison_rule_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["root_blocker"] == "DFM_LIKELIHOOD_RULE_NOT_SUPPLIED"

    assert EXPECTED_UPSTREAM <= set(data["upstream_required_objects"])
    assert EXPECTED_FIELDS <= set(data["required_likelihood_rule_fields"])
    assert EXPECTED_CHANNELS == set(data["required_probe_likelihood_channels"].keys())

    for channel in data["required_probe_likelihood_channels"].values():
        assert channel["status"] == "blocked_no_dfm_likelihood_rule"

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
    assert "DFM_LIKELIHOOD_RULE_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC likelihood rule target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
