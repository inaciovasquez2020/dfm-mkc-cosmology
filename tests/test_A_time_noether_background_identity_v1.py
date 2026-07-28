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
        "direct-lapse A-row time-Noether identity exceeded 90 seconds"
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


def _unfactored_lapse_background_residual(z):
    scalar_kinetic = (
        z["alpha"] * z["php"]**2
        + z["beta"] * z["ph"]**2 * z["thp"]**2
    )

    scalar_potential = (
        z["rho_star"]
        + z["m2"] * z["ph"]**2 / 2
        + z["lam"] * z["ph"]**4 / 4
    )

    return sp.Add(
        3 * z["a"]**2 * z["H"]**2
        / (8 * sp.pi * z["G"]),
        -z["Lambda"] * z["a"]**4
        / (8 * sp.pi * z["G"]),
        -z["a"]**2 * scalar_kinetic / 2,
        -z["a"]**4 * scalar_potential,
        -z["a"] * z["mb"] * z["Jb"],
        -z["kr"] * z["Jr"]**sp.Rational(4, 3),
        evaluate=False,
    )


def test_A_time_noether_background_identity():
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(90)

    try:
        assert complete.FIELD_ORDER == total.VARIABLES
        assert "A" in complete.FIELD_ORDER

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
            "A_time_parameter "
            "A_time_parameter_prime "
            "A_time_parameter_double_prime "
            "A_time_parameter_triple_prime"
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

        row = complete.euler_hessian()[
            complete.FIELD_ORDER.index("A")
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

        parameter_zero = {
            T: 0,
            Tp: 0,
            Tpp: 0,
            Tppp: 0,
        }

        coefficients = {
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

        lapse = _unfactored_lapse_background_residual(z)

        expected_T = sp.Add(
            -D_background(lapse),
            z["H"] * lapse,
            evaluate=False,
        )

        identity_residual = sp.cancel(
            sp.expand(coefficients["T"] - expected_T)
        )

        higher_parameter_residuals = {
            name: coefficients[name]
            for name in (
                "T_prime",
                "T_double_prime",
                "T_triple_prime",
                "parameter_free",
            )
        }

        print(
            "A_TIME_NOETHER_IDENTITY := "
            "C_A_T = -D_eta(E_lapse_Friedmann) "
            "+ H*E_lapse_Friedmann"
        )
        print(
            "A_TIME_NOETHER_IDENTITY_RESIDUAL := "
            f"{identity_residual}"
        )
        print(
            "A_HIGHER_PARAMETER_JET_RESIDUALS := "
            f"{higher_parameter_residuals}"
        )
        print(
            "BACKGROUND_RESIDUALS_FUNCTION_CALLED := false"
        )

        assert identity_residual == 0

        assert all(
            value == 0
            for value in higher_parameter_residuals.values()
        )

    finally:
        signal.alarm(0)
