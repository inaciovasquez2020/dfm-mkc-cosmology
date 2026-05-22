#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_frozen_prediction_map_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_FROZEN_PREDICTION_MAP_TARGET_2026_05_21.md"

EXPECTED_STATUS = "FROZEN_PREDICTION_MAP_TARGET_ONLY_PREDICTIONS_NOT_SUPPLIED"

REQUIRED_MISSING = {
    "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL",
    "DFM_PARAMETER_MAP",
    "DFM_PRIOR_RANGES",
    "DFM_OBSERVABLE_PREDICTION_RULES",
    "DFM_FROZEN_PREDICTION_VECTOR",
    "DFM_LIKELIHOOD_RULE",
    "DFM_HOLDOUT_SPLIT",
    "NO_POST_HOC_TUNING_CERTIFICATE",
}

REQUIRED_OBSERVABLES = {
    "CMB_TT_TE_EE",
    "CMB_LENSING",
    "BAO_DISTANCES",
    "SNIA_DISTANCES",
    "WEAK_LENSING_AND_CLUSTERING",
}

REQUIRED_BOUNDARY = [
    "Does not supply DFM equations.",
    "Does not supply DFM action functional.",
    "Does not supply DFM parameter map.",
    "Does not supply DFM observable prediction rules.",
    "Does not supply frozen DFM predictions.",
    "Does not execute CMB likelihood.",
    "Does not execute BAO likelihood.",
    "Does not execute SN likelihood.",
    "Does not execute DES likelihood.",
    "Does not prove DFM.",
    "Does not disprove Lambda-CDM.",
    "Does not replace CDM.",
]

REQUIRED_DOES_NOT_PROVE = {
    "DFM",
    "Lambda-CDM failure",
    "CDM replacement",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
}

def load_artifact() -> dict:
    if not ARTIFACT.exists():
        raise SystemExit(f"missing artifact: {ARTIFACT}")
    return json.loads(ARTIFACT.read_text())

def verify_artifact(data: dict) -> None:
    assert data["artifact"] == "DFM_MKC_FROZEN_PREDICTION_MAP_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["prediction_map_supplied"] is False
    assert data["frozen_predictions_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["root_blocker"] == "DFM_FROZEN_PREDICTION_MAP_NOT_SUPPLIED"

    missing = set(data["required_missing_objects"])
    assert REQUIRED_MISSING <= missing

    observables = {item["name"] for item in data["observable_targets"]}
    assert REQUIRED_OBSERVABLES <= observables

    boundary = "\n".join(data["boundary"])
    for token in REQUIRED_BOUNDARY:
        assert token in boundary

    does_not_prove = set(data["does_not_prove"])
    assert REQUIRED_DOES_NOT_PROVE <= does_not_prove

def verify_doc() -> None:
    if not DOC.exists():
        raise SystemExit(f"missing status doc: {DOC}")
    text = DOC.read_text()
    assert EXPECTED_STATUS in text
    for token in REQUIRED_BOUNDARY:
        assert token in text

def main() -> None:
    data = load_artifact()
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC frozen prediction map target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
