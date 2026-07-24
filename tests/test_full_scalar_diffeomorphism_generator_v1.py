import inspect
import json
from pathlib import Path

import sympy as sp

from dfm_mkc_solver import full_scalar_diffeomorphism_generator_v1 as gauge


def _all_zero(values):
    return all(sp.simplify(value) == 0 for value in values)


def test_tensorial_metric_lie_derivative():
    assert _all_zero(gauge.metric_lie_derivative_residuals().values())


def test_homogeneous_scalar_lie_derivatives():
    assert _all_zero(gauge.scalar_lie_derivative_residuals().values())


def test_weight_one_current_density_and_spatial_projection():
    z = gauge._symbols()
    T, L, k2 = z["T"], z["L"], z["k2"]
    J, Jp = z["Jbar_b_0"], z["Jbar_b_0_prime"]
    # Independent use of Lie J^0=T J'-J T'+J(T'-k2 L).
    minus_lie_zero = -(T*Jp-J*z["T_prime"]+J*(z["T_prime"]-k2*L))
    generator = gauge.scalar_diffeomorphism_generator()
    assert sp.simplify(generator["delta_J_b_0"]-minus_lie_zero) == 0
    # delta J^i=partial^i(delta_J_L), so J partial^i L'
    # projects without an extra sign or k2.
    assert sp.simplify(generator["delta_J_b_L"]-J*z["L_prime"]) == 0
    assert _all_zero(
        gauge.current_density_lie_derivative_residuals().values()
    )


def test_all_twelve_targets_and_canonical_order():
    assert tuple(gauge.scalar_diffeomorphism_generator()) == gauge.VARIABLES
    assert gauge.VARIABLES == (
        "A", "B", "psi", "E", "delta_phi", "delta_theta",
        "delta_J_b_0", "delta_J_b_L", "delta_ell_b",
        "delta_J_r_0", "delta_J_r_L", "delta_ell_r",
    )
    assert _all_zero(gauge.target_generator_residuals().values())


def test_exact_first_jet_prolongation_uses_total_derivative():
    base = gauge.scalar_diffeomorphism_generator()
    jets = gauge.scalar_diffeomorphism_jet_generator()
    assert tuple(jets) == tuple(f"{name}_prime" for name in gauge.VARIABLES)
    for name in gauge.VARIABLES:
        assert sp.simplify(
            jets[f"{name}_prime"]
            - gauge._total_conformal_time_derivative(base[name])
        ) == 0
    assert _all_zero(gauge.jet_prolongation_residuals().values())
    source = inspect.getsource(gauge.scalar_diffeomorphism_jet_generator)
    assert "_total_conformal_time_derivative" in source
    assert "entries" not in source


def test_bardeen_invariance():
    assert _all_zero(gauge.bardeen_invariance_residuals().values())


def test_no_imported_final_transformation_dictionary():
    source = inspect.getsource(gauge)
    assert "metric_constraint_elimination_v1" not in source
    assert "scalar_constraint_variational_bridge_v1" not in source
    assert not any(
        line.startswith("from dfm_mkc_solver") or
        line.startswith("import dfm_mkc_solver")
        for line in source.splitlines()
    )


def test_certificate_and_artifact_boundaries():
    cert = gauge.certificate()
    positive = (
        "metric_tensorial_lie_derivative",
        "homogeneous_scalar_lie_derivatives",
        "weight_one_current_density_lie_derivative",
        "all_twelve_target_transformations",
        "first_jet_total_derivative_prolongation",
        "bardeen_invariance",
        "full_scalar_diffeomorphism_generator_established",
    )
    assert all(cert[name] is True for name in positive)
    later = (
        "singular_lapse_shift_branch_classified",
        "reduced_physical_scalar_action_established",
        "weyl_observable_action_bound", "prediction_vector_computed",
        "local_identifiability_established",
        "full_lcdm_manifold_separation_established",
        "measurable_margin_established",
    )
    assert all(cert[name] is False for name in later)
    source = inspect.getsource(gauge.certificate)
    assert not any(f'"{name}": True' in source for name in positive)

    payload = json.loads(Path(
        "artifacts/dfm_mkc/full_scalar_diffeomorphism_generator_v1.json"
    ).read_text())
    assert payload["result_type"] == "full_scalar_diffeomorphism_generator"
    assert payload["novelty_claimed"] is False
    assert payload["full_scalar_diffeomorphism_generator_established"] is True
    assert all(payload[name] is False for name in later)
