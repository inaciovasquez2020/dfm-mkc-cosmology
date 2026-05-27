#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_numerical_boltzmann_solver_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1_2026_05_27.md")

SOURCE_ARTIFACTS = [
    Path("artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_linear_perturbation_system_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_act_planck_desi_prediction_vector_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_data_comparison_protocol_v1_2026_05_27.json"),
]

REQUIRED_BOUNDARIES = {
    "DFM-MKC executable Boltzmann solver",
    "DFM-MKC trusted external solver binding",
    "DFM-MKC numerical prediction vector",
    "DFM-MKC data comparison run",
    "DFM-MKC likelihood improvement",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter is a phase",
    "CMB fit",
    "ACT fit",
    "Planck fit",
    "DESI fit",
    "BAO fit",
    "weak lensing fit",
    "Boltzmann solver implementation",
    "matter power spectrum fit",
    "gravity closure",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def flat(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from flat(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from flat(value)
    else:
        yield str(obj)


def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing doc: {DOC}")
    for source in SOURCE_ARTIFACTS:
        require(source.exists(), f"missing source artifact: {source}")

    data = json.loads(ART.read_text())
    require(data["id"] == "DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1", "bad id")
    require(data["status"] == "SOLVER_INTERFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION", "bad status")

    blob = "\n".join(flat(data))
    for term in [
        "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
        "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
        "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1",
        "T_Psi(k, eta)",
        "T_delta_phi(k, eta)",
        "C_ell_TT_ACT",
        "C_ell_TT_Planck",
        "D_M_over_r_d",
        "P_k_linear",
        "sigma8",
        "constraint_residuals",
        "CLASS-compatible external binding",
        "CAMB-compatible external binding",
    ]:
        require(term in blob, f"missing term: {term}")

    acceptance = data["acceptance_test_result"]
    for key in [
        "source_dependencies_present",
        "solver_inputs_present",
        "equation_blocks_present",
        "required_numerical_methods_present",
        "required_solver_outputs_present",
        "external_solver_binding_option_present",
    ]:
        require(acceptance.get(key) is True, f"acceptance flag not true: {key}")

    for key in [
        "numerical_integration_supplied",
        "executable_solver_supplied",
        "trusted_external_binding_supplied",
        "prediction_vector_computed",
        "likelihood_run_supplied",
        "data_comparison_run_supplied",
        "empirical_status_promoted",
    ]:
        require(acceptance.get(key) is False, f"acceptance flag not false: {key}")

    missing_boundaries = REQUIRED_BOUNDARIES - set(data["does_not_prove"])
    require(not missing_boundaries, f"missing boundaries: {sorted(missing_boundaries)}")

    text = DOC.read_text()
    for term in [
        "DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1",
        "SOLVER_INTERFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION",
        "Does not prove",
        "DFM-MKC executable Boltzmann solver",
        "DFM-MKC empirical validation",
        "Lambda-CDM failure",
        "any Clay problem",
    ]:
        require(term in text, f"doc missing term: {term}")

    print("DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1_OK")
    print(json.dumps({
        "status": data["status"],
        "object": data["id"],
        "downstream_objects_still_required": data["downstream_objects_still_required"],
        "next_admissible_step": data["next_admissible_step"],
    }, indent=2))


if __name__ == "__main__":
    main()
