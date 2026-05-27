"""DFM-MKC production solver code surface v1.

This module supplies callable, importable, schema-checked entrypoints for the
DFM-MKC numerical prediction-vector pipeline. The physical numerical
integration is intentionally execution-gated and is not performed by this
surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


STATUS = "PRODUCTION_SOLVER_CODE_SURFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION"
OBJECT_ID = "DFM_MKC_PRODUCTION_SOLVER_CODE_V1"

REQUIRED_INPUT_BLOCKS = (
    "cosmological_parameters",
    "dfm_mkc_parameters",
    "grid_parameters",
    "solver_parameters",
    "reproducibility_parameters",
)

REQUIRED_OUTPUT_BLOCKS = (
    "background_outputs",
    "transfer_outputs",
    "observable_outputs",
    "diagnostic_outputs",
)

ENTRYPOINTS = (
    "dfm_mkc_solve_background",
    "dfm_mkc_solve_perturbations",
    "dfm_mkc_project_observables",
    "dfm_mkc_validate_solver_outputs",
    "dfm_mkc_run_prediction_vector",
)


@dataclass(frozen=True)
class SolverGateResult:
    object_id: str
    status: str
    numerical_integration_run: bool
    prediction_vector_computed: bool
    reason: str


def validate_solver_config(config: Mapping[str, Any]) -> bool:
    missing = [key for key in REQUIRED_INPUT_BLOCKS if key not in config]
    if missing:
        raise ValueError(f"missing required input blocks: {missing}")
    return True


def _blocked_result(reason: str) -> SolverGateResult:
    return SolverGateResult(
        object_id=OBJECT_ID,
        status=STATUS,
        numerical_integration_run=False,
        prediction_vector_computed=False,
        reason=reason,
    )


def dfm_mkc_solve_background(config: Mapping[str, Any]) -> SolverGateResult:
    validate_solver_config(config)
    return _blocked_result("background numerical integration is gated; no physical run is performed")


def dfm_mkc_solve_perturbations(background_artifact: Mapping[str, Any], config: Mapping[str, Any]) -> SolverGateResult:
    validate_solver_config(config)
    if not background_artifact:
        raise ValueError("background_artifact is required")
    return _blocked_result("perturbation numerical integration is gated; no physical run is performed")


def dfm_mkc_project_observables(transfer_artifact: Mapping[str, Any], config: Mapping[str, Any]) -> SolverGateResult:
    validate_solver_config(config)
    if not transfer_artifact:
        raise ValueError("transfer_artifact is required")
    return _blocked_result("observable projection is gated; no prediction vector is computed")


def dfm_mkc_validate_solver_outputs(output_artifact: Mapping[str, Any], tolerance_config: Mapping[str, Any]) -> bool:
    if not output_artifact:
        raise ValueError("output_artifact is required")
    if not tolerance_config:
        raise ValueError("tolerance_config is required")
    return True


def dfm_mkc_run_prediction_vector(config: Mapping[str, Any]) -> SolverGateResult:
    validate_solver_config(config)
    return _blocked_result("prediction-vector run is gated until a validated numerical implementation is supplied")
