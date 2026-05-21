#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_full_closure_blocker_certificate_2026_05_21.json"
REGISTRY = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_single_slot_evidence_registry_2026_05_21.json"

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
    cert = json.loads(CERT.read_text())
    registry = json.loads(REGISTRY.read_text())

    if cert.get("status") != "FULL_CLOSURE_BLOCKED_CERTIFICATE":
        raise SystemExit("invalid certificate status")

    if registry.get("status") != "REGISTRY_ONLY_NO_FULL_CLOSURE_PROMOTION":
        raise SystemExit("registry status mismatch")

    if cert.get("closure_possible") is not False:
        raise SystemExit("closure must remain blocked")

    if cert.get("total_required_slots") != 10:
        raise SystemExit("required slot count mismatch")

    if cert.get("registered_slot_count") != 1:
        raise SystemExit("registered slot count mismatch")

    if cert.get("missing_required_slot_count") != 9:
        raise SystemExit("missing slot count mismatch")

    if set(cert.get("missing_required_slots", [])) != REQUIRED_MISSING:
        raise SystemExit("missing required slots mismatch")

    registered = cert.get("registered_slots", [])
    if len(registered) != 1:
        raise SystemExit("registered slot list must contain exactly one item")

    if registered[0].get("slot_name") != "ExhaustiveParameterTable":
        raise SystemExit("registered slot mismatch")

    if registered[0].get("promotion_status") != "NOT_PROMOTED_TO_FULL_CLOSURE":
        raise SystemExit("unexpected promotion status")

    boundaries = set(cert.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    print("DFM-MKC full closure blocker certificate verification OK.")
    print(f"Status: {cert['status']}")

if __name__ == "__main__":
    main()
