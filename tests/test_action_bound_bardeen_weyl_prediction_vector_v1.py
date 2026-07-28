import math
from dataclasses import replace

import pytest
import sympy as sp

from dfm_mkc_solver import action_bound_bardeen_weyl_prediction_vector_v1 as p


def _state(**changes):
    values = dict(
        wave_number=2.0, scale_factor=1.5, conformal_hubble=0.7,
        gravitational_constant=1.0 / (8.0 * math.pi),
        delta_rho_total=0.4, momentum_source=0.2,
        baryon_velocity_divergence=0.3, source_distance=10.0,
        lens_distance=4.0, transverse_wave_number=1.5,
    )
    values.update(changes)
    return p.PredictionState(**values)


def test_exact_order_binding_operators_and_numeric_substitution():
    vector = p.action_bound_prediction_vector(_state())
    assert vector.prediction_names == (
        "Psi_B", "Phi_B", "W_plus", "eta_slip", "Sigma_Weyl",
        "S_ISW", "A_pec", "theta_b_prime", "K_kappa",
        "K_kappa_over_A_pec",
    )
    assert len(vector.components) == len(vector.numeric_vector) == 10
    assert vector.action_binding_established
    assert all(x.exact_binding_established for x in vector.components)
    assert all(all(r == 0 for r in x.provenance_residuals)
               for x in vector.components)
    psi, phi, weyl, slip, response, isw, force, theta_prime, kappa, joint = (
        vector.numeric_vector
    )
    assert phi == pytest.approx(psi)
    assert weyl == pytest.approx(phi + psi)
    assert slip == pytest.approx(1)
    assert response == pytest.approx(
        -8 * math.pi * _state().gravitational_constant
        * _state().scale_factor**2 / _state().wave_number**2
    )
    assert force == pytest.approx(_state().wave_number**2 * psi)
    assert theta_prime == pytest.approx(
        -_state().conformal_hubble * _state().baryon_velocity_divergence
        + force
    )
    assert theta_prime != _state().baryon_velocity_divergence
    assert joint == pytest.approx(kappa / force)
    assert isw == pytest.approx(vector.numeric_vector[5])
    assert p.PREDICTIONS_DERIVED == 10
    assert p.TEN_ACTION_BOUND_PREDICTIONS_DERIVED
    assert p.MEASURABLE_PREDICTION_VECTOR_COMPUTED


def test_p8_and_p10_are_independent_dynamics_outputs():
    vector = p.action_bound_prediction_vector()
    theta_b = next(s for s in vector.symbolic_vector[7].free_symbols
                   if str(s) == "theta_b")
    assert sp.cancel(vector.symbolic_vector[7] - theta_b) != 0
    assert theta_b not in vector.symbolic_vector[9].free_symbols
    assert vector.symbolic_vector[9].has(
        next(s for s in vector.symbolic_vector[9].free_symbols if str(s) == "k_perp")
    )
    assert vector.symbolic_vector[9].args[0] == vector.symbolic_vector[8]
    assert vector.symbolic_vector[9].args[1].base == vector.symbolic_vector[6]
    assert "A_pec != 0" in vector.components[9].domain_assumptions
    assert "fixed pressureless Schutz-Sorkin" in " ".join(
        vector.components[9].action_provenance
    )
    with pytest.raises(ValueError, match="lens_distance"):
        _state(lens_distance=10)


def test_production_bardeen_lapse_sign_perturbation_breaks_binding(monkeypatch):
    original = p.bridge.bardeen_weyl_definitions

    def changed(**kwargs):
        result = original(**kwargs)
        return replace(result, bardeen_lapse_potential=-result.bardeen_lapse_potential)

    monkeypatch.setattr(p.bridge, "bardeen_weyl_definitions", changed)
    vector = p.action_bound_prediction_vector()
    assert not vector.action_binding_established
    assert not all(c.exact_binding_established for c in vector.components[:6])


def test_production_metric_momentum_coefficient_perturbation_breaks_binding(monkeypatch):
    original = p.bridge.symbolic_metric_constraint_elimination

    def changed(**kwargs):
        result = original(**kwargs)
        solution = dict(result.solution)
        solution["P"] = 2 * solution["P"]
        solution["Phi_prime"] = 2 * solution["P"] - kwargs["conformal_hubble"] * solution["Psi"]
        return replace(result, solution=solution)

    monkeypatch.setattr(p.bridge, "symbolic_metric_constraint_elimination", changed)
    vector = p.action_bound_prediction_vector()
    assert not vector.action_binding_established
    assert not all(c.exact_binding_established for c in vector.components[:6])


def test_production_baryon_euler_coefficient_perturbation_breaks_p7_p8_p10(monkeypatch):
    original = p.visible.pressureless_baryon_euler_equation

    def changed(**kwargs):
        result = original(**kwargs)
        return replace(
            result,
            gravitational_force=2 * result.gravitational_force,
            velocity_divergence_prime=(
                result.velocity_divergence_prime + result.gravitational_force
            ),
            force_coefficient_residual=sp.Integer(1),
            fourier_sign_and_normalization_proved=False,
        )

    monkeypatch.setattr(p.visible, "pressureless_baryon_euler_equation", changed)
    vector = p.action_bound_prediction_vector()
    assert not vector.components[6].exact_binding_established
    assert not vector.components[7].exact_binding_established
    assert not vector.components[9].exact_binding_established


def test_production_lensing_coefficient_perturbation_breaks_p9_p10(monkeypatch):
    original = p.bridge.thin_plane_convergence_integrand
    monkeypatch.setattr(
        p.bridge, "thin_plane_convergence_integrand",
        lambda **kwargs: 2 * original(**kwargs),
    )
    vector = p.action_bound_prediction_vector()
    assert not vector.components[8].exact_binding_established
    assert not vector.components[9].exact_binding_established


def test_exactness_cannot_be_created_by_names_or_provenance(monkeypatch):
    original = p.bridge.fixed_action_source_domain_binding_certificate

    def changed():
        return replace(original(), action_binding_established=False)

    monkeypatch.setattr(
        p.bridge, "fixed_action_source_domain_binding_certificate", changed
    )
    vector = p.action_bound_prediction_vector()
    cosmetically_exact = tuple(
        replace(c, name="exact", action_provenance=("exact",))
        for c in vector.components
    )
    assert not vector.action_binding_established
    assert not any(c.exact_binding_established for c in cosmetically_exact)
