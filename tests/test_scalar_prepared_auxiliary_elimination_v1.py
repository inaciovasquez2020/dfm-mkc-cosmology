from types import MappingProxyType

import pytest
import sympy as sp

from dfm_mkc_solver import (
    scalar_prepared_auxiliary_elimination_v1 as auxiliary,
)


EXPECTED = {
    "h_chart_embedding",
    "second_order_block_symmetry",
    "auxiliary_block_symmetry",
    "kinetic_rank_one_decomposition",
    "auxiliary_rank_one_decomposition",
    "mixed_rank_one_decomposition",
    "auxiliary_determinant_lemma",
    "auxiliary_inverse_reconstruction",
    "effective_kinetic_schur_identity",
    "effective_kinetic_determinant_lemma",
}

SOLUTION_EXPECTED = {
    "auxiliary_gradient_affine_reconstruction",
    "auxiliary_inverse_source_application",
    "auxiliary_solution_reconstruction",
}


def test_exact_ten_residual_certificate():
    residuals = (
        auxiliary.exact_scalar_prepared_auxiliary_elimination_certificate()
    )
    assert set(residuals) == EXPECTED
    assert all(value == 0 for value in residuals.values())


def test_exact_structured_solution_certificate():
    residuals = (
        auxiliary.exact_scalar_prepared_auxiliary_solution_certificate()
    )
    assert set(residuals) == SOLUTION_EXPECTED
    assert all(value == 0 for value in residuals.values())


def test_orders_and_structured_determinants():
    data = auxiliary.scalar_prepared_auxiliary_elimination_data()
    assert data["velocity_order"] == (
        "delta_phi_prime", "delta_theta_prime",
    )
    assert data["auxiliary_order"] == (
        "delta_J_b_L", "delta_J_r_L",
    )
    assert data["structured_effective_determinant"] == (
        data["det_D"] * (1 - data["gamma"] * data["t"])
    )
    assert data["det_A"] == data["det_F"] * data["delta_A"]
    factors = data["prepared_scalar_factors"]
    assert factors["one_minus_gamma_t"] == 1
    assert factors["det_K_effective"] == factors["det_D"]


def test_structured_auxiliary_solution():
    data = auxiliary.scalar_prepared_auxiliary_elimination_data()
    solution = auxiliary.scalar_prepared_auxiliary_solution()
    assert isinstance(solution, MappingProxyType)
    with pytest.raises(TypeError):
        solution["solution"] = sp.zeros(2, 1)
    assert solution["order"] == ("delta_J_b_L", "delta_J_r_L")
    assert data["auxiliary_configuration"].shape == (2, 1)
    assert data["auxiliary_source"].shape == (2, 1)
    assert data["structured_auxiliary_solution"].shape == (2, 1)
    assert data["structured_auxiliary_inverse"].shape == (2, 2)
    assert all(
        value == 0
        for value in data["auxiliary_gradient_reconstruction_residuals"]
    )
    assert all(
        value == 0
        for value in data["auxiliary_solution_reconstruction_residuals"]
    )
    assert data["structured_auxiliary_solution"] == (
        -data["structured_auxiliary_inverse"] * data["auxiliary_source"]
    )


def test_fraction_free_determinant_and_theorem():
    data = auxiliary.scalar_prepared_auxiliary_elimination_data()
    R = data["fraction_free_matrix"]
    assert data["fraction_free_determinant"] == (
        R[0, 0] * R[1, 1] - R[0, 1] * R[1, 0]
    )
    theorem = auxiliary.scalar_prepared_auxiliary_elimination_theorem()
    assert isinstance(theorem, MappingProxyType)
    assert theorem["auxiliary_determinant_nonzero"] is True
    assert theorem["effective_kinetic_nondegenerate"] is True
    assert theorem["structured_auxiliary_solution_available"] is True
    assert theorem["auxiliary_solution_source"] == (
        "exact action-derived auxiliary Euler rows"
    )
    assert theorem["auxiliary_solution_reconstruction_exact"] is True
    with pytest.raises(TypeError):
        theorem["structured_auxiliary_solution_available"] = False
    assert len(theorem["limitations"]) == 5


def test_prepared_factors_are_scalar_and_unresolved_is_exact():
    data = auxiliary.scalar_prepared_auxiliary_elimination_data()
    factors = data["prepared_scalar_factors"]
    assert isinstance(factors, MappingProxyType)
    assert set(factors) == {
        "det_D", "det_F", "delta_A", "t", "s", "gamma",
        "one_minus_gamma_t", "det_A", "det_K_effective",
    }
    assert all(isinstance(value, sp.Expr) for value in factors.values())
    assert factors["one_minus_gamma_t"] == 1
    assert factors["det_K_effective"] == factors["det_D"]
    assert not data["unresolved_factors"]
