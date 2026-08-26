from dfm_mkc_solver.scalar_prepared_canonical_energy_coercivity_probe_v1 import (
    scalar_prepared_canonical_energy_coercivity_probe,
)


def test_prepared_canonical_energy_full_sylvester_coercivity():
    certificate = scalar_prepared_canonical_energy_coercivity_probe()
    assert certificate["hessian_symmetric"] is True
    assert certificate["all_leading_minors_strictly_positive"] is True, (
        "FIRST_COERCIVITY_OBSTRUCTION",
        certificate["first_obstruction"],
        certificate["leading_minor_statuses"],
    )
    assert certificate["sylvester_coercivity_established"] is True
