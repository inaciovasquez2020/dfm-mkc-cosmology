import json
from pathlib import Path

import sympy as sp

from dfm_mkc_solver.visible_sector_action_v1 import second_metric_response
from dfm_mkc_solver.visible_sector_offshell_scalar_hessian_v1 import (
    direct_second_differentiation_residual,
    mixed_action_hessian,
    number_density_variations,
    q_variations,
    scalar_flrw_hessian,
)


def test_q_n_and_covariant_exchange_symmetry():
    G = sp.diag(-2, 3)
    J = sp.Matrix(sp.symbols("J0:2"))
    h = sp.Matrix(2, 2, sp.symbols("h0:4"))
    k = sp.Matrix(2, 2, sp.symbols("k0:4"))
    h = (h + h.T) / 2
    k = (k + k.T) / 2
    j = sp.Matrix(sp.symbols("j0:2"))
    r = sp.Matrix(sp.symbols("r0:2"))
    qh, qk, qhk = q_variations(G=G, J=J, h=h, j=j, k=k, r=r)
    qk2, qh2, qkh = q_variations(G=G, J=J, h=k, j=r, k=h, r=j)
    assert sp.simplify(qh-qh2) == sp.simplify(qk-qk2) == 0
    assert sp.simplify(qhk-qkh) == 0
    q, n = sp.symbols("q n", positive=True)
    th, tk, hgk = sp.symbols("th tk hgk")
    dn = number_density_variations(
        n=n, q=q, dq_h=qh, dq_k=qk, d2q_hk=qhk,
        tr_h=th, tr_k=tk, h_g_k=hgk,
    )
    dn_swap = number_density_variations(
        n=n, q=q, dq_h=qk, dq_k=qh, d2q_hk=qkh,
        tr_h=tk, tr_k=th, h_g_k=hgk,
    )
    assert sp.simplify(dn[2]-dn_swap[2]) == 0


def test_complete_hessian_and_fixed_current_recovery():
    D, rho, rp, rpp, n = sp.symbols("D rho rp rpp n")
    th, tk, uh, uk, hgk, uhgku = sp.symbols("th tk uh uk hgk uhgku")
    dnh = n*(th+uh)/2
    dnk = n*(tk+uk)/2
    d2n = n*((th+uh)*(tk+uk)/4-hgk/2-uhgku-uh*uk/2)
    got = mixed_action_hessian(
        D=D, rho=rho, rho_prime=rp, rho_second=rpp, n=n,
        dn_h=dnh, dn_k=dnk, d2n=d2n, tr_h=th, tr_k=tk,
        h_g_k=hgk,
    )
    expected = second_metric_response(
        measure=D, density=rho, density_prime=rp, density_second=rpp,
        number_density=n, h_trace=th, k_trace=tk, h_velocity=uh,
        k_velocity=uk, h_metric_k=hgk,
        velocity_h_metric_k_velocity=uhgku,
    )
    assert sp.expand(got-expected) == 0
    x, y = sp.symbols("x y")
    assert mixed_action_hessian(
        D=D, rho=rho, rho_prime=rp, rho_second=rpp, n=n,
        dn_h=0, dn_k=0, d2n=0, tr_h=0, tr_k=0, h_g_k=0,
        j_dot_dmu=x, r_dot_dlambda=y,
    ) == -x-y


def test_scalar_blocks_directly_reconstructed():
    m, kap = sp.symbols("m_b kappa_r", positive=True)
    Hb = scalar_flrw_hessian(exponent=1, coefficient=m)
    Hr = scalar_flrw_hessian(exponent=sp.Rational(4, 3), coefficient=kap)
    a, J0, k2 = sp.symbols("a J0 k2", positive=True)
    assert Hb[:4, :4] == sp.Matrix([
        [0, 0, -a*m, 0], [0, a*J0*k2*m, 0, a*k2*m],
        [-a*m, 0, 0, 0], [0, a*k2*m, 0, a*k2*m/J0],
    ])
    assert Hr[0, 0] == Hr[0, 1] == Hr[2, 3] == 0
    assert Hb[3, 4] == Hb[4, 3] == -k2


def test_nonzero_shift_shift_coefficients():
    m, kap = sp.symbols("m_b kappa_r", positive=True)
    a, J0, k2 = sp.symbols("a J0 k2", positive=True)
    assert scalar_flrw_hessian(exponent=1, coefficient=m)[1, 1] == a*m*J0*k2
    assert scalar_flrw_hessian(
        exponent=sp.Rational(4, 3), coefficient=kap
    )[1, 1] == sp.Rational(4, 3)*kap*J0**sp.Rational(4, 3)*k2


def test_temporal_current_potential_pair_is_formally_self_adjoint():
    m = sp.symbols("m_b", positive=True)
    H = scalar_flrw_hessian(exponent=1, coefficient=m)
    d_eta = sp.Symbol("partial_eta", commutative=False)
    assert H[2, 4] == -d_eta
    assert H[4, 2] == d_eta


def test_direct_model_and_result_contract():
    assert direct_second_differentiation_residual() == 0
    path = Path(__file__).parents[1] / "artifacts/dfm_mkc/visible_sector_offshell_scalar_hessian_v1.json"
    payload = json.loads(path.read_text())
    assert payload["boundary_terms"]["unintegrated"] == (
        "-delta J^0 delta ell' - k^2 delta J_L delta ell"
    )
    assert payload["continuity_rows"]["both_sectors"] == "delta J_I^0' - k^2 delta J_{I,L}=0"
    assert "BB" not in payload["baryon_scalar_blocks"]["exact_zero_blocks"]
    assert "BB" not in payload["radiation_scalar_blocks"]["exact_zero_blocks"]
    assert payload["boundary_terms"]["temporal_operator_pair"] == (
        "H[deltaJ0,deltaell]=-partial_eta; "
        "H[deltaell,deltaJ0]=+partial_eta"
    )
    assert payload["certificates"]["direct"].endswith(
        "exact simplified residual zero."
    )
    assert payload["limitations"]["total_scalar_lapse_shift_hessian"] == "not established"
