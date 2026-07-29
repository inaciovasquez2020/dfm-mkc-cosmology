import math
from types import MappingProxyType

import pytest

from dfm_mkc_solver.charge_reduced_background_v1 import (
    ChargeReducedInitialData,
    ChargeReducedParameters,
    friedmann_hubble,
    validate_parameters,
    validate_state,
)
from dfm_mkc_solver.prepared_alpha_family_existence_v1 import (
    build_prepared_alpha_family_member,
    exact_prepared_alpha_family_existence_certificate,
    prepared_alpha_family_existence_theorem,
    prepared_alpha_thresholds,
)


PACKET = {
    "G_N": 1.0 / (8.0 * math.pi),
    "beta": 1.4,
    "mu": 0.8,
    "q": 0.35,
    "rho_b0": 0.12,
    "rho_r0": 8.0e-5,
    "rho_lambda": 0.7,
}


def test_exact_residuals_have_required_key_set_and_vanish():
    residuals = exact_prepared_alpha_family_existence_certificate()
    assert set(residuals) == {
        "circular_density_normalization",
        "prepared_initial_velocity",
        "prepared_initial_friedmann_identity",
        "initial_denominator_margin_identity",
        "initial_hubble_upper_identity",
        "forcing_upper_identity",
        "time_to_redshift_identity",
        "energy_threshold_identity",
        "strict_field_margin_identity",
        "field_lower_bound_identity",
        "canonical_lambda_density_mapping",
        "phase_derivative_majorant_identity",
    }
    assert all(residual == 0 for residual in residuals.values())


def test_theorem_mapping_is_immutable_and_complete():
    theorem = prepared_alpha_family_existence_theorem()
    assert isinstance(theorem, MappingProxyType)
    assert set(theorem) == {
        "branch",
        "exact_symbolic_identities",
        "nonnegative_decomposition_inequalities",
        "bootstrap_continuation",
        "conclusions",
        "limitations",
    }
    assert len(theorem["limitations"]) == 6
    with pytest.raises(TypeError):
        theorem["branch"] = "changed"


def test_dynamic_admissible_alpha_builds_exact_prepared_objects():
    thresholds = prepared_alpha_thresholds(**PACKET)
    alpha_valid = 0.5 * thresholds.alpha_max
    member = build_prepared_alpha_family_member(
        **PACKET,
        alpha=alpha_valid,
    )
    assert isinstance(member.parameters, ChargeReducedParameters)
    assert isinstance(member.initial_data, ChargeReducedInitialData)
    validate_parameters(member.parameters)
    state = (
        member.initial_data.phi,
        member.initial_data.v,
        member.initial_data.theta,
        member.initial_data.rho_m,
        member.initial_data.rho_r,
    )
    validate_state(state)
    H_constraint = friedmann_hubble(
        math.log(thresholds.a_i),
        state,
        member.parameters,
    )
    assert H_constraint == pytest.approx(member.H_i, rel=2.0e-15)
    assert member.v_i == pytest.approx(
        -1.5 * member.H_i * thresholds.phi_i,
        rel=0.0,
        abs=0.0,
    )
    assert math.isfinite(member.phase_upper)
    assert member.phase_upper > 0.0


def test_alpha_rejections_report_active_thresholds():
    thresholds = prepared_alpha_thresholds(**PACKET)
    with pytest.raises(ValueError, match="0 < alpha <= alpha_max"):
        build_prepared_alpha_family_member(**PACKET, alpha=0.0)
    with pytest.raises(ValueError, match="alpha_initial"):
        build_prepared_alpha_family_member(
            **PACKET,
            alpha=1.01 * thresholds.alpha_initial,
        )
    if thresholds.alpha_energy < thresholds.alpha_initial:
        with pytest.raises(ValueError, match="alpha_energy"):
            build_prepared_alpha_family_member(
                **PACKET,
                alpha=1.01 * thresholds.alpha_energy,
            )


def test_strengthened_energy_and_combined_thresholds():
    thresholds = prepared_alpha_thresholds(**PACKET)
    assert thresholds.alpha_energy == pytest.approx(
        PACKET["mu"] ** 2 / (16.0 * thresholds.C_B),
        rel=0.0,
        abs=0.0,
    )
    assert thresholds.alpha_max == min(
        thresholds.alpha_initial,
        thresholds.alpha_energy,
    )
