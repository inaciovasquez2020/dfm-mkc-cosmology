from types import MappingProxyType

from dfm_mkc_solver.scalar_prepared_canonical_energy_v1 import (
    PHYSICAL_FIELDS,
    scalar_prepared_canonical_energy_data,
    scalar_prepared_canonical_energy_theorem,
)


def test_prepared_canonical_second_variation_energy_is_exactly_legendre_derived():
    data = scalar_prepared_canonical_energy_data()
    theorem = scalar_prepared_canonical_energy_theorem()

    assert isinstance(data, MappingProxyType)
    assert data["physical_fields"] == PHYSICAL_FIELDS
    assert data["legendre_identity_residual"] == 0
    assert data["energy_zero_state_residual"] == 0
    assert data["energy_split_residual"] == 0
    assert data["action_derived"] is True
    assert data["auxiliaries_exactly_eliminated"] is True
    assert theorem["canonical_scalar_second_variation_energy_derived"] is True


def test_canonical_energy_keeps_full_coercivity_open():
    data = scalar_prepared_canonical_energy_data()
    theorem = scalar_prepared_canonical_energy_theorem()

    assert data["prepared_principal_nondegenerate"] is True
    assert data["full_coercivity_established"] is False
    assert theorem["full_coercivity_established"] is False
    assert len(theorem["limitations"]) == 4
