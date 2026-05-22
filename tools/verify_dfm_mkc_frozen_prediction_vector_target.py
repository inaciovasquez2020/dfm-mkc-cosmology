#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_frozen_prediction_vector_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_FROZEN_PREDICTION_VECTOR_TARGET_2026_05_21.md"

EXPECTED_STATUS = "FROZEN_PREDICTION_VECTOR_TARGET_ONLY_NOT_SUPPLIED"

EXPECTED_UPSTREAM = {
    "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL",
    "DFM_PARAMETER_MAP",
    "DFM_OBSERVABLE_PREDICTION_RULES",
}

EXPECTED_FIELDS = {
    "freeze_identifier",
    "freeze_timestamp",
    "source_commit",
    "dfm_equation_object_reference",
    "dfm_parameter_map_reference",
    "observable_prediction_rules_reference",
    "frozen_parameter_values",
    "frozen_prior_ranges",
    "holdout_split_reference",
    "no_post_hoc_tuning_certificate",
    "prediction_channel_vectors",
    "residual_vector_definitions",
    "covariance_alignment_metadata",
    "likelihood_input_format",
    "failure_mode_thresholds",
    "lambda_cdm_baseline_reference",
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
    "DFM_LIKELIHOOD_RULE",
    "DFM_HOLDOUT_SPLIT_EXECUTION",
    "DFM_VS_LAMBDA_CDM_COMPARISON",
    "EMPIRICAL_EVIDENCE_CLAIM",
}

EXPECTED_BOUNDARY = [
    "Target schema only.",
    "Does not supply DFM field equations.",
    "Does not supply DFM action functional.",
    "Does not supply DFM parameter map.",
    "Does not supply DFM observable prediction rules.",
    "Does not supply frozen DFM prediction values.",
    "Does not supply frozen parameter values.",
    "Does not supply holdout split execution.",
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
    assert data["artifact"] == "DFM_MKC_FROZEN_PREDICTION_VECTOR_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["frozen_prediction_vector_supplied"] is False
    assert data["prediction_values_frozen"] is False
    assert data["observable_prediction_rules_supplied"] is False
    assert data["parameter_values_frozen"] is False
    assert data["likelihood_ready"] is False
    assert data["root_blocker"] == "DFM_FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED"

    assert EXPECTED_UPSTREAM <= set(data["upstream_required_objects"])
    assert EXPECTED_FIELDS <= set(data["required_frozen_vector_fields"])
    assert EXPECTED_CHANNELS == set(data["required_prediction_channels"].keys())

    for channel in data["required_prediction_channels"].values():
        assert channel["status"] == "blocked_no_frozen_prediction_vector"

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
    assert "DFM_FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC frozen prediction vector target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
