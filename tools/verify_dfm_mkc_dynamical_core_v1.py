#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "DFM_MKC_dynamical_core_v1.json"

REQUIRED_STATUS = "SCAFFOLD_ONLY_DYNAMICAL_CORE_NOT_SUPPLIED"

REQUIRED_MISSING = {
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

REQUIRED_EVIDENCE_PATHS = [
    "artifacts/repo_intake/dfm_mkc_theory_content_digest_2026_05_21.json",
    "src/cosmology/observables/distances.py",
    "theory/deformation_field.md",
    "theory/parameters.md",
    "numerics/background_equations.md",
    "config/dfm_mkc_parameter_freeze.json",
    "dfm_mkc/model.py",
    "src/models/dfm_mkc.py",
    "mkc_solver.py",
]

REQUIRED_NULL_KEYS = [
    "action_functional_or_primitive_closed_form_field_equations",
    "matter_coupling_rule",
    "dark_sector_coupling_rule",
    "source_terms",
    "boundary_conditions",
    "exhaustive_parameter_table",
    "frozen_prediction_vector",
    "act_des_holdout_data",
    "residual_evaluation_result",
    "independent_replication_result",
]

def main() -> None:
    if not SPEC.exists():
        raise SystemExit(f"missing spec: {SPEC}")

    data = json.loads(SPEC.read_text())

    if data.get("status") != REQUIRED_STATUS:
        raise SystemExit("invalid status")

    missing = set(data.get("missing_objects", []))
    if missing != REQUIRED_MISSING:
        raise SystemExit(f"missing object mismatch: {sorted(REQUIRED_MISSING - missing)}")

    boundaries = set(data.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"boundary mismatch: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    closure = data.get("required_full_closure_input", {})
    for key in REQUIRED_NULL_KEYS:
        if key not in closure:
            raise SystemExit(f"missing closure key: {key}")
        if closure[key] is not None:
            raise SystemExit(f"non-null unsupported closure key: {key}")

    for rel in REQUIRED_EVIDENCE_PATHS:
        if not (ROOT / rel).exists():
            raise SystemExit(f"missing evidence path: {rel}")

    iface = data.get("available_observable_interface", {})
    if iface.get("required_model_method") != "model.H(z)":
        raise SystemExit("model.H(z) dependency not recorded")

    print("DFM-MKC dynamical core v1 scaffold verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
