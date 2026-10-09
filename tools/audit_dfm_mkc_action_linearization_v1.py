#!/usr/bin/env python3
"""Symbolic audit of the DFM-MKC first-order scalar perturbation record.

This is a bounded algebraic audit, not a complete tensor-perturbation engine.
It checks the first-order phase-current expansion from sqrt(-g) g^{mu nu},
and guards the two previously identified transcription defects in the stored
amplitude/phase equations. Requires SymPy (already a project dependency).
"""
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/repo_intake/dfm_mkc_linear_perturbation_system_v1_2026_05_27.json"


def main() -> None:
    eta, eps = sp.symbols("eta eps")
    beta, k = sp.symbols("beta k", nonzero=True)
    a = sp.Function("a")(eta)
    phi = sp.Function("phi_bar")(eta)
    dphi = sp.Function("delta_phi")(eta)
    theta = sp.Function("theta_bar")(eta)
    dtheta = sp.Function("delta_theta")(eta)
    psi = sp.Function("Psi")(eta)
    Phi = sp.Function("Phi")(eta)

    # sqrt(-g) g^{00} = -a^2 [1 - eps(Psi + 3 Phi)] + O(eps^2)
    # sqrt(-g) g^{ij} =  a^2 [1 + eps(Psi - Phi)] delta^{ij} + O(eps^2)
    sqrtg_g00 = -a**2 * (1 - eps * (psi + 3 * Phi))
    phi_full = phi + eps * dphi
    theta_dot_full = sp.diff(theta, eta) + eps * sp.diff(dtheta, eta)
    current_time = beta * phi_full**2 * theta_dot_full * sqrtg_g00
    derived_time_coefficient = sp.expand(current_time).coeff(eps, 1)

    expected_time_coefficient = -a**2 * beta * (
        phi**2 * sp.diff(dtheta, eta)
        + 2 * phi * sp.diff(theta, eta) * dphi
        - phi**2 * sp.diff(theta, eta) * (psi + 3 * Phi)
    )
    assert sp.simplify(derived_time_coefficient - expected_time_coefficient) == 0

    # At first order, the spatial current coefficient multiplies only the
    # first-order spatial gradient of delta_theta; perturbations of the
    # coefficient times that gradient are second order.
    sqrtg_gij_background = a**2
    phi_squared_background = phi**2
    spatial_current_divergence = (
        -beta * sqrtg_gij_background * phi_squared_background * k**2 * dtheta
    )
    spatial_divergence_after_sign = -spatial_current_divergence
    expected_spatial_divergence = a**2 * beta * phi**2 * k**2 * dtheta
    assert sp.simplify(spatial_divergence_after_sign - expected_spatial_divergence) == 0
    assert sp.simplify(spatial_current_divergence + expected_spatial_divergence) == 0

    data = json.loads(ART.read_text())
    equations = data["linearized_equations"]
    amplitude = equations["dfm_delta_phi_equation"]
    phase = equations["dfm_delta_theta_equation"]

    # Potential derivatives are outside alpha's wave-operator bracket.
    assert "alpha[delta_phi_double_prime" in amplitude
    assert "] + a^2 U_double_prime(phi_bar)delta_phi + 2 a^2 Psi U_prime(phi_bar)" in amplitude
    assert "(k^2 + a^2 U_double_prime(phi_bar))" not in amplitude

    # The full phase current is differentiated once; no duplicate product-rule term.
    assert "(a^2 beta[phi_bar^2 delta_theta_prime" in phase
    assert "theta_bar_prime delta_phi" in phase
    assert "Psi + 3 Phi" in phase
    assert "metric_source_theta" not in phase
    assert "amplitude_source_theta" not in phase
    assert " + 2 beta phi_bar phi_bar_prime delta_theta_prime" not in phase

    print("DFM_MKC_ACTION_LINEARIZATION_AUDIT_OK")
    print("phase_current_first_order_residual = 0")
    print("amplitude_potential_normalization = corrected")
    print("phase_product_rule_and_sources = corrected")
    print("scope = scalar-current expansion plus transcription guards; Einstein constraints and stress-energy perturbations remain unaudited")


if __name__ == "__main__":
    main()
