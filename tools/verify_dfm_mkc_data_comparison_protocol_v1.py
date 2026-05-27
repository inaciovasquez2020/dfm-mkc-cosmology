#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_data_comparison_protocol_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_DATA_COMPARISON_PROTOCOL_V1_2026_05_27.md")
SOURCE = Path("artifacts/repo_intake/dfm_mkc_act_planck_desi_prediction_vector_v1_2026_05_27.json")

REQUIRED_BOUNDARIES = {
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
    require(SOURCE.exists(), f"missing source prediction-vector artifact: {SOURCE}")

    data = json.loads(ART.read_text())
    require(data["id"] == "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1", "bad id")
    require(data["status"] == "DATA_COMPARISON_PROTOCOL_SUPPLIED_NO_EMPIRICAL_RUN", "bad status")
    require("DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in data["source_dependencies"], "missing prediction-vector dependency")

    blob = "\n".join(flat(data))
    for term in [
        "ACT DR6",
        "Planck",
        "DESI",
        "LCDM baseline prediction vector",
        "DFM-MKC prediction vector",
        "chi2",
        "delta_chi2",
        "log_likelihood",
        "AIC",
        "BIC",
        "whitened_residual_vector",
    ]:
        require(term in blob, f"missing protocol term: {term}")

    acceptance = data["acceptance_test_result"]
    for key in [
        "datasets_declared_present",
        "comparison_contract_present",
        "metrics_present",
        "acceptance_thresholds_present",
        "requires_prediction_vector",
    ]:
        require(acceptance.get(key) is True, f"acceptance flag not true: {key}")

    for key in [
        "numerical_run_supplied",
        "likelihood_values_supplied",
        "empirical_status_promoted",
        "lambda_cdm_failure_promoted",
        "dark_matter_replacement_promoted",
    ]:
        require(acceptance.get(key) is False, f"acceptance flag not false: {key}")

    missing_boundaries = REQUIRED_BOUNDARIES - set(data["does_not_prove"])
    require(not missing_boundaries, f"missing boundaries: {sorted(missing_boundaries)}")

    text = DOC.read_text()
    for term in [
        "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1",
        "DATA_COMPARISON_PROTOCOL_SUPPLIED_NO_EMPIRICAL_RUN",
        "Does not prove",
        "DFM-MKC empirical validation",
        "Lambda-CDM failure",
        "any Clay problem",
    ]:
        require(term in text, f"doc missing term: {term}")

    print("DFM_MKC_DATA_COMPARISON_PROTOCOL_V1_OK")
    print(json.dumps({
        "status": data["status"],
        "object": data["id"],
        "downstream_objects_still_required": data["downstream_objects_still_required"],
        "next_admissible_step": data["next_admissible_step"],
    }, indent=2))


if __name__ == "__main__":
    main()
