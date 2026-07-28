import signal

import sympy as sp

from dfm_mkc_solver import (
    complete_scalar_quadratic_action_v1 as complete,
)
from dfm_mkc_solver import (
    full_scalar_diffeomorphism_generator_v1 as gauge,
)
from dfm_mkc_solver import (
    total_scalar_lapse_shift_hessian_v1 as total,
)


TARGET_ROWS = (
    "psi",
    "E",
    "delta_phi",
    "delta_theta",
    "delta_J_b_0",
    "delta_J_r_0",
)


def _timeout_handler(_signum, _frame):
    raise TimeoutError(
        "established-row parameter-jet identities exceeded 120 seconds"
    )


def _collect_symbols(value, output):
    if isinstance(value, sp.Symbol):
        output.setdefault(str(value), value)
    elif isinstance(value, sp.Basic):
        for symbol in value.free_symbols:
            output.setdefault(str(symbol), symbol)
    elif isinstance(value, dict):
        for item in value.values():
            _collect_symbols(item, output)
    elif isinstance(value, (tuple, list)):
        for item in value:
            _collect_symbols(item, output)


def _unfactored_background_residuals(z):
    kinetic = (
        z["alpha"] * z["php"]**2
        + z["beta"] * z["ph"]**2 * z["thp"]**2
    )

    potential = (
        z["rho_star"]
        + z["m2"] * z["ph"]**2 / 2
        + z["lam"] * z["ph"]**4 / 4
    )

    lapse = sp.Add(
        3 * z["a"]**2 * z["H"]**2
        / (8 * sp.pi * z["G"]),
        -z["Lambda"] * z["a"]**4
        / (8 * sp.pi * z["G"]),
        -z["a"]**2 * kinetic / 2,
        -z["a"]**4 * potential,
        -z["a"] * z["mb"] * z["Jb"],
        -z["kr"] * z["Jr"]**sp.Rational(4, 3),
        evaluate=False,
    )

    spatial_trace = sp.Add(
        -z["Jb"] * z["mb"],
        -z["a"]**3 * z["lam"] * z["ph"]**4,
        -2 * z["a"]**3 * z["m2"] * z["ph"]**2,
        -4 * z["a"]**3 * z["rho_star"],
        z["a"] * kinetic,
        3 * z["H"]**2 * z["a"]
        / (4 * sp.pi * z["G"]),
        3 * z["Hp"] * z["a"]
        / (4 * sp.pi * z["G"]),
        -z["Lambda"] * z["a"]**3
        / (2 * sp.pi * z["G"]),
        evaluate=False,
    )

    phi = sp.Add(
        z["a"]**2
        * z["beta"]
        * z["ph"]
        * z["thp"]**2,
        -z["a"]**4
        * (
            z["m2"] * z["ph"]
            + z["lam"] * z["ph"]**3
        ),
        -2
        * z["H"]
        * z["a"]**2
        * z["alpha"]
        * z["php"],
        -z["a"]**2
        * z["alpha"]
        * z["phpp"],
        evaluate=False,
    )

    theta = sp.Add(
        -2
        * z["H"]
        * z["a"]**2
        * z["beta"]
        * z["ph"]**2
        * z["thp"],
        -2
        * z["a"]**2
        * z["beta"]
        * z["ph"]
        * z["php"]
        * z["thp"],
        -z["a"]**2
        * z["beta"]
        * z["ph"]**2
        * z["thpp"],
        evaluate=False,
    )

    return {
        "lapse_Friedmann": lapse,
        "spatial_trace": spatial_trace,
        "phi": phi,
        "theta": theta,
        "baryon_potential_flow": (
            -z["a"] * z["mb"] - z["ellbp"]
        ),
        "radiation_potential_flow": (
            -4
            * z["Jr"]**sp.Rational(1, 3)
            * z["kr"]
            / 3
            - z["ellrp"]
        ),
    }


def test_established_time_noether_parameter_jet_identities():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(120)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES
        assert all(
            row_name in complete.FIELD_ORDER
            for row_name in TARGET_ROWS
        )

        z = total._symbols()

        chart_symbols = {}
        _collect_symbols(z, chart_symbols)

        raw_generator = gauge.scalar_diffeomorphism_generator()

        raw_symbols = set().union(
            *(
                expression.free_symbols
                for expression in raw_generator.values()
            )
        )

        raw_by_name = {
            str(symbol): symbol
            for symbol in raw_symbols
        }

        for required_name in (
            "T",
            "T_prime",
            "L",
            "L_prime",
        ):
            assert required_name in raw_by_name

        T, Tp, Tpp, Tppp = sp.symbols(
            "established_time_parameter "
            "established_time_parameter_prime "
            "established_time_parameter_double_prime "
            "established_time_parameter_triple_prime"
        )

        Hpp, phppp, thppp = sp.symbols(
            "H_double_prime "
            "phi_bar_triple_prime "
            "theta_bar_triple_prime"
        )

        Jbppp, Jrppp = sp.symbols(
            "Jbar_b_0_triple_prime "
            "Jbar_r_0_triple_prime"
        )

        ellbppp, ellrppp = sp.symbols(
            "ell_bar_b_triple_prime "
            "ell_bar_r_triple_prime"
        )

        third_jet_map = {
            z["Hp"]: Hpp,
            z["phpp"]: phppp,
            z["thpp"]: thppp,
            z["Jbpp"]: Jbppp,
            z["Jrpp"]: Jrppp,
            z["ellbpp"]: ellbppp,
            z["ellrpp"]: ellrppp,
        }

        background_substitution = {
            symbol: chart_symbols[str(symbol)]
            for symbol in raw_symbols
            if str(symbol) in chart_symbols
        }

        parameter_substitution = {
            raw_by_name["T"]: T,
            raw_by_name["T_prime"]: Tp,
            raw_by_name["L"]: sp.Integer(0),
            raw_by_name["L_prime"]: sp.Integer(0),
        }

        generator = {
            field: expression.xreplace(
                background_substitution
            ).xreplace(
                parameter_substitution
            )
            for field, expression in raw_generator.items()
        }

        def D_extended(expression):
            return sp.Add(
                total._D_eta(expression),
                *(
                    sp.diff(expression, second_jet) * third_jet
                    for second_jet, third_jet
                    in third_jet_map.items()
                ),
                sp.diff(expression, T) * Tp,
                sp.diff(expression, Tp) * Tpp,
                sp.diff(expression, Tpp) * Tppp,
                evaluate=False,
            )

        generator_jets = {
            field: (
                expression,
                D_extended(expression),
                D_extended(D_extended(expression)),
            )
            for field, expression in generator.items()
        }

        parameter_zero = {
            T: 0,
            Tp: 0,
            Tpp: 0,
            Tppp: 0,
        }

        hessian = complete.euler_hessian()
        coefficients = {}

        for row_name in TARGET_ROWS:
            row = hessian[
                complete.FIELD_ORDER.index(row_name)
            ]

            residual = sp.Add(
                *(
                    operator.coefficient(0)
                    * generator_jets[column_name][0]
                    + operator.coefficient(1)
                    * generator_jets[column_name][1]
                    + operator.coefficient(2)
                    * generator_jets[column_name][2]
                    for column_name, operator in zip(
                        complete.FIELD_ORDER,
                        row,
                    )
                ),
                evaluate=False,
            )

            coefficients[row_name] = {
                "T_prime": sp.cancel(
                    sp.diff(residual, Tp).subs(
                        parameter_zero,
                        simultaneous=True,
                    )
                ),
                "T_double_prime": sp.cancel(
                    sp.diff(residual, Tpp).subs(
                        parameter_zero,
                        simultaneous=True,
                    )
                ),
                "T_triple_prime": sp.cancel(
                    sp.diff(residual, Tppp).subs(
                        parameter_zero,
                        simultaneous=True,
                    )
                ),
                "parameter_free": sp.cancel(
                    residual.subs(
                        parameter_zero,
                        simultaneous=True,
                    )
                ),
            }

        background = _unfactored_background_residuals(z)

        expected_T_prime = {
            "psi": (
                z["a"] * background["spatial_trace"]
                - background["lapse_Friedmann"]
            ),
            "E": (
                z["k2"]
                / 3
                * (
                    z["a"] * background["spatial_trace"]
                    - background["lapse_Friedmann"]
                )
            ),
            "delta_phi": -background["phi"],
            "delta_theta": -background["theta"],
            "delta_J_b_0": (
                -background["baryon_potential_flow"]
            ),
            "delta_J_r_0": (
                -background["radiation_potential_flow"]
            ),
        }

        identity_residuals = {
            row_name: sp.cancel(
                sp.expand(
                    coefficients[row_name]["T_prime"]
                    - expected_T_prime[row_name]
                )
            )
            for row_name in TARGET_ROWS
        }

        higher_jet_residuals = {
            row_name: {
                name: coefficients[row_name][name]
                for name in (
                    "T_double_prime",
                    "T_triple_prime",
                    "parameter_free",
                )
            }
            for row_name in TARGET_ROWS
        }

        print(
            "ESTABLISHED_ROW_T_PRIME_IDENTITIES := "
            "C_psi_Tp=a*E_spatial_trace-E_lapse; "
            "C_E_Tp=k2/3*C_psi_Tp; "
            "C_delta_phi_Tp=-E_phi; "
            "C_delta_theta_Tp=-E_theta; "
            "C_delta_J_b_0_Tp=-E_baryon_potential_flow; "
            "C_delta_J_r_0_Tp=-E_radiation_potential_flow"
        )
        print(
            "ESTABLISHED_ROW_T_PRIME_IDENTITY_RESIDUALS := "
            f"{identity_residuals}"
        )
        print(
            "ESTABLISHED_ROW_HIGHER_JET_RESIDUALS := "
            f"{higher_jet_residuals}"
        )
        print(
            "BACKGROUND_RESIDUALS_FUNCTION_CALLED := false"
        )

        assert all(
            residual == 0
            for residual in identity_residuals.values()
        )

        assert all(
            residual == 0
            for row in higher_jet_residuals.values()
            for residual in row.values()
        )

    finally:
        signal.alarm(0)
