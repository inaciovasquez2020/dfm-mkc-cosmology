import numpy as np
import pytest

from dfm_mkc_solver.scalar_constraint_variational_bridge_v1 import (
    ScalarConstraintBackground,
    ScalarConstraintMultipliers,
    ScalarConstraintSources,
    ScalarConstraintVariables,
    quadratic_constraint_lagrangian_density,
    scalar_constraint_matrix,
    scalar_constraint_residuals,
    scalar_constraint_variational_certificate,
    solve_constraints_and_bind_bardeen_weyl,
)


def _objects():
    background = ScalarConstraintBackground(
        wave_number=0.37,
        scale_factor=0.81,
        conformal_hubble=1.29,
        gravitational_constant=0.013,
    )
    sources = ScalarConstraintSources(
        delta_rho_total=0.024,
        momentum_source=-0.017,
        enthalpy_sigma_total=0.006,
    )
    variables = ScalarConstraintVariables(
        curvature_potential_phi=0.12,
        lapse_potential_psi=-0.08,
        momentum_combination=0.031,
    )
    multipliers = ScalarConstraintMultipliers(
        hamiltonian_multiplier=0.41,
        momentum_multiplier=-0.27,
        anisotropy_multiplier=0.19,
    )
    return background, sources, variables, multipliers


def test_constraint_matrix_has_exact_nonzero_k_determinant_and_rank():
    background, _, _, _ = _objects()
    matrix = scalar_constraint_matrix(background=background)

    assert matrix.shape == (3, 3)
    assert np.linalg.det(matrix) == pytest.approx(
        background.wave_number**6,
        rel=1.0e-12,
        abs=1.0e-15,
    )
    assert np.linalg.matrix_rank(matrix) == 3


def test_multiplier_variation_returns_constraint_residuals():
    background, sources, variables, multipliers = _objects()
    residuals = scalar_constraint_residuals(
        background=background,
        sources=sources,
        variables=variables,
    ).as_array()

    base = np.asarray(
        (
            multipliers.hamiltonian_multiplier,
            multipliers.momentum_multiplier,
            multipliers.anisotropy_multiplier,
        ),
        dtype=float,
    )
    finite_difference = np.empty(3, dtype=float)
    step = 1.0e-7

    for index in range(3):
        plus = base.copy()
        minus = base.copy()
        plus[index] += step
        minus[index] -= step

        plus_value = quadratic_constraint_lagrangian_density(
            background=background,
            sources=sources,
            variables=variables,
            multipliers=ScalarConstraintMultipliers(*plus),
        )
        minus_value = quadratic_constraint_lagrangian_density(
            background=background,
            sources=sources,
            variables=variables,
            multipliers=ScalarConstraintMultipliers(*minus),
        )
        finite_difference[index] = (
            plus_value - minus_value
        ) / (2.0 * step)

    assert finite_difference == pytest.approx(
        residuals,
        rel=1.0e-9,
        abs=1.0e-10,
    )


def test_mixed_hessian_is_symmetric_and_boundary_is_explicit():
    background, sources, variables, multipliers = _objects()
    certificate = scalar_constraint_variational_certificate(
        background=background,
        sources=sources,
        variables=variables,
        multipliers=multipliers,
    )

    assert certificate.exact_constraint_variational_carrier is True
    assert (
        certificate.unique_metric_constraint_solution_for_nonzero_k
        is True
    )
    assert certificate.constraint_matrix_rank == 3
    assert certificate.mixed_hessian_symmetry_residual == 0.0
    assert np.array_equal(
        certificate.mixed_hessian,
        certificate.mixed_hessian.T,
    )
    assert certificate.canonical_second_variation_identified is False
    assert certificate.action_binding_established is False


def test_existing_eliminator_binds_to_fixed_bardeen_weyl_sum():
    background, sources, _, _ = _objects()
    certificate = solve_constraints_and_bind_bardeen_weyl(
        background=background,
        sources=sources,
    )

    assert certificate.source_eliminator_reproduced is True
    assert certificate.newtonian_bardeen_binding_verified is True
    assert certificate.exact_constraint_variational_carrier is True
    assert certificate.weyl_potential_sum == pytest.approx(
        certificate.metric_curvature_potential_phi
        + certificate.metric_lapse_potential_psi
    )
    assert certificate.hamiltonian_residual == pytest.approx(
        0.0,
        abs=1.0e-12,
    )
    assert certificate.momentum_residual == pytest.approx(
        0.0,
        abs=1.0e-12,
    )
    assert certificate.anisotropy_residual == pytest.approx(
        0.0,
        abs=1.0e-12,
    )
    assert certificate.canonical_second_variation_identified is False
    assert certificate.action_binding_established is False
    assert (
        certificate.dfm_vs_lcdm_prediction_vector_computed
        is False
    )


def test_zero_wave_number_is_rejected():
    with pytest.raises(ValueError, match="wave_number must be nonzero"):
        ScalarConstraintBackground(
            wave_number=0.0,
            scale_factor=1.0,
            conformal_hubble=1.0,
            gravitational_constant=1.0,
        )
