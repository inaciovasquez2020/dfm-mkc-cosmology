"""DFM-MKC external solver adapter implementation surface v1.

This module supplies callable adapter gates for CLASS-compatible, CAMB-compatible,
or first-party DFM-MKC solver bindings. It does not select, execute, or validate
an external solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


STATUS = "EXTERNAL_SOLVER_ADAPTER_IMPLEMENTATION_SURFACE_SUPPLIED_NO_EXTERNAL_RUN"
OBJECT_ID = "DFM_MKC_EXTERNAL_SOLVER_ADAPTER_IMPLEMENTATION_V1"

ALLOWED_EXTERNAL_TARGETS = (
    "CLASS-compatible external binding",
    "CAMB-compatible external binding",
    "custom first-party DFM-MKC solver",
)

REQUIRED_BINDING_FIELDS = (
    "source_code_commit",
    "environment_lock",
    "input_schema",
    "output_schema",
    "unit_convention",
    "observable_ordering",
    "covariance_alignment",
    "reproducibility_hashes",
)

ADAPTER_ENTRYPOINTS = (
    "dfm_mkc_background_adapter",
    "dfm_mkc_perturbation_adapter",
    "dfm_mkc_observable_adapter",
    "dfm_mkc_diagnostic_adapter",
    "dfm_mkc_validate_external_binding",
)


@dataclass(frozen=True)
class AdapterGateResult:
    object_id: str
    status: str
    external_solver_executed: bool
    adapter_implemented: bool
    numerical_prediction_vector_computed: bool
    reason: str


def validate_external_binding_contract(binding: Mapping[str, Any]) -> bool:
    missing = [key for key in REQUIRED_BINDING_FIELDS if key not in binding]
    if missing:
        raise ValueError(f"missing required binding fields: {missing}")
    target = binding.get("external_target")
    if target is not None and target not in ALLOWED_EXTERNAL_TARGETS:
        raise ValueError(f"unsupported external target: {target}")
    return True


def _blocked_result(reason: str) -> AdapterGateResult:
    return AdapterGateResult(
        object_id=OBJECT_ID,
        status=STATUS,
        external_solver_executed=False,
        adapter_implemented=False,
        numerical_prediction_vector_computed=False,
        reason=reason,
    )


def dfm_mkc_background_adapter(binding: Mapping[str, Any]) -> AdapterGateResult:
    validate_external_binding_contract(binding)
    return _blocked_result("background adapter is declared but no external solver is executed")


def dfm_mkc_perturbation_adapter(binding: Mapping[str, Any]) -> AdapterGateResult:
    validate_external_binding_contract(binding)
    return _blocked_result("perturbation adapter is declared but no external solver is executed")


def dfm_mkc_observable_adapter(binding: Mapping[str, Any]) -> AdapterGateResult:
    validate_external_binding_contract(binding)
    return _blocked_result("observable adapter is declared but no prediction vector is computed")


def dfm_mkc_diagnostic_adapter(binding: Mapping[str, Any]) -> AdapterGateResult:
    validate_external_binding_contract(binding)
    return _blocked_result("diagnostic adapter is declared but no external validation run is performed")


def dfm_mkc_validate_external_binding(binding: Mapping[str, Any]) -> bool:
    return validate_external_binding_contract(binding)
