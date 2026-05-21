#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_frozen_axioms_placeholder_2026_05_21.json")
STATUS_DOC = Path("docs/status/DFM_MKC_FROZEN_AXIOMS_PLACEHOLDER_2026_05_21.md")

EXPECTED_STATUS = "FROZEN_AXIOMS_PLACEHOLDER_ONLY_FIELD_EQUATIONS_NOT_SUPPLIED"

REQUIRED_SLOTS = [
    "action_functional",
    "field_equations",
    "matter_coupling_rule",
    "parameter_table",
    "boundary_conditions",
    "prediction_map",
]

REQUIRED_BOUNDARY = [
    "placeholder only",
    "does not supply DFM-MKC field equations",
    "does not supply an action functional",
    "does not supply a likelihood rule",
    "does not execute the likelihood",
    "does not compute residuals",
    "does not supply empirical evidence",
    "does not promote any empirical slot",
]

REQUIRED_NONCLAIMS = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing artifact: {ARTIFACT}")
    if not STATUS_DOC.exists():
        fail(f"missing status doc: {STATUS_DOC}")

    data = json.loads(ARTIFACT.read_text())
    text = STATUS_DOC.read_text()

    if data.get("status") != EXPECTED_STATUS:
        fail("unexpected status")

    slots = data.get("frozen_axiom_slots", {})
    if list(slots.keys()) != REQUIRED_SLOTS:
        fail("slot list mismatch")

    for slot in REQUIRED_SLOTS:
        if slots[slot] is not None:
            fail(f"slot is not placeholder-null: {slot}")
        if slot not in text:
            fail(f"missing slot in status doc: {slot}")

    for boundary in REQUIRED_BOUNDARY:
        if boundary not in data["boundary"]:
            fail(f"missing artifact boundary: {boundary}")
        if boundary not in text:
            fail(f"missing status boundary: {boundary}")

    for nonclaim in REQUIRED_NONCLAIMS:
        if nonclaim not in data["does_not_prove"]:
            fail(f"missing artifact nonclaim: {nonclaim}")
        if nonclaim not in text:
            fail(f"missing status nonclaim: {nonclaim}")

    print("DFM-MKC frozen axioms placeholder verification OK.")
    print(f"Status: {EXPECTED_STATUS}")

if __name__ == "__main__":
    main()
