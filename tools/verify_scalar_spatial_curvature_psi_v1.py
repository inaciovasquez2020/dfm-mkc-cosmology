#!/usr/bin/env python3
"""Exact linearized spatial-curvature check for the omitted scalar mode psi.

For h_ij = a^2 (1 - 2 epsilon psi) delta_ij at fixed time, verifies
delta R^(3) = 4 Laplacian(psi)/a^2 to first order in epsilon.
This is a spatial-geometry identity only; it does not derive the full
four-dimensional quadratic action or count physical scalar degrees of freedom.
Requires SymPy.
"""
from __future__ import annotations

import sympy as sp


def truncate(expr: sp.Expr, eps: sp.Symbol, order: int = 1) -> sp.Expr:
    expr = sp.expand(expr)
    return sum(expr.coeff(eps, i) * eps**i for i in range(order + 1))


def main() -> None:
    x, y, z, eps = sp.symbols("x y z epsilon")
    a = sp.symbols("a", nonzero=True)
    coords = (x, y, z)
    psi = sp.Function("psi")(*coords)
    n = len(coords)

    spatial_metric = sp.diag(*[a**2 * (1 - 2 * eps * psi)] * n)
    inverse = spatial_metric.inv().applyfunc(
        lambda item: truncate(sp.series(item, eps, 0, 2).removeO(), eps)
    )

    gamma = [
        [
            [
                truncate(
                    sum(
                        inverse[i, ell]
                        * (
                            sp.diff(spatial_metric[ell, j], coords[k])
                            + sp.diff(spatial_metric[ell, k], coords[j])
                            - sp.diff(spatial_metric[j, k], coords[ell])
                        )
                        for ell in range(n)
                    )
                    / 2,
                    eps,
                )
                for k in range(n)
            ]
            for j in range(n)
        ]
        for i in range(n)
    ]

    ricci = sp.zeros(n, n)
    for j in range(n):
        for k in range(n):
            ricci[j, k] = truncate(
                sum(
                    sp.diff(gamma[i][j][k], coords[i])
                    - sp.diff(gamma[i][j][i], coords[k])
                    + sum(
                        gamma[i][i][ell] * gamma[ell][j][k]
                        - gamma[i][k][ell] * gamma[ell][j][i]
                        for ell in range(n)
                    )
                    for i in range(n)
                ),
                eps,
            )

    scalar = truncate(
        sum(
            inverse[i, j] * ricci[i, j]
            for i in range(n)
            for j in range(n)
        ),
        eps,
    )
    linearized_scalar = sp.simplify(sp.expand(scalar).coeff(eps, 1))
    expected = sp.simplify(
        4
        * sum(sp.diff(psi, coordinate, 2) for coordinate in coords)
        / a**2
    )
    residual = sp.simplify(linearized_scalar - expected)
    if residual != 0:
        raise AssertionError(
            "Linearized spatial Ricci scalar mismatch: "
            f"computed={linearized_scalar}, expected={expected}, residual={residual}"
        )

    fourier_psi = sp.Function("psi_amp")(z)
    fourier_subs = {
        psi: fourier_psi,
        sp.diff(psi, x): sp.Integer(0),
        sp.diff(psi, y): sp.Integer(0),
        sp.diff(psi, x, 2): sp.Integer(0),
        sp.diff(psi, y, 2): sp.Integer(0),
    }
    fourier_scalar = sp.simplify(expected.xreplace(fourier_subs))
    k = sp.symbols("k", nonzero=True)
    amplitude = sp.symbols("psi_k")
    mode_scalar = sp.simplify(
        fourier_scalar.subs(fourier_psi, amplitude * sp.exp(sp.I * k * z))
        .doit()
    )
    mode_scalar = sp.simplify(mode_scalar / (amplitude * sp.exp(sp.I * k * z)))
    if sp.simplify(mode_scalar + 4 * k**2 / a**2) != 0:
        raise AssertionError(f"Fourier curvature coefficient mismatch: {mode_scalar}")

    print("LINEARIZED_SPATIAL_RICCI_SCALAR := 4*Laplacian(psi)/a**2")
    print("NONZERO_FOURIER_MODE_CURVATURE := -4*k**2*psi_k/a**2")
    print("SPATIAL_CURVATURE_PSI_CHECK := PASS")
    print("BOUNDARY := spatial identity only; full quadratic action and physical DOF count remain open")


if __name__ == "__main__":
    main()
