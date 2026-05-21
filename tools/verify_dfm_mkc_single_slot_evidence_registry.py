#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_single_slot_evidence_registry_2026_05_21.json"
PACKET = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_exhaustive_parameter_table_evidence_packet_2026_05_21.json"

REQUIRED_BOUNDARIES = {
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
}

REQUIRED_MISSING = {
    "ActionFunctional_or_PrimitiveClosedFormFieldEquations",
    "MatterCouplingRule",
    "DarkSectorCouplingRule",
    "SourceTerms",
    "BoundaryConditions",
    "FrozenPredictionVector",
    "ACT_DES_HoldoutData",
    "ResidualEvaluationResult",
    "IndependentReplicationResult",
}

def main() -> None:
    registry = json.loads(REGISTRY.read_text())
    packet = json.loads(PACKET.read_text())

    if registry.get("status") != "REGISTRY_ONLY_NO_FULL_CLOSURE_PROMOTION":
        raise SystemExit("invalid registry status")

    if registry.get("full_closure_status") != "BLOCKED_MISSING_REQUIRED_SLOTS":
        raise SystemExit("invalid full closure status")

    if set(registry.get("missing_required_slots", [])) != REQUIRED_MISSING:
        raise SystemExit("missing required slots mismatch")

    packets = registry.get("registered_packets", [])
    if len(packets) != 1:
        raise SystemExit("registry must contain exactly one packet")

    entry = packets[0]
    if entry.get("slot_name") != "ExhaustiveParameterTable":
        raise SystemExit("registered slot mismatch")

    if entry.get("packet_path") != "artifacts/repo_intake/dfm_mkc_exhaustive_parameter_table_evidence_packet_2026_05_21.json":
        raise SystemExit("registered packet path mismatch")

    if entry.get("classification_status") != packet.get("classification_status"):
        raise SystemExit("classification status mismatch")

    if entry.get("promotion_status") != "NOT_PROMOTED_TO_FULL_CLOSURE":
        raise SystemExit("promotion status mismatch")

    slot_status = registry.get("slot_status", {})
    if slot_status.get("ExhaustiveParameterTable") != "SUPPLIED_UNVERIFIED_INPUT":
        raise SystemExit("ExhaustiveParameterTable status mismatch")

    for slot in REQUIRED_MISSING:
        if slot_status.get(slot) != "NOT_SUPPLIED":
            raise SystemExit(f"slot unexpectedly supplied: {slot}")

    boundaries = set(registry.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    print("DFM-MKC single-slot evidence registry verification OK.")
    print(f"Status: {registry['status']}")

if __name__ == "__main__":
    main()
