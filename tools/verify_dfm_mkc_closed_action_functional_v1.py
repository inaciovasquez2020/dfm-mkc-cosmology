#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1_2026_05_27.md")

REQUIRED_STATUS = "CONCRETE_ACTION_FUNCTIONAL_SUPPLIED_PHENOMENOLOGICAL_ONLY"

REQUIRED_TOP_LEVEL_KEYS = {
    "id",
    "date",
    "status",
    "source_dependency",
    "object_type",
    "purpose",
    "spacetime_domain",
    "field_inventory",
    "dynamical_variables",
    "allowed_parameters",
    "potential",
    "lagrangian_density",
    "action_integral",
    "variation_rules",
    "boundary_terms",
    "units_and_dimensions",
    "reduction_to_known_limits",
    "acceptance_test_result",
    "downstream_objects_still_required",
    "does_not_prove",
    "next_admissible_step",
}

REQUIRED_TARGET_CONTENTS = {
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
}

REQUIRED_FIELDS = {
    "Lorentzian metric g_{mu nu}",
    "rigidity amplitude phi: M -> R",
    "periodic structural phase theta: M -> R / 2pi Z",
}

REQUIRED_PARAMETERS = {
    "G",
    "Lambda",
    "alpha",
    "beta",
    "m_phi_squared",
    "lambda_phi",
    "rho_star",
}

REQUIRED_DOWNSTREAM = {
    "DFM_MKC_FIELD_EQUATIONS_V1",
    "DFM_MKC_MATTER_COUPLING_RULE_V1",
    "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
    "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
}

REQUIRED_BOUNDARIES = {
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

    data = json.loads(ART.read_text())

    missing_keys = REQUIRED_TOP_LEVEL_KEYS - set(data)
    require(not missing_keys, f"missing top-level keys: {sorted(missing_keys)}")

    require(data["id"] == "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1", f"bad id: {data['id']}")
    require(data["status"] == REQUIRED_STATUS, f"bad status: {data['status']}")
    require(data["object_type"] == "closed covariant action functional", f"bad object type: {data['object_type']}")

    for key in REQUIRED_TARGET_CONTENTS:
        require(key in data, f"missing target content key: {key}")
        require(data[key], f"empty target content key: {key}")

    fields_text = set()
    for value in data["field_inventory"].values():
        if isinstance(value, list):
            fields_text.update(value)
    missing_fields = REQUIRED_FIELDS - fields_text
    require(not missing_fields, f"missing fields: {sorted(missing_fields)}")

    params = set(data["allowed_parameters"])
    missing_params = REQUIRED_PARAMETERS - params
    require(not missing_params, f"missing parameters: {sorted(missing_params)}")

    lagrangian_blob = "\n".join(flatten_values(data["lagrangian_density"]))
    require("(R - 2 Lambda)/(16 pi G)" in lagrangian_blob, "missing Einstein-Hilbert term")
    require("nabla_mu phi" in lagrangian_blob, "missing phi kinetic term")
    require("nabla_mu theta" in lagrangian_blob, "missing theta kinetic term")
    require("U(phi)" in lagrangian_blob, "missing potential term")
    require("L_vis(psi_vis, g)" in lagrangian_blob, "missing visible sector term")

    action = data["action_integral"]
    require(action["closed_action"] is True, "action must be marked closed")
    require(action["post_hoc_terms_allowed"] is False, "post-hoc terms must be forbidden")
    require("S_GHY" in "\n".join(flatten_values(action)), "missing GHY boundary term")

    acceptance = data["acceptance_test_result"]
    require(acceptance["target"] == "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1", "bad acceptance target")
    require(acceptance["required_contents_present"] is True, "required contents not accepted")
    require(acceptance["closed_variational_principle_present"] is True, "closed variational principle not accepted")
    require(acceptance["field_equations_derivable_without_post_hoc_terms"] is True, "field equation derivability not accepted")
    require(acceptance["empirical_status_promoted"] is False, "must not promote empirical status")

    downstream = set(data["downstream_objects_still_required"])
    require(REQUIRED_DOWNSTREAM <= downstream, f"missing downstream objects: {sorted(REQUIRED_DOWNSTREAM - downstream)}")

    boundaries = set(data["does_not_prove"])
    missing_boundaries = REQUIRED_BOUNDARIES - boundaries
    require(not missing_boundaries, f"missing boundaries: {sorted(missing_boundaries)}")

    require(
        data["next_admissible_step"] == "Derive DFM_MKC_FIELD_EQUATIONS_V1 from this action functional.",
        "bad next admissible step"
    )

    text = DOC.read_text()
    required_doc_terms = [
        "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1",
        "CONCRETE_ACTION_FUNCTIONAL_SUPPLIED_PHENOMENOLOGICAL_ONLY",
        "L_total",
        "S_DFM_MKC_V1",
        "Gibbons-Hawking-York",
        "Does not prove",
        "DFM_MKC_FIELD_EQUATIONS_V1",
    ]
    for term in required_doc_terms:
        require(term in text, f"doc missing term: {term}")

    for boundary in REQUIRED_BOUNDARIES:
        require(boundary.lower() in text.lower(), f"doc missing boundary: {boundary}")

    print("DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1_OK")
    print(json.dumps({
        "status": data["status"],
        "object": data["id"],
        "parameter_count": len(data["allowed_parameters"]),
        "downstream_objects_still_required": data["downstream_objects_still_required"],
        "next_admissible_step": data["next_admissible_step"]
    }, indent=2))

if __name__ == "__main__":
    main()
