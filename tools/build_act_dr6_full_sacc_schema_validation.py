#!/usr/bin/env python3
import importlib
import json
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_execution_and_local_sha256_comparison_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_full_sacc_schema_validation_2026_05_22.json"

REQUIRED_STRUCTURAL_CHECKS = [
    "local_payload_exists",
    "reproducible_download_sha256_matched",
    "sacc_module_importable",
    "sacc_load_fits_available",
    "sacc_payload_loads",
    "data_vector_present",
    "covariance_present",
    "tracers_present",
]

def safe_len(obj):
    try:
        return len(obj)
    except Exception:
        return None

def main():
    source = json.loads(SOURCE.read_text())
    local_path = ROOT / source["local_path"]

    checks = {
        "local_payload_exists": local_path.exists(),
        "reproducible_download_sha256_matched": source["download_reproduces_local_sha256"] is True,
        "sacc_module_importable": False,
        "sacc_load_fits_available": False,
        "sacc_payload_loads": False,
        "data_vector_present": False,
        "covariance_present": False,
        "tracers_present": False,
    }

    observed = {
        "sacc_import_error": None,
        "sacc_load_error": None,
        "data_vector_length": None,
        "covariance_shape": None,
        "tracer_count": None,
    }

    try:
        sacc = importlib.import_module("sacc")
        checks["sacc_module_importable"] = True
        load_fits = getattr(getattr(sacc, "Sacc", None), "load_fits", None)
        checks["sacc_load_fits_available"] = callable(load_fits)

        if callable(load_fits):
            loaded = load_fits(str(local_path))
            checks["sacc_payload_loads"] = True

            mean = getattr(loaded, "mean", None)
            covariance = getattr(loaded, "covariance", None)
            tracers = getattr(loaded, "tracers", None)

            observed["data_vector_length"] = safe_len(mean)
            checks["data_vector_present"] = observed["data_vector_length"] is not None and observed["data_vector_length"] > 0

            covmat = getattr(covariance, "covmat", None) if covariance is not None else None
            shape = getattr(covmat, "shape", None)
            observed["covariance_shape"] = list(shape) if shape is not None else None
            checks["covariance_present"] = shape is not None and len(shape) == 2 and shape[0] > 0 and shape[1] > 0

            observed["tracer_count"] = safe_len(tracers) if tracers is not None else None
            checks["tracers_present"] = observed["tracer_count"] is not None and observed["tracer_count"] > 0

    except Exception as exc:
        if not checks["sacc_module_importable"]:
            observed["sacc_import_error"] = repr(exc)
        else:
            observed["sacc_load_error"] = "".join(traceback.format_exception_only(type(exc), exc)).strip()

    full_pass = all(checks.values())
    status = (
        "FULL_SACC_SCHEMA_VALIDATION_PASSED_NOT_LIKELIHOOD_EXECUTION"
        if full_pass else
        "FULL_SACC_SCHEMA_VALIDATION_BLOCKED_OR_PARTIAL"
    )

    artifact = {
        "object": "ACT_DR6_FULL_SACC_SCHEMA_VALIDATION",
        "date": "2026-05-22",
        "status": status,
        "source_object": source["object"],
        "local_path": source["local_path"],
        "local_sha256": source["local_sha256"],
        "required_structural_checks": REQUIRED_STRUCTURAL_CHECKS,
        "checks": checks,
        "observed": observed,
        "full_sacc_schema_validation_passed": full_pass,
        "certified_for_profiled_likelihood_execution": full_pass,
        "required_next_object": (
            "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT"
            if full_pass else
            "INSTALL_SACC_READER_OR_REPAIR_ACT_DR6_SACC_SCHEMA_LOAD"
        ),
        "does_not_prove": [
            "executed multiprobe likelihood run",
            "Lambda-CDM rejection",
            "six-parameter flat Lambda-CDM rejection",
            "alternative-model validation",
            "DFM-MKC validation",
            "dark matter resolution",
            "dark energy resolution",
            "any Clay problem"
        ]
    }

    OUT.write_text(json.dumps(artifact, indent=2) + "\n")
    print("ACT DR6 full SACC schema validation artifact written.")
    print("Status:", status)
    print("Full SACC schema validation passed:", full_pass)

if __name__ == "__main__":
    main()
