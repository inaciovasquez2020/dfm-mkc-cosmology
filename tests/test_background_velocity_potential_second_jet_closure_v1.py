import sympy as sp

from dfm_mkc_solver import (
    total_scalar_lapse_shift_hessian_v1 as total,
)


def test_background_velocity_potential_second_jet_closure():
    z = total._symbols()

    closure = (
        total.background_velocity_potential_second_jet_closure()
    )

    assert closure["pivots"] == (
        z["ellbpp"],
        z["ellrpp"],
    )

    assert set(closure["pivot_substitution"]) == {
        z["ellbpp"],
        z["ellrpp"],
    }

    assert sp.cancel(
        closure["pivot_substitution"][z["ellbpp"]]
        + z["H"] * z["a"] * z["mb"]
    ) == 0

    assert sp.cancel(
        closure["pivot_substitution"][z["ellrpp"]]
        + 4
        * z["Jrp"]
        * z["kr"]
        / (9 * z["Jr"]**sp.Rational(2, 3))
    ) == 0

    assert all(
        residual == 0
        for residual in closure[
            "substitution_back_residuals"
        ].values()
    )

    assert closure["domain_conditions"] == ()

    assert all(
        denominator == 1
        for denominator in closure[
            "denominators"
        ].values()
    )
