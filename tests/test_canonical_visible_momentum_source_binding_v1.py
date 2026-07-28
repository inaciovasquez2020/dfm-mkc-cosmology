import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


def _sector_row_expression(*, sector, row_index, q, qp, qpp):
    row = complete.sector_hessians()[sector][row_index]
    return sp.Add(
        *(
            operator.coefficient(0) * q[name]
            + operator.coefficient(1) * qp[name]
            + operator.coefficient(2) * qpp[name]
            for name, operator in zip(complete.FIELD_ORDER, row)
        )
    )


def test_visible_action_B_row_equals_declared_momentum_sources():
    assert complete.FIELD_ORDER == total.VARIABLES

    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))
    qpp = {
        name: sp.Symbol(f"{name}_double_prime")
        for name in total.VARIABLES
    }

    row_index = complete.FIELD_ORDER.index("B")
    shell = total.on_shell_reduction()["substitution"]

    gauge = {
        q["B"]: 0,
        qp["B"]: 0,
        qpp["B"]: 0,
        q["E"]: 0,
        qp["E"]: 0,
        qpp["E"]: 0,
    }

    baryon_row = sp.factor(
        _sector_row_expression(
            sector="b",
            row_index=row_index,
            q=q,
            qp=qp,
            qpp=qpp,
        )
        .subs(shell, simultaneous=True)
        .subs(gauge, simultaneous=True)
    )

    radiation_row = sp.factor(
        _sector_row_expression(
            sector="r",
            row_index=row_index,
            q=q,
            qp=qp,
            qpp=qpp,
        )
        .subs(shell, simultaneous=True)
        .subs(gauge, simultaneous=True)
    )

    normalization = z["a"]**2 / (4 * sp.pi * z["G"])
    einstein_source_factor = (
        normalization
        * 4
        * sp.pi
        * z["G"]
        * z["a"]**2
    )

    baryon_momentum_action = sp.factor(
        -baryon_row / einstein_source_factor
    )
    radiation_momentum_action = sp.factor(
        -radiation_row / einstein_source_factor
    )

    baryon_momentum_declared = sp.factor(
        -z["k2"]
        * z["mb"]
        * q["delta_J_b_L"]
        / z["a"]**3
    )

    radiation_momentum_declared = sp.factor(
        -sp.Rational(4, 3)
        * z["k2"]
        * z["kr"]
        * z["Jr"]**sp.Rational(1, 3)
        * q["delta_J_r_L"]
        / z["a"]**4
    )

    baryon_residual = sp.factor(
        baryon_momentum_action - baryon_momentum_declared
    )
    radiation_residual = sp.factor(
        radiation_momentum_action - radiation_momentum_declared
    )

    total_action = sp.factor(
        baryon_momentum_action + radiation_momentum_action
    )
    total_declared = sp.factor(
        baryon_momentum_declared + radiation_momentum_declared
    )
    total_residual = sp.factor(total_action - total_declared)

    print(
        "ACTION_DERIVED_BARYON_MOMENTUM := "
        f"{baryon_momentum_action}"
    )
    print(
        "DECLARED_BARYON_MOMENTUM := "
        f"{baryon_momentum_declared}"
    )
    print(
        "ACTION_DERIVED_RADIATION_MOMENTUM := "
        f"{radiation_momentum_action}"
    )
    print(
        "DECLARED_RADIATION_MOMENTUM := "
        f"{radiation_momentum_declared}"
    )
    print(f"BARYON_BINDING_RESIDUAL := {baryon_residual}")
    print(f"RADIATION_BINDING_RESIDUAL := {radiation_residual}")
    print(f"TOTAL_VISIBLE_MOMENTUM := {total_action}")
    print(f"TOTAL_VISIBLE_BINDING_RESIDUAL := {total_residual}")

    assert sp.simplify(baryon_residual) == 0
    assert sp.simplify(radiation_residual) == 0
    assert sp.simplify(total_residual) == 0
