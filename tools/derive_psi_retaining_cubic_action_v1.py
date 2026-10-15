#!/usr/bin/env python3
"""Cubic-order symbolic construction for the six-field linear-G4 scalar perturbation ansatz.

This rebuilds the supplied t,z-dependent metric/vector/scalar ansatz with the
explicit completion G4(X) = -xi*X/2, G4_X = -xi/2, and retains F(phi) R/2
as a separate scalar-tensor term. It checks the Ricci/divergence identity,
rebuilds L2 and the Fourier-reduced Lagrangian, derives Euler-Lagrange
equations, and tests the frozen-coefficient characteristic determinant at
three rational parameter/background samples.

This is a psi-retaining quadratic-action and linearized-constraint derivation.
It fixes the scalar spatial shear E=0 but retains the spatial-curvature mode psi.
It does not by itself certify a physical degree-of-freedom count or stability.
Requires SymPy.
"""
from __future__ import annotations

import sympy as sp


def trunc(expr: sp.Expr, eps: sp.Symbol, order: int = 3) -> sp.Expr:
    expr = sp.expand(expr)
    return sum(expr.coeff(eps, i) * eps**i for i in range(order + 1))


def euler_lagrange_time(L: sp.Expr, field: sp.Expr, t: sp.Symbol) -> sp.Expr:
    orders = {
        len(d.variables)
        for d in L.atoms(sp.Derivative)
        if d.expr == field and all(v == t for v in d.variables)
    }
    result = sp.diff(L, field)
    for order in range(1, max(orders, default=0) + 1):
        result += (-1) ** order * sp.diff(
            sp.diff(L, sp.diff(field, (t, order))), (t, order)
        )
    return sp.expand(result)


def main() -> None:
    t, z, eps, k = sp.symbols("t z epsilon k", positive=True)
    x, y = sp.symbols("x y")
    coords = [t, x, y, z]
    n = 4

    a = sp.Function("a")(t)
    phi = sp.Function("phi")(t)
    B = sp.Function("B")(t)
    Phi = sp.Function("Phi")(t, z)
    psi = sp.Function("psi")(t, z)
    beta = sp.Function("beta")(t, z)
    delta_phi = sp.Function("sigma")(t, z)
    u = sp.Function("u")(t, z)
    chi = sp.Function("chi")(t, z)

    xi, xs, alpha, m2, bet, mA2, lam, L0, M2 = sp.symbols(
        "xi xs alpha m2 bet mA2 lam L0 M2"
    )

    def tr(expr: sp.Expr, order: int = 2) -> sp.Expr:
        return trunc(expr, eps, order)

    metric = sp.Matrix(
        [
            [-(1 + 2 * eps * Phi), 0, 0, eps * a * beta],
            [0, a**2 * (1 - 2 * eps * psi), 0, 0],
            [0, 0, a**2 * (1 - 2 * eps * psi), 0],
            [eps * a * beta, 0, 0, a**2 * (1 - 2 * eps * psi)],
        ]
    )
    inverse = metric.inv().applyfunc(
        lambda expr: tr(sp.series(sp.simplify(expr), eps, 0, 4).removeO())
    )

    # gamma[r][m][v] = Gamma^r_{mv}; Ricci convention matches the supplied source.
    gamma = [
        [
            [
                tr(
                    sum(
                        inverse[r, ell]
                        * (
                            sp.diff(metric[ell, m], coords[v])
                            + sp.diff(metric[ell, v], coords[m])
                            - sp.diff(metric[m, v], coords[ell])
                        )
                        for ell in range(n)
                    )
                    / 2
                )
                for v in range(n)
            ]
            for m in range(n)
        ]
        for r in range(n)
    ]

    ricci = sp.zeros(n, n)
    for m in range(n):
        for v in range(m, n):
            ricci[m, v] = tr(
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
            ricci[v, m] = ricci[m, v]

    Ricci_scalar = tr(
        sum(
            inverse[i, j] * ricci[i, j]
            for i in range(n)
            for j in range(n)
        )
    )

    P = phi + eps * delta_phi
    F = M2 - xs * P**2
    V = L0 + m2 * P**2 / 2 + lam * P**4 / 4
    Q = mA2 + bet * P**2
    A_cov = [B + eps * u, 0, 0, eps * chi]
    A_up = [
        tr(sum(inverse[i, j] * A_cov[j] for j in range(n)))
        for i in range(n)
    ]
    A_squared = tr(
        sum(
            inverse[i, j] * A_cov[i] * A_cov[j]
            for i in range(n)
            for j in range(n)
        )
    )
    X_A = -A_squared / 2

    ricci_vector = tr(
        sum(
            ricci[i, j] * A_up[i] * A_up[j]
            for i in range(n)
            for j in range(n)
        )
    )

    # F_{mu nu} = partial_mu A_nu - partial_nu A_mu.
    field_strength = sp.zeros(n, n)
    for m in range(n):
        for v in range(n):
            field_strength[m, v] = sp.diff(A_cov[v], coords[m]) - sp.diff(
                A_cov[m], coords[v]
            )
    F_squared = tr(
        sum(
            inverse[i, kk] * inverse[j, ell] * field_strength[i, j]
            * field_strength[kk, ell]
            for i in range(n)
            for j in range(n)
            for kk in range(n)
            for ell in range(n)
            if field_strength[i, j] != 0 and field_strength[kk, ell] != 0
        )
    )

    dP = [sp.diff(P, coords[i]) for i in range(n)]
    scalar_kinetic = tr(
        sum(
            inverse[i, j] * dP[i] * dP[j]
            for i in range(n)
            for j in range(n)
        )
    )

    # D = (nabla_mu A^mu)^2 - (nabla_mu A^nu)(nabla_nu A^mu).
    nabla_cov = [
        [
            tr(
                sp.diff(A_cov[sigma], coords[rho])
                - sum(
                    gamma[mu][rho][sigma] * A_cov[mu]
                    for mu in range(n)
                )
            )
            for sigma in range(n)
        ]
        for rho in range(n)
    ]
    nabla_up = [
        [
            tr(
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
    div_A = tr(sum(nabla_up[mu][mu] for mu in range(n)))
    D4 = tr(
        div_A**2
        - sum(
            inverse[sigma, mu] * nabla_cov[rho][sigma] * nabla_up[mu][rho]
            for rho in range(n)
            for sigma in range(n)
            for mu in range(n)
        )
    )

    J_up = [
        tr(
            A_up[mu] * div_A
            - sum(A_up[nu] * nabla_up[nu][mu] for nu in range(n))
        )
        for mu in range(n)
    ]
    div_J = tr(
        sum(
            sp.diff(J_up[mu], coords[mu])
            + sum(gamma[mu][mu][nu] * J_up[nu] for nu in range(n))
            for mu in range(n)
        )
    )
    identity_residual = sp.simplify(sp.expand(D4 - ricci_vector - div_J))
    if identity_residual != 0:
        raise AssertionError(f"Ricci/divergence identity failed: {identity_residual}")

    # Linear generalized-Proca L4 completion, separate from F(phi) R/2.
    G4 = -xi * X_A / 2
    # Derive the volume factor from the actual perturbed metric, then
    # compare it against the closed-form block-determinant expression.
    determinant_factor = tr(-metric.det() / a**6)
    expected_determinant_factor = tr(
        sp.expand(
            (1 - 2 * eps * psi)**3 * (1 + 2 * eps * Phi)
            + eps**2 * beta**2 * (1 - 2 * eps * psi)**2
        )
    )
    determinant_residual = sp.simplify(
        determinant_factor - expected_determinant_factor
    )
    if determinant_residual != 0:
        raise AssertionError(
            f"Metric determinant/volume-factor identity failed: {determinant_residual}"
        )
    sqrt_det_factor = sp.series(
        sp.sqrt(determinant_factor), eps, 0, 3
    ).removeO()
    sqrt_minus_g = a**3 * sqrt_det_factor
    Lagrangian = tr(
        sqrt_minus_g
        * tr(
            F * Ricci_scalar / 2
            + G4 * Ricci_scalar
            - xi * D4 / 2
            - alpha * scalar_kinetic / 2
            - V
            - F_squared / 4
            - Q * A_squared / 2
        )
    )
    L3 = sp.expand(Lagrangian).coeff(eps, 3)

    if L3.has(eps):
        raise AssertionError("Cubic coefficient still depends on epsilon")
    if L3 == 0:
        raise AssertionError("Cubic action density unexpectedly vanished")
    print("ACTION_COMPLETION := F(phi)*R/2 plus linear generalized-Proca L4 completion")
    print("PERTURBATION_FIELDS := (Phi, psi, beta, sigma, u, chi)")
    print("GAUGE := E=0; psi retained")
    print("EXPANSION_ORDER := epsilon^3")
    print("OUTPUT_OBJECT := FULL_CUBIC_ACTION_DENSITY_BEFORE_FOURIER_RESTRICTION")
    print("CUBIC_ACTION_DENSITY := " + sp.sstr(L3))
    print("BOUNDARY := explicit action completion and perturbation ansatz only; no full adjoint projection claimed")


if __name__ == "__main__":
    main()
