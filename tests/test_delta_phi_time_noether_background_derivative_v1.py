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


def _timeout_handler(_signum, _frame):
    raise TimeoutError(
        "delta_phi time-Noether derivative identity "
        "exceeded 90 seconds"
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


def test_delta_phi_time_noether_is_negative_phi_euler_derivative():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(90)

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

        T, Tp, Tpp, Tppp = sp.symbols(
            "phi_time_parameter "
            "phi_time_parameter_prime "
            "phi_time_parameter_double_prime "
            "phi_time_parameter_triple_prime"
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

        row = complete.euler_hessian()[
            complete.FIELD_ORDER.index("delta_phi")
        ]

        noether_expression = sp.Add(
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

        parameter_zero = {
            T: 0,
            Tp: 0,
            Tpp: 0,
            Tppp: 0,
        }

        noether_coefficient = sp.cancel(
            sp.diff(noether_expression, T).subs(
                parameter_zero,
                simultaneous=True,
            )
        )

        phi_background_residual = (
            total.background_residuals()["phi"]
        )

        phi_residual_derivative = sp.cancel(
            D_extended(phi_background_residual).subs(
                parameter_zero,
                simultaneous=True,
            )
        )

        identity_residual = sp.cancel(
            noether_coefficient
            + phi_residual_derivative
        )

        print(
            "DELTA_PHI_TIME_NOETHER_COEFFICIENT := "
            f"{noether_coefficient}"
        )
        print(
            "PHI_BACKGROUND_RESIDUAL_DERIVATIVE := "
            f"{phi_residual_derivative}"
        )
        print(
            "DELTA_PHI_DERIVATIVE_IDENTITY_RESIDUAL := "
            f"{identity_residual}"
        )

        assert identity_residual == 0

    finally:
        signal.alarm(0)
