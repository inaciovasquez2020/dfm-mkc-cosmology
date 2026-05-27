#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_dark_sector_closed_object_target_packet_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_DARK_SECTOR_CLOSED_OBJECT_TARGET_PACKET_2026_05_27.md")

REQUIRED_STATUS = "TARGET_PACKET_ONLY_OBJECTS_NOT_SUPPLIED"

REQUIRED_TARGETS = {
    "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1",
    "DFM_MKC_FIELD_EQUATIONS_V1",
    "DFM_MKC_MATTER_COUPLING_RULE_V1",
    "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
    "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
}

REQUIRED_BOUNDARIES = {
    "DFM-MKC closed action functional",
    "DFM-MKC field equations",
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

REQUIRED_ACCEPTANCE_FLAGS = {
    "all_targets_must_be_supplied_before_validation_claim",
    "no_single_target_promotes_empirical_status",
    "requires_public_reproducible_code_before_experimental_claim",
    "requires_blind_holdout_success_before_replacement_claim",
    "requires_independent_reproduction_before_mainstream_replacement_claim",
}

REQUIRED_CONTENTS_BY_TARGET = {
    "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1": {
        "spacetime_domain",
        "field_inventory",
        "dynamical_variables",
        "action_integral",
        "lagrangian_density",
        "allowed_parameters",
        "variation_rules",
        "boundary_terms",
        "units_and_dimensions",
        "reduction_to_known_limits",
    },
    "DFM_MKC_FIELD_EQUATIONS_V1": {
        "metric_equation",
        "dark_sector_equation",
        "constraint_equations",
        "conservation_laws",
        "stress_energy_tensor",
        "gauge_or_coordinate_conditions",
        "well_posedness_assumptions",
        "known_limit_recovery",
    },
    "DFM_MKC_MATTER_COUPLING_RULE_V1": {
        "ordinary_matter_coupling",
        "photon_coupling",
        "geodesic_or_optical_rule",
        "stress_energy_exchange_rule",
        "equivalence_principle_status",
        "lensing_prediction_rule",
        "baryonic_limit",
        "radiation_limit",
    },
    "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1": {
        "background_solution",
        "perturbation_variables",
        "gauge_choice",
        "linearized_equations",
        "initial_conditions",
        "transfer_functions",
        "growth_equation",
        "stability_conditions",
        "cmb_observable_mapping",
        "matter_power_mapping",
    },
    "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1": {
        "frozen_parameter_table",
        "dataset_binding",
        "observable_vector_definition",
        "cmb_tt_te_ee_prediction",
        "cmb_lensing_prediction",
        "bao_prediction",
        "matter_power_prediction",
        "likelihood_interface",
        "lcdm_baseline_comparison_rule",
        "blind_holdout_rule",
    },
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    require(DOC.exists(), f"missing status doc: {DOC}")

    data = json.loads(ART.read_text())
    require(data["status"] == REQUIRED_STATUS, f"bad status: {data['status']}")

    targets = data.get("target_objects", [])
    target_ids = {target.get("id") for target in targets}
    require(REQUIRED_TARGETS == target_ids, f"target mismatch: {sorted(REQUIRED_TARGETS ^ target_ids)}")

    for target in targets:
        tid = target["id"]
        require(target["status"] == "MISSING_OBJECT_TARGET_ONLY", f"{tid} has bad status {target['status']}")
        contents = set(target.get("required_contents", []))
        missing_contents = REQUIRED_CONTENTS_BY_TARGET[tid] - contents
        require(not missing_contents, f"{tid} missing contents: {sorted(missing_contents)}")
        require("acceptance_test" in target and target["acceptance_test"], f"{tid} missing acceptance test")

    packet_rule = data.get("packet_acceptance_rule", {})
    missing_flags = REQUIRED_ACCEPTANCE_FLAGS - set(packet_rule)
    require(not missing_flags, f"missing packet flags: {sorted(missing_flags)}")
    for flag in REQUIRED_ACCEPTANCE_FLAGS:
        require(packet_rule[flag] is True, f"packet flag must be true: {flag}")

    boundaries = set(data.get("does_not_prove", []))
    missing_boundaries = REQUIRED_BOUNDARIES - boundaries
    require(not missing_boundaries, f"missing boundaries: {sorted(missing_boundaries)}")

    require(
        data.get("next_admissible_step") == "Supply DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1 as a concrete mathematical object.",
        "bad next admissible step"
    )

    text = DOC.read_text()
    for required in REQUIRED_TARGETS:
        require(required in text, f"doc missing target {required}")
    for boundary in REQUIRED_BOUNDARIES:
        require(boundary.lower() in text.lower(), f"doc missing boundary {boundary}")

    print("DFM_MKC_DARK_SECTOR_CLOSED_OBJECT_TARGET_PACKET_OK")
    print(json.dumps({
        "status": data["status"],
        "target_count": len(targets),
        "targets": sorted(target_ids),
        "next_admissible_step": data["next_admissible_step"]
    }, indent=2))

if __name__ == "__main__":
    main()
