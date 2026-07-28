import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


def test_canonical_A_row_has_exact_hamiltonian_source_decomposition():
    assert complete.FIELD_ORDER == total.VARIABLES

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

    newtonian_gauge = {
        q["B"]: 0,
        qp["B"]: 0,
        qpp["B"]: 0,
        q["E"]: 0,
        qp["E"]: 0,
        qpp["E"]: 0,
    }
    row_expression = sp.expand(
        row_expression.subs(newtonian_gauge, simultaneous=True)
    )

    hamiltonian_metric_kernel = (
        z["k2"] * q["psi"]
        + 3 * z["H"] * (
            qp["psi"] + z["H"] * q["A"]
        )
    )

    normalization = sp.factor(
        sp.diff(row_expression, qp["psi"])
        / (3 * z["H"])
    )
    expected_normalization = -z["a"]**2 / (4 * sp.pi * z["G"])

    assert sp.simplify(
        normalization - expected_normalization
    ) == 0

    source_remainder = sp.factor(
        row_expression
        - normalization * hamiltonian_metric_kernel
    )

    delta_rho_action = sp.factor(
        source_remainder
        / (
            normalization
            * 4
            * sp.pi
            * z["G"]
            * z["a"]**2
        )
    )

    reconstruction_residual = sp.factor(
        row_expression
        - normalization
        * (
            hamiltonian_metric_kernel
            + 4
            * sp.pi
            * z["G"]
            * z["a"]**2
            * delta_rho_action
        )
    )

    print(f"HAMILTONIAN_NORMALIZATION := {normalization}")
    print(f"ACTION_DERIVED_DELTA_RHO := {delta_rho_action}")
    print(
        "SOURCE_DECOMPOSITION_RESIDUAL := "
        f"{reconstruction_residual}"
    )

    assert sp.simplify(delta_rho_action) != 0
    assert sp.simplify(reconstruction_residual) == 0
