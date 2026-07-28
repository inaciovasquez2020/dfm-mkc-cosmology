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
        "canonical delta_theta variational binding exceeded 120 seconds"
    )


def test_canonical_delta_theta_row_is_direct_original_action_variation():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(120)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES
        assert "delta_theta" in complete.FIELD_ORDER

        z = total._symbols()

        a = z["a"]
        k2 = z["k2"]

        alpha = z["alpha"]
        beta = z["beta"]
        rho_star = z["rho_star"]
        m2 = z["m2"]
        lam = z["lam"]

        ph = z["ph"]
        php = z["php"]
        thp = z["thp"]

        q = dict(zip(total.VARIABLES, z["q"]))
        qp = dict(zip(total.VARIABLES, z["qp"]))
        qpp = {
            name: sp.Symbol(
                f"{name}_double_prime"
            )
            for name in total.VARIABLES
        }

        t, s, c, sn = sp.symbols(
            "delta_theta_test_parameter "
            "delta_theta_general_parameter "
            "delta_theta_cosine "
            "delta_theta_sine"
        )

        u, up = sp.symbols(
            "delta_theta_test_amplitude "
            "delta_theta_test_amplitude_prime"
        )

        k = sp.sqrt(k2)

        A = s * q["A"]
        B = s * q["B"]
        psi = s * q["psi"]
        E = s * q["E"]

        delta_phi = s * q["delta_phi"]
        delta_phi_prime = s * qp["delta_phi"]

        delta_theta = (
            s * q["delta_theta"]
            + t * u
        )
        delta_theta_prime = (
            s * qp["delta_theta"]
            + t * up
        )

        f = 1 + (-2 * psi - 2 * k2 * E) * c
        g = 1 - 2 * psi * c

        N = a * (1 + A * c)
        N1 = -a**2 * k * B * sn

        phi = ph + delta_phi * c
        phi_t = php + delta_phi_prime * c
        theta_t = thp + delta_theta_prime * c

        phi_x = -k * delta_phi * sn
        theta_x = -k * delta_theta * sn

        N_up = N1 / (a**2 * f)

        invariant_phi_time = (
            phi_t - N_up * phi_x
        ) / N

        invariant_theta_time = (
            theta_t - N_up * theta_x
        ) / N

        potential = (
            rho_star
            + m2 * phi**2 / 2
            + lam * phi**4 / 4
        )

        measure = N * a**3 * sp.sqrt(f * g**2)

        original_dfm_action = measure * (
            alpha * invariant_phi_time**2 / 2
            - alpha * phi_x**2 / (2 * a**2 * f)
            + beta * phi**2 * invariant_theta_time**2 / 2
            - beta * phi**2 * theta_x**2 / (2 * a**2 * f)
            - potential
        )

        mixed_density = sp.expand(
            2
            * total._avg(
                sp.diff(
                    original_dfm_action,
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

        coefficient_u = sp.expand(
            sp.diff(mixed_density, u)
        )

        coefficient_up = sp.expand(
            sp.diff(mixed_density, up)
        )

        def D_linear(expression):
            derivative = total._D_eta(expression)

            for name in total.VARIABLES:
                q_derivative = total._D_eta(q[name])

                if q_derivative == 0:
                    derivative += (
                        sp.diff(expression, q[name])
                        * qp[name]
                    )
                else:
                    assert q_derivative == qp[name]

                qp_derivative = total._D_eta(qp[name])

                if qp_derivative == 0:
                    derivative += (
                        sp.diff(expression, qp[name])
                        * qpp[name]
                    )
                else:
                    assert qp_derivative == qpp[name]

            return sp.expand(derivative)

        independently_linearized_theta_euler = sp.expand(
            coefficient_u
            - D_linear(coefficient_up)
        )

        row = complete.euler_hessian()[
            complete.FIELD_ORDER.index("delta_theta")
        ]

        canonical_delta_theta_row = sp.expand(
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
            canonical_delta_theta_row
            - independently_linearized_theta_euler
        )

        atoms = (
            tuple(q[name] for name in total.VARIABLES)
            + tuple(qp[name] for name in total.VARIABLES)
            + tuple(qpp[name] for name in total.VARIABLES)
        )

        coefficient_residuals = {
            str(atom): sp.cancel(
                sp.diff(difference, atom)
            )
            for atom in atoms
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

        nonzero_coefficients = {
            name: residual
            for name, residual in coefficient_residuals.items()
            if residual != 0
        }

        print(
            "DELTA_THETA_VARIATIONAL_SOURCE := "
            "independent mixed variation of the unexpanded "
            "covariant DFM action"
        )
        print(
            "DELTA_THETA_ROW_NONZERO_COEFFICIENT_RESIDUALS := "
            f"{nonzero_coefficients}"
        )
        print(
            "DELTA_THETA_ROW_PARAMETER_FREE_RESIDUAL := "
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
