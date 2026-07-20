import importlib.util
import sys
from pathlib import Path

import pytest


CODE = Path(
    "src/dfm_mkc_solver/"
    "dark_sector_phase_perturbation_v1.py"
)

spec = importlib.util.spec_from_file_location(
    "dark_sector_phase_perturbation_v1",
    CODE,
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_action_derived_phase_sources_close_the_phase_equation():
    certificate = module.dark_sector_phase_perturbation(
        scale_factor=2.0,
        conformal_hubble=0.5,
        wave_number=2.0,
        phi_background=4.0,
        phi_prime_background=1.0,
        theta_prime_background=3.0,
        delta_phi=0.2,
        delta_phi_prime=0.1,
        delta_theta=0.4,
        delta_theta_prime=0.3,
        psi_metric=0.05,
        psi_metric_prime=0.02,
        phi_metric=0.07,
        phi_metric_prime=0.01,
        beta=5.0,
    )

    assert certificate.theta_background_double_prime == pytest.approx(
        -4.5
    )
    assert certificate.metric_combination == pytest.approx(0.26)
    assert certificate.metric_combination_prime == pytest.approx(
        0.05
    )
    assert certificate.normalized_current_perturbation == pytest.approx(
        -0.18
    )
    assert certificate.current_perturbation == pytest.approx(
        -57.6
    )
    assert certificate.delta_theta_double_prime == pytest.approx(
        -1.975
    )

    assert abs(certificate.normalized_equation_residual) < 1.0e-13
    assert abs(certificate.full_equation_residual) < 1.0e-12

    assert certificate.action_derived_phase_sources_supplied is True
    assert certificate.metric_sources_solved is False
    assert certificate.complete_perturbation_system_closed is False


def test_phase_degeneracy_surface_is_rejected():
    with pytest.raises(
        ValueError,
        match="phi_background must be nonzero",
    ):
        module.dark_sector_phase_perturbation(
            scale_factor=1.0,
            conformal_hubble=0.0,
            wave_number=1.0,
            phi_background=0.0,
            phi_prime_background=0.0,
            theta_prime_background=0.0,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta=0.0,
            delta_theta_prime=0.0,
            psi_metric=0.0,
            psi_metric_prime=0.0,
            phi_metric=0.0,
            phi_metric_prime=0.0,
            beta=1.0,
        )
