from __future__ import annotations

import math
import statistics
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from dfm_mkc_solver.dark_sector_fourier_mode_integrator_v1 import (
    integrate_dark_sector_fourier_mode,
)


MASS_FREQUENCY = 1.0
AMPLITUDE = 1.0e-6
TIME_START = 0.0
TIME_END = 30.0
STEPS = 15_000


def _descending_zero_crossings(
    times: tuple[float, ...],
    states: tuple[tuple[float, float, float, float], ...],
) -> tuple[float, ...]:
    crossings: list[float] = []

    for index in range(len(states) - 1):
        left = states[index][0]
        right = states[index + 1][0]

        if left > 0.0 and right <= 0.0:
            denominator = left - right
            assert denominator > 0.0

            fraction = left / denominator
            crossing = (
                times[index]
                + fraction * (times[index + 1] - times[index])
            )
            crossings.append(crossing)

    return tuple(crossings)


def _extract_frequency(
    times: tuple[float, ...],
    states: tuple[tuple[float, float, float, float], ...],
) -> float:
    crossings = _descending_zero_crossings(times, states)

    assert len(crossings) >= 4

    periods = tuple(
        crossings[index + 1] - crossings[index]
        for index in range(len(crossings) - 1)
    )

    assert all(period > 0.0 for period in periods)

    return 2.0 * math.pi / statistics.fmean(periods)


def _exact_coefficient(wave_number: float) -> float:
    return 1.0 / (
        math.sqrt(MASS_FREQUENCY**2 + wave_number**2)
        + MASS_FREQUENCY
    ) ** 2


def _numerical_coefficient(wave_number: float) -> tuple[float, float]:
    certificate = integrate_dark_sector_fourier_mode(
        conformal_time_start=TIME_START,
        conformal_time_end=TIME_END,
        steps=STEPS,
        initial_state=(AMPLITUDE, 0.0, 0.0, 0.0),
        scale_factor=1.0,
        conformal_hubble=0.0,
        wave_number=wave_number,
        gravitational_constant=1.0e-16,
        phi_background=1.0,
        phi_prime_background=0.0,
        theta_prime_background=0.0,
        alpha=1.0,
        beta=1.0,
        rho_star=0.0,
        m_phi_squared=1.0,
        lambda_phi=0.0,
    )

    assert certificate.fixed_background_integration_completed is True
    assert certificate.all_instantaneous_rhs_certificates_closed is True
    assert certificate.cosmological_background_evolved is False
    assert certificate.visible_sector_evolved is False
    assert certificate.observable_computed is False
    assert certificate.max_component_residual < 1.0e-10

    omega_numerical = _extract_frequency(
        certificate.times,
        certificate.states,
    )
    slow_frequency = omega_numerical - MASS_FREQUENCY

    assert slow_frequency > 0.0

    coefficient = (
        slow_frequency**2
        / wave_number**4
    )

    return omega_numerical, coefficient


def test_three_mode_dispersion_converges_to_quarter_coefficient():
    wave_numbers = (1.0 / 4.0, 1.0 / 8.0, 1.0 / 16.0)

    numerical_coefficients: list[float] = []
    next_order_diagnostics: list[float] = []

    for wave_number in wave_numbers:
        omega_numerical, coefficient_numerical = (
            _numerical_coefficient(wave_number)
        )

        omega_exact = math.sqrt(
            MASS_FREQUENCY**2 + wave_number**2
        )
        coefficient_exact = _exact_coefficient(wave_number)

        assert math.isclose(
            omega_numerical,
            omega_exact,
            rel_tol=1.0e-5,
            abs_tol=1.0e-8,
        )
        assert math.isclose(
            coefficient_numerical,
            coefficient_exact,
            rel_tol=1.0e-3,
            abs_tol=1.0e-7,
        )

        numerical_coefficients.append(coefficient_numerical)
        next_order_diagnostics.append(
            (
                coefficient_numerical
                - 1.0 / (4.0 * MASS_FREQUENCY**2)
            )
            / wave_number**2
        )

    assert (
        numerical_coefficients[0]
        < numerical_coefficients[1]
        < numerical_coefficients[2]
        < 1.0 / 4.0
    )

    quarter_errors = tuple(
        abs(coefficient - 1.0 / 4.0)
        for coefficient in numerical_coefficients
    )

    assert quarter_errors[2] < quarter_errors[1] < quarter_errors[0]

    assert (
        next_order_diagnostics[0]
        > next_order_diagnostics[1]
        > next_order_diagnostics[2]
        > -1.0 / 8.0
    )

    assert math.isclose(
        next_order_diagnostics[-1],
        -1.0 / 8.0,
        rel_tol=1.0e-2,
        abs_tol=1.0e-3,
    )
