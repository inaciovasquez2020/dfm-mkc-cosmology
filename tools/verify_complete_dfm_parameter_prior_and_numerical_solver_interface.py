#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/complete_dfm_parameter_prior_and_numerical_solver_interface_2026_05_22.json"
DOC = ROOT / "docs/status/COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE_2026_05_22.md"
SPEC = ROOT / "specs/COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE.md"

STATUS = "SOLVER_INTERFACE_ONLY_NO_EXECUTED_VALIDATION"
NEXT = "EXECUTABLE_DFM_BACKGROUND_SOLVER_WITH_SYNTHETIC_SANITY_CHECK"

PARAMETERS = {
    "H0",
    "Omega_b0",
    "Omega_c0",
    "Omega_r0",
    "V0",
    "lambda",
    "beta",
    "Phi_i",
    "dot_Phi_i",
}

BOUNDARIES = {
    "DFM-MKC validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "gravity closure",
    "empirical validation",
    "ACT validation",
    "DESI validation",
    "DES validation",
    "P vs NP",
    "any Clay problem",
}

GATES = {
    "parameter_vector_complete",
    "solver_rhs_defined",
    "lambda_cdm_limit_checked",
    "observable_prediction_map_defined",
    "holdout_likelihood_not_executed",
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ARTIFACT.exists(), f"Missing artifact: {ARTIFACT}")
    require(DOC.exists(), f"Missing doc: {DOC}")
    require(SPEC.exists(), f"Missing spec: {SPEC}")

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    doc = DOC.read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")

    require(data["id"] == "COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE", "Bad id")
    require(data["status"] == STATUS, "Bad status")
    require(data["next_admissible_object"] == NEXT, "Bad next object")
    require(set(data["does_not_prove"]) == BOUNDARIES, "Bad boundary set")
    require(set(data["validation_gates"]) == GATES, "Bad validation gates")

    parameter_symbols = {row["symbol"] for row in data["parameter_vector"]}
    require(parameter_symbols == PARAMETERS, "Bad parameter vector")
    require(len(data["parameter_vector"]) == 9, "Expected nine parameters")

    solver = data["solver_interface"]
    require(solver["independent_variable"] == "N=ln(a)", "Bad independent variable")
    require("lambda_cdm_limit" in solver, "Missing Lambda-CDM limit")
    require("H^2=(1/(3M_Pl^2))(rho_b+rho_r+rho_c+0.5 dot_Phi^2+V0 exp(-lambda Phi/M_Pl))" in solver["constraints"], "Missing Friedmann constraint")

    obs = data["observable_interface"]
    require(obs["likelihood_rule"] == "logL(theta)=-(1/2)chi2_total(theta)", "Bad likelihood rule")
    require("H(z)" in obs["background_outputs"], "Missing H(z)")
    require("D_M(z)/r_d" in obs["bao_outputs"], "Missing BAO output")
    require("ell_A" in obs["cmb_act_compressed_outputs"], "Missing ACT/CMB output")
    require("mu(z)" in obs["sne_des_outputs"], "Missing SNe/DES output")

    for phrase in [STATUS, NEXT, "MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1"]:
        require(phrase in doc + spec, f"Missing phrase: {phrase}")

    for boundary in BOUNDARIES:
        require(boundary in doc, f"Doc missing boundary: {boundary}")
        require(boundary in spec, f"Spec missing boundary: {boundary}")

    print("Complete DFM parameter-prior and numerical-solver interface verification OK.")
    print(f"Status: {STATUS}")
    print(f"Next admissible object: {NEXT}")

if __name__ == "__main__":
    main()
