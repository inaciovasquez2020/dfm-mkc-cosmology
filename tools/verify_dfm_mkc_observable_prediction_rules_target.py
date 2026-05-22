#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_observable_prediction_rules_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_OBSERVABLE_PREDICTION_RULES_TARGET_2026_05_21.md"

EXPECTED_STATUS = "OBSERVABLE_PREDICTION_RULES_TARGET_ONLY_NOT_SUPPLIED"

EXPECTED_FIELDS = {
    "observable_channel_name",
    "input_parameter_dependencies",
    "input_initial_condition_dependencies",
    "input_boundary_condition_dependencies",
    "forward_model_equations",
    "projection_from_dfm_state_to_observable",
    "units_and_normalization",
    "redshift_domain",
    "scale_domain",
    "nuisance_parameter_separation",
    "calibration_rule",
    "covariance_compatibility_rule",
    "residual_vector_definition",
    "lambda_cdm_baseline_comparison_rule",
    "holdout_freeze_rule",
    "failure_mode_definition",
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
    "DFM_FROZEN_PREDICTION_VECTOR",
    "DFM_LIKELIHOOD_RULE",
    "DFM_HOLDOUT_SPLIT",
    "DFM_VS_LAMBDA_CDM_COMPARISON",
}

EXPECTED_BOUNDARY = [
    "Target schema only.",
    "Does not supply DFM field equations.",
    "Does not supply DFM action functional.",
    "Does not supply DFM parameter map.",
    "Does not supply DFM observable prediction rules.",
    "Does not supply channel projection rules.",
    "Does not supply residual vector rules.",
    "Does not supply covariance compatibility rules.",
    "Does not supply frozen predictions.",
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
    assert data["artifact"] == "DFM_MKC_OBSERVABLE_PREDICTION_RULES_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["observable_prediction_rules_supplied"] is False
    assert data["channel_projection_rules_supplied"] is False
    assert data["residual_vector_rules_supplied"] is False
    assert data["covariance_compatibility_supplied"] is False
    assert data["likelihood_ready"] is False
    assert data["root_blocker"] == "DFM_OBSERVABLE_PREDICTION_RULES_NOT_SUPPLIED"

    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in data["upstream_required_objects"]
    assert "DFM_PARAMETER_MAP" in data["upstream_required_objects"]
    assert EXPECTED_FIELDS <= set(data["required_prediction_rule_fields"])
    assert EXPECTED_CHANNELS == set(data["required_observable_channels"].keys())

    for channel in data["required_observable_channels"].values():
        assert channel["status"] == "blocked_no_dfm_observable_prediction_rule"

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
    assert "DFM_OBSERVABLE_PREDICTION_RULES_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC observable prediction rules target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
