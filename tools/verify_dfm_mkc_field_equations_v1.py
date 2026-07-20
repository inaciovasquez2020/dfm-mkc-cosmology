#!/usr/bin/env python3
import json
from pathlib import Path

import sympy as sp

ART = Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_FIELD_EQUATIONS_V1_2026_05_27.md")
SOURCE = Path("artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json")

REQUIRED_STATUS = "CONCRETE_FIELD_EQUATIONS_DERIVED_PHENOMENOLOGICAL_ONLY"

REQUIRED_TOP_LEVEL_KEYS = {
    "id",
    "date",
    "status",
    "source_dependency",
    "source_artifact",
    "object_type",
    "purpose",
    "action_recalled",
    "metric_equation",
    "dark_sector_equations",
    "constraint_equations",
    "conservation_laws",
    "stress_energy_tensor",
    "gauge_or_coordinate_conditions",
    "known_limit_recovery",
    "derivation_status",
    "acceptance_test_result",
    "downstream_objects_still_required",
    "does_not_prove",
    "next_admissible_step",
}

REQUIRED_DOWNSTREAM = {
    "DFM_MKC_MATTER_COUPLING_RULE_V1",
    "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
    "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
}

REQUIRED_BOUNDARIES = {
    "DFM-MKC matter coupling law",
    "DFM-MKC linear perturbation system",
    "DFM-MKC ACT Planck DESI prediction vector",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter is a phase",
    "dark energy resolution",
    "dark matter resolution",
    "gravity closure",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

REQUIRED_ACCEPTANCE_TRUE = {
    "metric_equation_present",
    "dark_sector_equations_present",
    "constraint_equations_present",
    "conservation_laws_present",
    "stress_energy_tensor_present",
    "gauge_or_coordinate_conditions_present",
    "known_limit_recovery_present",
}

REQUIRED_DERIVATION_TRUE = {
    "metric_variation_performed",
    "phi_variation_performed",
    "theta_variation_performed",
    "visible_sector_equation_deferred_to_L_vis",
    "derived_without_post_hoc_terms",
    "derived_from_closed_action_functional_v1",
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def flatten_values(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from flatten_values(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from flatten_values(value)
    else:
        yield str(obj)


def verify_flat_flrw_reduction() -> None:
    """Verify the homogeneous (-+++) FLRW reduction algebraically."""
    alpha, beta, phi, phi_dot, phi_ddot = sp.symbols(
        "alpha beta phi phi_dot phi_ddot",
        nonzero=True,
    )
    theta_dot, H, a, U, U_prime, Q_theta = sp.symbols(
        "theta_dot H a U U_prime Q_theta",
        nonzero=True,
    )

    box_phi = -(phi_ddot + 3 * H * phi_dot)
    nabla_theta_squared = -(theta_dot**2)

    covariant_phi_equation = (
        alpha * box_phi
        - beta * phi * nabla_theta_squared
        - U_prime
    )
    flrw_phi_equation = (
        alpha * (phi_ddot + 3 * H * phi_dot)
        - beta * phi * theta_dot**2
        + U_prime
    )

    require(
        sp.simplify(covariant_phi_equation + flrw_phi_equation) == 0,
        "FLRW phi equation does not follow from the covariant equation",
    )

    rho = (
        alpha * phi_dot**2 / 2
        + beta * phi**2 * theta_dot**2 / 2
        + U
    )
    pressure = (
        alpha * phi_dot**2 / 2
        + beta * phi**2 * theta_dot**2 / 2
        - U
    )

    require(
        sp.simplify(
            rho
            + pressure
            - alpha * phi_dot**2
            - beta * phi**2 * theta_dot**2
        ) == 0,
        "dark-sector rho+p identity failed",
    )

    theta_dot_from_charge = Q_theta / (a**3 * beta * phi**2)

    require(
        sp.simplify(
            beta * phi**2 * theta_dot_from_charge**2 / 2
            - Q_theta**2 / (2 * beta * a**6 * phi**2)
        ) == 0,
        "charge-reduced phase energy identity failed",
    )

    require(
        sp.simplify(
            beta * phi * theta_dot_from_charge**2
            - Q_theta**2 / (beta * a**6 * phi**3)
        ) == 0,
        "charge-reduced phi-force identity failed",
    )



def verify_conditional_dust_radiation_charge_reduced_ivp() -> None:
    """Verify the conditional dust-radiation charge-reduced IVP."""
    a, alpha, beta, phi = sp.symbols(
        "a alpha beta phi",
        nonzero=True,
    )
    H, v, rho_m, rho_r = sp.symbols(
        "H v rho_m rho_r",
    )
    G, Lambda, Q_theta = sp.symbols(
        "G Lambda Q_theta",
    )
    rho_star, m_phi_squared, lambda_phi = sp.symbols(
        "rho_star m_phi_squared lambda_phi",
    )

    potential = (
        rho_star
        + m_phi_squared * phi**2 / 2
        + lambda_phi * phi**4 / 4
    )
    potential_prime = (
        m_phi_squared * phi
        + lambda_phi * phi**3
    )

    require(
        sp.simplify(
            sp.diff(potential, phi) - potential_prime
        ) == 0,
        "quartic potential derivative identity failed",
    )

    phase_energy = (
        Q_theta**2
        / (2 * beta * a**6 * phi**2)
    )

    rho_dfm = (
        alpha * v**2 / 2
        + phase_energy
        + potential
    )
    pressure_dfm = (
        alpha * v**2 / 2
        + phase_energy
        - potential
    )

    rho_visible = rho_m + rho_r
    pressure_visible = rho_r / 3

    require(
        sp.simplify(
            rho_visible
            + pressure_visible
            - rho_m
            - sp.Rational(4, 3) * rho_r
        ) == 0,
        "visible dust-radiation rho+p identity failed",
    )

    rho_total = rho_visible + rho_dfm
    pressure_total = pressure_visible + pressure_dfm

    a_dot = a * H
    phi_dot = v
    v_dot = (
        -3 * H * v
        + Q_theta**2
        / (alpha * beta * a**6 * phi**3)
        - potential_prime / alpha
    )
    rho_m_dot = -3 * H * rho_m
    rho_r_dot = -4 * H * rho_r

    rho_total_dot = sp.simplify(
        sp.diff(rho_total, a) * a_dot
        + sp.diff(rho_total, phi) * phi_dot
        + sp.diff(rho_total, v) * v_dot
        + sp.diff(rho_total, rho_m) * rho_m_dot
        + sp.diff(rho_total, rho_r) * rho_r_dot
    )

    require(
        sp.simplify(
            rho_total_dot
            + 3 * H * (rho_total + pressure_total)
        ) == 0,
        "conditional total continuity identity failed",
    )

    H_dot = (
        -4 * sp.pi * G
        * (rho_total + pressure_total)
    )

    friedmann_derivative_residual = sp.simplify(
        2 * H * H_dot
        - (8 * sp.pi * G / 3) * rho_total_dot
    )

    require(
        friedmann_derivative_residual == 0,
        "Friedmann-Raychaudhuri compatibility identity failed",
    )


def main() -> None:
    verify_flat_flrw_reduction()
    verify_conditional_dust_radiation_charge_reduced_ivp()

    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing status doc: {DOC}")
    require(SOURCE.exists(), f"missing source action artifact: {SOURCE}")

    data = json.loads(ART.read_text())

    missing_keys = REQUIRED_TOP_LEVEL_KEYS - set(data)
    require(not missing_keys, f"missing top-level keys: {sorted(missing_keys)}")

    require(data["id"] == "DFM_MKC_FIELD_EQUATIONS_V1", f"bad id: {data['id']}")
    require(data["status"] == REQUIRED_STATUS, f"bad status: {data['status']}")
    require(data["source_dependency"] == "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1", "bad source dependency")

    metric_blob = "\n".join(flatten_values(data["metric_equation"]))
    require("G_{mu nu} + Lambda g_{mu nu}" in metric_blob, "missing metric equation")
    require("T_vis_{mu nu}" in metric_blob, "missing visible stress-energy")
    require("T_DFM_MKC_{mu nu}" in metric_blob, "missing dark stress-energy")
    require(data["metric_equation"]["post_hoc_source_terms_added"] is False, "post-hoc metric source terms must be false")

    dark_blob = "\n".join(flatten_values(data["dark_sector_equations"]))
    require("alpha Box_g phi" in dark_blob, "missing phi equation")
    require("nabla_mu(beta phi^2 nabla^mu theta)" in dark_blob, "missing theta equation")
    require(data["dark_sector_equations"]["post_hoc_force_terms_added"] is False, "post-hoc force terms must be false")

    constraint_blob = "\n".join(flatten_values(data["constraint_equations"]))
    require("nabla^mu" in constraint_blob, "missing covariant conservation constraint")
    require("J_theta" in constraint_blob, "missing phase current conservation")

    conservation_blob = "\n".join(flatten_values(data["conservation_laws"]))
    require("T_vis_{mu nu}" in conservation_blob, "missing visible conservation term")
    require("T_DFM_MKC_{mu nu}" in conservation_blob, "missing dark conservation term")

    stress_blob = "\n".join(flatten_values(data["stress_energy_tensor"]))
    require("alpha nabla_mu phi nabla_nu phi" in stress_blob, "missing phi stress term")
    require("beta phi^2 nabla_mu theta nabla_nu theta" in stress_blob, "missing theta stress term")
    require("U(phi)" in stress_blob, "missing potential stress term")

    gauge_blob = "\n".join(flatten_values(data["gauge_or_coordinate_conditions"]))
    require("No coordinate gauge is fixed" in gauge_blob, "missing covariant gauge statement")
    require("DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in gauge_blob, "missing perturbation deferral")

    known_limits = data["known_limit_recovery"]
    require(isinstance(known_limits, list) and len(known_limits) >= 4, "insufficient known-limit recovery entries")

    derivation = data["derivation_status"]
    for key in REQUIRED_DERIVATION_TRUE:
        require(derivation.get(key) is True, f"derivation flag not true: {key}")

    acceptance = data["acceptance_test_result"]
    require(acceptance["target"] == "DFM_MKC_FIELD_EQUATIONS_V1", "bad acceptance target")
    for key in REQUIRED_ACCEPTANCE_TRUE:
        require(acceptance.get(key) is True, f"acceptance flag not true: {key}")
    require(acceptance["empirical_status_promoted"] is False, "must not promote empirical status")

    downstream = set(data["downstream_objects_still_required"])
    require(REQUIRED_DOWNSTREAM <= downstream, f"missing downstream objects: {sorted(REQUIRED_DOWNSTREAM - downstream)}")

    boundaries = set(data["does_not_prove"])
    missing_boundaries = REQUIRED_BOUNDARIES - boundaries
    require(not missing_boundaries, f"missing boundaries: {sorted(missing_boundaries)}")

    require(
        data["next_admissible_step"] == "Supply DFM_MKC_MATTER_COUPLING_RULE_V1 as the explicit visible-sector and photon coupling interface.",
        "bad next admissible step",
    )

    text = DOC.read_text()
    required_doc_terms = [
        "DFM_MKC_FIELD_EQUATIONS_V1",
        "CONCRETE_FIELD_EQUATIONS_DERIVED_PHENOMENOLOGICAL_ONLY",
        "G_{mu nu} + Lambda g_{mu nu}",
        "T_DFM_MKC_{mu nu}",
        "alpha Box_g phi",
        "nabla_mu(beta phi^2 nabla^mu theta)",
        "Does not prove",
        "DFM_MKC_MATTER_COUPLING_RULE_V1",
    ]
    for term in required_doc_terms:
        require(term in text, f"doc missing term: {term}")

    for boundary in REQUIRED_BOUNDARIES:
        require(boundary.lower() in text.lower(), f"doc missing boundary: {boundary}")

    print("DFM_MKC_FIELD_EQUATIONS_V1_OK")
    print(json.dumps({
        "status": data["status"],
        "object": data["id"],
        "source_dependency": data["source_dependency"],
        "downstream_objects_still_required": data["downstream_objects_still_required"],
        "next_admissible_step": data["next_admissible_step"],
    }, indent=2))

if __name__ == "__main__":
    main()
