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
        "canonical psi variational binding exceeded 180 seconds"
    )


def test_canonical_psi_row_is_direct_complete_original_action_variation():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(180)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES
        assert "psi" in complete.FIELD_ORDER

        z = total._symbols()

        (
            a,
            H,
            k2,
            G,
            Lambda,
            alpha,
            beta,
            rho_star,
            m2,
            lam,
            ph,
            th,
            php,
            thp,
            Jb,
            Jr,
            mb,
            kr,
            ellbp,
            ellrp,
        ) = (
            z[name]
            for name in (
                "a",
                "H",
                "k2",
                "G",
                "Lambda",
                "alpha",
                "beta",
                "rho_star",
                "m2",
                "lam",
                "ph",
                "th",
                "php",
                "thp",
                "Jb",
                "Jr",
                "mb",
                "kr",
                "ellbp",
                "ellrp",
            )
        )

        q = dict(zip(total.VARIABLES, z["q"]))
        qp = dict(zip(total.VARIABLES, z["qp"]))
        qpp = {
            name: sp.Symbol(
                f"{name}_double_prime"
            )
            for name in total.VARIABLES
        }

        t, s, c, sn = sp.symbols(
            "psi_test_parameter "
            "psi_general_parameter "
            "psi_cosine "
            "psi_sine"
        )

        u, up = sp.symbols(
            "psi_test_amplitude "
            "psi_test_amplitude_prime"
        )

        amplitudes = {
            name: (
                s * q[name]
                + (
                    t * u
                    if name == "psi"
                    else 0
                )
            )
            for name in total.VARIABLES
        }

        derivatives = {
            name: (
                s * qp[name]
                + (
                    t * up
                    if name == "psi"
                    else 0
                )
            )
            for name in total.VARIABLES
        }

        k = sp.sqrt(k2)

        A, B, psi, E = (
            amplitudes[name]
            for name in (
                "A",
                "B",
                "psi",
                "E",
            )
        )

        psip = derivatives["psi"]
        Ep = derivatives["E"]

        f = 1 + (
            -2 * psi
            - 2 * k2 * E
        ) * c
        g = 1 - 2 * psi * c

        fx = (
            k
            * (
                2 * psi
                + 2 * k2 * E
            )
            * sn
        )
        gx = 2 * k * psi * sn
        gxx = 2 * k2 * psi * c

        N = a * (1 + A * c)
        N1 = -a**2 * k * B * sn
        N1x = -a**2 * k2 * B * c

        fdot = (
            2 * H * f
            + (
                -2 * psip
                - 2 * k2 * Ep
            )
            * c
        )
        gdot = (
            2 * H * g
            - 2 * psip * c
        )

        D1N1 = (
            N1x
            - fx * N1 / (2 * f)
        )
        D2N2 = gx * N1 / (2 * f)

        K1 = (
            a**2
            * (
                fdot
                - 2 * D1N1 / a**2
            )
            / (2 * N)
        )
        K2 = (
            a**2
            * (
                gdot
                - 2 * D2N2 / a**2
            )
            / (2 * N)
        )

        Ksq = (
            (K1 / (a**2 * f)) ** 2
            + 2 * (K2 / (a**2 * g)) ** 2
        )
        Ktrace = (
            K1 / (a**2 * f)
            + 2 * K2 / (a**2 * g)
        )

        R3 = (
            -4 * f * g * gxx
            + f * gx**2
            + 2 * g * fx * gx
        ) / (
            2
            * a**2
            * f**2
            * g**2
        )

        measure = (
            N
            * a**3
            * sp.sqrt(f * g**2)
        )

        original_eh_ghy_action = (
            measure
            * (
                R3
                + Ksq
                - Ktrace**2
                - 2 * Lambda
            )
            / (16 * sp.pi * G)
        )

        delta_phi = amplitudes["delta_phi"]
        delta_theta = amplitudes["delta_theta"]
        delta_phi_prime = derivatives["delta_phi"]
        delta_theta_prime = derivatives["delta_theta"]

        phi = ph + delta_phi * c
        phi_t = php + delta_phi_prime * c
        theta_t = thp + delta_theta_prime * c

        phi_x = -k * delta_phi * sn
        theta_x = -k * delta_theta * sn

        N_up = N1 / (a**2 * f)

        invariant_phi_time = (
            phi_t
            - N_up * phi_x
        ) / N

        invariant_theta_time = (
            theta_t
            - N_up * theta_x
        ) / N

        potential = (
            rho_star
            + m2 * phi**2 / 2
            + lam * phi**4 / 4
        )

        original_dfm_action = measure * (
            alpha * invariant_phi_time**2 / 2
            - alpha * phi_x**2 / (2 * a**2 * f)
            + beta * phi**2 * invariant_theta_time**2 / 2
            - beta * phi**2 * theta_x**2 / (2 * a**2 * f)
            - potential
        )

        def original_fluid_action(
            *,
            background_current,
            exponent,
            coefficient,
            current_zero_name,
            current_longitudinal_name,
            potential_name,
            background_potential_prime,
        ):
            current_zero = (
                background_current
                + amplitudes[current_zero_name] * c
            )
            current_one = (
                -k
                * amplitudes[current_longitudinal_name]
                * sn
            )

            current_norm_squared = (
                N**2 * current_zero**2
                - a**2
                * f
                * (
                    current_one
                    + N_up * current_zero
                ) ** 2
            )

            number_density = (
                sp.sqrt(current_norm_squared)
                / measure
            )

            return (
                -measure
                * coefficient
                * number_density**exponent
                - current_zero
                * (
                    background_potential_prime
                    + derivatives[potential_name] * c
                )
                - current_one
                * (
                    -k
                    * amplitudes[potential_name]
                    * sn
                )
            )

        original_baryon_action = original_fluid_action(
            background_current=Jb,
            exponent=sp.Integer(1),
            coefficient=mb,
            current_zero_name="delta_J_b_0",
            current_longitudinal_name="delta_J_b_L",
            potential_name="delta_ell_b",
            background_potential_prime=ellbp,
        )

        original_radiation_action = original_fluid_action(
            background_current=Jr,
            exponent=sp.Rational(4, 3),
            coefficient=kr,
            current_zero_name="delta_J_r_0",
            current_longitudinal_name="delta_J_r_L",
            potential_name="delta_ell_r",
            background_potential_prime=ellrp,
        )

        complete_original_action = sp.Add(
            original_eh_ghy_action,
            original_dfm_action,
            original_baryon_action,
            original_radiation_action,
            evaluate=False,
        )

        mixed_density = sp.factor(
            2
            * total._avg(
                sp.diff(
                    complete_original_action,
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
            sp.diff(
                mixed_density,
                u,
            )
        )

        coefficient_up = sp.expand(
            sp.diff(
                mixed_density,
                up,
            )
        )

        def D_linear(expression):
            derivative = total._D_eta(expression)

            for name in total.VARIABLES:
                q_derivative = total._D_eta(q[name])

                if q_derivative == 0:
                    derivative += (
                        sp.diff(
                            expression,
                            q[name],
                        )
                        * qp[name]
                    )
                else:
                    assert q_derivative == qp[name]

                qp_derivative = total._D_eta(qp[name])

                if qp_derivative == 0:
                    derivative += (
                        sp.diff(
                            expression,
                            qp[name],
                        )
                        * qpp[name]
                    )
                else:
                    assert qp_derivative == qpp[name]

            return sp.expand(derivative)

        independently_linearized_spatial_trace = sp.expand(
            coefficient_u
            - D_linear(coefficient_up)
        )

        row = complete.euler_hessian()[
            complete.FIELD_ORDER.index("psi")
        ]

        canonical_psi_row = sp.expand(
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
            canonical_psi_row
            - independently_linearized_spatial_trace
        )

        atoms = (
            tuple(q[name] for name in total.VARIABLES)
            + tuple(qp[name] for name in total.VARIABLES)
            + tuple(qpp[name] for name in total.VARIABLES)
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
            "PSI_VARIATIONAL_SOURCE := "
            "independent mixed variation of the complete "
            "unexpanded four-sector original action"
        )
        print(
            "PSI_VARIATIONAL_SECTORS := "
            "eh_ghy dfm baryon radiation"
        )
        print(
            "PSI_ROW_NONZERO_COEFFICIENT_RESIDUALS := "
            f"{nonzero_coefficients}"
        )
        print(
            "PSI_ROW_PARAMETER_FREE_RESIDUAL := "
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
