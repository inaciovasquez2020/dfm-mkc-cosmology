"""Action-derived scalar lapse--shift Hessian for canonical DFM--MKC cosmology.

Only rows and columns containing the ADM lapse ``A`` or scalar shift ``B``
are claimed here.  The calculation uses a real cosine representative of one
nonzero Fourier pair and multiplies its spatial average by two, which is
equivalent to the usual ``k,-k`` pairing.  Fields and first conformal-time
derivatives are independent SymPy jets throughout.
"""

from __future__ import annotations

from functools import lru_cache
import importlib

import sympy as sp


VARIABLES = (
    "A", "B", "psi", "E", "delta_phi", "delta_theta",
    "delta_J_b_0", "delta_J_b_L", "delta_ell_b",
    "delta_J_r_0", "delta_J_r_L", "delta_ell_r",
)
JETS = VARIABLES + tuple(f"{x}_prime" for x in VARIABLES)


def _avg(expr, c, s):
    """Average a quadratic Fourier jet over space."""
    expr = sp.expand(expr)
    out = sp.Integer(0)
    for term in sp.Add.make_args(expr):
        powers = term.as_powers_dict()
        pc, ps = powers.get(c, 0), powers.get(s, 0)
        rest = term / c**pc / s**ps
        if pc == ps == 0:
            out += rest
        elif pc == 2 and ps == 0:
            out += rest / 2
        elif pc == 0 and ps == 2:
            out += rest / 2
        # all linear and c*s terms average to zero
    return sp.expand(out)


def _fourier_pair_quadratic_density(expr, eps, c, s):
    """Twice the averaged epsilon-squared coefficient for the real mode."""
    # Differentiation at epsilon=0 avoids expanding irrelevant higher orders
    # of rational ADM expressions.
    return sp.factor(_avg(sp.diff(expr, eps, 2).subs(eps, 0), c, s))


@lru_cache(maxsize=1)
def _symbols():
    a, H, k2, G, Lambda = sp.symbols(
        "a H k2 G Lambda", positive=True
    )
    alpha, beta = sp.symbols("alpha beta", positive=True)
    rho_star, m2, lam = sp.symbols("rho_star m_phi_squared lambda_phi")
    ph, th, php, thp, phpp, thpp = sp.symbols(
        "phi_bar theta_bar phi_bar_prime theta_bar_prime "
        "phi_bar_double_prime theta_bar_double_prime"
    )
    Hp, ap = sp.symbols("H_prime a_prime")
    Jb, Jr, mb, kr = sp.symbols(
        "Jbar_b_0 Jbar_r_0 m_b kappa_r", positive=True
    )
    Jbp, Jrp = sp.symbols("Jbar_b_0_prime Jbar_r_0_prime")
    ellbp, ellrp, ellbpp, ellrpp = sp.symbols(
        "ell_bar_b_prime ell_bar_r_prime "
        "ell_bar_b_double_prime ell_bar_r_double_prime"
    )
    names = VARIABLES
    q = sp.symbols(" ".join(names))
    qp = sp.symbols(" ".join(f"{x}_prime" for x in names))
    return locals()


@lru_cache(maxsize=1)
def _sector_quadratic_densities():
    """Return exact spatially averaged epsilon-squared sector densities."""
    z = _symbols()
    (a, H, k2, G, Lambda, alpha, beta, rho_star, m2, lam,
     ph, th, php, thp, Jb, Jr, mb, kr, ellbp, ellrp) = (
        z[n] for n in (
            "a", "H", "k2", "G", "Lambda", "alpha", "beta",
            "rho_star", "m2", "lam", "ph", "th", "php", "thp",
            "Jb", "Jr", "mb", "kr", "ellbp", "ellrp"
        )
    )
    q = dict(zip(VARIABLES, z["q"]))
    qp = dict(zip(VARIABLES, z["qp"]))
    eps, c, s = sp.symbols("epsilon cosine sine")
    k = sp.sqrt(k2)

    A, B, psi, E = (q[x] for x in ("A", "B", "psi", "E"))
    psip, Ep = (qp[x] for x in ("psi", "E"))
    f1 = -2 * psi - 2 * k2 * E
    f2 = -2 * psi
    f = 1 + eps * f1 * c
    g = 1 + eps * f2 * c
    fx, gx = -eps * k * f1 * s, -eps * k * f2 * s
    gxx = -eps * k2 * f2 * c
    N = a * (1 + eps * A * c)
    N1 = -a**2 * eps * k * B * s
    N1x = -a**2 * eps * k2 * B * c
    fdot = 2 * H * f + eps * (-2 * psip - 2 * k2 * Ep) * c
    gdot = 2 * H * g - 2 * eps * psip * c
    D1N1 = N1x - fx * N1 / (2 * f)
    D2N2 = gx * N1 / (2 * f)
    K1 = a**2 * (fdot - 2 * D1N1 / a**2) / (2 * N)
    K2 = a**2 * (gdot - 2 * D2N2 / a**2) / (2 * N)
    Ksq = (K1 / (a**2 * f)) ** 2 + 2 * (K2 / (a**2 * g)) ** 2
    Ktrace = K1 / (a**2 * f) + 2 * K2 / (a**2 * g)
    R3 = (-4*f*g*gxx + f*gx**2 + 2*g*fx*gx) / (
        2*a**2*f**2*g**2
    )
    measure = N * a**3 * sp.sqrt(f * g**2)
    leh = measure * (R3 + Ksq - Ktrace**2 - 2*Lambda) / (
        16 * sp.pi * G
    )

    dph, dth = q["delta_phi"], q["delta_theta"]
    dphp, dthp = qp["delta_phi"], qp["delta_theta"]
    phi = ph + eps*dph*c
    phi_t = php + eps*dphp*c
    theta_t = thp + eps*dthp*c
    phi_x, theta_x = -eps*k*dph*s, -eps*k*dth*s
    Nup = N1 / (a**2*f)
    inv_time_phi = (phi_t - Nup*phi_x) / N
    inv_time_theta = (theta_t - Nup*theta_x) / N
    grad_phi = phi_x**2 / (a**2*f)
    grad_theta = theta_x**2 / (a**2*f)
    U = rho_star + m2*phi**2/2 + lam*phi**4/4
    ldfm = measure * (
        alpha*inv_time_phi**2/2 - alpha*grad_phi/2
        + beta*phi**2*inv_time_theta**2/2
        - beta*phi**2*grad_theta/2 - U
    )

    def fluid(J0, exponent, coefficient, j0n, jln, elln, ellbar):
        j0, jl, de = q[j0n], q[jln], q[elln]
        dep = qp[elln]
        Jzero = J0 + eps*j0*c
        Jone = -eps*k*jl*s
        dens = N**2*Jzero**2 - a**2*f*(Jone + Nup*Jzero)**2
        number = sp.sqrt(dens) / measure
        rho = coefficient * number**exponent
        return -measure*rho - Jzero*(ellbar + eps*dep*c) - Jone*(-eps*k*de*s)

    lb = fluid(Jb, sp.Integer(1), mb, "delta_J_b_0",
               "delta_J_b_L", "delta_ell_b", ellbp)
    lr = fluid(Jr, sp.Rational(4, 3), kr, "delta_J_r_0",
               "delta_J_r_L", "delta_ell_r", ellrp)
    return {
        "eh_ghy": _fourier_pair_quadratic_density(leh, eps, c, s),
        "dfm": _fourier_pair_quadratic_density(ldfm, eps, c, s),
        "b": _fourier_pair_quadratic_density(lb, eps, c, s),
        "r": _fourier_pair_quadratic_density(lr, eps, c, s),
    }


@lru_cache(maxsize=1)
def _action_quadratic_density():
    """Return the exact total averaged coefficient of epsilon squared."""
    return sp.expand(sum(_sector_quadratic_densities().values(), sp.Integer(0)))


@lru_cache(maxsize=1)
def _original_sector_actions_two_parameter():
    """Unexpanded original actions carrying two independent variations.

    ``t`` carries independent lapse and shift test amplitudes and ``s``
    carries a general scalar variation.  No quadratic action or Hessian is
    used in constructing these expressions.
    """
    z = _symbols()
    (a, H, k2, G, Lambda, alpha, beta, rho_star, m2, lam,
     ph, th, php, thp, Jb, Jr, mb, kr, ellbp, ellrp) = (
        z[n] for n in (
            "a", "H", "k2", "G", "Lambda", "alpha", "beta",
            "rho_star", "m2", "lam", "ph", "th", "php", "thp",
            "Jb", "Jr", "mb", "kr", "ellbp", "ellrp"
        )
    )
    t, s, c, sn = sp.symbols(
        "original_parameter_t original_parameter_s "
        "original_cosine original_sine"
    )
    uA, uB = sp.symbols("original_u_A original_u_B")
    v = sp.symbols(" ".join(f"original_v_{name}" for name in VARIABLES))
    vp = sp.symbols(
        " ".join(f"original_v_{name}_prime" for name in VARIABLES)
    )
    amplitudes = {
        name: s*value + t*({"A": uA, "B": uB}.get(name, 0))
        for name, value in zip(VARIABLES, v)
    }
    derivatives = {
        name: s*value for name, value in zip(VARIABLES, vp)
    }
    k = sp.sqrt(k2)
    A, B, psi, E = (amplitudes[x] for x in ("A", "B", "psi", "E"))
    psip, Ep = (derivatives[x] for x in ("psi", "E"))
    f, g = 1+(-2*psi-2*k2*E)*c, 1-2*psi*c
    fx, gx, gxx = (
        k*(2*psi+2*k2*E)*sn, 2*k*psi*sn, 2*k2*psi*c
    )
    N, N1 = a*(1+A*c), -a**2*k*B*sn
    N1x = -a**2*k2*B*c
    fdot = 2*H*f+(-2*psip-2*k2*Ep)*c
    gdot = 2*H*g-2*psip*c
    D1N1, D2N2 = N1x-fx*N1/(2*f), gx*N1/(2*f)
    K1 = a**2*(fdot-2*D1N1/a**2)/(2*N)
    K2 = a**2*(gdot-2*D2N2/a**2)/(2*N)
    Ksq = (K1/(a**2*f))**2+2*(K2/(a**2*g))**2
    Ktrace = K1/(a**2*f)+2*K2/(a**2*g)
    R3 = (-4*f*g*gxx+f*gx**2+2*g*fx*gx)/(2*a**2*f**2*g**2)
    measure = N*a**3*sp.sqrt(f*g**2)
    eh = measure*(R3+Ksq-Ktrace**2-2*Lambda)/(16*sp.pi*G)

    dph, dth = amplitudes["delta_phi"], amplitudes["delta_theta"]
    dphp = derivatives["delta_phi"]
    dthp = derivatives["delta_theta"]
    phi, phi_t, theta_t = ph+dph*c, php+dphp*c, thp+dthp*c
    phi_x, theta_x = -k*dph*sn, -k*dth*sn
    Nup = N1/(a**2*f)
    itp = (phi_t-Nup*phi_x)/N
    itt = (theta_t-Nup*theta_x)/N
    U = rho_star+m2*phi**2/2+lam*phi**4/4
    dfm = measure*(
        alpha*itp**2/2-alpha*phi_x**2/(2*a**2*f)
        + beta*phi**2*itt**2/2-beta*phi**2*theta_x**2/(2*a**2*f)-U
    )

    def fluid(J0, exponent, coefficient, j0n, jln, elln, ellbar):
        j0, jl, de = (amplitudes[x] for x in (j0n, jln, elln))
        dep = derivatives[elln]
        Jzero, Jone = J0+j0*c, -k*jl*sn
        dens = N**2*Jzero**2-a**2*f*(Jone+Nup*Jzero)**2
        number = sp.sqrt(dens)/measure
        return (
            -measure*coefficient*number**exponent
            - Jzero*(ellbar+dep*c)-Jone*(-k*de*sn)
        )

    actions = {
        "eh_ghy": eh,
        "dfm": dfm,
        "b": fluid(Jb, sp.Integer(1), mb, "delta_J_b_0",
                   "delta_J_b_L", "delta_ell_b", ellbp),
        "r": fluid(Jr, sp.Rational(4, 3), kr, "delta_J_r_0",
                   "delta_J_r_L", "delta_ell_r", ellrp),
    }
    return {
        "actions": actions, "parameters": (t, s), "waves": (c, sn),
        "constraint_amplitudes": (uA, uB), "variations": v,
        "variation_derivatives": vp,
    }


def _euler_operator(L2, variable):
    z = _symbols()
    q = dict(zip(VARIABLES, z["q"]))
    qp = dict(zip(VARIABLES, z["qp"]))
    # A and B have no derivative jet, so their rows are ordinary variations.
    return sp.expand(sp.diff(L2, q[variable]))


def _linearized_row(variable):
    L2 = _action_quadratic_density()
    row = _euler_operator(L2, variable)
    z = _symbols()
    q = dict(zip(VARIABLES, z["q"]))
    qp = dict(zip(VARIABLES, z["qp"]))
    return {
        name: sp.simplify(sp.diff(row, q[name]))
        for name in VARIABLES
    } | {
        f"{name}_prime": sp.simplify(sp.diff(row, qp[name]))
        for name in VARIABLES
    }


def _D_eta(expr):
    """Exact conformal-time derivative on the declared background jet."""
    z = _symbols()
    derivative = {
        z["a"]: z["a"] * z["H"],
        z["H"]: z["Hp"],
        z["ph"]: z["php"],
        z["php"]: z["phpp"],
        z["th"]: z["thp"],
        z["thp"]: z["thpp"],
        z["Jb"]: z["Jbp"],
        z["Jr"]: z["Jrp"],
        z["ellbp"]: z["ellbpp"],
        z["ellrp"]: z["ellrpp"],
    }
    return sp.expand(sum(sp.diff(expr, x) * dx for x, dx in derivative.items()))


def _operator_rows():
    raw = {"A": _linearized_row("A"), "B": _linearized_row("B")}
    return {
        constraint: {
            name: (raw[constraint][name], raw[constraint][f"{name}_prime"])
            for name in VARIABLES
        }
        for constraint in ("A", "B")
    }


def _second_variation_columns():
    """Euler columns obtained independently by varying each field first."""
    z = _symbols()
    q = dict(zip(VARIABLES, z["q"]))
    qp = dict(zip(VARIABLES, z["qp"]))
    density = _action_quadratic_density()
    answer = {}
    for name in VARIABLES:
        momentum = sp.diff(density, qp[name])
        for constraint in ("A", "B"):
            c = sp.diff(momentum, q[constraint])
            answer[name, constraint] = (
                sp.simplify(
                    sp.diff(density, q[name], q[constraint]) - _D_eta(c)
                ),
                sp.simplify(-c),
            )
    return answer


def _imported_visible_blocks():
    mod = importlib.import_module(
        "dfm_mkc_solver.visible_sector_offshell_scalar_hessian_v1"
    )
    z = _symbols()
    return {
        "b": mod.scalar_flrw_hessian(exponent=sp.Integer(1), coefficient=z["mb"]),
        "r": mod.scalar_flrw_hessian(
            exponent=sp.Rational(4, 3), coefficient=z["kr"]
        ),
    }


def build_total_scalar_lapse_shift_hessian():
    """Return the complete two-row/two-column jet Hessian.

    Entries are coefficients in the action-derived A and B Euler rows.
    The visible 5x5 blocks are imported from the merged visible module and
    checked, rather than transcribed.
    """
    rows = _operator_rows()
    independent = _second_variation_columns()
    columns = {
        name: {constraint: independent[name, constraint]
               for constraint in ("A", "B")}
        for name in VARIABLES
    }
    return {
        "variables": VARIABLES,
        "jets": JETS,
        "rows": rows,
        "columns": columns,
        "visible_import_residual": visible_import_residual(),
        "quadratic_density": _action_quadratic_density(),
    }


def hamiltonian_constraint_row():
    """Original-sector lapse variation, before row assembly."""
    return _direct_constraint_rows_from_original_sectors()["A"]


def momentum_constraint_row():
    """Original-sector shift variation, before row assembly."""
    return _direct_constraint_rows_from_original_sectors()["B"]


@lru_cache(maxsize=1)
def _direct_constraint_rows_from_original_sectors():
    original = _original_sector_actions_two_parameter()
    t, s = original["parameters"]
    c, sn = original["waves"]
    action = sp.Add(*tuple(original["actions"].values()), evaluate=False)
    mixed = sp.factor(
        2*_avg(sp.diff(action, t, s).subs({t: 0, s: 0}), c, sn)
    )
    uA, uB = original["constraint_amplitudes"]
    v, vp = original["variations"], original["variation_derivatives"]
    result = {}
    for constraint, amplitude in (("A", uA), ("B", uB)):
        first_variation = sp.diff(mixed, amplitude)
        result[constraint] = {
            **{name: sp.simplify(sp.diff(first_variation, x))
               for name, x in zip(VARIABLES, v)},
            **{f"{name}_prime":
               sp.simplify(sp.diff(first_variation, x))
               for name, x in zip(VARIABLES, vp)},
        }
    return result


def hamiltonian_row_residual():
    assembled = _linearized_row("A")
    independently_varied = hamiltonian_constraint_row()
    return tuple(
        sp.simplify(independently_varied[name] - assembled[name])
        for name in JETS
    )


def momentum_row_residual():
    assembled = _linearized_row("B")
    independently_varied = momentum_constraint_row()
    return tuple(
        sp.simplify(independently_varied[name] - assembled[name])
        for name in JETS
    )


def visible_import_residual():
    """Exact equality certificate against the merged corrected visible blocks."""
    z = _symbols()
    imported = _imported_visible_blocks()
    q = dict(zip(VARIABLES, z["q"]))
    maps = {
        "b": ("delta_J_b_0", "delta_J_b_L", "delta_ell_b"),
        "r": ("delta_J_r_0", "delta_J_r_L", "delta_ell_r"),
    }
    residuals = []
    for sector, (j0, jl, ell) in maps.items():
        L2 = _sector_quadratic_densities()[sector]
        Jlocal = z["Jb"] if sector == "b" else z["Jr"]
        H = imported[sector].subs(
            {sp.Symbol("J0", positive=True): Jlocal}
        )
        names = ("A", "B", j0, jl)
        for i, left in enumerate(names):
            for j, right in enumerate(names):
                residuals.append(sp.simplify(
                    sp.diff(L2, q[left], q[right]) - H[i, j]
                ))
        d_eta = sp.Symbol("partial_eta", commutative=False)
        qp = dict(zip(VARIABLES, z["qp"]))
        local_j0_ell = sp.diff(L2, q[j0], qp[ell]) * d_eta
        local_ell_j0 = (
            -sp.diff(L2, qp[ell], q[j0]) * d_eta
            - _D_eta(sp.diff(L2, qp[ell], q[j0]))
        )
        local_jl_ell = sp.diff(L2, q[jl], q[ell])
        local_ell_jl = sp.diff(L2, q[ell], q[jl])
        residuals.extend((
            sp.simplify(local_j0_ell - H[2, 4]),
            sp.simplify(local_ell_j0 - H[4, 2]),
            sp.simplify(local_jl_ell - H[3, 4]),
            sp.simplify(local_ell_jl - H[4, 3]),
        ))
    return tuple(residuals)


def fourier_normalization_residual():
    """Ordinary pair-density derivatives equal the merged visible Hessians."""
    z = _symbols()
    q = dict(zip(VARIABLES, z["q"]))
    imported = _imported_visible_blocks()
    output = {}
    for sector, names, Jlocal in (
        ("b", ("A", "B", "delta_J_b_0", "delta_J_b_L"), z["Jb"]),
        ("r", ("A", "B", "delta_J_r_0", "delta_J_r_L"), z["Jr"]),
    ):
        target = imported[sector].subs(
            {sp.Symbol("J0", positive=True): Jlocal}
        )
        density = _sector_quadratic_densities()[sector]
        output[sector] = tuple(
            sp.simplify(sp.diff(density, q[u], q[v]) - target[i, j])
            for i, u in enumerate(names)
            for j, v in enumerate(names)
        )
    return output


def formal_adjoint_residual():
    """Independent Euler columns minus exact formal adjoints of the rows."""
    rows = _operator_rows()
    columns = _second_variation_columns()
    return {
        constraint: {
            name: (
                sp.simplify(
                    columns[name, constraint][0]
                    - (rows[constraint][name][0]
                       - _D_eta(rows[constraint][name][1]))
                ),
                sp.simplify(
                    columns[name, constraint][1]
                    + rows[constraint][name][1]
                ),
            )
            for name in VARIABLES
        }
        for constraint in ("A", "B")
    }


@lru_cache(maxsize=1)
def _full_matrix_adm_pair_density():
    """Independent 3x3 determinant/inverse/connection ADM+GHY calculation."""
    z = _symbols()
    a, H, k2, G, La = (z[x] for x in ("a", "H", "k2", "G", "Lambda"))
    q, qp = dict(zip(VARIABLES, z["q"])), dict(zip(VARIABLES, z["qp"]))
    eps, c, s = sp.symbols("epsilon_matrix cosine_matrix sine_matrix")
    k = sp.sqrt(k2)

    def dx(expr):
        return sp.diff(expr, c)*(-k*s) + sp.diff(expr, s)*(k*c)

    f = 1 + eps*(-2*q["psi"]-2*k2*q["E"])*c
    g = 1 - 2*eps*q["psi"]*c
    h = a**2*sp.diag(f, g, g)
    hinv = h.inv()
    det_h = h.det()
    lapse = a*(1+eps*q["A"]*c)
    shift = sp.Matrix([-a**2*eps*k*q["B"]*s, 0, 0])
    gamma = [[[sp.Integer(0) for _ in range(3)] for _ in range(3)]
             for _ in range(3)]
    for m in range(3):
        for i in range(3):
            for j in range(3):
                gamma[m][i][j] = sp.expand(sum(
                    hinv[m, n] * (
                        (dx(h[n, j]) if i == 0 else 0)
                        + (dx(h[n, i]) if j == 0 else 0)
                        - (dx(h[i, j]) if n == 0 else 0)
                    )/2 for n in range(3)
                ))
    ricci = sp.zeros(3)
    for i in range(3):
        for j in range(3):
            ricci[i, j] = sp.expand(sum(
                (dx(gamma[m][i][j]) if m == 0 else 0)
                - (dx(gamma[m][i][m]) if j == 0 else 0)
                + sum(gamma[m][m][n]*gamma[n][i][j]
                      - gamma[m][j][n]*gamma[n][i][m]
                      for n in range(3))
                for m in range(3)
            ))
    R3 = sp.expand(sum(hinv[i, j]*ricci[i, j]
                       for i in range(3) for j in range(3)))
    hdot = a**2*sp.diag(
        2*H*f + eps*(-2*qp["psi"]-2*k2*qp["E"])*c,
        2*H*g - 2*eps*qp["psi"]*c,
        2*H*g - 2*eps*qp["psi"]*c,
    )
    K = sp.zeros(3)
    for i in range(3):
        for j in range(3):
            DiNj = (dx(shift[j]) if i == 0 else 0) - sum(
                gamma[m][i][j]*shift[m] for m in range(3)
            )
            DjNi = (dx(shift[i]) if j == 0 else 0) - sum(
                gamma[m][j][i]*shift[m] for m in range(3)
            )
            K[i, j] = (hdot[i, j]-DiNj-DjNi)/(2*lapse)
    Kmixed = hinv*K
    Ktrace = sp.trace(Kmixed)
    Ksquare = sp.trace(Kmixed*Kmixed)
    density = (
        lapse*sp.sqrt(det_h)*(R3+Ksquare-Ktrace**2-2*La)
        /(16*sp.pi*G)
    )
    return _fourier_pair_quadratic_density(density, eps, c, s)


def full_matrix_adm_residual():
    """Full-matrix A/B rows minus the optimized diagonal representative."""
    z = _symbols()
    q, qp = dict(zip(VARIABLES, z["q"])), dict(zip(VARIABLES, z["qp"]))
    full = _full_matrix_adm_pair_density()
    optimized = _sector_quadratic_densities()["eh_ghy"]
    return {
        constraint: tuple(
            sp.simplify(
                sp.diff(full, q[constraint], variable)
                - sp.diff(optimized, q[constraint], variable)
            )
            for variable in q.values()
        ) + tuple(
            sp.simplify(
                sp.diff(full, q[constraint], variable)
                - sp.diff(optimized, q[constraint], variable)
            )
            for variable in qp.values()
        )
        for constraint in ("A", "B")
    }


def background_residuals():
    """Euler--Lagrange residuals of the homogeneous action, without EOM use."""
    z = _symbols()
    a, H, Hp, G, La = z["a"], z["H"], z["Hp"], z["G"], z["Lambda"]
    al, be, ph, php, phpp = (
        z["alpha"], z["beta"], z["ph"], z["php"], z["phpp"]
    )
    th, thp, thpp = z["th"], z["thp"], z["thpp"]
    Jb, Jr, Jbp, Jrp = z["Jb"], z["Jr"], z["Jbp"], z["Jrp"]
    n, adot = sp.symbols("background_lapse a_background_prime", positive=True)
    U = z["rho_star"] + z["m2"]*ph**2/2 + z["lam"]*ph**4/4
    nb, nr = Jb/a**3, Jr/a**3
    homogeneous = (
        -6*adot**2/(16*sp.pi*G*n)
        - 2*La*a**4*n/(16*sp.pi*G)
        + a**2*(al*php**2 + be*ph**2*thp**2)/(2*n)
        - a**4*n*U
        - a**4*n*(z["mb"]*nb + z["kr"]*nr**sp.Rational(4, 3))
        - Jb*z["ellbp"] - Jr*z["ellrp"]
    )
    lapse = sp.diff(homogeneous, n).subs({n: 1, adot: a*H})
    da = sp.diff(homogeneous, a)
    dap = sp.diff(homogeneous, adot)
    Ddap = (
        sp.diff(dap, a)*adot + sp.diff(dap, adot)*a*(H**2+Hp)
    )
    scale = (da-Ddap).subs({n: 1, adot: a*H})
    phi = (
        sp.diff(homogeneous, ph)
        - (
            sp.diff(sp.diff(homogeneous, php), a)*a*H
            + sp.diff(sp.diff(homogeneous, php), ph)*php
            + sp.diff(sp.diff(homogeneous, php), php)*phpp
        )
    ).subs(n, 1)
    theta = (
        sp.diff(homogeneous, th)
        - (
            sp.diff(sp.diff(homogeneous, thp), a)*a*H
            + sp.diff(sp.diff(homogeneous, thp), ph)*php
            + sp.diff(sp.diff(homogeneous, thp), thp)*thpp
        )
    ).subs(n, 1)
    return {
        "lapse_Friedmann": sp.factor(lapse),
        "spatial_trace": sp.factor(scale),
        "phi": sp.factor(phi),
        "theta": sp.factor(theta),
        "baryon_continuity": Jbp,
        "radiation_continuity": Jrp,
        "baryon_potential_flow": sp.factor(
            sp.diff(homogeneous, Jb).subs({n: 1, adot: a*H})
        ),
        "radiation_potential_flow": sp.factor(
            sp.diff(homogeneous, Jr).subs({n: 1, adot: a*H})
        ),
    }


@lru_cache(maxsize=1)
def background_on_shell_chart():
    """Solve the eight homogeneous residuals on one explicit regular chart."""
    z = _symbols()
    residuals = background_residuals()
    pivots = (
        z["Lambda"], z["Hp"], z["phpp"], z["thpp"],
        z["Jbp"], z["Jrp"], z["ellbp"], z["ellrp"],
    )
    equations = tuple(residuals)
    solved = sp.solve(
        [residuals[name] for name in equations], pivots,
        dict=True, simplify=False,
    )
    if len(solved) != 1 or set(solved[0]) != set(pivots):
        raise ValueError("homogeneous residuals do not define the stated chart")
    substitution = {pivot: sp.factor(solved[0][pivot]) for pivot in pivots}
    denominators = {
        str(pivot): sp.factor(sp.denom(sp.cancel(substitution[pivot])))
        for pivot in pivots
    }
    return {
        "pivot_substitution": substitution,
        "pivot_equations": dict(zip(pivots, equations)),
        "denominators": denominators,
        "chart_conditions": tuple(
            sp.Ne(value, 0, evaluate=False) for value in (
                z["a"], z["G"], z["alpha"], z["beta"], z["ph"],
                z["Jb"], z["Jr"],
            )
        ),
    }


@lru_cache(maxsize=1)
def background_residual_decomposition():
    """Derive the exact off-shell/on-shell split and residual coefficients."""
    residuals = background_residuals()
    chart = background_on_shell_chart()
    substitution = chart["pivot_substitution"]
    pivots = tuple(substitution)
    equation_names = tuple(chart["pivot_equations"][p] for p in pivots)
    residual_vector = sp.Matrix([residuals[name] for name in equation_names])
    # The homogeneous system is affine in the declared pivots.  Its exact
    # Jacobian maps pivot displacement from the solved chart to residuals.
    jacobian = residual_vector.jacobian(pivots)
    pivot_displacement = sp.Matrix([
        p-substitution[p] for p in pivots
    ])
    if any(sp.simplify(x) != 0 for x in
           residual_vector-jacobian*pivot_displacement):
        raise ValueError("background pivot system is not affine")

    off_shell = _operator_rows()
    on_shell = {
        constraint: {
            name: tuple(sp.factor(value.subs(substitution, simultaneous=True))
                        for value in pair)
            for name, pair in entries.items()
        }
        for constraint, entries in off_shell.items()
    }
    combinations, check = {}, {}
    for constraint in ("A", "B"):
        combinations[constraint], check[constraint] = {}, {}
        for name in VARIABLES:
            coefficient_pairs, remainder = [], []
            for part in (0, 1):
                difference = sp.expand(
                    off_shell[constraint][name][part]
                    - on_shell[constraint][name][part]
                )
                gradient = sp.Matrix([
                    sp.diff(difference, pivot) for pivot in pivots
                ])
                if any(pivot in value.free_symbols
                       for value in gradient for pivot in pivots):
                    raise ValueError("operator row is nonlinear in chart pivots")
                weights = jacobian.T.inv()*gradient
                coefficients = {
                    equation: sp.factor(weight)
                    for equation, weight in zip(equation_names, weights)
                }
                coefficient_pairs.append(coefficients)
                remainder.append(sp.simplify(
                    difference-sum(coefficients[equation]*residuals[equation]
                                   for equation in equation_names)
                ))
            combinations[constraint][name] = tuple(coefficient_pairs)
            check[constraint][name] = tuple(remainder)
    return {
        "off_shell": off_shell,
        "on_shell": on_shell,
        "pivot_substitution": substitution,
        "linear_combination": combinations,
        "residual": check,
        "chart_conditions": chart["chart_conditions"],
    }


def on_shell_reduction():
    decomposition = background_residual_decomposition()
    return {
        "substitution": decomposition["pivot_substitution"],
        "rows": decomposition["on_shell"],
    }


@lru_cache(maxsize=1)
def direct_mixed_differentiation_residual():
    """Original-sector mixed variation minus adjoint bulk plus boundary."""
    original = _original_sector_actions_two_parameter()
    t, s = original["parameters"]
    c, sn = original["waves"]
    action = sp.Add(*tuple(original["actions"].values()), evaluate=False)
    direct = sp.factor(
        2*_avg(sp.diff(action, t, s).subs({t: 0, s: 0}), c, sn)
    )
    v, vp = original["variations"], original["variation_derivatives"]
    uA, uB, uAp, uBp = sp.symbols("u_A u_B u_A_prime u_B_prime")
    original_uA, original_uB = original["constraint_amplitudes"]
    direct = direct.subs({original_uA: uA, original_uB: uB})
    rows = _operator_rows()
    bulk_plus_boundary = sp.Integer(0)
    for constraint, u, up in (("A", uA, uAp), ("B", uB, uBp)):
        for name, value, valuep in zip(VARIABLES, v, vp):
            c0, c1 = rows[constraint][name]
            adjoint_bulk = value*((c0-_D_eta(c1))*u-c1*up)
            boundary_derivative = (
                up*c1*value + u*_D_eta(c1)*value + u*c1*valuep
            )
            bulk_plus_boundary += adjoint_bulk + boundary_derivative
    return sp.simplify(direct - bulk_plus_boundary)


def certificate():
    L2 = _action_quadratic_density()
    z = _symbols()
    q, qp = dict(zip(VARIABLES, z["q"])), dict(zip(VARIABLES, z["qp"]))
    no_kinetic = all(
        sp.diff(L2, left, right) == 0
        for left in (qp["A"], qp["B"])
        for right in tuple(q.values()) + tuple(qp.values())
    )
    def exact_zero_family(value):
        if isinstance(value, dict):
            return all(exact_zero_family(x) for x in value.values())
        if isinstance(value, (tuple, list)):
            return all(exact_zero_family(x) for x in value)
        return sp.simplify(value) == 0

    decomposition = background_residual_decomposition()
    flags = {
        "full_adm_plus_ghy_expansion":
            exact_zero_family(full_matrix_adm_residual()),
        "visible_import_exact": exact_zero_family(visible_import_residual()),
        "fourier_normalization_exact":
            exact_zero_family(fourier_normalization_residual()),
        "hamiltonian_row_reconstructed":
            exact_zero_family(hamiltonian_row_residual()),
        "momentum_row_reconstructed":
            exact_zero_family(momentum_row_residual()),
        "lapse_shift_time_derivatives_absent": no_kinetic,
        "formal_adjoint_exchange_symmetry":
            exact_zero_family(formal_adjoint_residual()),
        "background_residual_decomposition":
            exact_zero_family(decomposition["residual"]),
        "direct_mixed_differentiation":
            exact_zero_family(direct_mixed_differentiation_residual()),
    }
    return {
        **flags,
        "all_independent_residual_families_zero": all(flags.values()),
        "direct_mixed_differentiation_residual":
            direct_mixed_differentiation_residual(),
        "boundary_terms": (
            "[u H_{A,q}v-u(H_{q,A})^*v]_{eta_i}^{eta_f}=0; "
            "[delta J_I^0 delta ell_I]_{eta_i}^{eta_f}=0"
        ),
        "claim_boundaries": {
            "reduced_physical_scalar_action": False,
            "weyl_observable_action_bound": False,
            "prediction_vector": False,
            "local_identifiability": False,
            "full_lcdm_manifold_separation": False,
            "measurable_margin": False,
            "novelty": False,
        },
    }
