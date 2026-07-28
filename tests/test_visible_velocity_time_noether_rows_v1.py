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
    "delta_J_b_0",
    "delta_J_r_0",
)


def _timeout_handler(_signum, _frame):
    raise TimeoutError(
        "corrected visible time-Noether check exceeded 60 seconds"
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


def test_visible_velocity_time_noether_rows_close_exactly():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(60)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES

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
            "visible_time_parameter "
            "visible_time_parameter_prime "
            "visible_time_parameter_double_prime "
            "visible_time_parameter_triple_prime"
        )

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

        def D_eta(expression):
            return sp.Add(
                total._D_eta(expression),
                sp.diff(expression, T) * Tp,
                sp.diff(expression, Tp) * Tpp,
                sp.diff(expression, Tpp) * Tppp,
                evaluate=False,
            )

        generator_jets = {
            field: (
                expression,
                D_eta(expression),
                D_eta(D_eta(expression)),
            )
            for field, expression in generator.items()
        }

        parameter_zero = {
            T: 0,
            Tp: 0,
            Tpp: 0,
            Tppp: 0,
        }

        raw_coefficients = {}

        for row_name in TARGET_ROWS:
            row = complete.euler_hessian()[
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

            raw_coefficients[row_name] = sp.cancel(
                sp.diff(residual, T).subs(
                    parameter_zero,
                    simultaneous=True,
                )
            )

        expected_coefficients = {
            "delta_J_b_0": (
                z["ellbpp"]
                + z["H"] * z["a"] * z["mb"]
            ),
            "delta_J_r_0": (
                z["ellrpp"]
                + 4
                * z["Jrp"]
                * z["kr"]
                / (9 * z["Jr"]**sp.Rational(2, 3))
            ),
        }

        identification_residuals = {
            row_name: sp.cancel(
                raw_coefficients[row_name]
                - expected_coefficients[row_name]
            )
            for row_name in TARGET_ROWS
        }

        closure = (
            total.background_velocity_potential_second_jet_closure()
        )["pivot_substitution"]

        closed_residuals = {
            row_name: sp.cancel(
                raw_coefficients[row_name].subs(
                    closure,
                    simultaneous=True,
                )
            )
            for row_name in TARGET_ROWS
        }

        print(
            "BARYON_RAW_TIME_NOETHER_COEFFICIENT := "
            f"{raw_coefficients['delta_J_b_0']}"
        )
        print(
            "RADIATION_RAW_TIME_NOETHER_COEFFICIENT := "
            f"{raw_coefficients['delta_J_r_0']}"
        )
        print(
            "IDENTIFICATION_RESIDUALS := "
            f"{identification_residuals}"
        )
        print(
            "CLOSED_VISIBLE_TIME_NOETHER_RESIDUALS := "
            f"{closed_residuals}"
        )

        assert all(
            residual == 0
            for residual in identification_residuals.values()
        )

        assert all(
            residual == 0
            for residual in closed_residuals.values()
        )

    finally:
        signal.alarm(0)
