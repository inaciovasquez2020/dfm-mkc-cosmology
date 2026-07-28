import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


def test_complete_canonical_B_row_equals_total_momentum_constraint():
    assert complete.FIELD_ORDER == total.VARIABLES

    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))
    qpp = {
        name: sp.Symbol(f"{name}_double_prime")
        for name in total.VARIABLES
    }

    row_index = complete.FIELD_ORDER.index("B")
    row = complete.euler_hessian()[row_index]

    canonical_row = sp.Add(
        *(
            operator.coefficient(0) * q[name]
            + operator.coefficient(1) * qp[name]
            + operator.coefficient(2) * qpp[name]
            for name, operator in zip(complete.FIELD_ORDER, row)
        )
    )

    canonical_row = sp.expand(
        canonical_row.subs(
            total.on_shell_reduction()["substitution"],
            simultaneous=True,
        )
    )

    canonical_row = sp.expand(
        canonical_row.subs(
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

    metric_kernel = z["k2"] * (
        qp["psi"] + z["H"] * q["A"]
    )

    dark_momentum = sp.factor(
        z["k2"]
        * (
            z["alpha"]
            * z["php"]
            * q["delta_phi"]
            + z["beta"]
            * z["ph"]**2
            * z["thp"]
            * q["delta_theta"]
        )
        / z["a"]**2
    )

    visible_momentum = sp.factor(
        -z["k2"]
        * (
            4
            * z["Jr"]**sp.Rational(1, 3)
            * q["delta_J_r_L"]
            * z["kr"]
            + 3
            * z["a"]
            * q["delta_J_b_L"]
            * z["mb"]
        )
        / (3 * z["a"]**4)
    )

    total_momentum = sp.factor(
        dark_momentum + visible_momentum
    )

    normalization = z["a"]**2 / (4 * sp.pi * z["G"])

    expected_row = sp.factor(
        normalization
        * (
            metric_kernel
            - 4
            * sp.pi
            * z["G"]
            * z["a"]**2
            * total_momentum
        )
    )

    residual = sp.factor(canonical_row - expected_row)

    print(f"CANONICAL_B_ROW := {canonical_row}")
    print(f"DECLARED_DARK_MOMENTUM := {dark_momentum}")
    print(f"DECLARED_VISIBLE_MOMENTUM := {visible_momentum}")
    print(f"DECLARED_TOTAL_MOMENTUM := {total_momentum}")
    print(f"TOTAL_MOMENTUM_BINDING_RESIDUAL := {residual}")

    assert sp.simplify(residual) == 0
