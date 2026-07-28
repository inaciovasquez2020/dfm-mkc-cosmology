import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


def test_full_canonical_hessian_annihilates_spatial_gauge_generator():
    assert complete.FIELD_ORDER == total.VARIABLES

    z = total._symbols()

    L, Lp, Lpp, Lppp = sp.symbols(
        "spatial_L spatial_L_prime "
        "spatial_L_double_prime spatial_L_triple_prime"
    )

    derivative_map = {
        L: Lp,
        Lp: Lpp,
        Lpp: Lppp,
        z["Jb"]: z["Jbp"],
        z["Jbp"]: z["Jbpp"],
        z["Jr"]: z["Jrp"],
        z["Jrp"]: z["Jrpp"],
    }

    def D(expr):
        return sp.expand(
            sum(
                sp.diff(expr, symbol) * derivative
                for symbol, derivative in derivative_map.items()
            )
        )

    generator = {
        "A": sp.Integer(0),
        "B": -Lp,
        "psi": sp.Integer(0),
        "E": -L,
        "delta_phi": sp.Integer(0),
        "delta_theta": sp.Integer(0),
        "delta_J_b_0": z["Jb"] * z["k2"] * L,
        "delta_J_b_L": z["Jb"] * Lp,
        "delta_ell_b": sp.Integer(0),
        "delta_J_r_0": z["Jr"] * z["k2"] * L,
        "delta_J_r_L": z["Jr"] * Lp,
        "delta_ell_r": sp.Integer(0),
    }

    generator_jets = {
        name: (value, D(value), D(D(value)))
        for name, value in generator.items()
    }

    shell = dict(total.on_shell_reduction()["substitution"])
    differential_closure = (
        total.background_current_differential_closure()
    )
    shell.update(differential_closure["pivot_substitution"])

    hessian = complete.euler_hessian()
    gauge_atoms = (L, Lp, Lpp, Lppp)

    failures = []

    for row_name, row in zip(complete.FIELD_ORDER, hessian):
        residual = sp.Add(
            *(
                operator.coefficient(0)
                * generator_jets[column_name][0]
                + operator.coefficient(1)
                * generator_jets[column_name][1]
                + operator.coefficient(2)
                * generator_jets[column_name][2]
                for column_name, operator
                in zip(complete.FIELD_ORDER, row)
            )
        )

        residual = sp.expand(
            residual.subs(shell, simultaneous=True)
        )
        residual = sp.expand(
            residual.subs(shell, simultaneous=True)
        )

        for atom in gauge_atoms:
            coefficient = sp.cancel(residual.coeff(atom))
            if coefficient != 0:
                failures.append(
                    (row_name, str(atom), coefficient)
                )

        constant = sp.cancel(
            residual.subs(
                {atom: 0 for atom in gauge_atoms},
                simultaneous=True,
            )
        )
        if constant != 0:
            failures.append(
                (row_name, "constant", constant)
            )

    print(f"CANONICAL_ROWS_CHECKED := {len(complete.FIELD_ORDER)}")
    print(f"SPATIAL_GAUGE_JETS_CHECKED := {len(gauge_atoms)}")
    print(f"NONZERO_NOETHER_RESIDUALS := {len(failures)}")

    if failures:
        for row_name, atom, residual in failures[:12]:
            print(
                "NOETHER_RESIDUAL := "
                f"row={row_name}; atom={atom}; residual={residual}"
            )

    assert not failures, "\n".join(
        f"{row_name}/{atom}: {residual}"
        for row_name, atom, residual in failures
    )
