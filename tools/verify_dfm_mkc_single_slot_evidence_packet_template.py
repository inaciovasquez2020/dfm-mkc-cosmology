#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_single_slot_evidence_packet_template_2026_05_21.json"
GATE = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_single_slot_promotion_gate_2026_05_21.json"

REQUIRED_STATUS = "TEMPLATE_ONLY_NO_EVIDENCE_SUPPLIED"
REQUIRED_GATE_STATUS = "PROMOTION_GATE_ONLY_NO_SLOT_PROMOTED"

REQUIRED_SLOTS = {
    "ActionFunctional_or_PrimitiveClosedFormFieldEquations",
    "MatterCouplingRule",
    "DarkSectorCouplingRule",
    "SourceTerms",
    "BoundaryConditions",
    "ExhaustiveParameterTable",
    "FrozenPredictionVector",
    "ACT_DES_HoldoutData",
    "ResidualEvaluationResult",
    "IndependentReplicationResult",
}

REQUIRED_PACKET_KEYS = {
    "slot_name",
    "evidence_path",
    "evidence_sha256",
    "verifier_path",
    "test_path",
    "classification_status",
    "does_not_prove",
}

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

NULL_FIELDS = {
    "slot_name",
    "evidence_path",
    "evidence_sha256",
    "verifier_path",
    "test_path",
    "classification_status",
}

def main() -> None:
    data = json.loads(TEMPLATE.read_text())
    gate = json.loads(GATE.read_text())

    if data.get("status") != REQUIRED_STATUS:
        raise SystemExit("invalid template status")

    if gate.get("status") != REQUIRED_GATE_STATUS:
        raise SystemExit("promotion gate status mismatch")

    if set(data.get("eligible_slots", [])) != REQUIRED_SLOTS:
        raise SystemExit("eligible slot mismatch")

    if data.get("currently_promoted_slots") != []:
        raise SystemExit("template promoted a slot")

    packet = data.get("template_packet", {})
    if set(packet) != REQUIRED_PACKET_KEYS:
        raise SystemExit("template packet key mismatch")

    for key in NULL_FIELDS:
        if packet.get(key) is not None:
            raise SystemExit(f"template field must remain null: {key}")

    boundaries = set(data.get("does_not_prove", []))
    packet_boundaries = set(packet.get("does_not_prove", []))

    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    if not REQUIRED_BOUNDARIES.issubset(packet_boundaries):
        raise SystemExit(f"missing packet boundaries: {sorted(REQUIRED_BOUNDARIES - packet_boundaries)}")

    print("DFM-MKC single-slot evidence packet template verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
