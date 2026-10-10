#!/usr/bin/env python3
"""Lapse-retaining FLRW background audit for the completed generalized-Proca L4 model.

Uses A_mu=(B(t),0,0,0), where B is the covariant component A_0, and
ds^2=-N(t)^2 dt^2+a(t)^2 d\vec{x}^2. The script checks the curvature and
D invariants, removes the a-double-dot term by a boundary integration, derives
the N,a,phi,B Euler-Lagrange equations, and verifies the temporal-vector
equation. It does not establish an on-shell perturbative degree-of-freedom
count or stability.
"""
from __future__ import annotations

import sympy as sp


def main() -> None:
    t = sp.symbols("t", real=True)
    N, a, phi, B = (sp.Function(name)(t) for name in ("N", "a", "phi", "B"))
    xi, xs, alpha, mA2, bet, m2, lam, L0, M2 = sp.symbols(
        "xi xs alpha mA2 bet m2 lam L0 M2"
    )

    F = M2 - xs * phi**2
    Q = mA2 + bet * phi**2
    V = L0 + m2 * phi**2 / 2 + lam * phi**4 / 4
    adot, addot, Ndot = sp.diff(a, t), sp.diff(a, t, 2), sp.diff(N, t)
    Bdot, phidot = sp.diff(B, t), sp.diff(phi, t)

    R = 6 / N**2 * (addot / a + adot**2 / a**2 - adot * Ndot / (a * N))
    D = (
        6 * B * adot / (a * N**4) * (Bdot - B * Ndot / N)
        + 6 * B**2 * adot**2 / (a**2 * N**4)
    )
    L = sp.expand(
        N * a**3
        * (
            (F / 2 - xi * B**2 / (4 * N**2)) * R
            - xi * D / 2
            + alpha * phidot**2 / (2 * N**2)
            - V
            + Q * B**2 / (2 * N**2)
        )
    )

    # Replace C*a'' by -Cdot*a' modulo the total derivative d(C*a')/dt.
    coefficient_addot = sp.diff(L, addot)
    L_first = sp.expand(
        L
        - sp.diff(coefficient_addot * adot, t)
        + sp.diff(coefficient_addot, t) * adot
    )
    if any(len(d.variables) >= 2 for d in L_first.atoms(sp.Derivative)):
        raise AssertionError("Boundary-reduced Lagrangian still has higher derivatives")

    fields = (N, a, phi, B)
    equations = {
        field: sp.factor(
            sp.diff(L_first, field)
            - sp.diff(sp.diff(L_first, sp.diff(field, t)), t)
        )
        for field in fields
    }

    # Exact check: the A_0 equation is algebraic in B and contains no B-dot.
    expected_B_equation = (
        a * B / N**3
        * (N**2 * a**2 * Q + 3 * xi * (a * addot - adot**2))
    )
    if sp.simplify(equations[B] - expected_B_equation) != 0:
        raise AssertionError("Temporal-vector background equation mismatch")
    if Bdot in equations[B].atoms(sp.Derivative):
        raise AssertionError("Temporal-vector equation unexpectedly contains B-dot")

    # The lapse equation must be derived before imposing N=1.
    if sp.simplify(equations[N]) == 0:
        raise AssertionError("Lapse constraint unexpectedly vanishes")

    print("LAPSE_DEPENDENT_FLRW_ACTION := BUILT")
    print("BOUNDARY_REDUCTION_TO_FIRST_DERIVATIVES := PASS")
    print("EULER_LAGRANGE_EQUATIONS := DERIVED (N, a, phi, B)")
    print("LAPSE_CONSTRAINT := DERIVED_BEFORE_SETTING_N_TO_1")
    print("TEMPORAL_VECTOR_EQUATION := PASS")
    print("E_B := a*B/N^3 * (N^2*a^2*Q + 3*xi*(a*a_ddot - a_dot^2))")
    print("B_DYNAMICAL_ORDER := ALGEBRAIC_BACKGROUND_EQUATION")
    print("BOUNDARY := NO_ON_SHELL_PERTURBATION_RANK_OR_STABILITY_CLAIM")


if __name__ == "__main__":
    main()
