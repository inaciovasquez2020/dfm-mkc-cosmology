"""Exact off-shell Schutz--Sorkin Hessian for the visible scalar fluids.

The action density is exactly ``-D*rho(n)-J^mu*partial_mu(ell)``.  All
objects in this module are SymPy expressions.  In particular, no field
equation is used in forming either the covariant or scalar Hessian.
"""

from __future__ import annotations

import sympy as sp


def number_density_variations(
    *, n, q, dq_h, dq_k, d2q_hk, tr_h, tr_k, h_g_k
):
    """Return (delta_h n, delta_k n, delta_k delta_h n).

    ``h_g_k`` denotes h^{ab} g_{ac} g_{bd} k^{cd}.  The q variations may
    contain both metric and current variations.
    """
    p_h = dq_h / (2 * q) + tr_h / 2
    p_k = dq_k / (2 * q) + tr_k / 2
    return (
        sp.expand(n * p_h),
        sp.expand(n * p_k),
        sp.expand(
            n
            * (
                p_h * p_k
                + d2q_hk / (2 * q)
                - dq_h * dq_k / (2 * q**2)
                - h_g_k / 2
            )
        ),
    )


def q_variations(*, G, J, h, j, k, r):
    """Exact q=-G_ab J^a J^b variations for inverse-metric directions.

    Matrices are finite-dimensional tensor representatives.  This is also a
    convenient exact certificate of the index formula

      dq[h,j] = J^T G h G J - 2 J^T G j,
      d2q = -J^T(GkGhG+GhGkG)J
             +2 J^T GhG r +2 J^T GkG j -2 j^T G r.
    """
    scalar = lambda x: sp.expand(x[0])
    dq_h = scalar(J.T * G * h * G * J - 2 * J.T * G * j)
    dq_k = scalar(J.T * G * k * G * J - 2 * J.T * G * r)
    d2q = scalar(
        -J.T * (G * k * G * h * G + G * h * G * k * G) * J
        + 2 * J.T * G * h * G * r
        + 2 * J.T * G * k * G * j
        - 2 * j.T * G * r
    )
    return dq_h, dq_k, d2q


def mixed_action_hessian(
    *,
    D,
    rho,
    rho_prime,
    rho_second,
    n,
    dn_h,
    dn_k,
    d2n,
    tr_h,
    tr_k,
    h_g_k,
    j_dot_dmu=0,
    r_dot_dlambda=0,
):
    """Complete mixed Hessian of the local action density.

    The last two arguments are j^mu partial_mu(mu) and
    r^mu partial_mu(lambda).  They display the symmetric current-potential
    block without integrating by parts.
    """
    dD_h = -D * tr_h / 2
    dD_k = -D * tr_k / 2
    d2D = D * (tr_h * tr_k / 4 + h_g_k / 2)
    return sp.expand(
        -rho * d2D
        - rho_prime * (dD_h * dn_k + dD_k * dn_h)
        - D * rho_second * dn_h * dn_k
        - D * rho_prime * d2n
        - j_dot_dmu
        - r_dot_dlambda
    )


def scalar_flrw_hessian(*, exponent, coefficient):
    """Return the exact Fourier scalar Hessian in (A,B,dJ0,dJL,dell).

    The entries containing ``d_eta`` are differential-operator entries:
    H[dJ0,dell]=-partial_eta and H[dell,dJ0]=+partial_eta are formal
    adjoints under the recorded vanishing temporal boundary variation.
    Spatial Fourier factors use exp(i k.x), hence partial_i partial^i=-k^2.
    """
    a, J0, k2 = sp.symbols("a J0 k2", positive=True)
    A, B, x, y = sp.symbols("A B deltaJ0 deltaJL")
    q = a**2 * (
        (1 + A) ** 2 * (J0 + x) ** 2
        - k2 * (y + B * (J0 + x)) ** 2
    )
    D = a**4 * (1 + A)
    density = coefficient * (sp.sqrt(q) / D) ** exponent
    local = -D * density
    variables = (A, B, x, y)
    four = sp.Matrix(
        [
            [
                sp.simplify(
                    sp.diff(local, u, v).subs({A: 0, B: 0, x: 0, y: 0})
                )
                for v in variables
            ]
            for u in variables
        ]
    )
    d_eta = sp.Symbol("partial_eta", commutative=False)
    H = sp.zeros(5)
    H[:4, :4] = four
    H[2, 4] = -d_eta
    H[4, 2] = d_eta
    H[3, 4] = H[4, 3] = -k2
    return H


def direct_second_differentiation_residual():
    """Direct finite-dimensional Hessian minus the covariant chain rule."""
    t, s = sp.symbols("t s")
    g0, g1, J0, J1, e0, e1 = sp.symbols(
        "g0 g1 J0 J1 e0 e1", positive=True
    )
    h0, h1, k0, k1, j0, j1, r0, r1 = sp.symbols(
        "h0 h1 k0 k1 j0 j1 r0 r1"
    )
    lam0, lam1, mu0, mu1 = sp.symbols("lam0 lam1 mu0 mu1")
    Ginv = sp.diag(-g0 + t * h0 + s * k0, g1 + t * h1 + s * k1)
    G = Ginv.inv()
    J = sp.Matrix([J0 + t * j0 + s * r0, J1 + t * j1 + s * r1])
    D = sp.sqrt(-G.det())
    q = sp.expand(-(J.T * G * J)[0])
    n = sp.sqrt(q) / D
    ell_gradient = sp.Matrix(
        [e0 + t * lam0 + s * mu0, e1 + t * lam1 + s * mu1]
    )
    c = sp.Symbol("c")
    gamma = sp.Integer(2)
    action = -D * c * n**gamma - (
        J.T * ell_gradient
    )[0]
    direct = sp.diff(action, t, s).subs({t: 0, s: 0})

    G0 = sp.diag(-1 / g0, 1 / g1)
    Jbase = sp.Matrix([J0, J1])
    h = sp.diag(h0, h1)
    k = sp.diag(k0, k1)
    j = sp.Matrix([j0, j1])
    r = sp.Matrix([r0, r1])
    q0 = sp.expand(-(Jbase.T * G0 * Jbase)[0])
    D0 = 1 / sp.sqrt(g0 * g1)
    n0 = sp.sqrt(q0) / D0
    tr_h = sp.trace(G0 * h)
    tr_k = sp.trace(G0 * k)
    h_g_k = sp.trace(h * G0 * k * G0)
    dq_h, dq_k, d2q = q_variations(
        G=G0, J=Jbase, h=h, j=j, k=k, r=r
    )
    dn_h, dn_k, d2n = number_density_variations(
        n=n0,
        q=q0,
        dq_h=dq_h,
        dq_k=dq_k,
        d2q_hk=d2q,
        tr_h=tr_h,
        tr_k=tr_k,
        h_g_k=h_g_k,
    )
    chain = mixed_action_hessian(
        D=D0,
        rho=c * n0**gamma,
        rho_prime=c * gamma * n0 ** (gamma - 1),
        rho_second=c * gamma * (gamma - 1) * n0 ** (gamma - 2),
        n=n0,
        dn_h=dn_h,
        dn_k=dn_k,
        d2n=d2n,
        tr_h=tr_h,
        tr_k=tr_k,
        h_g_k=h_g_k,
        j_dot_dmu=(j.T * sp.Matrix([mu0, mu1]))[0],
        r_dot_dlambda=(r.T * sp.Matrix([lam0, lam1]))[0],
    )
    return sp.simplify(direct - chain)


def continuity_row():
    return "deltaJ0' - k^2 deltaJ_L = 0"


def potential_flow_rows():
    return (
        "partial_0 ell = rho'(n) u_0",
        "i k_i delta ell = delta[rho'(n) u_i]",
    )
