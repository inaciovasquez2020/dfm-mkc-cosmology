"""Exact cubic obstruction test on the exceptional generalized-Proca branch.

This is a deliberately bounded test, not a full nonlinear-symmetry or DOF proof.
It restricts the source action to a static, z-dependent subspace:
  g_{mu nu} = diag(-1, h, h, h), h = 1 - 2 eps p(z)
  A_mu = (b0 * (1 + eps p(z)), 0, 0, 0)
  phi = 0, chi = beta = Phi = sigma = 0.
It uses xi=-1/2, M2=b0**2/4 and the audited completion
G4=-xi*X_A/2, with X_A=-A_mu A^mu/2.

On this subspace R is the 3D conformal spatial Ricci scalar, R_tt=0,
D4=0, and F_{mu nu}F^{mu nu}=-2 (A0')**2/h. The cubic variation is
tested against a periodic mode triad. This can obstruct the proposed
leading null direction; it does not rule out every possible nonlinear
symmetry of the full theory.
"""
import sympy as sp


def test_exceptional_branch_has_nonzero_cubic_noether_residual():
    z, eps = sp.symbols("z epsilon", real=True)
    b0, A = sp.symbols("b0 A", nonzero=True, real=True)
    q = sp.symbols("q", positive=True, real=True)
    p = sp.Function("p")(z)
    xi = -sp.Rational(1, 2)
    M2 = b0**2 / 4

    h = 1 - 2 * eps * p
    A0 = b0 * (1 + eps * p)

    # For ds^2=-dt^2+h(z)(dx^2+dy^2+dz^2):
    # R = -2 h''/h^2 + 3(h')^2/(2h^3), R_tt=0.
    ricci_scalar = -2 * sp.diff(h, z, 2) / h**2 + sp.Rational(3, 2) * sp.diff(h, z)**2 / h**3
    field_strength_squared = -2 * sp.diff(A0, z)**2 / h
    volume = h**sp.Rational(3, 2)
    curvature_coefficient = M2 / 2 - xi * A0**2 / 4

    # D4 vanishes on this restricted static, purely temporal-vector subspace.
    lagrangian_density = volume * (
        curvature_coefficient * ricci_scalar - field_strength_squared / 4
    )
    cubic_density = sp.expand(
        sp.series(lagrangian_density, eps, 0, 4).removeO()
    ).coeff(eps, 3)

    expected_cubic = b0**2 * (
        6 * p**2 * sp.diff(p, z, 2) + 11 * p * sp.diff(p, z)**2
    ) / 2
    assert sp.simplify(cubic_density - expected_cubic) == 0

    # The candidate leading transformation is delta p=f, delta u=b0*f.
    # On this restricted subspace u=b0*p, so it is the variation along p.
    p_mode = A * sp.cos(q * z)
    f_mode = sp.cos(2 * q * z)
    p1 = sp.diff(p, z)
    p2 = sp.diff(p, z, 2)
    delta_density = (
        sp.diff(cubic_density, p) * f_mode
        + sp.diff(cubic_density, p1) * sp.diff(f_mode, z)
        + sp.diff(cubic_density, p2) * sp.diff(f_mode, z, 2)
    )
    delta_density = delta_density.xreplace({
        p: p_mode,
        p1: sp.diff(p_mode, z),
        p2: sp.diff(p_mode, z, 2),
    })
    residual = sp.simplify(
        sp.integrate(sp.expand_trig(delta_density), (z, 0, 2 * sp.pi / q))
    )
    assert sp.simplify(residual + 3 * sp.pi * A**2 * b0**2 * q / 4) == 0
    assert residual != 0


if __name__ == "__main__":
    test_exceptional_branch_has_nonzero_cubic_noether_residual()
    print("EXCEPTIONAL_BRANCH_CUBIC_OBSTRUCTION := VERIFIED")
    print("INTEGRATED_CUBIC_VARIATION := -3*pi*A**2*b0**2*q/4")
    print("SCOPE := RESTRICTED_STATIC_MODE_TRIAD; NOT_A_FULL_NONLINEAR_DOF_PROOF")
