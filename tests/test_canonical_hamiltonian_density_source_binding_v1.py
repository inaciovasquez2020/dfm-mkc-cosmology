import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


def test_action_derived_density_equals_declared_dark_plus_visible_source():
    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))
    qpp = {
        name: sp.Symbol(f"{name}_double_prime")
        for name in total.VARIABLES
    }

    row_index = complete.FIELD_ORDER.index("A")
    row = complete.euler_hessian()[row_index]

    row_expression = sp.Add(
        *(
            operator.coefficient(0) * q[name]
            + operator.coefficient(1) * qp[name]
            + operator.coefficient(2) * qpp[name]
            for name, operator in zip(complete.FIELD_ORDER, row)
        )
    )

    row_expression = sp.expand(
        row_expression.subs(
            total.on_shell_reduction()["substitution"],
            simultaneous=True,
        )
    )

    row_expression = sp.expand(
        row_expression.subs(
            {
                q["B"]: 0,
                qp["B"]: 0,
                qpp["B"]: 0,
                q["E"]: 0,
                qp["E"]: 0,
                qpp["E"]: 0,
            },
            simultaneous=True,
        )
    )

    hamiltonian_metric_kernel = (
        z["k2"] * q["psi"]
        + 3 * z["H"] * (
            qp["psi"] + z["H"] * q["A"]
        )
    )

    normalization = -z["a"]**2 / (4 * sp.pi * z["G"])

    delta_rho_action = sp.factor(
        (
            row_expression
            - normalization * hamiltonian_metric_kernel
        )
        / (
            normalization
            * 4
            * sp.pi
            * z["G"]
            * z["a"]**2
        )
    )

    symbols = {
        str(symbol): symbol
        for symbol in delta_rho_action.free_symbols
    }

    def symbol(name):
        assert name in symbols, f"missing canonical symbol {name}"
        return symbols[name]

    a = symbol("a")
    A = symbol("A")
    psi = symbol("psi")
    alpha = symbol("alpha")
    beta = symbol("beta")
    phi = symbol("phi_bar")
    phi_prime = symbol("phi_bar_prime")
    theta_prime = symbol("theta_bar_prime")
    delta_phi = symbol("delta_phi")
    delta_phi_prime = symbol("delta_phi_prime")
    delta_theta_prime = symbol("delta_theta_prime")
    m_phi_squared = symbol("m_phi_squared")
    lambda_phi = symbol("lambda_phi")
    Jb = symbol("Jbar_b_0")
    Jr = symbol("Jbar_r_0")
    delta_Jb = symbol("delta_J_b_0")
    delta_Jr = symbol("delta_J_r_0")
    m_b = symbol("m_b")
    kappa_r = symbol("kappa_r")

    enthalpy_dark = (
        alpha * phi_prime**2
        + beta * phi**2 * theta_prime**2
    ) / a**2

    delta_rho_dark_zero_metric = (
        alpha * phi_prime * delta_phi_prime
        + beta * (
            phi**2 * theta_prime * delta_theta_prime
            + phi * theta_prime**2 * delta_phi
        )
    ) / a**2 + (
        m_phi_squared * phi
        + lambda_phi * phi**3
    ) * delta_phi

    delta_rho_dark = (
        delta_rho_dark_zero_metric
        - enthalpy_dark * A
    )

    delta_rho_visible = (
        m_b * delta_Jb / a**3
        + sp.Rational(4, 3)
        * kappa_r
        * Jr**sp.Rational(1, 3)
        * delta_Jr
        / a**4
        + 3 * Jb * m_b * psi / a**3
        + 4
        * kappa_r
        * Jr**sp.Rational(4, 3)
        * psi
        / a**4
    )

    declared_total = sp.factor(
        delta_rho_dark + delta_rho_visible
    )
    residual = sp.factor(
        delta_rho_action - declared_total
    )

    print(f"ACTION_DERIVED_DELTA_RHO := {delta_rho_action}")
    print(f"DECLARED_DARK_DELTA_RHO := {sp.factor(delta_rho_dark)}")
    print(
        "DECLARED_VISIBLE_DELTA_RHO := "
        f"{sp.factor(delta_rho_visible)}"
    )
    print(f"DENSITY_SOURCE_BINDING_RESIDUAL := {residual}")

    assert sp.simplify(residual) == 0
