from dfm_mkc_solver.scalar_prepared_canonical_energy_coercivity_probe_v1 import (
    scalar_prepared_canonical_energy_coercivity_probe,
)


def test_prepared_canonical_energy_probe_fails_closed_at_first_unresolved_pivot():
    certificate = scalar_prepared_canonical_energy_coercivity_probe()
    assert certificate["hessian_symmetric"] is True
    assert certificate["all_leading_minors_strictly_positive"] is False
    assert certificate["sylvester_coercivity_established"] is False
    obstruction = certificate["first_obstruction"]
    assert obstruction is not None
    assert obstruction[0] == 2
    assert obstruction[1] == "unresolved"
    assert certificate["ldlt_pivot_statuses"] == ("positive", "unresolved")
