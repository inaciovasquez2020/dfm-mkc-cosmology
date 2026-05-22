#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_parameter_map_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_PARAMETER_MAP_TARGET_2026_05_21.md"

EXPECTED_STATUS = "PARAMETER_MAP_TARGET_ONLY_NOT_SUPPLIED"

EXPECTED_FIELDS = {
    "primitive_parameter_names",
    "parameter_definitions",
    "dimensional_units",
    "allowed_domains",
    "prior_ranges",
    "frozen_values_or_free_status",
    "physical_interpretation",
    "degeneracy_structure",
    "lambda_cdm_parameter_correspondence_or_explicit_noncorrespondence",
    "matter_sector_parameters",
    "dark_sector_parameters",
    "initial_condition_parameters",
    "boundary_condition_parameters",
    "nuisance_parameter_separation",
    "observable_channel_dependencies",
    "calibration_parameters",
    "holdout_freeze_certificate",
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
    "DFM_OBSERVABLE_PREDICTION_RULES",
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
    "Does not supply parameter values.",
    "Does not supply prior ranges.",
    "Does not freeze DFM parameters.",
    "Does not supply observable prediction rules.",
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
    assert data["artifact"] == "DFM_MKC_PARAMETER_MAP_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["parameter_map_supplied"] is False
    assert data["parameter_values_frozen"] is False
    assert data["prior_ranges_supplied"] is False
    assert data["dimension_units_supplied"] is False
    assert data["observable_parameter_projection_enabled"] is False
    assert data["root_blocker"] == "DFM_PARAMETER_MAP_NOT_SUPPLIED"

    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in data["upstream_required_objects"]
    assert EXPECTED_FIELDS <= set(data["required_parameter_object_fields"])
    assert EXPECTED_CHANNELS <= set(data["required_prediction_channels_blocked"])
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
    assert "DFM_PARAMETER_MAP_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC parameter map target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
