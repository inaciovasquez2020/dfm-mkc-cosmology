"""Regression for the physical H0-normalized DFM wavenumber map."""

from __future__ import annotations

import math

import pytest

from dfm_mkc_solver.dfm_cdm_wavenumber_unit_map_v1 import (
    build_dfm_cdm_wavenumber_unit_map,
)


def test_planck_h0_wavenumber_round_trips() -> None:
    mapping = build_dfm_cdm_wavenumber_unit_map(H0_km_s_Mpc=67.4)

    assert math.isclose(mapping.h, 0.674, rel_tol=0.0, abs_tol=1.0e-15)
    assert math.isclose(
        mapping.hubble_length_Mpc,
        4447.959317507418,
        rel_tol=1.0e-15,
        abs_tol=0.0,
    )

    for physical_k in (0.0, 1.0e-4, 0.01, 0.0674, 0.2):
        code_k = mapping.wavenumber_code_from_Mpc_inverse(physical_k)
        recovered = mapping.wavenumber_Mpc_inverse_from_code(code_k)
        assert math.isclose(
            recovered,
            physical_k,
            rel_tol=1.0e-15,
            abs_tol=1.0e-18,
        )

    for physical_k_h in (0.0, 1.0e-4, 0.01, 0.1, 0.2):
        code_k = mapping.wavenumber_code_from_h_Mpc_inverse(physical_k_h)
        recovered = mapping.wavenumber_h_Mpc_inverse_from_code(code_k)
        assert math.isclose(
            recovered,
            physical_k_h,
            rel_tol=1.0e-15,
            abs_tol=1.0e-18,
        )


def test_sigma8_radius_has_exact_h0_normalized_reduction() -> None:
    mapping = build_dfm_cdm_wavenumber_unit_map(H0_km_s_Mpc=67.4)

    assert math.isclose(
        mapping.r8_Mpc,
        8.0 / 0.674,
        rel_tol=1.0e-15,
        abs_tol=0.0,
    )
    assert math.isclose(
        mapping.r8_code,
        800.0 / mapping.speed_of_light_km_s,
        rel_tol=1.0e-15,
        abs_tol=0.0,
    )

    code_k = mapping.wavenumber_code_from_h_Mpc_inverse(0.1)
    assert math.isclose(
        code_k,
        0.1 * mapping.speed_of_light_km_s / 100.0,
        rel_tol=1.0e-15,
        abs_tol=0.0,
    )
    assert math.isclose(
        code_k * mapping.r8_code,
        0.8,
        rel_tol=1.0e-15,
        abs_tol=1.0e-15,
    )


def test_existing_regression_mode_is_not_a_sigma8_scale_proxy() -> None:
    mapping = build_dfm_cdm_wavenumber_unit_map(H0_km_s_Mpc=67.4)

    regression_k_code = 0.005
    regression_k_h_Mpc = (
        mapping.wavenumber_h_Mpc_inverse_from_code(regression_k_code)
    )

    assert math.isclose(
        regression_k_h_Mpc,
        1.6678204759907602e-6,
        rel_tol=1.0e-15,
        abs_tol=0.0,
    )
    assert regression_k_h_Mpc < 1.0e-4


def test_invalid_inputs_fail_closed() -> None:
    with pytest.raises(ValueError):
        build_dfm_cdm_wavenumber_unit_map(H0_km_s_Mpc=0.0)

    mapping = build_dfm_cdm_wavenumber_unit_map(H0_km_s_Mpc=67.4)
    with pytest.raises(ValueError):
        mapping.wavenumber_code_from_Mpc_inverse(-1.0)
    with pytest.raises(ValueError):
        mapping.length_code_from_Mpc(0.0)
