#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/filled_closed_dfm_field_equations_action_functional_2026_05_22.json"
DOC = ROOT / "docs/status/FILLED_CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_2026_05_22.md"

STATUS = "SUPPLIED_CANDIDATE_DYNAMICAL_CORE_ONLY_NO_VALIDATION"
MODEL = "MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1"

FIELDS = {
    "g_munu Lorentzian metric with signature (-,+,+,+)",
    "Phi real scalar DFM dark-sector field",
    "psi_b baryonic matter fields",
    "psi_c cold dark-sector matter fields",
    "psi_r radiation fields",
    "T_b_munu baryonic stress-energy tensor",
    "T_c_munu cold dark-sector stress-energy tensor",
    "T_r_munu radiation stress-energy tensor",
    "T_Phi_munu scalar DFM stress-energy tensor",
    "T_int_munu interaction-transfer bookkeeping tensor defined through Q_nu",
}

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

REQUIRED_KEYS = {
    "action_functional",
    "closed_equations",
    "flrw_reduction",
    "parameters",
    "observable_prediction_map",
    "lambda_cdm_embedding",
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ARTIFACT.exists(), f"Missing artifact: {ARTIFACT}")
    require(DOC.exists(), f"Missing doc: {DOC}")

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")

    require(data["id"] == "FILLED_CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL", "Bad id")
    require(data["status"] == STATUS, "Bad status")
    require(data["model_name"] == MODEL, "Bad model name")
    require(set(data["primitive_fields"]) == FIELDS, "Bad primitive fields")
    require(set(data["does_not_prove"]) == BOUNDARIES, "Bad does_not_prove set")

    for key in REQUIRED_KEYS:
        require(key in data, f"Missing required section: {key}")

    require(len(data["parameters"]) == 9, "Expected nine parameters")
    require(data["lambda_cdm_embedding"]["limit"], "Missing Lambda-CDM embedding limit")
    require(data["observable_prediction_map"]["likelihood"], "Missing likelihood rule")
    require(data["next_admissible_object"] == "COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE", "Bad next object")

    for phrase in [
        STATUS,
        MODEL,
        "A(Phi)=exp(beta Phi/M_Pl)",
        "Lambda-CDM embedding",
        "COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE",
    ]:
        require(phrase in doc, f"Doc missing phrase: {phrase}")

    for boundary in BOUNDARIES:
        require(boundary in doc, f"Doc missing boundary: {boundary}")

    print("Filled closed DFM field equations/action functional verification OK.")
    print(f"Status: {STATUS}")
    print(f"Model: {MODEL}")

if __name__ == "__main__":
    main()
