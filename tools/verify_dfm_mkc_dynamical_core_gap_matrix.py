#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_dynamical_core_gap_matrix_2026_05_21.json"

REQUIRED_STATUS = "GAP_MATRIX_ONLY_NO_CLOSURE_PROMOTION"
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
    data = json.loads(ARTIFACT.read_text())

    if data.get("status") != REQUIRED_STATUS:
        raise SystemExit("invalid gap-matrix status")

    if data.get("all_required_slots_status") != "NOT_SUPPLIED":
        raise SystemExit("gap matrix promoted a required slot")

    matrix = data.get("gap_matrix", {})
    if set(matrix) != REQUIRED_SLOTS:
        raise SystemExit(f"slot mismatch: {sorted(REQUIRED_SLOTS - set(matrix))}")

    for slot, entry in matrix.items():
        if entry.get("status") != "NOT_SUPPLIED":
            raise SystemExit(f"slot promoted unexpectedly: {slot}")
        if "promotion_rule" not in entry:
            raise SystemExit(f"missing promotion rule: {slot}")
        if "candidate_repository_signals" not in entry:
            raise SystemExit(f"missing candidate signals: {slot}")

    boundaries = set(data.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    if data.get("source_audit_status") != "SOURCE_AUDIT_ONLY_NO_CLOSURE_PROMOTION":
        raise SystemExit("source audit status mismatch")

    print("DFM-MKC dynamical core gap matrix verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
