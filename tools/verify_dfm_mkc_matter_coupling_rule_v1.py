#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_MATTER_COUPLING_RULE_V1_2026_05_27.md")
SOURCE = Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json")

REQUIRED_STATUS = "CONCRETE_MATTER_COUPLING_RULE_SUPPLIED_PHENOMENOLOGICAL_ONLY"

REQUIRED_TOP_LEVEL_KEYS = {
    "id",
    "date",
    "status",
    "source_dependency",
    "source_artifact",
    "object_type",
    "purpose",
    "coupling_principle",
    "ordinary_matter_coupling",
    "photon_coupling",
    "geodesic_or_optical_rule",
    "stress_energy_exchange_rule",
    "equivalence_principle_status",
    "lensing_prediction_rule",
    "radiation_limit",
    "baryonic_limit",
    "downstream_pipeline_targets",
    "acceptance_test_result",
    "downstream_objects_still_required",
    "does_not_prove",
    "next_admissible_step",
}

REQUIRED_ACCEPTANCE_TRUE = {
    "ordinary_matter_coupling_present",
    "photon_coupling_present",
    "geodesic_or_optical_rule_present",
    "stress_energy_exchange_rule_present",
    "equivalence_principle_status_present",
    "lensing_prediction_rule_present",
    "baryonic_limit_present",
    "radiation_limit_present",
}

REQUIRED_ACCEPTANCE_FALSE = {
    "direct_visible_dark_couplings_introduced",
    "dataset_tuned_couplings_introduced",
    "empirical_status_promoted",
}

REQUIRED_DOWNSTREAM = {
    "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
    "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
    "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1",
}

REQUIRED_BOUNDARIES = {
    "DFM-MKC linear perturbation system",
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
    require(SOURCE.exists(), f"missing source field-equations artifact: {SOURCE}")

    data = json.loads(ART.read_text())

    missing_keys = REQUIRED_TOP_LEVEL_KEYS - set(data)
    require(not missing_keys, f"missing top-level keys: {sorted(missing_keys)}")

    require(data["id"] == "DFM_MKC_MATTER_COUPLING_RULE_V1", f"bad id: {data['id']}")
    require(data["status"] == REQUIRED_STATUS, f"bad status: {data['status']}")
    require(data["source_dependency"] == "DFM_MKC_FIELD_EQUATIONS_V1", "bad source dependency")

    principle = data["coupling_principle"]
    require(principle["direct_phi_visible_coupling"] is False, "direct phi-visible coupling must be false")
    require(principle["direct_theta_visible_coupling"] is False, "direct theta-visible coupling must be false")
    require(principle["dataset_tuned_couplings_allowed"] is False, "dataset-tuned couplings must be false")
    require("metric" in principle["statement"].lower(), "coupling statement must be metric based")

    ordinary_blob = "\n".join(flatten_values(data["ordinary_matter_coupling"]))
    require("S_vis" in ordinary_blob, "missing visible action")
    require("T_vis_{mu nu}" in ordinary_blob, "missing visible stress-energy")
    require("u^mu nabla_mu u^nu = 0" in ordinary_blob, "missing massive geodesic rule")

    photon_blob = "\n".join(flatten_values(data["photon_coupling"]))
    require("S_EM" in photon_blob, "missing Maxwell action")
    require("F_{mu nu}" in photon_blob, "missing field strength")
    require("k^mu k_mu = 0" in photon_blob, "missing null condition")
    require("k^mu nabla_mu k^nu = 0" in photon_blob, "missing photon geodesic rule")
    require(data["photon_coupling"]["direct_phi_photon_coupling"] is False, "direct phi-photon coupling must be false")
    require(data["photon_coupling"]["direct_theta_photon_coupling"] is False, "direct theta-photon coupling must be false")

    exchange_blob = "\n".join(flatten_values(data["stress_energy_exchange_rule"]))
    require("T_vis_{mu nu}" in exchange_blob, "missing visible conservation")
    require("T_DFM_MKC_{mu nu}" in exchange_blob, "missing dark conservation")
    require("Q_nu = 0" in exchange_blob, "missing zero exchange current")

    equivalence_blob = "\n".join(flatten_values(data["equivalence_principle_status"]))
    require("weak equivalence principle" in equivalence_blob.lower(), "missing weak equivalence principle status")
    require(data["equivalence_principle_status"]["violation_terms_introduced"] is False, "equivalence violation terms must be false")

    lensing_blob = "\n".join(flatten_values(data["lensing_prediction_rule"]))
    require("null geodesics" in lensing_blob.lower(), "missing null geodesic lensing rule")
    require("DFM-MKC" in lensing_blob, "missing DFM-MKC lensing route")

    downstream_targets = {target["id"] for target in data["downstream_pipeline_targets"]}
    require(REQUIRED_DOWNSTREAM <= downstream_targets, f"missing downstream pipeline targets: {sorted(REQUIRED_DOWNSTREAM - downstream_targets)}")

    acceptance = data["acceptance_test_result"]
    require(acceptance["target"] == "DFM_MKC_MATTER_COUPLING_RULE_V1", "bad acceptance target")
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
        data["next_admissible_step"] == "Supply DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1 from the field equations and matter coupling rule.",
        "bad next admissible step",
    )

    text = DOC.read_text()
    required_doc_terms = [
        "DFM_MKC_MATTER_COUPLING_RULE_V1",
        "CONCRETE_MATTER_COUPLING_RULE_SUPPLIED_PHENOMENOLOGICAL_ONLY",
        "Visible matter and photons couple to the spacetime metric",
        "S_vis",
        "T_vis_{mu nu}",
        "S_EM",
        "k^mu k_mu = 0",
        "Q_nu = 0",
        "Does not prove",
        "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1",
        "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1",
        "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1",
    ]
    for term in required_doc_terms:
        require(term in text, f"doc missing term: {term}")

    for boundary in REQUIRED_BOUNDARIES:
        require(boundary.lower() in text.lower(), f"doc missing boundary: {boundary}")

    print("DFM_MKC_MATTER_COUPLING_RULE_V1_OK")
    print(json.dumps({
        "status": data["status"],
        "object": data["id"],
        "source_dependency": data["source_dependency"],
        "downstream_objects_still_required": data["downstream_objects_still_required"],
        "next_admissible_step": data["next_admissible_step"]
    }, indent=2))

if __name__ == "__main__":
    main()
