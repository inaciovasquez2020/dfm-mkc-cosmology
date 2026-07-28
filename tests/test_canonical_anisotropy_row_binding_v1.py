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
        "canonical anisotropy-row binding exceeded 120 seconds"
    )


def test_canonical_anisotropy_row_binding():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(120)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES
        assert "psi" in complete.FIELD_ORDER
        assert "E" in complete.FIELD_ORDER

        z = total._symbols()

        q = dict(zip(total.VARIABLES, z["q"]))
        qp = dict(zip(total.VARIABLES, z["qp"]))
        qpp = {
            name: sp.Symbol(
                f"{name}_double_prime"
            )
            for name in total.VARIABLES
        }

        hessian = complete.euler_hessian()

        def raw_row(field):
            row = hessian[
                complete.FIELD_ORDER.index(field)
            ]

            return sp.Add(
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

        on_shell = total.on_shell_reduction()[
            "substitution"
        ]

        newtonian_gauge = {
            q["B"]: 0,
            qp["B"]: 0,
            qpp["B"]: 0,
            q["E"]: 0,
            qp["E"]: 0,
            qpp["E"]: 0,
        }

        psi_row = sp.expand(
            raw_row("psi").subs(
                on_shell,
                simultaneous=True,
            ).subs(
                newtonian_gauge,
                simultaneous=True,
            )
        )

        E_row = sp.expand(
            raw_row("E").subs(
                on_shell,
                simultaneous=True,
            ).subs(
                newtonian_gauge,
                simultaneous=True,
            )
        )

        canonical_anisotropy_row = sp.expand(
            E_row
            - z["k2"] * psi_row / 3
        )

        # In Newtonian gauge:
        # canonical psi is the Bardeen curvature potential Phi,
        # canonical A is the Bardeen lapse potential Psi.
        anisotropy_target = sp.expand(
            z["k2"] * (q["psi"] - q["A"])
        )

        expected_normalization = (
            -z["a"]**2
            * z["k2"]
            / (12 * sp.pi * z["G"])
        )

        proportionality_residual = sp.cancel(
            sp.expand(
                canonical_anisotropy_row
                - expected_normalization
                * anisotropy_target
            )
        )

        target_A_coefficient = sp.cancel(
            sp.diff(
                anisotropy_target,
                q["A"],
            )
        )

        row_A_coefficient = sp.cancel(
            sp.diff(
                canonical_anisotropy_row,
                q["A"],
            )
        )

        cross_multiplied_residual = sp.cancel(
            sp.expand(
                target_A_coefficient
                * canonical_anisotropy_row
                - row_A_coefficient
                * anisotropy_target
            )
        )

        print(
            "CANONICAL_ANISOTROPY_ROW := "
            "R_E - k2/3*R_psi"
        )
        print(
            "CANONICAL_ANISOTROPY_TARGET := "
            "k2*(psi-A)"
        )
        print(
            "ANISOTROPY_ROW_NORMALIZATION := "
            f"{expected_normalization}"
        )
        print(
            "ANISOTROPY_PROPORTIONALITY_RESIDUAL := "
            f"{proportionality_residual}"
        )
        print(
            "ANISOTROPY_CROSS_MULTIPLIED_RESIDUAL := "
            f"{cross_multiplied_residual}"
        )

        assert proportionality_residual == 0
        assert cross_multiplied_residual == 0

    finally:
        signal.alarm(0)
