#!/usr/bin/env python3
"""Symbolically verify the Ricci/divergence identity in a 4D test geometry.

Convention:
    R_mn = d_r Gamma^r_mn - d_n Gamma^r_mr
           + Gamma^r_rl Gamma^l_mn - Gamma^r_nl Gamma^l_mr

The test metric is diagonal, with arbitrary t,z dependence:
    ds^2 = -N(t,z)^2 dt^2 + a(t,z)^2 (dx^2 + dy^2) + C(t,z)^2 dz^2.
The vector has arbitrary covariant components A_0(t,z), A_3(t,z).

This is a bounded symbolic identity check. It does not verify the user's full
off-diagonal perturbed metric, the completed quadratic action, or physical
degree-of-freedom counting.
"""
from __future__ import annotations

import sympy as sp


def ricci_divergence_residual() -> sp.Expr:
    t, x, y, z = sp.symbols("t x y z")
    N = sp.Function("N")(t, z)
    a = sp.Function("a")(t, z)
    C = sp.Function("C")(t, z)
    A0 = sp.Function("A0")(t, z)
    A3 = sp.Function("A3")(t, z)
    coords = [t, x, y, z]
    n = 4

    metric = sp.diag(-N**2, a**2, a**2, C**2)
    inverse = sp.simplify(metric.inv())

    # gamma[r][m][v] = Gamma^r_{mv}
    gamma = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for m in range(n):
            for v in range(n):
                gamma[r][m][v] = sp.factor(
                    sum(
                        inverse[r, ell]
                        * (
                            sp.diff(metric[ell, v], coords[m])
                            + sp.diff(metric[ell, m], coords[v])
                            - sp.diff(metric[m, v], coords[ell])
                        )
                        for ell in range(n)
                    )
                    / 2
                )

    ricci = sp.MutableDenseMatrix.zeros(n, n)
    for m in range(n):
        for v in range(n):
            ricci[m, v] = sp.factor(
                sum(
                    sp.diff(gamma[r][m][v], coords[r])
                    - sp.diff(gamma[r][m][r], coords[v])
                    + sum(
                        gamma[r][r][ell] * gamma[ell][m][v]
                        - gamma[r][v][ell] * gamma[ell][m][r]
                        for ell in range(n)
                    )
                    for r in range(n)
                )
            )

    A_cov = [A0, sp.S.Zero, sp.S.Zero, A3]
    A_up = [
        sp.factor(sum(inverse[i, j] * A_cov[j] for j in range(n)))
        for i in range(n)
    ]
    # nabla_cov[rho][sigma] = nabla_rho A_sigma
    nabla_cov = [
        [
            sp.factor(
                sp.diff(A_cov[sigma], coords[rho])
                - sum(
                    gamma[ell][rho][sigma] * A_cov[ell]
                    for ell in range(n)
                )
            )
            for sigma in range(n)
        ]
        for rho in range(n)
    ]
    # nabla_up[mu][rho] = nabla_mu A^rho
    nabla_up = [
        [
            sp.factor(
                sp.diff(A_up[rho], coords[mu])
                + sum(
                    gamma[rho][mu][ell] * A_up[ell]
                    for ell in range(n)
                )
            )
            for rho in range(n)
        ]
        for mu in range(n)
    ]

    div_A = sp.factor(sum(nabla_up[mu][mu] for mu in range(n)))
    derivative_combination = sp.factor(
        div_A**2
        - sum(
            inverse[sigma, mu]
            * nabla_cov[rho][sigma]
            * nabla_up[mu][rho]
            for rho in range(n)
            for sigma in range(n)
            for mu in range(n)
        )
    )
    ricci_vector_contraction = sp.factor(
        sum(
            ricci[i, j] * A_up[i] * A_up[j]
            for i in range(n)
            for j in range(n)
        )
    )

    # J^mu = A^mu div(A) - A^nu nabla_nu A^mu
    J_up = [
        sp.factor(
            A_up[mu] * div_A
            - sum(A_up[nu] * nabla_up[nu][mu] for nu in range(n))
        )
        for mu in range(n)
    ]
    div_J = sp.factor(
        sum(
            sp.diff(J_up[mu], coords[mu])
            + sum(gamma[mu][mu][nu] * J_up[nu] for nu in range(n))
            for mu in range(n)
        )
    )

    # Convention-specific identity: D - R_mn A^m A^n - nabla_mu J^mu = 0.
    return sp.factor(
        derivative_combination - ricci_vector_contraction - div_J
    )


def main() -> None:
    residual = ricci_divergence_residual()
    if residual != 0:
        raise AssertionError(f"Ricci/divergence identity residual is nonzero: {residual}")
    print("RICCI_DIVERGENCE_IDENTITY_4D_DIAGONAL_OK")
    print("Scope: arbitrary t,z functions; diagonal metric; A_0 and A_3 components.")
    print("Boundary: full off-diagonal perturbation and physical DOF count remain unverified.")


if __name__ == "__main__":
    main()
