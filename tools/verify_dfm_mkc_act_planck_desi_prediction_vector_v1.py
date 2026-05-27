#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_act_planck_desi_prediction_vector_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1_2026_05_27.md")

SOURCE_ARTIFACTS = [
    Path("artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_linear_perturbation_system_v1_2026_05_27.json"),
]

REQUIRED_BOUNDARIES = {
    "DFM-MKC numerical prediction vector",
    "DFM-MKC data comparison",
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
    require(data["id"] == "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1", "bad id")
    require(data["status"] == "PREDICTION_VECTOR_INTERFACE_SUPPLIED_NO_NUMERICAL_EVALUATION", "bad status")

    blob = "\n".join(flat(data))
    for term in [
        "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
        "C_ell_TT_ACT",
        "C_ell_TT_Planck",
        "D_M_over_r_d",
        "P_k_linear",
        "sigma8",
        "C_ell_shear",
    ]:
        require(term in blob, f"missing term: {term}")

    acceptance = data["acceptance_test_result"]
    for key in [
        "input_parameter_block_present",
        "background_solver_outputs_present",
        "perturbation_solver_outputs_present",
        "act_slots_present",
        "planck_slots_present",
        "desi_slots_present",
        "matter_power_slots_present",
        "weak_lensing_slots_present",
        "observable_maps_present",
    ]:
        require(acceptance.get(key) is True, f"acceptance flag not true: {key}")

    for key in [
        "numerical_prediction_vector_supplied",
        "likelihood_supplied",
        "data_comparison_supplied",
        "empirical_status_promoted",
    ]:
        require(acceptance.get(key) is False, f"acceptance flag not false: {key}")

    missing_boundaries = REQUIRED_BOUNDARIES - set(data["does_not_prove"])
    require(not missing_boundaries, f"missing boundaries: {sorted(missing_boundaries)}")

    text = DOC.read_text()
    for term in [
        "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
        "PREDICTION_VECTOR_INTERFACE_SUPPLIED_NO_NUMERICAL_EVALUATION",
        "Does not prove",
        "DFM-MKC empirical validation",
        "Lambda-CDM failure",
        "any Clay problem",
    ]:
        require(term in text, f"doc missing term: {term}")

    print("DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1_OK")
    print(json.dumps({
        "status": data["status"],
        "object": data["id"],
        "downstream_objects_still_required": data["downstream_objects_still_required"],
        "next_admissible_step": data["next_admissible_step"],
    }, indent=2))


if __name__ == "__main__":
    main()
