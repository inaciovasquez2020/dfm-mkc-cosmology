import sympy as sp
from dataclasses import replace

from dfm_mkc_solver import scalar_constraint_variational_bridge_v1 as bridge


def test_fixed_action_source_image_constraint_and_observable_binding():
    certificate = bridge.fixed_action_source_domain_binding_certificate()

    assert certificate.domain_assumptions == (
        "a > 0",
        "k != 0 (k2=k**2)",
        "G != 0",
    )
    assert len(certificate.background_equations_used) == 8
    assert certificate.sector_anisotropy_rows["dfm"] == 0
    assert certificate.sector_anisotropy_rows["b"] == 0
    assert certificate.sector_anisotropy_rows["r"] == 0
    assert certificate.fixed_action_source_image[
        "enthalpy_sigma_total"
    ] == 0
    assert all(
        residual == 0
        for residual in certificate.normalized_row_residuals.values()
    )
    assert certificate.matrix_identity_residual == sp.zeros(3, 3)
    assert certificate.source_vector_identity_residual == sp.zeros(3, 1)
    assert certificate.solution_residual == sp.zeros(3, 1)
    assert all(
        residual == 0
        for residual in certificate.eliminator_solution_residuals.values()
    )
    assert all(
        residual == 0
        for residual in certificate.bardeen_identity_residuals.values()
    )
    assert certificate.canonical_second_variation_identified is True
    assert certificate.fixed_action_source_domain_identified is True
    assert certificate.fixed_action_anisotropic_stress_zero is True
    assert certificate.action_derived_constraints_established is True
    assert (
        certificate.action_derived_bardeen_weyl_observable_established
        is True
    )
    assert certificate.eliminator_binding_independent is True
    assert certificate.bardeen_binding_independent is True
    assert certificate.canonical_psi_prime_coefficient.name == "k2"
    assert certificate.canonical_psi_prime_coefficient_nonzero is True
    assert certificate.phi_prime_action_row_residual == 0
    assert certificate.eliminator_momentum_identity_residual == 0
    assert certificate.momentum_chart_identity_residual == 0
    assert certificate.momentum_chart_identity_proved is True
    assert certificate.action_binding_established is True
    assert (
        certificate.unrestricted_anisotropic_source_action_binding_established
        is False
    )


def test_unrestricted_source_interface_remains_unbound():
    certificate = bridge.canonical_metric_constraint_action_binding_certificate()

    assert certificate.canonical_second_variation_identified is True
    assert certificate.action_binding_established is False


def test_momentum_chart_identity_is_not_a_definition():
    certificate = bridge.fixed_action_source_domain_binding_certificate()
    row = certificate.normalized_canonical_momentum_row
    psi_prime = next(
        symbol for symbol in row.free_symbols
        if symbol.name == "psi_prime"
    )

    k2 = certificate.canonical_psi_prime_coefficient
    assert sp.cancel(sp.expand(row).coeff(psi_prime) - k2) == 0
    assert sp.cancel(row.subs(
        psi_prime, certificate.phi_prime_from_action_row
    )) == 0
    assert certificate.eliminator_momentum_identity_residual == 0
    assert certificate.momentum_chart_identity_residual == 0


def test_changed_canonical_psi_prime_coefficient_breaks_chart_identity():
    certificate = bridge.fixed_action_source_domain_binding_certificate()
    row = certificate.normalized_canonical_momentum_row
    psi_prime = next(
        symbol for symbol in row.free_symbols
        if symbol.name == "psi_prime"
    )
    k2 = certificate.canonical_psi_prime_coefficient
    changed_row = sp.expand(row + k2 * psi_prime)
    changed_phi_prime = sp.solve(
        sp.Eq(changed_row, 0), psi_prime, dict=False
    )[0]
    canonical_A = next(
        symbol for symbol in changed_phi_prime.free_symbols
        if symbol.name == "A"
    )
    changed_residual = sp.cancel(
        changed_phi_prime.subs(
            canonical_A,
            certificate.production_eliminator_solution["Psi"],
        )
        + next(symbol for symbol in row.free_symbols if symbol.name == "H")
        * certificate.production_eliminator_solution["Psi"]
        - certificate.production_eliminator_solution["P"]
    )

    assert sp.cancel(changed_row.coeff(psi_prime) - 2 * k2) == 0
    assert changed_residual != 0


def test_changed_production_eliminator_p_breaks_chart_identity(monkeypatch):
    production_constructor = bridge.symbolic_metric_constraint_elimination

    def changed_constructor(**kwargs):
        representation = production_constructor(**kwargs)
        changed_solution = dict(representation.solution)
        changed_solution["P"] = 2 * changed_solution["P"]
        return replace(representation, solution=changed_solution)

    monkeypatch.setattr(
        bridge,
        "symbolic_metric_constraint_elimination",
        changed_constructor,
    )
    certificate = bridge.fixed_action_source_domain_binding_certificate()

    assert certificate.eliminator_momentum_identity_residual != 0
    assert certificate.momentum_chart_identity_residual != 0
    assert certificate.momentum_chart_identity_proved is False
    assert certificate.action_binding_established is False


def test_eliminator_matrix_provenance_detects_changed_coefficient(
    monkeypatch,
):
    production_constructor = bridge.symbolic_metric_constraint_elimination

    def changed_constructor(**kwargs):
        representation = production_constructor(**kwargs)
        changed_matrix = representation.constraint_matrix.copy()
        changed_matrix[0, 0] += 1
        return replace(representation, constraint_matrix=changed_matrix)

    monkeypatch.setattr(
        bridge,
        "symbolic_metric_constraint_elimination",
        changed_constructor,
    )
    certificate = bridge.fixed_action_source_domain_binding_certificate()

    assert certificate.matrix_identity_residual != sp.zeros(3, 3)
    assert certificate.eliminator_binding_independent is False
    assert certificate.action_derived_constraints_established is False
    assert certificate.action_binding_established is False


def test_bardeen_definition_provenance_detects_changed_sign(monkeypatch):
    production_constructor = bridge.bardeen_weyl_definitions

    def changed_constructor(**kwargs):
        definitions = production_constructor(**kwargs)
        changed_lapse = (
            -kwargs["lapse_potential"]
            + kwargs["conformal_hubble"] * definitions.scalar_shear
            + kwargs["scalar_shear_prime"]
        )
        return replace(
            definitions,
            bardeen_lapse_potential=changed_lapse,
            weyl_potential_sum=(
                changed_lapse
                + definitions.bardeen_curvature_potential
            ),
        )

    monkeypatch.setattr(
        bridge,
        "bardeen_weyl_definitions",
        changed_constructor,
    )
    certificate = bridge.fixed_action_source_domain_binding_certificate()

    assert any(
        residual != 0
        for residual in certificate.bardeen_identity_residuals.values()
    )
    assert certificate.bardeen_binding_independent is False
    assert (
        certificate.action_derived_bardeen_weyl_observable_established
        is False
    )
    assert certificate.action_binding_established is False
