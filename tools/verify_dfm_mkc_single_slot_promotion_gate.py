#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_single_slot_promotion_gate_2026_05_21.json"
GAP = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_dynamical_core_gap_matrix_2026_05_21.json"

REQUIRED_STATUS = "PROMOTION_GATE_ONLY_NO_SLOT_PROMOTED"
REQUIRED_GAP_STATUS = "GAP_MATRIX_ONLY_NO_CLOSURE_PROMOTION"

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

REQUIRED_EVIDENCE_FIELDS = {
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

def main() -> None:
    gate = json.loads(GATE.read_text())
    gap = json.loads(GAP.read_text())

    if gate.get("status") != REQUIRED_STATUS:
        raise SystemExit("invalid promotion-gate status")

    if gap.get("status") != REQUIRED_GAP_STATUS:
        raise SystemExit("gap matrix status mismatch")

    if set(gate.get("eligible_slots", [])) != REQUIRED_SLOTS:
        raise SystemExit("eligible slot mismatch")

    promoted = gate.get("currently_promoted_slots", [])
    if promoted != []:
        raise SystemExit("promotion gate unexpectedly promotes a slot")

    if len(promoted) > 1:
        raise SystemExit("promotion gate violates single-slot rule")

    if set(gate.get("required_evidence_fields_for_future_promotion", [])) != REQUIRED_EVIDENCE_FIELDS:
        raise SystemExit("future evidence field mismatch")

    boundaries = set(gate.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    print("DFM-MKC single-slot promotion gate verification OK.")
    print(f"Status: {gate['status']}")

if __name__ == "__main__":
    main()
