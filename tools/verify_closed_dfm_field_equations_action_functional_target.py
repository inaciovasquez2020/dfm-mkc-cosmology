#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/closed_dfm_field_equations_action_functional_target_2026_05_22.json"
DOC = ROOT / "docs/status/CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_TARGET_2026_05_22.md"

STATUS = "TARGET_ONLY_OBJECT_NOT_SUPPLIED"
MISSING = "CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL"

BOUNDARIES = {
    "DFM-MKC validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "gravity closure",
    "empirical validation",
    "P vs NP",
    "any Clay problem",
}

REQUIRED = {
    "primitive fields",
    "dynamical equations or variational action",
    "source terms",
    "coupling constants",
    "units and dimensions",
    "gauge or symmetry assumptions",
    "boundary or initial conditions",
    "parameter table",
    "prediction map to observables",
}

data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
doc = DOC.read_text(encoding="utf-8")

assert data["status"] == STATUS
assert data["minimal_missing_object"] == MISSING
assert set(data["required_payload"]) == REQUIRED
assert set(data["does_not_prove"]) == BOUNDARIES

for item in REQUIRED | BOUNDARIES | {STATUS, MISSING}:
    assert item in doc

print("Closed DFM field-equations/action-functional target verification OK.")
print(f"Status: {STATUS}")
print(f"Minimal missing object: {MISSING}")
