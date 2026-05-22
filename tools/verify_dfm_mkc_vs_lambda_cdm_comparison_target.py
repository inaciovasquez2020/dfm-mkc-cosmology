#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_vs_lambda_cdm_comparison_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_VS_LAMBDA_CDM_COMPARISON_TARGET_2026_05_21.md"

EXPECTED_STATUS = "DFM_VS_LAMBDA_CDM_COMPARISON_TARGET_ONLY_NOT_SUPPLIED"

EXPECTED_UPSTREAM = {
    "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL",
    "DFM_PARAMETER_MAP",
    "DFM_OBSERVABLE_PREDICTION_RULES",
    "DFM_FROZEN_PREDICTION_VECTOR",
    "DFM_LIKELIHOOD_RULE",
    "DFM_HOLDOUT_SPLIT",
    "DFM_EXTERNAL_DATA_MANIFEST",
}

EXPECTED_FIELDS = {
    "comparison_identifier",
    "source_commit",
    "external_data_manifest_reference",
    "field_equations_or_action_functional_reference",
    "parameter_map_reference",
    "observable_prediction_rules_reference",
    "frozen_prediction_vector_reference",
    "likelihood_rule_reference",
    "holdout_split_reference",
    "lambda_cdm_baseline_reference",
    "dfm_metric_outputs",
    "lambda_cdm_metric_outputs",
    "delta_chi_square",
    "delta_aic",
    "delta_bic",
    "posterior_predictive_checks",
    "probe_by_probe_residuals",
    "joint_likelihood_result",
    "holdout_survival_status",
    "independent_reproduction_status",
    "claim_interpretation_rule",
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

EXPECTED_DECISION_OUTPUTS = {
    "dfm_chi_square",
    "lambda_cdm_chi_square",
    "delta_chi_square",
    "dfm_aic",
    "lambda_cdm_aic",
    "delta_aic",
    "dfm_bic",
    "lambda_cdm_bic",
    "delta_bic",
    "holdout_survival_boolean",
    "probe_consistency_table",
    "failure_mode_report",
    "no_post_hoc_tuning_audit",
}

EXPECTED_DOWNSTREAM = {
    "DFM_EMPIRICAL_EVIDENCE_CLAIM",
    "DFM_LAMBDA_CDM_FAILURE_CLAIM",
    "DFM_CDM_REPLACEMENT_CLAIM",
    "DFM_FINAL_COSMOLOGY_CLOSURE_CLAIM",
}

EXPECTED_BOUNDARY = [
    "Target schema only.",
    "Does not execute DFM-vs-Lambda-CDM comparison.",
    "Does not supply DFM metrics.",
    "Does not supply Lambda-CDM metrics.",
    "Does not compute delta chi-square.",
    "Does not compute delta AIC.",
    "Does not compute delta BIC.",
    "Does not execute holdout evaluation.",
    "Does not supply independent validation.",
    "Does not produce empirical evidence.",
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
    assert data["artifact"] == "DFM_MKC_VS_LAMBDA_CDM_COMPARISON_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["comparison_executed"] is False
    assert data["dfm_metrics_supplied"] is False
    assert data["lambda_cdm_metrics_supplied"] is False
    assert data["model_comparison_metrics_supplied"] is False
    assert data["holdout_evaluation_executed"] is False
    assert data["independent_validation_supplied"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["dfm_proved"] is False
    assert data["lambda_cdm_disproved"] is False
    assert data["cdm_replaced"] is False
    assert data["root_blocker"] == "DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED"

    assert EXPECTED_UPSTREAM <= set(data["upstream_required_objects"])
    assert EXPECTED_FIELDS <= set(data["required_comparison_fields"])
    assert EXPECTED_CHANNELS == set(data["required_probe_comparison_channels"].keys())
    assert EXPECTED_DECISION_OUTPUTS <= set(data["required_decision_outputs"])

    for channel in data["required_probe_comparison_channels"].values():
        assert channel["status"] == "blocked_no_comparison_execution"

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
    assert "DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC vs Lambda-CDM comparison target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
