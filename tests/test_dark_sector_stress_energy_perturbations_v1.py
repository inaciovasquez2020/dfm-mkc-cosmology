import importlib.util
import sys
from pathlib import Path

import pytest


CODE = Path(
    "src/dfm_mkc_solver/"
    "dark_sector_stress_energy_perturbations_v1.py"
)

spec = importlib.util.spec_from_file_location(
    "dark_sector_stress_energy_perturbations_v1",
    CODE,
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_action_derived_stress_energy_sources():
    certificate = (
        module.dark_sector_stress_energy_perturbations(
            scale_factor=2.0,
            wave_number=6.0,
            phi_background=3.0,
            phi_prime_background=4.0,
            theta_prime_background=5.0,
            delta_phi=0.1,
            delta_phi_prime=0.2,
            delta_theta=0.3,
            delta_theta_prime=0.4,
            psi_metric=0.05,
            alpha=2.0,
            beta=3.0,
            rho_star=13.0,
            m_phi_squared=7.0,
            lambda_phi=11.0,
        )
    )

    assert certificate.potential == pytest.approx(267.25)
    assert certificate.potential_slope == pytest.approx(318.0)

    assert certificate.background_energy_density == pytest.approx(
        355.625
    )
    assert certificate.background_pressure == pytest.approx(
        -178.875
    )
    assert certificate.background_enthalpy == pytest.approx(
        176.75
    )

    assert certificate.kinetic_source_perturbation == pytest.approx(
        10.6875
    )
    assert certificate.potential_source_perturbation == pytest.approx(
        31.8
    )
    assert certificate.delta_energy_density == pytest.approx(
        42.4875
    )
    assert certificate.delta_pressure == pytest.approx(
        -21.1125
    )

    assert certificate.momentum_potential == pytest.approx(
        10.325
    )
    assert certificate.momentum_divergence_source == pytest.approx(
        371.7
    )
    assert certificate.scalar_anisotropic_stress == 0.0

    assert abs(
        certificate.energy_pressure_difference_residual
    ) < 1.0e-13
    assert abs(
        certificate.enthalpy_identity_residual
    ) < 1.0e-13

    assert certificate.action_derived_sources_supplied is True
    assert certificate.perturbation_evolution_solved is False
    assert certificate.observational_prediction_computed is False


def test_invalid_source_parameters_are_rejected():
    with pytest.raises(
        ValueError,
        match="scale_factor must be positive",
    ):
        module.dark_sector_stress_energy_perturbations(
            scale_factor=0.0,
            wave_number=1.0,
            phi_background=1.0,
            phi_prime_background=0.0,
            theta_prime_background=0.0,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta=0.0,
            delta_theta_prime=0.0,
            psi_metric=0.0,
            alpha=1.0,
            beta=1.0,
            rho_star=0.0,
            m_phi_squared=0.0,
            lambda_phi=0.0,
        )

    with pytest.raises(
        ValueError,
        match="wave_number must be nonnegative",
    ):
        module.dark_sector_stress_energy_perturbations(
            scale_factor=1.0,
            wave_number=-1.0,
            phi_background=1.0,
            phi_prime_background=0.0,
            theta_prime_background=0.0,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta=0.0,
            delta_theta_prime=0.0,
            psi_metric=0.0,
            alpha=1.0,
            beta=1.0,
            rho_star=0.0,
            m_phi_squared=0.0,
            lambda_phi=0.0,
        )
