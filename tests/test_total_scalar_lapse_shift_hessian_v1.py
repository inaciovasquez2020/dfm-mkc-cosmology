import json
import inspect
from pathlib import Path

import sympy as sp

from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total
from dfm_mkc_solver.visible_sector_offshell_scalar_hessian_v1 import (
    scalar_flrw_hessian,
)


def test_full_adm_plus_ghy_expansion_and_no_lapse_shift_kinetics():
    sectors = total._sector_quadratic_densities()
    assert set(sectors) == {"eh_ghy", "dfm", "b", "r"}
    assert sectors["eh_ghy"] != 0
    z = total._symbols()
    L2 = total._action_quadratic_density()
    A1, B1 = z["qp"][0], z["qp"][1]
    for jet in z["q"] + z["qp"]:
        assert sp.diff(L2, A1, jet) == 0
        assert sp.diff(L2, B1, jet) == 0


def test_exact_imported_visible_subblock():
    assert scalar_flrw_hessian(exponent=1, coefficient=sp.Symbol(
        "m_b", positive=True
    )).shape == (5, 5)
    assert all(value == 0 for value in total.visible_import_residual())
    assert all(
        value == 0
        for family in total.fourier_normalization_residual().values()
        for value in family
    )


def test_constraint_rows_are_independent_action_variations():
    L2 = total._action_quadratic_density()
    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    for variable, public in (
        ("A", total.hamiltonian_constraint_row()),
        ("B", total.momentum_constraint_row()),
    ):
        varied = sp.diff(L2, q[variable])
        for name, x in q.items():
            assert sp.simplify(sp.diff(varied, x) - public[name]) == 0
    assert all(x == 0 for x in total.hamiltonian_row_residual())
    assert all(x == 0 for x in total.momentum_row_residual())


def test_formal_adjoint_boundary_and_direct_certificate():
    cert = total.certificate()
    assert cert["formal_adjoint_exchange_symmetry"]
    assert "eta_i" in cert["boundary_terms"]
    assert cert["direct_mixed_differentiation_residual"] == 0
    assert all(
        value == 0
        for constraint in total.formal_adjoint_residual().values()
        for pair in constraint.values()
        for value in pair
    )
    assert all(
        value == 0
        for constraint in total.full_matrix_adm_residual().values()
        for value in constraint
    )


def test_offshell_and_onshell_are_separately_labelled():
    residuals = total.background_residuals()
    reduced = total.on_shell_reduction()
    assert residuals and all(value != 0 for value in residuals.values())
    assert set(reduced) == {"substitution", "rows"}
    assert set(reduced["substitution"]) == {
        total._symbols()[name] for name in (
            "Lambda", "Hp", "phpp", "thpp", "Jbp", "Jrp",
            "ellbp", "ellrp",
        )
    }
    decomposition = total.background_residual_decomposition()
    assert set(decomposition) == {
        "off_shell", "on_shell", "pivot_substitution",
        "linear_combination", "residual", "chart_conditions",
    }
    assert decomposition["off_shell"] is not decomposition["on_shell"]
    assert any(
        decomposition["off_shell"][constraint][name] !=
        decomposition["on_shell"][constraint][name]
        for constraint in ("A", "B") for name in total.VARIABLES
    )
    assert any(
        coefficient != 0
        for constraint in decomposition["linear_combination"].values()
        for variable in constraint.values()
        for component in variable
        for coefficient in component.values()
    )
    assert all(
        value == 0
        for constraint in decomposition["residual"].values()
        for pair in constraint.values()
        for value in pair
    )


def test_canonical_current_second_jet_and_total_derivative_rules():
    z = total._symbols()
    assert str(z["Jbpp"]) == "Jbar_b_0_double_prime"
    assert str(z["Jrpp"]) == "Jbar_r_0_double_prime"
    assert total._D_eta(z["Jbp"]) == z["Jbpp"]
    assert total._D_eta(z["Jrp"]) == z["Jrpp"]


def test_current_differential_closure_is_derived_and_exact():
    z = total._symbols()
    sources = total.background_residuals()
    independently_differentiated = {
        name: total._D_eta(sources[name])
        for name in ("baryon_continuity", "radiation_continuity")
    }
    assert independently_differentiated["baryon_continuity"] == z["Jbpp"]
    assert independently_differentiated["radiation_continuity"] == z["Jrpp"]

    closure = total.background_current_differential_closure()
    assert closure["source_residuals"] == {
        name: sources[name] for name in closure["source_residual_names"]
    }
    assert closure["differentiated_residuals"] == independently_differentiated
    assert closure["pivot_substitution"] == {
        z["Jbpp"]: sp.Integer(0),
        z["Jrpp"]: sp.Integer(0),
    }
    assert all(
        expression.subs(
            closure["pivot_substitution"], simultaneous=True
        ) == 0
        for expression in independently_differentiated.values()
    )
    assert all(
        residual == 0
        for residual in closure["substitution_back_residuals"].values()
    )
    assert closure["certificates"]["canonical_current_jet_order"] == 2
    assert all(closure["certificates"]["total_derivative_rules"].values())
    assert closure["certificates"]["differentiated_equations_derived"]
    assert all(closure["certificates"]["substitution_back_zero"].values())
    assert closure["certificates"]["F_zero_condition_used"] is False
    assert closure["certificates"]["gauge_fixing_used"] is False
    assert closure["certificates"]["constraint_elimination_used"] is False
    assert (
        closure["certificates"]["complete_background_differential_closure"]
        is False
    )
    source = inspect.getsource(total.background_current_differential_closure)
    assert "background_residuals()" in source
    assert "_D_eta(expression)" in source
    assert "sp.solve(" in source


def test_certificates_are_not_source_level_shortcuts():
    module_source = inspect.getsource(total)
    direct_source = inspect.getsource(total.direct_mixed_differentiation_residual)
    direct_rows_source = inspect.getsource(
        total._direct_constraint_rows_from_original_sectors
    )
    original_source = inspect.getsource(
        total._original_sector_actions_two_parameter
    )
    decomposition_source = inspect.getsource(
        total.background_residual_decomposition
    )
    hamiltonian_source = inspect.getsource(total.hamiltonian_constraint_row)
    momentum_source = inspect.getsource(total.momentum_constraint_row)
    certificate_source = inspect.getsource(total.certificate)
    assert "R_phi" not in module_source
    assert "R_theta" not in module_source
    assert "R_a" not in module_source
    assert "R_J_" not in module_source
    assert "residuals.extend((sp.Integer(0)" not in module_source
    for forbidden in (
        "_action_quadratic_density", "_linearized_row",
        "hamiltonian_constraint_row", "momentum_constraint_row",
        "_sector_quadratic_densities",
    ):
        assert forbidden not in direct_source
    assert "_original_sector_actions_two_parameter" in direct_source
    assert "_original_sector_actions_two_parameter" in direct_rows_source
    assert "_sector_quadratic_densities" not in direct_rows_source
    assert "_action_quadratic_density" not in direct_rows_source
    assert "_linearized_row" not in direct_rows_source
    assert "_sector_quadratic_densities" not in original_source
    assert "_action_quadratic_density" not in original_source
    assert "_linearized_row" not in original_source
    assert "sp.Integer(0) for equation in residuals" not in decomposition_source
    assert "dict(entries)" not in decomposition_source
    assert "_action_quadratic_density" not in hamiltonian_source
    assert "_linearized_row" not in hamiltonian_source
    assert "_action_quadratic_density" not in momentum_source
    assert "_linearized_row" not in momentum_source
    for flag in (
        "full_adm_plus_ghy_expansion",
        "formal_adjoint_exchange_symmetry",
        "hamiltonian_row_reconstructed",
        "momentum_row_reconstructed",
        "background_residual_decomposition",
        "direct_mixed_differentiation",
    ):
        assert f'"{flag}": True' not in certificate_source


def test_artifact_schema_flags_and_claim_boundaries():
    path = Path("artifacts/dfm_mkc/total_scalar_lapse_shift_hessian_v1.json")
    payload = json.loads(path.read_text())
    expected = [
        "result_type", "novelty_claimed", "complete_action_identifier",
        "eh_ghy_scalar_constraint_hessian_established",
        "dfm_scalar_constraint_hessian_established",
        "visible_scalar_constraint_hessian_bound",
        "total_scalar_lapse_shift_hessian_established",
        "hamiltonian_row_action_derived", "momentum_row_action_derived",
        "lapse_shift_time_derivatives_absent",
        "formal_adjoint_exchange_symmetry_established",
        "background_residuals_explicit", "ready_for_constraint_elimination",
        "reduced_physical_scalar_action_established",
        "weyl_observable_action_bound", "prediction_vector_computed",
        "local_identifiability_established",
        "full_lcdm_manifold_separation_established",
        "measurable_margin_established", "action", "conventions", "variables",
        "eh_ghy_sector", "dfm_sector", "visible_sector",
        "total_lapse_shift_operator", "hamiltonian_row", "momentum_row",
        "background_equations", "boundary_terms", "certificates",
        "domain_conditions", "limitations", "provenance",
    ]
    assert list(payload)[:len(expected)] == expected
    assert payload["result_type"] == "total_scalar_lapse_shift_hessian"
    assert payload["novelty_claimed"] is False
    assert all(payload[key] is True for key in expected[3:13])
    assert all(payload[key] is False for key in expected[13:19])
    assert all(payload[key] not in ("", [], {}) for key in expected[19:])
    assert payload["canonical_background_current_jet_order"] == 2
    assert payload["background_current_differential_closure_proved"] is True
    assert payload["complete_background_differential_closure_proved"] is False
    assert payload["complete_gauge_Noether_identity_proved"] is False
    assert payload["F_zero_branch_classification"] == "unclassified"
    assert payload["physical_strong_coupling_proved"] is False
    assert "gauge fixing" not in payload["certificates"].lower()
    assert "strong coupling" not in payload["limitations"].lower()
