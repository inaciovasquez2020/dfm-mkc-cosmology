"""Exact scalar diffeomorphism generator and its first-jet prolongation.

The convention is ``Delta(delta X)=-Lie_xi(X_bar)``, with
``xi^0=T``, ``xi^i=partial^i L`` and ``partial_i partial^i=-k2``.
All expressions are off shell.
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


VARIABLES = (
    "A", "B", "psi", "E", "delta_phi", "delta_theta",
    "delta_J_b_0", "delta_J_b_L", "delta_ell_b",
    "delta_J_r_0", "delta_J_r_L", "delta_ell_r",
)


@lru_cache(maxsize=1)
def _symbols():
    names = (
        "a H H_prime k2 T T_prime T_double_prime "
        "L L_prime L_double_prime "
        "phi_bar_prime phi_bar_double_prime "
        "theta_bar_prime theta_bar_double_prime "
        "Jbar_b_0 Jbar_b_0_prime Jbar_b_0_double_prime "
        "ell_bar_b_prime ell_bar_b_double_prime "
        "Jbar_r_0 Jbar_r_0_prime Jbar_r_0_double_prime "
        "ell_bar_r_prime ell_bar_r_double_prime"
    )
    values = sp.symbols(names)
    return dict(zip(names.split(), values))


def _zero(expr):
    return sp.simplify(sp.expand(expr))


def _metric_projection():
    """Project ``-Lie_xi gbar`` onto the declared ADM scalar amplitudes."""
    z = _symbols()
    a, H = z["a"], z["H"]
    T, Tp, L, Lp = z["T"], z["T_prime"], z["L"], z["L_prime"]

    # Coefficients after factoring the Fourier structures: 1 for 00,
    # partial_i for 0i, and (delta_ij, partial_i partial_j) for ij.
    minus_lie_00 = 2*a**2*(H*T + Tp)
    minus_lie_0i = a**2*(T - Lp)
    minus_lie_ij_trace = -2*a**2*H*T
    minus_lie_ij_longitudinal = -2*a**2*L
    return {
        "A": _zero(-minus_lie_00/(2*a**2)),
        "B": _zero(minus_lie_0i/a**2),
        "psi": _zero(-minus_lie_ij_trace/(2*a**2)),
        "E": _zero(minus_lie_ij_longitudinal/(2*a**2)),
    }


def _scalar_projection():
    """Apply ``-xi^mu partial_mu`` to homogeneous background scalars."""
    z = _symbols()
    T = z["T"]
    return {
        "delta_phi": -z["phi_bar_prime"]*T,
        "delta_theta": -z["theta_bar_prime"]*T,
        "delta_ell_b": -z["ell_bar_b_prime"]*T,
        "delta_ell_r": -z["ell_bar_r_prime"]*T,
    }


def _current_projection(J, Jp):
    """Project the negative weight-one vector-density Lie derivative."""
    z = _symbols()
    T, L, Lp, k2 = z["T"], z["L"], z["L_prime"], z["k2"]
    # (Lie J)^0=T J' + J partial_i partial^i L.
    temporal = -(T*Jp - J*k2*L)
    # -(Lie J)^i=J partial^i L'=partial^i(J L').
    longitudinal = J*Lp
    return temporal, longitudinal


def scalar_diffeomorphism_generator():
    """Return all twelve transformations in canonical order."""
    z = _symbols()
    metric = _metric_projection()
    scalars = _scalar_projection()
    jb0, jbL = _current_projection(z["Jbar_b_0"], z["Jbar_b_0_prime"])
    jr0, jrL = _current_projection(z["Jbar_r_0"], z["Jbar_r_0_prime"])
    derived = {
        **metric, **scalars,
        "delta_J_b_0": jb0, "delta_J_b_L": jbL,
        "delta_J_r_0": jr0, "delta_J_r_L": jrL,
    }
    return {name: derived[name] for name in VARIABLES}


def _total_conformal_time_derivative(expr):
    """One explicit total conformal-time derivative on the symbol algebra."""
    z = _symbols()
    derivative = {
        z["H"]: z["H_prime"],
        z["T"]: z["T_prime"],
        z["T_prime"]: z["T_double_prime"],
        z["L"]: z["L_prime"],
        z["L_prime"]: z["L_double_prime"],
        z["phi_bar_prime"]: z["phi_bar_double_prime"],
        z["theta_bar_prime"]: z["theta_bar_double_prime"],
        z["Jbar_b_0"]: z["Jbar_b_0_prime"],
        z["Jbar_b_0_prime"]: z["Jbar_b_0_double_prime"],
        z["ell_bar_b_prime"]: z["ell_bar_b_double_prime"],
        z["Jbar_r_0"]: z["Jbar_r_0_prime"],
        z["Jbar_r_0_prime"]: z["Jbar_r_0_double_prime"],
        z["ell_bar_r_prime"]: z["ell_bar_r_double_prime"],
    }
    return _zero(sum(sp.diff(expr, old)*new for old, new in derivative.items()))


def scalar_diffeomorphism_jet_generator():
    """First-jet prolongation, obtained only by the total derivative."""
    base = scalar_diffeomorphism_generator()
    return {
        f"{name}_prime": _total_conformal_time_derivative(base[name])
        for name in VARIABLES
    }


def _target_generator():
    z = _symbols()
    H, T, Tp = z["H"], z["T"], z["T_prime"]
    L, Lp, k2 = z["L"], z["L_prime"], z["k2"]
    Jb, Jbp = z["Jbar_b_0"], z["Jbar_b_0_prime"]
    Jr, Jrp = z["Jbar_r_0"], z["Jbar_r_0_prime"]
    entries = (
        -H*T-Tp, T-Lp, H*T, -L,
        -z["phi_bar_prime"]*T, -z["theta_bar_prime"]*T,
        -Jbp*T+Jb*k2*L, Jb*Lp, -z["ell_bar_b_prime"]*T,
        -Jrp*T+Jr*k2*L, Jr*Lp, -z["ell_bar_r_prime"]*T,
    )
    return dict(zip(VARIABLES, entries))


def metric_lie_derivative_residuals():
    target = _target_generator()
    return {name: _zero(value-target[name])
            for name, value in _metric_projection().items()}


def scalar_lie_derivative_residuals():
    target = _target_generator()
    return {name: _zero(value-target[name])
            for name, value in _scalar_projection().items()}


def current_density_lie_derivative_residuals():
    z, target = _symbols(), _target_generator()
    jb = _current_projection(z["Jbar_b_0"], z["Jbar_b_0_prime"])
    jr = _current_projection(z["Jbar_r_0"], z["Jbar_r_0_prime"])
    values = dict(zip(
        ("delta_J_b_0", "delta_J_b_L", "delta_J_r_0", "delta_J_r_L"),
        jb + jr,
    ))
    return {name: _zero(value-target[name]) for name, value in values.items()}


def target_generator_residuals():
    actual, target = scalar_diffeomorphism_generator(), _target_generator()
    return {name: _zero(actual[name]-target[name]) for name in VARIABLES}


def jet_prolongation_residuals():
    actual = scalar_diffeomorphism_jet_generator()
    target = _target_generator()
    return {f"{name}_prime": _zero(
        actual[f"{name}_prime"]-_total_conformal_time_derivative(target[name])
    ) for name in VARIABLES}


def bardeen_invariance_residuals():
    z = _symbols()
    g = scalar_diffeomorphism_generator()
    delta_sigma = _zero(g["B"]-scalar_diffeomorphism_jet_generator()["E_prime"])
    delta_sigma_prime = _total_conformal_time_derivative(delta_sigma)
    return {
        "sigma_minus_T": _zero(delta_sigma-z["T"]),
        "Phi_B": _zero(g["A"]+z["H"]*delta_sigma+delta_sigma_prime),
        "Psi_B": _zero(g["psi"]-z["H"]*delta_sigma),
    }


REDUCED_NEWTONIAN_STATE_ORDER = (
    "delta_phi",
    "delta_phi_prime",
    "delta_theta",
    "delta_theta_prime",
)


def residual_newtonian_gauge_triviality_residuals():
    """Prove that scalar diffeomorphisms preserving B=E=0 are trivial."""
    z = _symbols()
    generator = scalar_diffeomorphism_generator()
    jets = scalar_diffeomorphism_jet_generator()
    return {
        "E_shift_plus_L": _zero(generator["E"] + z["L"]),
        "E_prime_shift_plus_L_prime": _zero(
            jets["E_prime"] + z["L_prime"]
        ),
        "B_shift_after_L_zero_minus_T": _zero(
            generator["B"].subs(z["L_prime"], 0) - z["T"]
        ),
        "B_prime_shift_after_L_zero_minus_T_prime": _zero(
            jets["B_prime"].subs(z["L_double_prime"], 0)
            - z["T_prime"]
        ),
    }


def reduced_newtonian_state_shift_residuals():
    """Restrict the four evolved scalar shifts to residual Newtonian gauge."""
    z = _symbols()
    generator = scalar_diffeomorphism_generator()
    jets = scalar_diffeomorphism_jet_generator()
    residual_gauge = {
        z["L"]: 0,
        z["L_prime"]: 0,
        z["L_double_prime"]: 0,
        z["T"]: 0,
        z["T_prime"]: 0,
        z["T_double_prime"]: 0,
    }
    shifts = (
        generator["delta_phi"],
        jets["delta_phi_prime"],
        generator["delta_theta"],
        jets["delta_theta_prime"],
    )
    return {
        name: _zero(shift.subs(residual_gauge, simultaneous=True))
        for name, shift in zip(REDUCED_NEWTONIAN_STATE_ORDER, shifts)
    }


def reduced_newtonian_trajectory_equivariance_residuals():
    """Verify partial_N Phi + D Phi F = F o Phi for the reduced flow.

    Newtonian-gauge preservation forces the residual scalar-gauge action to
    be the identity. The equivariance residual therefore vanishes for every
    four-component vector field, including the reduced comparison flow.
    """
    state = sp.Matrix(sp.symbols("y0:4"))
    vector_field = sp.Matrix(sp.symbols("F0:4"))
    shift = sp.Matrix(
        tuple(reduced_newtonian_state_shift_residuals().values())
    )
    transformed_state = state + shift
    residual = _zero(
        transformed_state.jacobian(state) * vector_field - vector_field
    )
    return {
        name: _zero(residual[index])
        for index, name in enumerate(REDUCED_NEWTONIAN_STATE_ORDER)
    }


def certificate():
    families = {
        "metric_tensorial_lie_derivative":
            metric_lie_derivative_residuals(),
        "homogeneous_scalar_lie_derivatives":
            scalar_lie_derivative_residuals(),
        "weight_one_current_density_lie_derivative":
            current_density_lie_derivative_residuals(),
        "all_twelve_target_transformations": target_generator_residuals(),
        "first_jet_total_derivative_prolongation":
            jet_prolongation_residuals(),
        "bardeen_invariance": bardeen_invariance_residuals(),
    }
    flags = {
        name: all(_zero(value) == 0 for value in residuals.values())
        for name, residuals in families.items()
    }
    return {
        **flags,
        "full_scalar_diffeomorphism_generator_established": all(flags.values()),
        "singular_lapse_shift_branch_classified": False,
        "reduced_physical_scalar_action_established": False,
        "weyl_observable_action_bound": False,
        "prediction_vector_computed": False,
        "local_identifiability_established": False,
        "full_lcdm_manifold_separation_established": False,
        "measurable_margin_established": False,
    }
