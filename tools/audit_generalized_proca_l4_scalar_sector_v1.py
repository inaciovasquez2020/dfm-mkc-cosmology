#!/usr/bin/env python3
"""Bounded symbolic audit of the linear-G4 scalar perturbation ansatz.

This rebuilds the supplied t,z-dependent metric/vector/scalar ansatz with the
explicit completion G4(X) = -xi*X/2, G4_X = -xi/2, and retains F(phi) R/2
as a separate scalar-tensor term. It checks the Ricci/divergence identity,
rebuilds L2 and the Fourier-reduced Lagrangian, derives Euler-Lagrange
equations, and tests the frozen-coefficient characteristic determinant at
three rational parameter/background samples.

This is not a full scalar-sector DOF proof: the metric ansatz omits an explicit
scalar spatial-curvature perturbation. Sampled determinant degrees are not a
generic theorem. Requires SymPy.
"""
from __future__ import annotations

import sympy as sp


def trunc(expr: sp.Expr, eps: sp.Symbol, order: int = 2) -> sp.Expr:
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
            [0, a**2, 0, 0],
            [0, 0, a**2, 0],
            [eps * a * beta, 0, 0, a**2],
        ]
    )
    inverse = metric.inv().applyfunc(
        lambda expr: tr(sp.series(sp.simplify(expr), eps, 0, 3).removeO())
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
    sqrt_det_factor = sp.series(
        sp.sqrt(1 + 2 * eps * Phi + eps**2 * beta**2), eps, 0, 3
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
    L2 = sp.expand(Lagrangian).coeff(eps, 2)

    # Fourier parity ansatz inherited from the supplied source.
    amplitudes = {
        name: sp.Function(name + "t")(t)
        for name in ("Phi", "beta", "sigma", "u", "chi")
    }
    replacements = {
        Phi: amplitudes["Phi"] * sp.cos(k * z),
        delta_phi: amplitudes["sigma"] * sp.cos(k * z),
        u: amplitudes["u"] * sp.cos(k * z),
        beta: amplitudes["beta"] * sp.sin(k * z),
        chi: amplitudes["chi"] * sp.sin(k * z),
    }
    Lk = sp.expand(L2.subs(replacements).doit())
    Lk = sp.simplify(sp.integrate(Lk, (z, 0, 2 * sp.pi / k)) * k / (2 * sp.pi))

    fields = list(amplitudes.values())
    EL = {
        name: euler_lagrange_time(Lk, field, t)
        for name, field in amplitudes.items()
    }

    # Kinetic Hessian: field order (Phi, beta, sigma, u, chi).
    velocities = [sp.diff(field, t) for field in fields]
    kinetic_hessian = sp.hessian(Lk, velocities)
    expected_hessian = sp.zeros(5)
    expected_hessian[2, 2] = alpha * a**3 / 2
    expected_hessian[4, 4] = a / 2
    if sp.simplify(kinetic_hessian - expected_hessian) != sp.zeros(5):
        raise AssertionError("Kinetic Hessian does not match the derived diagonal form")

    # Frozen-coefficient characteristic matrix. This is a local symbol, not an
    # exact global characteristic polynomial on a time-dependent background.
    s = sp.Symbol("s")
    amp_symbols = {
        name: sp.Symbol("A_" + name) for name in amplitudes
    }
    char_subs = {}
    for name, field in amplitudes.items():
        char_subs[field] = amp_symbols[name]
        orders = {
            len(d.variables)
            for equation in EL.values()
            for d in equation.atoms(sp.Derivative)
            if d.expr == field and all(v == t for v in d.variables)
        }
        for order in orders:
            char_subs[sp.diff(field, (t, order))] = amp_symbols[name] * s**order

    EL_symbolic = {
        name: sp.expand(equation.xreplace(char_subs))
        for name, equation in EL.items()
    }
    characteristic = sp.Matrix(
        [
            [
                sp.diff(EL_symbolic[row], amp_symbols[col])
                for col in amplitudes
            ]
            for row in amplitudes
        ]
    )

    auxiliary = [amplitudes["Phi"], amplitudes["beta"], amplitudes["u"]]
    auxiliary_hessian = sp.hessian(Lk, auxiliary)
    derivative_atoms = sorted(
        set().union(
            *(entry.atoms(sp.Derivative) for entry in list(characteristic) + list(auxiliary_hessian))
        ),
        key=str,
    )
    derivative_placeholders = {
        derivative: sp.Symbol(f"background_derivative_{i}")
        for i, derivative in enumerate(derivative_atoms)
    }
    characteristic_without_derivatives = characteristic.xreplace(derivative_placeholders)
    auxiliary_without_derivatives = auxiliary_hessian.xreplace(derivative_placeholders)

    parameter_symbols = {
        "xi": xi,
        "xs": xs,
        "alpha": alpha,
        "m2": m2,
        "bet": bet,
        "mA2": mA2,
        "lam": lam,
        "L0": L0,
        "M2": M2,
    }
    samples = [
        ([2, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 3, 2, 1, 1, 2, 3], 1),
        ([3, 2, 1, 2, 2, 1, 2, 3, 2, 1, 3, 1, 2, 3, 2, 1, 4], 2),
        ([4, 1, 2, 5, 2, 3, 1, 1, 3, 2, 1, 2, 4, 1, 3, 2, 5], 3),
    ]
    determinant_degrees = []
    auxiliary_nonzero = []
    for values, B_dot in samples:
        a0, a1, a2, phi0, phi1, phi2, B0, k0 = values[:8]
        substitutions = {
            a: sp.Rational(a0),
            phi: sp.Rational(phi0),
            B: sp.Rational(B0),
            k: sp.Rational(k0),
        }
        for name, value in zip(parameter_symbols, values[8:]):
            substitutions[parameter_symbols[name]] = sp.Rational(value)
        for derivative, placeholder in derivative_placeholders.items():
            if derivative.expr == a:
                value = a2 if len(derivative.variables) == 2 else a1
            elif derivative.expr == phi:
                value = phi2 if len(derivative.variables) == 2 else phi1
            elif derivative.expr == B:
                value = B_dot
            else:
                raise AssertionError(f"Unexpected background derivative: {derivative}")
            substitutions[placeholder] = sp.Rational(value)

        numeric_characteristic = characteristic_without_derivatives.xreplace(substitutions)
        determinant = numeric_characteristic.det(method="domain-ge")
        degree = sp.Poly(determinant, s).degree()
        if degree != 4:
            raise AssertionError(f"Sampled characteristic degree was {degree}, expected 4")
        determinant_degrees.append(degree)

        numeric_auxiliary = auxiliary_without_derivatives.xreplace(substitutions)
        auxiliary_det = numeric_auxiliary.det(method="domain-ge")
        if auxiliary_det == 0:
            raise AssertionError("Auxiliary algebraic block singular at a declared sample")
        auxiliary_nonzero.append(True)

    print("RICCI_DIVERGENCE_IDENTITY_ON_PERTURBED_ANSATZ := PASS")
    print("CORRECTED_L2_BUILD := PASS")
    print("FOURIER_REDUCTION := PASS")
    print("EL_EQUATIONS := PASS (5 fields)")
    print("KINETIC_HESSIAN := diag(0, 0, alpha*a(t)^3/2, 0, a(t)/2)")
    print("KINETIC_HESSIAN_RANK := 2 conditional on a(t) != 0 and alpha != 0")
    print(f"FROZEN_SYMBOL_SAMPLE_DEGREES := {determinant_degrees}")
    print(f"AUXILIARY_BLOCK_NONZERO_SAMPLES := {len(auxiliary_nonzero)}/3")
    print("BOUNDARY := restricted metric ansatz; sampled symbol is not a generic theorem")
    print("PHYSICAL_SCALAR_DOF_COUNT := OPEN (spatial scalar metric perturbation omitted)")


if __name__ == "__main__":
    main()
