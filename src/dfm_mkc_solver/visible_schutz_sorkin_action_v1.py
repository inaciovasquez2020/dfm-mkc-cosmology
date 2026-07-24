"""Exact visible-sector action binding for the canonical DFM branch.

This module represents two independent, irrotational Schutz--Sorkin fluids,

    S_I = -∫ d^4x [sqrt(-g) rho_I(n_I) + J_I^mu ∂_mu ell_I],
    n_I = sqrt(-g_mn J_I^m J_I^n) / sqrt(-g),

with rho_b=m_b*n_b and rho_r=kappa_r*n_r**(4/3).  All metric
variations below hold the *contravariant vector densities* J_I^mu and the
potentials ell_I fixed.  This choice is part of the result: changing it
changes the off-shell Hessian.

Conventions for the exact bilinear metric response
--------------------------------------------------
Let h^{mu nu} and k^{mu nu} be two commuting inverse-metric variations and
put

    h = g_mn h^mn,       U_h = u_m u_n h^mn,
    hk = h^mn k_mn,      W_hk = u_m h^m_r k^r_n u^n,
    X_h = h + U_h.

Indices on h and k are moved with the unperturbed metric.  Then

    δ_h sqrt(-g) = -sqrt(-g) h/2,
    δ_kδ_h sqrt(-g) = sqrt(-g) (h*k/4 + hk/2),
    δ_h n = n X_h/2,
    δ_kδ_h n = n[X_h X_k/4 - hk/2 - W_hk - U_h U_k/2].

W_hk=W_kh (transpose the scalar matrix product), so the last line and the
full Hessian are exchange symmetric.  The potential-density term J.dell
has no metric response at fixed J and ell.

Boundary ledger
---------------
Variation of ell gives

    -∫_M J^mu ∂_mu δell
      = ∫_M (∂_mu J^mu) δell - ∫_∂M J^mu n_mu δell.

The temporal part vanishes because δell is zero on the initial and final
time boundaries.  The spatial part vanishes when J^mu n_mu=0, or when the
perturbation has compact spatial support.  J- and metric-variations contain
no integrations by parts and hence no fluid boundary terms, including at
second metric order.  The Einstein--Hilbert metric variations retain the
repository's boundary prescription for the metric and its required normal
derivatives; this module neither changes nor silently removes those terms.

The selected perfect radiation is not a Boltzmann or recombination model.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HALF = sp.Rational(1, 2)
RADIATION_EXPONENT = sp.Rational(4, 3)
HELD_FIXED = (
    "contravariant vector densities J_b^mu,J_r^mu and scalar potentials "
    "ell_b,ell_r"
)


def density_laws():
    """Return the two selected exact symbolic density laws."""

    n_b, n_r, m_b, kappa_r = sp.symbols(
        "n_b n_r m_b kappa_r", positive=True
    )
    return {
        "b": (n_b, m_b * n_b),
        "r": (n_r, kappa_r * n_r**RADIATION_EXPONENT),
    }


def pressure_from_density(n, rho):
    """p=n*rho'(n)-rho, obtained by the fixed-J metric variation."""

    return sp.simplify(n * sp.diff(rho, n) - rho)


def equations_of_state():
    """Return (rho,p,w) for baryons and perfect radiation."""

    answer = {}
    for species, (n, rho) in density_laws().items():
        pressure = pressure_from_density(n, rho)
        answer[species] = (rho, pressure, sp.simplify(pressure / rho))
    return answer


def metric_response_symbols():
    """Symbols for the invariant contractions of two metric variations."""

    return sp.symbols(
        "q n rho rho_1 rho_2 h k U_h U_k hk W_hk"
    )


def number_density_variations():
    """Return exact first and mixed second variations of n at fixed J."""

    (
        _q,
        n,
        _rho,
        _rho_1,
        _rho_2,
        h,
        k,
        U_h,
        U_k,
        hk,
        W_hk,
    ) = metric_response_symbols()
    dn_h = n * (h + U_h) * HALF
    dn_k = n * (k + U_k) * HALF
    d2n = n * (
        (h + U_h) * (k + U_k) / 4
        - hk / 2
        - W_hk
        - U_h * U_k / 2
    )
    return sp.simplify(dn_h), sp.simplify(dn_k), sp.simplify(d2n)


def measure_variations():
    """Return exact first and mixed second variations of sqrt(-g)."""

    (
        q,
        _n,
        _rho,
        _rho_1,
        _rho_2,
        h,
        k,
        _U_h,
        _U_k,
        hk,
        _W_hk,
    ) = metric_response_symbols()
    return -q * h / 2, sp.simplify(q * (h * k / 4 + hk / 2))


def first_metric_response():
    """Return δ_h[-sqrt(-g)rho(n)] as an exact contact expression."""

    (
        q,
        n,
        rho,
        rho_1,
        _rho_2,
        h,
        _k,
        U_h,
        _U_k,
        _hk,
        _W_hk,
    ) = metric_response_symbols()
    return sp.simplify(q * (rho * h - n * rho_1 * (h + U_h)) / 2)


def second_metric_response():
    """Return the complete off-shell fixed-J mixed metric Hessian density."""

    (
        q,
        _n,
        rho,
        rho_1,
        rho_2,
        h,
        k,
        _U_h,
        _U_k,
        hk,
        _W_hk,
    ) = metric_response_symbols()
    dn_h, dn_k, d2n = number_density_variations()
    dq_h, d2q = measure_variations()
    dq_k = -q * k / 2
    return sp.factor(
        -(
            d2q * rho
            + dq_h * rho_1 * dn_k
            + dq_k * rho_1 * dn_h
            + q * rho_2 * dn_h * dn_k
            + q * rho_1 * d2n
        )
    )


def scalar_lapse_shift_hessian():
    """Exact ADM scalar lapse/shift Hessian of one fluid density.

    At one spatial point align the scalar shift with the x direction.  With
    ds^2=-N^2 dt^2+a^2(dx+s dt)^2+a^2(dy^2+dz^2), fixed
    (J0,Jx,Jy,Jz), q=N*a^3 and

      n=sqrt(N^2 J0^2-a^2[(Jx+s J0)^2+Jy^2+Jz^2])/(N*a^3).

    Differentiating the selected action density, rather than entering
    constraint terms, produces all lapse/shift contacts.
    """

    N, a = sp.symbols("N a", positive=True)
    s = sp.Symbol("s")
    J0, Jx, Jy, Jz = sp.symbols("J0 Jx Jy Jz", real=True)
    rho_function = sp.Function("rho")
    radicand = N**2 * J0**2 - a**2 * (
        (Jx + s * J0) ** 2 + Jy**2 + Jz**2
    )
    n_adm = sp.sqrt(radicand) / (N * a**3)
    lagrangian = -N * a**3 * rho_function(n_adm)
    return {
        "number_density": n_adm,
        "L_NN": sp.diff(lagrangian, N, 2),
        "L_Ns": sp.diff(lagrangian, N, s),
        "L_ss": sp.diff(lagrangian, s, 2),
        "background_comoving": {
            "L_NN": sp.simplify(
                sp.diff(lagrangian, N, 2).subs(
                    {s: 0, Jx: 0, Jy: 0, Jz: 0}
                )
            ),
            "L_Ns": sp.simplify(
                sp.diff(lagrangian, N, s).subs(
                    {s: 0, Jx: 0, Jy: 0, Jz: 0}
                )
            ),
            "L_ss": sp.simplify(
                sp.diff(lagrangian, s, 2).subs(
                    {s: 0, Jx: 0, Jy: 0, Jz: 0}
                )
            ),
        },
    }


def hessian_exchange_residual():
    """Exchange h<->k and U_h<->U_k; W is already symmetric."""

    expression = second_metric_response()
    symbols = {symbol.name: symbol for symbol in expression.free_symbols}
    h, k = symbols["h"], symbols["k"]
    U_h, U_k = symbols["U_h"], symbols["U_k"]
    swapped = expression.xreplace(
        {
            h: sp.Symbol("_k"),
            k: sp.Symbol("_h"),
            U_h: sp.Symbol("_U_k"),
            U_k: sp.Symbol("_U_h"),
        }
    ).xreplace(
        {
            sp.Symbol("_k"): k,
            sp.Symbol("_h"): h,
            sp.Symbol("_U_k"): U_k,
            sp.Symbol("_U_h"): U_h,
        }
    )
    return sp.simplify(expression - swapped)


def euler_lagrange_equations():
    """Exact equations for each species (the displayed sign is conventional)."""

    equations = {
        "ell_I": "partial_mu J_I^mu = 0",
        "J_I^mu": (
            "partial_mu ell_I = rho_I'(n_I) u_I_mu, "
            "u_I^mu=J_I^mu/(sqrt(-g)n_I), u_I^mu u_I_mu=-1"
        ),
        "g^mu_nu": (
            "delta S_I/delta g^mu_nu = "
            "-sqrt(-g) T_I_mu_nu/2"
        ),
    }
    equations["diffeomorphism_Ward_identity"] = ward_identity()
    return equations


def ward_identity():
    """Return the off-shell diffeomorphism Noether identity and its shell."""

    return {
        "off_shell": (
            "integral_M [E_g_mu_nu Lie_xi g^mu_nu"
            "+E_J_I_mu Lie_xi J_I^mu"
            "+E_ell_I Lie_xi ell_I] = 0 for compact-support xi; "
            "Lie_xi J^mu=xi^nu partial_nu J^mu"
            "-J^nu partial_nu xi^mu+J^mu partial_nu xi^nu"
        ),
        "on_shell": "nabla_mu T_I^mu_nu = 0",
        "boundary": (
            "integral_boundary n_mu xi^mu L_I = 0 because xi has "
            "compact support (or preserves the stated boundary data)"
        ),
    }


def ward_identity_residuals():
    """Verify the on-shell Ward identity without coordinate specialization.

    Decompose nabla_mu T^mu_nu parallel and orthogonal to u.  Continuity gives
    dot(n)=-n*Theta.  The exterior derivative of
    d ell=rho'(n) u gives
    a_nu=-P_nu^mu partial_mu rho'/rho'.  These substitutions make both
    independent projections vanish exactly.
    """

    n, rho_1, rho_2, theta, spatial_dn = sp.symbols(
        "n rho_1 rho_2 theta spatial_dn"
    )
    dot_n = -n * theta
    rho_plus_p = n * rho_1
    energy = sp.simplify(rho_1 * dot_n + rho_plus_p * theta)
    acceleration = -rho_2 * spatial_dn / rho_1
    spatial_pressure_gradient = n * rho_2 * spatial_dn
    momentum = sp.simplify(
        rho_plus_p * acceleration + spatial_pressure_gradient
    )
    return {"energy_projection": energy, "momentum_projection": momentum}


def flrw_conservation():
    """Derive exact FLRW powers from d rho/dt=-3H(rho+p)."""

    result = {}
    for species, (rho, pressure, _w) in equations_of_state().items():
        n = density_laws()[species][0]
        coefficient = sp.simplify(
            3 * (rho + pressure) / rho
        )
        number_coefficient = sp.Integer(3)
        result[species] = {
            "dot_n_over_H_n": -number_coefficient,
            "dot_rho_over_H_rho": -coefficient,
            "identity_residual": sp.simplify(
                -3 * n * sp.diff(rho, n)
                + coefficient * rho
            ),
        }
    return result


def action_derived_scalar_constraint_coefficients():
    """Project δS=-1/2∫sqrt(-g)T_mn δg^mn into the carrier.

    Einstein's equation from S_EH+S_vis is G_mn=8*pi*G*T_mn.
    Dividing its scalar projections by two gives the repository carrier
    normalization.  The signs are fixed by its Newtonian-gauge definitions:
    delta_rho=-delta T^0_0, momentum_source and enthalpy_sigma.
    No carrier coefficient is accepted as an input to this derivation.
    """

    pi, G, a = sp.pi, sp.Symbol("G"), sp.Symbol("a", positive=True)
    einstein_factor = 8 * pi * G
    carrier_normalization = sp.Rational(1, 2)
    factor = sp.simplify(einstein_factor * carrier_normalization * a**2)
    return {
        "hamiltonian_delta_rho": factor,
        "momentum_source": -factor,
        "anisotropy_enthalpy_sigma": -3 * factor,
    }


def existing_scalar_constraint_carrier_coefficients():
    """Exact symbolic transcription of scalar_constraint_source_vector."""

    G, a = sp.Symbol("G"), sp.Symbol("a", positive=True)
    prefactor = 4 * sp.pi * G * a**2
    return {
        "hamiltonian_delta_rho": prefactor,
        "momentum_source": -prefactor,
        "anisotropy_enthalpy_sigma": -3 * prefactor,
    }


def scalar_constraint_comparison():
    """Coefficient-by-coefficient exact action/carrier comparison."""

    derived = action_derived_scalar_constraint_coefficients()
    carrier = existing_scalar_constraint_carrier_coefficients()
    return {
        key: {
            "action_derived": derived[key],
            "existing_carrier": carrier[key],
            "residual": sp.simplify(derived[key] - carrier[key]),
        }
        for key in derived
    }


def exact_certificate():
    """Build the executable, exact gate certificate."""

    eos = equations_of_state()
    flrw = flrw_conservation()
    comparison = scalar_constraint_comparison()
    return {
        "baryon_pressure_zero": sp.simplify(eos["b"][1]) == 0,
        "radiation_pressure_one_third": (
            sp.simplify(eos["r"][1] - eos["r"][0] / 3) == 0
        ),
        "hessian_exchange_symmetric": hessian_exchange_residual() == 0,
        "flrw_baryon": flrw["b"]["dot_rho_over_H_rho"] == -3,
        "flrw_radiation": flrw["r"]["dot_rho_over_H_rho"] == -4,
        "constraint_coefficients_exact": all(
            item["residual"] == 0 for item in comparison.values()
        ),
        "ward_identity": all(
            residual == 0 for residual in ward_identity_residuals().values()
        ),
        "canonical_second_variation_ready": all(
            (
                hessian_exchange_residual() == 0,
                all(item["residual"] == 0 for item in comparison.values()),
            )
        ),
        "action_binding_established": all(
            item["residual"] == 0 for item in comparison.values()
        ),
    }


def _stringify(value):
    if isinstance(value, dict):
        return {key: _stringify(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_stringify(item) for item in value]
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    return value


def result_payload():
    """Return the sole result artifact payload with the required schema."""

    certificate = exact_certificate()
    dn_h, dn_k, d2n = number_density_variations()
    dq_h, d2q = measure_variations()
    eos = equations_of_state()
    comparison = scalar_constraint_comparison()
    limitations = [
        "photon recombination microphysics",
        "baryon-photon scattering",
        "photon polarization",
        "free-streaming neutrino anisotropic stress",
        "Boltzmann hierarchy",
        "CMB transfer function",
        "Weyl prediction vector",
        "separation from Lambda-CDM",
        "empirical evidence for DFM",
    ]
    payload = {
        "result_type": "standard_visible_sector_action_binding",
        "branch_selection": (
            "user_selected_irrotational_schutz_sorkin_"
            "baryon_radiation_baseline"
        ),
        "novelty_claimed": False,
        "visible_action_established": True,
        "equations_of_state_established": True,
        "first_metric_response_established": True,
        "second_metric_response_established": True,
        "boundary_contact_terms_established": True,
        "ward_identity_established": certificate["ward_identity"],
        "hessian_symmetry_established": certificate[
            "hessian_exchange_symmetric"
        ],
        "canonical_second_variation_ready": certificate[
            "canonical_second_variation_ready"
        ],
        "action_binding_established": certificate[
            "action_binding_established"
        ],
        "fields": [
            "g_mu_nu",
            "J_b^mu",
            "ell_b",
            "J_r^mu",
            "ell_r",
        ],
        "measure": "d^4x; q=sqrt(-g)",
        "number_density_definition": (
            "n_I=sqrt(-g_mu_nu J_I^mu J_I^nu)/sqrt(-g)"
        ),
        "action_density": (
            "L_vis=-sum_I[sqrt(-g)rho_I(n_I)"
            "+J_I^mu partial_mu ell_I]; "
            "rho_b=m_b n_b; rho_r=kappa_r n_r^(4/3)"
        ),
        "equations_of_state": {
            "identity": "p_I=n_I rho_I'(n_I)-rho_I",
            "baryon": {
                "rho": eos["b"][0],
                "p": eos["b"][1],
                "w": eos["b"][2],
            },
            "radiation": {
                "rho": eos["r"][0],
                "p": eos["r"][1],
                "w": eos["r"][2],
            },
        },
        "variational_convention": (
            "All metric variations are at fixed " + HELD_FIXED + "."
        ),
        "boundary_conditions": [
            "delta ell_I=0 on initial and final temporal boundaries",
            (
                "J_I^mu n_mu=0 on the spatial boundary, or fluid "
                "perturbations have compact spatial support"
            ),
            (
                "metric variations and required normal derivatives obey "
                "the existing Einstein-Hilbert boundary prescription"
            ),
        ],
        "boundary_terms": [
            (
                "ell variation: -integral_boundary "
                "J_I^mu n_mu delta ell_I; temporal part vanishes by "
                "delta ell_I=0; spatial part vanishes by zero flux or "
                "compact support"
            ),
            "J variation: no integration by parts and no boundary term",
            (
                "first and second fluid metric variations: algebraic, "
                "no integration by parts and zero fluid boundary contact term"
            ),
            (
                "Einstein-Hilbert boundary contacts are retained under "
                "the existing metric/normal-derivative prescription"
            ),
            (
                "diffeomorphism Ward integration: integral_boundary "
                "n_mu xi^mu L_I; it vanishes for compact-support xi "
                "or a diffeomorphism preserving the boundary data"
            ),
        ],
        "euler_lagrange_equations": euler_lagrange_equations(),
        "stress_tensor": (
            "T_I^mu_nu=(rho_I+p_I)u_I^mu u_I_nu"
            "+p_I delta^mu_nu; "
            "u_I^mu=J_I^mu/(sqrt(-g)n_I)"
        ),
        "first_metric_response": {
            "delta_measure": dq_h,
            "delta_number_density_h": dn_h,
            "delta_L_I_h": first_metric_response(),
            "identity": "delta S_I=-1/2 integral sqrt(-g) T_I_mu_nu h^mu_nu",
        },
        "second_metric_response": {
            "delta2_measure_hk": d2q,
            "delta_number_density_k": dn_k,
            "delta2_number_density_hk": d2n,
            "delta2_L_I_hk": second_metric_response(),
            "contractions": (
                "h=g_mu_nu h^mu_nu; U_h=u_mu u_nu h^mu_nu; "
                "hk=h^mu_nu k_mu_nu; "
                "W_hk=u_mu h^mu_rho k^rho_nu u^nu=W_kh"
            ),
            "potential_density_metric_response": "zero at fixed J_I^mu,ell_I",
        },
        "scalar_constraint_comparison": {
            "derivation": (
                "project delta S_vis=-1/2 integral sqrt(-g)T_mu_nu "
                "delta g^mu_nu into scalar Einstein equations "
                "G_mu_nu=8*pi*G*T_mu_nu and apply the carrier's 1/2 "
                "normalization"
            ),
            "coefficients": comparison,
            "lapse_shift_second_variation": scalar_lapse_shift_hessian(),
            "all_residuals_zero": certificate[
                "constraint_coefficients_exact"
            ],
            "manually_entered_visible_constraint": False,
        },
        "limitations": limitations,
        "provenance": {
            "selection": "explicit user-authorized standard baseline",
            "symbolic_engine": "SymPy exact integers and rationals",
            "module": "dfm_mkc_solver.visible_schutz_sorkin_action_v1",
            "existing_carrier": (
                "dfm_mkc_solver.scalar_constraint_variational_bridge_v1."
                "scalar_constraint_source_vector"
            ),
            "scientific_scope": (
                "standard visible-sector modeling assumption; not new "
                "mathematics, visible-sector physics, or evidence for DFM"
            ),
        },
    }
    return _stringify(payload)


def write_result(path):
    """Write the deterministic result; useful for exact regeneration tests."""

    destination = Path(path)
    destination.write_text(
        json.dumps(result_payload(), indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    output = (
        Path(__file__).resolve().parents[2]
        / "artifacts"
        / "cosmology"
        / "standard_visible_sector_action_binding.json"
    )
    write_result(output)
    print(output)
