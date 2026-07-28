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
    "delta_J_b_L",
    "delta_ell_b",
    "delta_J_r_L",
    "delta_ell_r",
)


def _timeout_handler(_signum, _frame):
    raise TimeoutError(
        "visible complementary time-Noether identities "
        "exceeded 120 seconds"
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


def test_visible_complementary_time_noether_identities():
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
            "visible_complementary_time_parameter "
            "visible_complementary_time_parameter_prime "
            "visible_complementary_time_parameter_double_prime "
            "visible_complementary_time_parameter_triple_prime"
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

        def D_background(expression):
            return sp.Add(
                total._D_eta(expression),
                *(
                    sp.diff(expression, second_jet) * third_jet
                    for second_jet, third_jet
                    in third_jet_map.items()
                ),
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

        def row_parameter_coefficients(row_name):
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

            return {
                "T": sp.cancel(
                    sp.diff(residual, T).subs(
                        parameter_zero,
                        simultaneous=True,
                    )
                ),
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

        coefficients = {
            row_name: row_parameter_coefficients(row_name)
            for row_name in TARGET_ROWS
        }

        background = total.background_residuals()

        baryon_continuity = background["baryon_continuity"]
        radiation_continuity = background["radiation_continuity"]

        identity_residuals = {
            "delta_J_b_L_T": sp.cancel(
                coefficients["delta_J_b_L"]["T"]
                + z["k2"]
                * background["baryon_potential_flow"]
            ),
            "delta_J_r_L_T": sp.cancel(
                coefficients["delta_J_r_L"]["T"]
                + z["k2"]
                * background["radiation_potential_flow"]
            ),
            "delta_ell_b_T": sp.cancel(
                coefficients["delta_ell_b"]["T"]
                + D_background(baryon_continuity)
            ),
            "delta_ell_b_T_prime": sp.cancel(
                coefficients["delta_ell_b"]["T_prime"]
                + baryon_continuity
            ),
            "delta_ell_r_T": sp.cancel(
                coefficients["delta_ell_r"]["T"]
                + D_background(radiation_continuity)
            ),
            "delta_ell_r_T_prime": sp.cancel(
                coefficients["delta_ell_r"]["T_prime"]
                + radiation_continuity
            ),
        }

        unchecked_coefficients = (
            coefficients["delta_J_b_L"]["T_prime"],
            coefficients["delta_J_b_L"]["T_double_prime"],
            coefficients["delta_J_b_L"]["T_triple_prime"],
            coefficients["delta_J_b_L"]["parameter_free"],
            coefficients["delta_J_r_L"]["T_prime"],
            coefficients["delta_J_r_L"]["T_double_prime"],
            coefficients["delta_J_r_L"]["T_triple_prime"],
            coefficients["delta_J_r_L"]["parameter_free"],
            coefficients["delta_ell_b"]["T_double_prime"],
            coefficients["delta_ell_b"]["T_triple_prime"],
            coefficients["delta_ell_b"]["parameter_free"],
            coefficients["delta_ell_r"]["T_double_prime"],
            coefficients["delta_ell_r"]["T_triple_prime"],
            coefficients["delta_ell_r"]["parameter_free"],
        )

        print(
            "VISIBLE_COMPLEMENTARY_TIME_NOETHER_IDENTITIES := "
            "C_delta_J_b_L_T=-k2*E_baryon_potential_flow; "
            "C_delta_J_r_L_T=-k2*E_radiation_potential_flow; "
            "C_delta_ell_b_T=-D_eta(E_baryon_continuity); "
            "C_delta_ell_b_T_prime=-E_baryon_continuity; "
            "C_delta_ell_r_T=-D_eta(E_radiation_continuity); "
            "C_delta_ell_r_T_prime=-E_radiation_continuity"
        )
        print(
            "VISIBLE_COMPLEMENTARY_IDENTITY_RESIDUALS := "
            f"{identity_residuals}"
        )

        assert all(
            residual == 0
            for residual in identity_residuals.values()
        )

        assert all(
            coefficient == 0
            for coefficient in unchecked_coefficients
        )

    finally:
        signal.alarm(0)
