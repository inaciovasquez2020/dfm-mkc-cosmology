#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dark_matter_replacement_validation_toolkit_2026_05_27.json")

REQUIRED_KEYS = {
    "id",
    "date",
    "status",
    "purpose",
    "mainstream_target_to_replace",
    "required_closed_objects",
    "required_observables",
    "minimum_victory_condition",
    "current_missing_objects",
    "does_not_prove",
    "next_admissible_objects",
}

REQUIRED_STATUS = "VALIDATION_TOOLKIT_ONLY_NOT_EXPERIMENTALLY_VALIDATED"

REQUIRED_OBJECTS = {
    "closed_action_functional_or_field_equations",
    "matter_coupling_rule",
    "cosmological_background_solution",
    "linear_perturbation_system",
    "prediction_vector_generator",
    "likelihood_rule",
    "parameter_table",
    "baseline_lcdm_comparison",
    "blind_forecast_protocol",
    "external_replication_packet",
}

REQUIRED_OBSERVABLES = {
    "galaxy_rotation_curves",
    "weak_lensing",
    "strong_lensing",
    "cluster_lensing_mass_offsets",
    "bullet_cluster_type_separation",
    "cmb_tt_te_ee_spectra",
    "cmb_lensing",
    "bao_distance_ladder",
    "matter_power_spectrum",
    "growth_rate_observables",
    "cluster_abundance",
    "cosmic_shear",
}

REQUIRED_BOUNDARIES = {
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

REQUIRED_NEXT = {
    "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1",
    "DFM_MKC_FIELD_EQUATIONS_V1",
    "DFM_MKC_MATTER_COUPLING_RULE_V1",
    "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
    "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def main() -> None:
    require(ART.exists(), f"missing artifact: {ART}")
    data = json.loads(ART.read_text())

    missing_keys = REQUIRED_KEYS - set(data)
    require(not missing_keys, f"missing keys: {sorted(missing_keys)}")

    require(data["status"] == REQUIRED_STATUS, f"bad status: {data['status']}")

    objects = set(data["required_closed_objects"])
    require(REQUIRED_OBJECTS <= objects, f"missing required closed objects: {sorted(REQUIRED_OBJECTS - objects)}")

    observables = set(data["required_observables"])
    require(REQUIRED_OBSERVABLES <= observables, f"missing required observables: {sorted(REQUIRED_OBSERVABLES - observables)}")

    boundaries = set(data["does_not_prove"])
    require(REQUIRED_BOUNDARIES <= boundaries, f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    next_objects = set(data["next_admissible_objects"])
    require(REQUIRED_NEXT <= next_objects, f"missing next admissible objects: {sorted(REQUIRED_NEXT - next_objects)}")

    victory = data["minimum_victory_condition"]
    require("statement" in victory, "missing minimum victory statement")
    require("required_before_claim" in victory, "missing required_before_claim")
    require("blind_holdout_success" in victory["required_before_claim"], "missing blind holdout requirement")
    require("independent_reproduction" in victory["required_before_claim"], "missing independent reproduction requirement")

    print("DARK_MATTER_REPLACEMENT_VALIDATION_TOOLKIT_OK")
    print(json.dumps({
        "status": data["status"],
        "closed_object_count": len(data["required_closed_objects"]),
        "observable_count": len(data["required_observables"]),
        "missing_object_count": len(data["current_missing_objects"]),
        "next_admissible_objects": data["next_admissible_objects"]
    }, indent=2))

if __name__ == "__main__":
    main()
