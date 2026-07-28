import signal

import sympy as sp

from dfm_mkc_solver import (
    complete_scalar_quadratic_action_v1 as complete,
)
from dfm_mkc_solver import (
    total_scalar_lapse_shift_hessian_v1 as total,
)


def _timeout_handler(_signum, _frame):
    raise TimeoutError(
        "canonical delta_J_b_0 variational binding exceeded 120 seconds"
    )


def test_canonical_delta_j_b_0_row_is_direct_original_action_variation():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(120)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES
        assert "delta_J_b_0" in complete.FIELD_ORDER

        z = total._symbols()

        a = z["a"]
        k2 = z["k2"]
        Jb = z["Jb"]
        mb = z["mb"]
        ellbp = z["ellbp"]

        q = dict(zip(total.VARIABLES, z["q"]))
        qp = dict(zip(total.VARIABLES, z["qp"]))
        qpp = {
            name: sp.Symbol(
                f"{name}_double_prime"
            )
            for name in total.VARIABLES
        }

        t, s, c, sn = sp.symbols(
            "delta_J_b_0_test_parameter "
            "delta_J_b_0_general_parameter "
            "delta_J_b_0_cosine "
            "delta_J_b_0_sine"
        )

        u = sp.Symbol(
            "delta_J_b_0_test_amplitude"
        )

        k = sp.sqrt(k2)

        A = s * q["A"]
        B = s * q["B"]
        psi = s * q["psi"]
        E = s * q["E"]

        delta_J_b_0 = (
            s * q["delta_J_b_0"]
            + t * u
        )
        delta_J_b_L = s * q["delta_J_b_L"]
        delta_ell_b = s * q["delta_ell_b"]
        delta_ell_b_prime = s * qp["delta_ell_b"]

        f = 1 + (-2 * psi - 2 * k2 * E) * c
        g = 1 - 2 * psi * c

        N = a * (1 + A * c)
        N1 = -a**2 * k * B * sn
        N_up = N1 / (a**2 * f)

        measure = N * a**3 * sp.sqrt(f * g**2)

        Jzero = Jb + delta_J_b_0 * c
        Jone = -k * delta_J_b_L * sn

        current_norm_squared = (
            N**2 * Jzero**2
            - a**2
            * f
            * (Jone + N_up * Jzero) ** 2
        )

        number_density = (
            sp.sqrt(current_norm_squared)
            / measure
        )

        original_baryon_action = (
            -measure * mb * number_density
            - Jzero
            * (
                ellbp
                + delta_ell_b_prime * c
            )
            - Jone
            * (
                -k * delta_ell_b * sn
            )
        )

        mixed_density = sp.expand(
            2
            * total._avg(
                sp.diff(
                    original_baryon_action,
                    t,
                    s,
                ).subs(
                    {
                        t: 0,
                        s: 0,
                    },
                    simultaneous=True,
                ),
                c,
                sn,
            )
        )

        independently_linearized_baryon_j0_euler = sp.expand(
            sp.diff(
                mixed_density,
                u,
            )
        )

        row = complete.euler_hessian()[
            complete.FIELD_ORDER.index(
                "delta_J_b_0"
            )
        ]

        canonical_delta_j_b_0_row = sp.expand(
            sp.Add(
                *(
                    operator.coefficient(0) * q[name]
                    + operator.coefficient(1) * qp[name]
                    + operator.coefficient(2) * qpp[name]
                    for name, operator in zip(
                        complete.FIELD_ORDER,
                        row,
                    )
                ),
                evaluate=False,
            )
        )

        difference = sp.expand(
            canonical_delta_j_b_0_row
            - independently_linearized_baryon_j0_euler
        )

        atoms = (
            tuple(
                q[name]
                for name in total.VARIABLES
            )
            + tuple(
                qp[name]
                for name in total.VARIABLES
            )
            + tuple(
                qpp[name]
                for name in total.VARIABLES
            )
        )

        coefficient_residuals = {
            str(atom): sp.cancel(
                sp.diff(
                    difference,
                    atom,
                )
            )
            for atom in atoms
        }

        nonzero_coefficients = {
            name: residual
            for name, residual
            in coefficient_residuals.items()
            if residual != 0
        }

        parameter_free_residual = sp.cancel(
            difference.subs(
                {
                    atom: 0
                    for atom in atoms
                },
                simultaneous=True,
            )
        )

        print(
            "DELTA_J_B_0_VARIATIONAL_SOURCE := "
            "independent mixed variation of the unexpanded "
            "pressureless Schutz-Sorkin baryon action"
        )
        print(
            "DELTA_J_B_0_ROW_NONZERO_COEFFICIENT_RESIDUALS := "
            f"{nonzero_coefficients}"
        )
        print(
            "DELTA_J_B_0_ROW_PARAMETER_FREE_RESIDUAL := "
            f"{parameter_free_residual}"
        )
        print(
            "BACKGROUND_ON_SHELL_REDUCTION_CALLED := false"
        )
        print(
            "QUADRATIC_DENSITY_USED_TO_CONSTRUCT_TARGET := false"
        )

        assert not nonzero_coefficients
        assert parameter_free_residual == 0

    finally:
        signal.alarm(0)
