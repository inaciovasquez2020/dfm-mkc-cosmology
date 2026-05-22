#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_remaining_structure_actions_registry_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_REMAINING_STRUCTURE_ACTIONS_REGISTRY_2026_05_21.md"

def main():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    assert data["status"] == "REMAINING_STRUCTURE_ACTIONS_REGISTRY_ONLY"
    assert data["claim_level"] == "registry_only"
    assert data["phase_count"] == 16
    assert data["action_count"] >= 100
    assert data["all_actions_completed"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["dfm_proved"] is False
    assert data["lambda_cdm_disproved"] is False
    assert data["cdm_replaced"] is False
    assert data["current_root_blocker"] == "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_NOT_SUPPLIED"
    assert data["current_safe_next_action"] == "DFM_MKC_TERMINAL_BLOCKER_EXHAUSTION_CERTIFICATE"

    phases = {phase["phase"] for phase in data["phases"]}
    assert "PHASE_1_BLOCKER_COMPLETION" in phases
    assert "PHASE_6_DFM_CORE_TARGETS" in phases
    assert "PHASE_10_LIKELIHOOD_TARGETS" in phases
    assert "PHASE_15_TERMINAL_DECISION_LAYER" in phases

    actions = {item["name"] for phase in data["phases"] for item in phase["actions"]}
    assert "DFM_MKC_TERMINAL_BLOCKER_EXHAUSTION_CERTIFICATE" in actions
    assert "PLANCK_2018_CMB_SOURCE_POINTER" in actions
    assert "DFM_FIELD_EQUATIONS_SUPPLIED_TARGET" in actions
    assert "DFM_LIKELIHOOD_EXECUTION_TARGET" in actions
    assert "INDEPENDENT_REPRODUCTION_TARGET" in actions
    assert "FINAL_COSMOLOGY_CLOSURE_DECISION_LOCK" in actions

    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not supply DFM field equations.",
        "Does not supply frozen DFM prediction values.",
        "Does not execute any likelihood.",
        "Does not execute DFM-vs-Lambda-CDM comparison.",
        "Does not supply empirical evidence.",
        "Does not prove DFM.",
        "Does not disprove Lambda-CDM.",
        "Does not replace CDM.",
        "Does not claim final cosmology closure.",
    ]:
        assert token in boundary
        assert token in doc

    for phase in data["phases"]:
        assert phase["status"] == "open"
        for item in phase["actions"]:
            assert item["status"] == "pending"
            assert item["claim_level"] == "target_or_blocker_only"
            assert item["completed"] is False

    print("DFM-MKC remaining structure actions registry verification OK.")
    print(f"Status: {data['status']}")
    print(f"Phase count: {data['phase_count']}")
    print(f"Action count: {data['action_count']}")
    print(f"Current root blocker: {data['current_root_blocker']}")
    print(f"Current safe next action: {data['current_safe_next_action']}")

if __name__ == "__main__":
    main()
