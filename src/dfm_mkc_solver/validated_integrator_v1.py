"""DFM-MKC validated numerical integrator gate surface v1.

This module supplies callable validation gates for a future numerical integrator.
It does not perform physical integration, does not compute a prediction vector,
and does not promote empirical status.
"""

from __future__ import annotations

from typing import Any, Mapping


OBJECT_ID = "DFM_MKC_VALIDATED_NUMERICAL_INTEGRATOR_V1"
STATUS = "VALIDATED_NUMERICAL_INTEGRATOR_GATE_SUPPLIED_NO_NUMERICAL_RUN"

REQUIRED_CONFIG_BLOCKS = (
    "cosmological_parameters",
    "dfm_mkc_parameters",
    "grid_parameters",
    "solver_parameters",
    "reproducibility_parameters",
)

REQUIRED_VALIDATION_BLOCKS = (
    "finite_output_check",
    "constraint_residual_check",
    "grid_convergence_check",
    "ell_max_convergence_check",
    "hash_reproducibility_check",
)

ENTRYPOINTS = (
    "validate_integrator_config",
    "validate_integrator_diagnostics",
    "run_validated_integrator_gate",
)


def validate_integrator_config(config: Mapping[str, Any]) -> bool:
    missing = [key for key in REQUIRED_CONFIG_BLOCKS if key not in config]
    if missing:
        raise ValueError(f"missing required config blocks: {missing}")
    return True


def validate_integrator_diagnostics(diagnostics: Mapping[str, Any]) -> bool:
    missing = [key for key in REQUIRED_VALIDATION_BLOCKS if key not in diagnostics]
    if missing:
        raise ValueError(f"missing required validation blocks: {missing}")
    return True


def run_validated_integrator_gate(
    config: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    validate_integrator_config(config)
    validate_integrator_diagnostics(diagnostics)
    return {
        "object_id": OBJECT_ID,
        "status": STATUS,
        "config_schema_valid": True,
        "diagnostic_schema_valid": True,
        "numerical_integration_run": False,
        "prediction_vector_computed": False,
        "likelihood_run_supplied": False,
        "empirical_status_promoted": False,
        "reason": "validated integrator gate supplied; physical numerical integration remains blocked",
    }
