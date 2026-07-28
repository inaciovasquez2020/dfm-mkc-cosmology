import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


def test_E_row_is_the_spatial_adjoint_noether_combination():
    assert complete.FIELD_ORDER == total.VARIABLES

    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))

    qpp = {
        name: sp.Symbol("{}_double_prime".format(name))
        for name in total.VARIABLES
    }
    qppp = {
        name: sp.Symbol("{}_triple_prime".format(name))
        for name in total.VARIABLES
    }

    def row_expression(field):
        row = complete.euler_hessian()[
            complete.FIELD_ORDER.index(field)
        ]
        return sp.Add(
            *(
                operator.coefficient(0) * q[name]
                + operator.coefficient(1) * qp[name]
                + operator.coefficient(2) * qpp[name]
                for name, operator
                in zip(complete.FIELD_ORDER, row)
            )
        )

    def D(expr):
        perturbation_derivative = sp.Add(
            *(
                sp.diff(expr, q[name]) * qp[name]
                + sp.diff(expr, qp[name]) * qpp[name]
                + sp.diff(expr, qpp[name]) * qppp[name]
                for name in total.VARIABLES
            )
        )

        return sp.expand(
            total._D_eta(expr)
            + perturbation_derivative
        )

    rows = {
        field: row_expression(field)
        for field in (
            "B",
            "E",
            "delta_J_b_0",
            "delta_J_b_L",
            "delta_J_r_0",
            "delta_J_r_L",
        )
    }

    adjoint_combination = sp.expand(
        D(rows["B"])
        + z["Jb"] * z["k2"] * rows["delta_J_b_0"]
        - D(z["Jb"] * rows["delta_J_b_L"])
        + z["Jr"] * z["k2"] * rows["delta_J_r_0"]
        - D(z["Jr"] * rows["delta_J_r_L"])
    )

    residual = sp.expand(
        rows["E"] - adjoint_combination
    )

    shell = dict(
        total.on_shell_reduction()["substitution"]
    )
    shell.update(
        total.background_current_differential_closure()[
            "pivot_substitution"
        ]
    )

    residual = sp.expand(
        residual.subs(shell, simultaneous=True)
    )
    residual = sp.expand(
        residual.subs(shell, simultaneous=True)
    )

    atoms = (
        tuple(q[name] for name in total.VARIABLES)
        + tuple(qp[name] for name in total.VARIABLES)
        + tuple(qpp[name] for name in total.VARIABLES)
        + tuple(qppp[name] for name in total.VARIABLES)
    )

    failures = []

    for atom in atoms:
        coefficient = sp.cancel(residual.coeff(atom))
        if coefficient != 0:
            failures.append((str(atom), coefficient))

    zero_map = {atom: 0 for atom in atoms}
    constant = sp.cancel(
        residual.subs(zero_map, simultaneous=True)
    )
    if constant != 0:
        failures.append(("constant", constant))

    print(
        "PERTURBATION_COEFFICIENTS_CHECKED := "
        f"{len(atoms) + 1}"
    )
    print(
        "NONZERO_ADJOINT_NOETHER_RESIDUALS := "
        f"{len(failures)}"
    )

    if failures:
        for atom, value in failures[:12]:
            print(
                "ADJOINT_NOETHER_RESIDUAL := "
                f"atom={atom}; residual={value}"
            )

    assert not failures, "\n".join(
        f"{atom}: {value}"
        for atom, value in failures
    )
