"""DFM-MKC external solver validation-run gate surface v1.

This module supplies callable validation-run gates for a future hash-locked
external solver execution. It does not execute an external solver, compute a
prediction vector, or promote empirical status.
"""

from __future__ import annotations

from typing import Any, Mapping


OBJECT_ID = "DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1"
STATUS = "EXTERNAL_SOLVER_VALIDATION_RUN_GATE_SUPPLIED_NO_EXTERNAL_EXECUTION"

REQUIRED_BINDING_FIELDS = (
    "external_target",
    "source_code_commit",
    "environment_lock",
    "input_schema",
    "output_schema",
    "unit_convention",
    "observable_ordering",
    "covariance_alignment",
    "reproducibility_hashes",
)

REQUIRED_RUN_FIELDS = (
    "input_hash",
    "output_hash",
    "diagnostic_hash",
    "finite_output_check",
    "constraint_residual_check",
    "convergence_summary",
    "reproducibility_summary",
)

ENTRYPOINTS = (
    "validate_external_solver_binding",
    "validate_external_solver_run_record",
    "run_external_solver_validation_gate",
)


def validate_external_solver_binding(binding: Mapping[str, Any]) -> bool:
    missing = [key for key in REQUIRED_BINDING_FIELDS if key not in binding]
    if missing:
        raise ValueError(f"missing required binding fields: {missing}")
    return True


def validate_external_solver_run_record(run_record: Mapping[str, Any]) -> bool:
    missing = [key for key in REQUIRED_RUN_FIELDS if key not in run_record]
    if missing:
        raise ValueError(f"missing required run-record fields: {missing}")
    return True


def run_external_solver_validation_gate(
    binding: Mapping[str, Any],
    run_record: Mapping[str, Any],
) -> dict[str, Any]:
    validate_external_solver_binding(binding)
    validate_external_solver_run_record(run_record)
    return {
        "object_id": OBJECT_ID,
        "status": STATUS,
        "binding_schema_valid": True,
        "run_record_schema_valid": True,
        "external_solver_executed": False,
        "numerical_prediction_vector_computed": False,
        "likelihood_run_supplied": False,
        "empirical_status_promoted": False,
        "reason": "external solver validation gate supplied; no external solver execution is performed",
    }
