#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_AUDIT = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_dynamical_core_source_audit_2026_05_21.json"
OUT = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_dynamical_core_gap_matrix_2026_05_21.json"

SLOTS = [
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
]

PATTERN_TO_SLOT = {
    "action_functional": "ActionFunctional_or_PrimitiveClosedFormFieldEquations",
    "primitive_field_equation": "ActionFunctional_or_PrimitiveClosedFormFieldEquations",
    "matter_coupling": "MatterCouplingRule",
    "dark_sector_coupling": "DarkSectorCouplingRule",
    "source_terms": "SourceTerms",
    "boundary_conditions": "BoundaryConditions",
    "parameters": "ExhaustiveParameterTable",
    "prediction_vector": "FrozenPredictionVector",
}

BOUNDARIES = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def main() -> None:
    audit = json.loads(SOURCE_AUDIT.read_text())

    slot_candidates = {slot: [] for slot in SLOTS}

    for item in audit.get("files", []):
        if not item.get("exists"):
            continue
        path = item["path"]
        for pattern_name, hits in item.get("pattern_hits", {}).items():
            slot = PATTERN_TO_SLOT.get(pattern_name)
            if slot is None or not hits:
                continue
            slot_candidates[slot].append({
                "path": path,
                "pattern": pattern_name,
                "hit_count": len(hits),
                "sample_hits": hits[:3],
            })

    gap_matrix = {}
    for slot in SLOTS:
        gap_matrix[slot] = {
            "status": "NOT_SUPPLIED",
            "candidate_repository_signals": slot_candidates[slot],
            "promotion_rule": "May be promoted only by supplied explicit equations, coupling rules, source/boundary data, frozen predictions, holdout residuals, or independent replication evidence.",
        }

    data = {
        "schema_version": "DFM_MKC_DYNAMICAL_CORE_GAP_MATRIX_V1",
        "status": "GAP_MATRIX_ONLY_NO_CLOSURE_PROMOTION",
        "date": "2026-05-21",
        "base_audit": "artifacts/repo_intake/dfm_mkc_dynamical_core_source_audit_2026_05_21.json",
        "source_audit_status": audit.get("status"),
        "gap_matrix": gap_matrix,
        "all_required_slots_status": "NOT_SUPPLIED",
        "next_admissible_object": "A supplied primitive equation/coupling/parameter/prediction packet that can fill exactly one slot.",
        "does_not_prove": BOUNDARIES,
    }

    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(str(OUT))
    print("DFM-MKC dynamical core gap matrix built.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
