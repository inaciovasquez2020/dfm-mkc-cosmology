#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_dynamical_core_source_audit_2026_05_21.json"

CANDIDATE_PATHS = [
    "specs/DFM_MKC_dynamical_core_v1.json",
    "theory/deformation_field.md",
    "theory/parameters.md",
    "numerics/background_equations.md",
    "config/dfm_mkc_parameter_freeze.json",
    "dfm_mkc/constants.py",
    "dfm_mkc/model.py",
    "dfm_mkc/likelihoods.py",
    "src/models/dfm_mkc.py",
    "src/cosmology/observables/distances.py",
    "mkc_solver.py",
]

PATTERNS = {
    "action_functional": r"\b(action|lagrangian|functional|S\s*=|L\s*=)\b",
    "primitive_field_equation": r"\b(field equation|eom|equation of motion|H\(z\)|dH|derivative|ode|friedmann|background)\b",
    "matter_coupling": r"\b(matter|baryon|radiation|omega_m|Omega_m|rho_m|pressure|density)\b",
    "dark_sector_coupling": r"\b(dark|deformation|mkc|kappa|coupling|sector)\b",
    "source_terms": r"\b(source|source term|forcing|inhomogeneous|rhs)\b",
    "boundary_conditions": r"\b(boundary|initial condition|z0|a0|today|normalization)\b",
    "parameters": r"\b(parameter|theta|freeze|prior|bounds|omega|Omega|H0|S8|sigma8)\b",
    "prediction_vector": r"\b(prediction|vector|observable|distance|bao|des|act|cmb|residual)\b",
}

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def line_hits(text: str, pattern: str):
    rx = re.compile(pattern, re.IGNORECASE)
    hits = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if rx.search(line):
            hits.append({"line": idx, "text": line[:220]})
    return hits[:25]

def main() -> None:
    files = []
    aggregate_hits = {key: 0 for key in PATTERNS}

    for rel in CANDIDATE_PATHS:
        path = ROOT / rel
        if not path.exists():
            files.append({"path": rel, "exists": False})
            continue

        text = path.read_text(errors="replace")
        pattern_hits = {}
        for key, pattern in PATTERNS.items():
            hits = line_hits(text, pattern)
            pattern_hits[key] = hits
            aggregate_hits[key] += len(hits)

        files.append({
            "path": rel,
            "exists": True,
            "sha256": sha256_text(text),
            "bytes": len(text.encode("utf-8")),
            "line_count": len(text.splitlines()),
            "pattern_hits": pattern_hits,
        })

    supplied_closure_objects = []
    missing_closure_objects = [
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

    data = {
        "schema_version": "DFM_MKC_DYNAMICAL_CORE_SOURCE_AUDIT_V1",
        "status": "SOURCE_AUDIT_ONLY_NO_CLOSURE_PROMOTION",
        "date": "2026-05-21",
        "base_scaffold": "specs/DFM_MKC_dynamical_core_v1.json",
        "candidate_paths": CANDIDATE_PATHS,
        "files": files,
        "aggregate_pattern_hits": aggregate_hits,
        "supplied_closure_objects": supplied_closure_objects,
        "missing_closure_objects": missing_closure_objects,
        "admissible_next_step": "Manually classify any concrete equations/couplings/parameters found by this audit before replacing null fields in specs/DFM_MKC_dynamical_core_v1.json.",
        "does_not_prove": [
            "DFM-MKC",
            "Lambda-CDM failure",
            "ACT/DES holdout survival",
            "independent empirical validation",
            "dark-energy resolution",
            "dark-matter resolution",
            "Nobel-level physical discovery",
            "any Clay problem"
        ]
    }

    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(str(OUT))
    print("DFM-MKC dynamical core source audit built.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
