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
        "E-row versus psi-row time-Noether relation "
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


def test_E_time_noether_coefficient_is_k2_over_three_times_psi():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(120)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES
        assert "psi" in complete.FIELD_ORDER
        assert "E" in complete.FIELD_ORDER

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
            "E_relation_time_parameter "
            "E_relation_time_parameter_prime "
            "E_relation_time_parameter_double_prime "
            "E_relation_time_parameter_triple_prime"
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

        def row_time_coefficient(row_name):
            row = complete.euler_hessian()[
                complete.FIELD_ORDER.index(row_name)
            ]

            expression = sp.Add(
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

            return sp.expand(
                sp.diff(expression, T).subs(
                    parameter_zero,
                    simultaneous=True,
                )
            )

        psi_coefficient = row_time_coefficient("psi")
        E_coefficient = row_time_coefficient("E")

        relation_residual = sp.cancel(
            sp.expand(
                E_coefficient
                - z["k2"] * psi_coefficient / 3
            )
        )

        print(
            "E_TIME_NOETHER_PSI_RELATION := "
            "C_E_T = k2/3*C_psi_T"
        )
        print(
            "E_TIME_NOETHER_PSI_RELATION_RESIDUAL := "
            f"{relation_residual}"
        )

        assert relation_residual == 0

    finally:
        signal.alarm(0)
