import importlib.util
import sys
from pathlib import Path

import pytest


CODE = Path(
    "src/dfm_mkc_solver/"
    "dark_sector_amplitude_perturbation_v1.py"
)

spec = importlib.util.spec_from_file_location(
    "dark_sector_amplitude_perturbation_v1",
    CODE,
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_amplitude_equation_is_solved_with_zero_residual():
    certificate = module.dark_sector_amplitude_perturbation(
        scale_factor=2.0,
        conformal_hubble=0.5,
        wave_number=3.0,
        phi_background=4.0,
        phi_prime_background=1.2,
        theta_prime_background=0.7,
        delta_phi=0.1,
        delta_phi_prime=0.2,
        delta_theta_prime=0.3,
        psi_metric=0.05,
        psi_metric_prime=0.02,
        phi_metric_prime=0.04,
        alpha=2.0,
        beta=3.0,
        m_phi_squared=5.0,
        lambda_phi=7.0,
    )

    assert certificate.potential_slope == pytest.approx(468.0)
    assert certificate.potential_curvature == pytest.approx(341.0)

    assert certificate.metric_derivative_combination == pytest.approx(
        0.14
    )
    assert certificate.phase_coupling_bracket == pytest.approx(
        1.533
    )
    assert certificate.effective_frequency_squared == pytest.approx(
        1372.265
    )
    assert certificate.delta_phi_double_prime == pytest.approx(
        -322.2325
    )

    assert abs(certificate.amplitude_equation_residual) < 1.0e-12

    assert (
        certificate.action_consistent_amplitude_equation_supplied
        is True
    )
    assert certificate.metric_derivatives_solved is False
    assert certificate.complete_perturbation_system_closed is False


def test_invalid_amplitude_parameters_are_rejected():
    with pytest.raises(
        ValueError,
        match="scale_factor must be positive",
    ):
        module.dark_sector_amplitude_perturbation(
            scale_factor=0.0,
            conformal_hubble=0.0,
            wave_number=1.0,
            phi_background=1.0,
            phi_prime_background=0.0,
            theta_prime_background=0.0,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta_prime=0.0,
            psi_metric=0.0,
            psi_metric_prime=0.0,
            phi_metric_prime=0.0,
            alpha=1.0,
            beta=1.0,
            m_phi_squared=0.0,
            lambda_phi=0.0,
        )

    with pytest.raises(
        ValueError,
        match="alpha must be positive",
    ):
        module.dark_sector_amplitude_perturbation(
            scale_factor=1.0,
            conformal_hubble=0.0,
            wave_number=1.0,
            phi_background=1.0,
            phi_prime_background=0.0,
            theta_prime_background=0.0,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta_prime=0.0,
            psi_metric=0.0,
            psi_metric_prime=0.0,
            phi_metric_prime=0.0,
            alpha=0.0,
            beta=1.0,
            m_phi_squared=0.0,
            lambda_phi=0.0,
        )
