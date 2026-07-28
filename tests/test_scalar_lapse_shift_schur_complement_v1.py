import sympy as sp

from dfm_mkc_solver import (
    scalar_lapse_shift_schur_complement_v1 as schur,
)


def test_exact_scalar_lapse_shift_schur_complement():
    data = schur.scalar_lapse_shift_schur_complement()
    certificate = schur.certificate()

    assert data["constraint_block"].shape == (2, 2)
    assert data["source_vector"].shape == (2, 1)
    assert data["solution"].shape == (2, 1)

    assert data["determinant"] != 0
    assert isinstance(data["determinant_domain"], sp.Ne)

    assert certificate.constraint_fields == ("A", "B")
    assert len(certificate.reduced_fields) == 10

    assert certificate.constraint_time_jets_absent is True
    assert certificate.constraint_block_symmetric is True
    assert certificate.constraint_gradient_affine is True
    assert certificate.adjugate_identity_exact is True
    assert certificate.constraint_solution_exact is True
    assert certificate.reduced_density_constraint_free is True
    assert certificate.determinant_domain_required is True
    assert certificate.exact_schur_complement_constructed is True

    assert certificate.spatial_gauge_quotient_applied is False
