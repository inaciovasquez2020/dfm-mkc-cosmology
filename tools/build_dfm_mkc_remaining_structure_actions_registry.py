#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/repo_intake/dfm_mkc_remaining_structure_actions_registry_2026_05_21.json"

phase_names = [
    "PHASE_1_BLOCKER_COMPLETION",
    "PHASE_2_EXTERNAL_SOURCE_POINTERS",
    "PHASE_3_PAYLOAD_ACQUISITION",
    "PHASE_4_PAYLOAD_VERIFICATION",
    "PHASE_5_THEORY_INTAKE",
    "PHASE_6_DFM_CORE_TARGETS",
    "PHASE_7_PARAMETER_LAYER",
    "PHASE_8_OBSERVABLE_PREDICTION_LAYER",
    "PHASE_9_FROZEN_PREDICTION_LAYER",
    "PHASE_10_LIKELIHOOD_TARGETS",
    "PHASE_11_HOLDOUT_SPLIT_LAYER",
    "PHASE_12_EXECUTED_COMPARISON_LAYER",
    "PHASE_13_EMPIRICAL_EVIDENCE_LAYER",
    "PHASE_14_INDEPENDENT_REPRODUCTION_LAYER",
    "PHASE_15_TERMINAL_DECISION_LAYER",
    "PHASE_16_PUBLIC_COMMUNICATION_LAYER",
]

required_actions = {
    "PHASE_1_BLOCKER_COMPLETION": ["DFM_MKC_TERMINAL_BLOCKER_EXHAUSTION_CERTIFICATE"],
    "PHASE_2_EXTERNAL_SOURCE_POINTERS": ["PLANCK_2018_CMB_SOURCE_POINTER"],
    "PHASE_6_DFM_CORE_TARGETS": ["DFM_FIELD_EQUATIONS_SUPPLIED_TARGET"],
    "PHASE_12_EXECUTED_COMPARISON_LAYER": ["DFM_LIKELIHOOD_EXECUTION_TARGET"],
    "PHASE_14_INDEPENDENT_REPRODUCTION_LAYER": ["INDEPENDENT_REPRODUCTION_TARGET"],
    "PHASE_15_TERMINAL_DECISION_LAYER": ["FINAL_COSMOLOGY_CLOSURE_DECISION_LOCK"],
}

def make_action(name):
    return {
        "name": name,
        "status": "pending",
        "claim_level": "target_or_blocker_only",
        "completed": False,
    }

def main():
    phases = []
    for index, phase_name in enumerate(phase_names, start=1):
        names = list(required_actions.get(phase_name, []))
        while len(names) < 7:
            names.append(f"{phase_name}_ACTION_{len(names) + 1:02d}")
        phases.append({
            "phase": phase_name,
            "status": "open",
            "actions": [make_action(name) for name in names],
        })

    data = {
        "artifact": "DFM_MKC_REMAINING_STRUCTURE_ACTIONS_REGISTRY",
        "date": "2026-05-21",
        "status": "REMAINING_STRUCTURE_ACTIONS_REGISTRY_ONLY",
        "claim_level": "registry_only",
        "phase_count": len(phases),
        "action_count": sum(len(phase["actions"]) for phase in phases),
        "all_actions_completed": False,
        "likelihood_executed": False,
        "empirical_evidence_supplied": False,
        "dfm_proved": False,
        "lambda_cdm_disproved": False,
        "cdm_replaced": False,
        "current_root_blocker": "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_NOT_SUPPLIED",
        "current_safe_next_action": "DFM_MKC_TERMINAL_BLOCKER_EXHAUSTION_CERTIFICATE",
        "phases": phases,
        "boundary": [
            "Does not supply DFM field equations.",
            "Does not supply DFM action functional.",
            "Does not supply DFM parameter values.",
            "Does not supply DFM observable prediction rules.",
            "Does not supply frozen DFM prediction values.",
            "Does not execute any likelihood.",
            "Does not execute DFM-vs-Lambda-CDM comparison.",
            "Does not supply empirical evidence.",
            "Does not prove DFM.",
            "Does not disprove Lambda-CDM.",
            "Does not replace CDM.",
            "Does not claim final cosmology closure.",
            "Does not claim Nobel-level physical discovery.",
            "Does not claim any Clay problem.",
        ],
        "does_not_prove": [
            "DFM",
            "Lambda-CDM failure",
            "CDM replacement",
            "dark-energy resolution",
            "dark-matter resolution",
            "final cosmology closure",
            "Nobel-level physical discovery",
            "any Clay problem",
        ],
    }
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

if __name__ == "__main__":
    main()
