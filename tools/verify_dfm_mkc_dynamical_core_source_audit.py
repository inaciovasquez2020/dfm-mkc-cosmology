#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_dynamical_core_source_audit_2026_05_21.json"

REQUIRED_STATUS = "SOURCE_AUDIT_ONLY_NO_CLOSURE_PROMOTION"
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
    "ExhaustiveParameterTable",
    "FrozenPredictionVector",
    "ACT_DES_HoldoutData",
    "ResidualEvaluationResult",
    "IndependentReplicationResult",
}

def main() -> None:
    if not ARTIFACT.exists():
        raise SystemExit(f"missing artifact: {ARTIFACT}")

    data = json.loads(ARTIFACT.read_text())

    if data.get("status") != REQUIRED_STATUS:
        raise SystemExit("invalid source-audit status")

    boundaries = set(data.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    missing = set(data.get("missing_closure_objects", []))
    if missing != REQUIRED_MISSING:
        raise SystemExit(f"missing closure mismatch: {sorted(REQUIRED_MISSING - missing)}")

    if data.get("supplied_closure_objects") != []:
        raise SystemExit("source audit must not claim supplied closure objects")

    files = data.get("files", [])
    if not files:
        raise SystemExit("source audit has no files")

    for item in files:
        if item.get("exists"):
            if not item.get("sha256"):
                raise SystemExit(f"missing sha256 for {item.get('path')}")
            if item.get("bytes", 0) <= 0:
                raise SystemExit(f"empty file recorded for {item.get('path')}")
            if "pattern_hits" not in item:
                raise SystemExit(f"missing pattern hits for {item.get('path')}")

    if data.get("base_scaffold") != "specs/DFM_MKC_dynamical_core_v1.json":
        raise SystemExit("base scaffold mismatch")

    print("DFM-MKC dynamical core source audit verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
