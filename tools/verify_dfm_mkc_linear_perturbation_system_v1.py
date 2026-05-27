#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_linear_perturbation_system_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1_2026_05_27.md")
SOURCE_FIELD = Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json")
SOURCE_COUPLING = Path("artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json")

REQUIRED_STATUS = "CONCRETE_LINEAR_PERTURBATION_SYSTEM_SUPPLIED_PHENOMENOLOGICAL_ONLY"

REQUIRED_TOP_LEVEL_KEYS = {
    "id",
    "date",
    "status",
    "source_dependencies",
    "source_artifacts",
    "object_type",
    "purpose",
    "background_solution",
    "gauge_choice",
    "perturbation_variables",
    "linearized_equations",
    "source_terms",
    "initial_conditions",
    "transfer_functions",
    "growth_equation",
    "stability_conditions",
    "cmb_observable_mapping",
    "matter_power_mapping",
    "acceptance_test_result",
    "downstream_objects_still_required",
    "does_not_prove",
    "next_admissible_step",
}

REQUIRED_ACCEPTANCE_TRUE = {
    "background_solution_present",
    "perturbation_variables_present",
    "gauge_choice_present",
    "linearized_equations_present",
    "initial_conditions_present",
    "transfer_functions_present",
    "growth_equation_present",
    "stability_conditions_present",
    "cmb_observable_mapping_present",
    "matter_power_mapping_present",
}

REQUIRED_ACCEPTANCE_FALSE = {
    "prediction_vector_supplied",
    "data_comparison_supplied",
    "empirical_status_promoted",
}

REQUIRED_DOWNSTREAM = {
    "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
    "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1",
}

REQUIRED_BOUNDARIES = {
    "DFM-MKC ACT Planck DESI prediction vector",
    "DFM-MKC data comparison",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter is a phase",
    "galaxy rotation curve fit",
    "CMB fit",
    "BAO fit",
    "weak lensing fit",
    "Bullet Cluster explanation",
    "linear perturbation numerical solution",
    "Boltzmann solver implementation",
    "matter power spectrum fit",
    "cosmic shear fit",
    "dark energy resolution",
    "dark matter resolution",
    "gravity closure",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
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


def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing status doc: {DOC}")
    require(SOURCE_FIELD.exists(), f"missing source field-equations artifact: {SOURCE_FIELD}")
    require(SOURCE_COUPLING.exists(), f"missing source matter-coupling artifact: {SOURCE_COUPLING}")

    data = json.loads(ART.read_text())

    missing_keys = REQUIRED_TOP_LEVEL_KEYS - set(data)
    require(not missing_keys, f"missing top-level keys: {sorted(missing_keys)}")

    require(data["id"] == "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1", f"bad id: {data['id']}")
    require(data["status"] == REQUIRED_STATUS, f"bad status: {data['status']}")
    require("DFM_MKC_FIELD_EQUATIONS_V1" in data["source_dependencies"], "missing field-equations dependency")
    require("DFM_MKC_MATTER_COUPLING_RULE_V1" in data["source_dependencies"], "missing matter-coupling dependency")

    background_blob = "\n".join(flatten_values(data["background_solution"]))
    require("FLRW" in background_blob, "missing FLRW background")
    require("phi_bar" in background_blob, "missing phi background")
    require("theta_bar" in background_blob, "missing theta background")

    gauge_blob = "\n".join(flatten_values(data["gauge_choice"]))
    require("Newtonian gauge" in gauge_blob, "missing Newtonian gauge")
    require("Psi" in gauge_blob, "missing Psi")
    require("Phi" in gauge_blob, "missing Phi")

    variables_blob = "\n".join(flatten_values(data["perturbation_variables"]))
    for term in ["delta_phi", "delta_theta", "delta_b", "v_b", "delta_gamma", "v_gamma"]:
        require(term in variables_blob, f"missing perturbation variable: {term}")

    equations_blob = "\n".join(flatten_values(data["linearized_equations"]))
    for term in [
        "k^2 Phi",
        "Phi_prime + Hc Psi",
        "alpha[delta_phi_double_prime",
        "beta phi_bar^2 delta_theta_prime",
        "delta_b_prime",
        "v_b_prime",
        "delta_gamma_prime",
        "v_gamma_prime",
    ]:
        require(term in equations_blob, f"missing linearized equation term: {term}")

    source_blob = "\n".join(flatten_values(data["source_terms"]))
    require("delta_rho_DFM_MKC" in source_blob, "missing DFM-MKC density source")
    require("T_DFM_MKC_{mu nu}" in source_blob, "missing DFM-MKC stress tensor source")

    initial_blob = "\n".join(flatten_values(data["initial_conditions"]))
    require("R_star" in initial_blob, "missing primordial curvature template")
    require(data["initial_conditions"]["frozen_before_data_claim"] is True, "initial conditions must freeze before data claim")

    transfer_blob = "\n".join(flatten_values(data["transfer_functions"]))
    for term in ["T_Psi", "T_Phi", "T_delta_phi", "T_delta_theta"]:
        require(term in transfer_blob, f"missing transfer function: {term}")

    growth_blob = "\n".join(flatten_values(data["growth_equation"]))
    require("S_DFM_MKC" in growth_blob, "missing DFM-MKC growth source")
    require("No numerical f sigma_8 or P(k) prediction" in growth_blob, "missing no-growth-prediction boundary")

    stability_blob = "\n".join(flatten_values(data["stability_conditions"]))
    require("alpha > 0" in stability_blob, "missing alpha stability sign")
    require("beta > 0" in stability_blob, "missing beta stability sign")
    require(data["stability_conditions"]["full_well_posedness_proved"] is False, "must not claim full well-posedness")

    cmb_blob = "\n".join(flatten_values(data["cmb_observable_mapping"]))
    require("DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in cmb_blob, "missing CMB prediction-vector deferral")
    require(data["cmb_observable_mapping"]["no_cmb_fit_claim"] is True, "must not claim CMB fit")

    matter_blob = "\n".join(flatten_values(data["matter_power_mapping"]))
    require("DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in matter_blob, "missing matter-power prediction-vector deferral")
    require(data["matter_power_mapping"]["no_matter_power_fit_claim"] is True, "must not claim matter-power fit")

    acceptance = data["acceptance_test_result"]
    require(acceptance["target"] == "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1", "bad acceptance target")
    for key in REQUIRED_ACCEPTANCE_TRUE:
        require(acceptance.get(key) is True, f"acceptance flag not true: {key}")
    for key in REQUIRED_ACCEPTANCE_FALSE:
        require(acceptance.get(key) is False, f"acceptance flag not false: {key}")

    downstream = set(data["downstream_objects_still_required"])
    require(REQUIRED_DOWNSTREAM <= downstream, f"missing downstream objects: {sorted(REQUIRED_DOWNSTREAM - downstream)}")

    boundaries = set(data["does_not_prove"])
    missing_boundaries = REQUIRED_BOUNDARIES - boundaries
    require(not missing_boundaries, f"missing boundaries: {sorted(missing_boundaries)}")

    require(
        data["next_admissible_step"] == "Supply DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1 from the linear perturbation system.",
        "bad next admissible step",
    )

    text = DOC.read_text()
    required_doc_terms = [
        "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
        "CONCRETE_LINEAR_PERTURBATION_SYSTEM_SUPPLIED_PHENOMENOLOGICAL_ONLY",
        "Newtonian gauge",
        "delta_phi",
        "delta_theta",
        "k^2 Phi",
        "S_DFM_MKC",
        "Does not prove",
        "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
        "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1",
    ]
    for term in required_doc_terms:
        require(term in text, f"doc missing term: {term}")

    for boundary in REQUIRED_BOUNDARIES:
        require(boundary.lower() in text.lower(), f"doc missing boundary: {boundary}")

    print("DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1_OK")
    print(json.dumps({
        "status": data["status"],
        "object": data["id"],
        "source_dependencies": data["source_dependencies"],
        "downstream_objects_still_required": data["downstream_objects_still_required"],
        "next_admissible_step": data["next_admissible_step"],
    }, indent=2))


if __name__ == "__main__":
    main()
