import importlib.util
import math
import sys
from pathlib import Path

import pytest
import sympy as sp


CODE = Path(
    "src/dfm_mkc_solver/metric_constraint_elimination_v1.py"
)

spec = importlib.util.spec_from_file_location(
    "metric_constraint_elimination_v1",
    CODE,
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_exact_symbolic_production_representation_solves_constraints():
    k2, a, H, G, rho, momentum, sigma = sp.symbols(
        "k2 a H G rho momentum sigma", nonzero=True
    )
    representation = module.symbolic_metric_constraint_elimination(
        wave_number_squared=k2,
        scale_factor=a,
        conformal_hubble=H,
        gravitational_constant=G,
        delta_rho_total=rho,
        momentum_source=momentum,
        enthalpy_sigma_total=sigma,
    )
    solution_vector = sp.Matrix((
        representation.solution["Phi"],
        representation.solution["Psi"],
        representation.solution["P"],
    ))

    assert (
        representation.constraint_matrix * solution_vector
        + representation.source_vector
    ).applyfunc(sp.cancel) == sp.zeros(3, 1)
    assert sp.cancel(
        representation.solution["Phi_prime"]
        + H * representation.solution["Psi"]
        - representation.solution["P"]
    ) == 0


def test_scalar_metric_constraints_are_eliminated_exactly():
    certificate = (
        module.eliminate_newtonian_metric_constraints(
            wave_number=2.0,
            scale_factor=1.5,
            conformal_hubble=0.7,
            gravitational_constant=1.0 / (8.0 * math.pi),
            delta_rho_total=0.4,
            momentum_source=0.2,
            enthalpy_sigma_total=0.1,
        )
    )

    assert certificate.momentum_combination == pytest.approx(
        0.05625,
        abs=1.0e-14,
    )
    assert certificate.phi == pytest.approx(
        -0.14203125,
        abs=1.0e-14,
    )
    assert certificate.psi == pytest.approx(
        -0.22640625,
        abs=1.0e-14,
    )
    assert certificate.phi_prime == pytest.approx(
        0.214734375,
        abs=1.0e-14,
    )

    assert abs(certificate.poisson_residual) < 1.0e-14
    assert abs(certificate.momentum_residual) < 1.0e-14
    assert abs(certificate.anisotropy_residual) < 1.0e-14

    assert certificate.source_level_constraints_eliminated is True
    assert certificate.constrained_quadratic_action_derived is False
    assert certificate.perturbation_system_closed is False


def test_zero_fourier_mode_is_rejected():
    with pytest.raises(
        ValueError,
        match="wave_number must be nonzero",
    ):
        module.eliminate_newtonian_metric_constraints(
            wave_number=0.0,
            scale_factor=1.0,
            conformal_hubble=1.0,
            gravitational_constant=1.0,
            delta_rho_total=0.0,
            momentum_source=0.0,
            enthalpy_sigma_total=0.0,
        )
