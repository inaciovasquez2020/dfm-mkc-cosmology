import inspect
import json
from pathlib import Path

import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


ARTIFACT = Path("artifacts/dfm_mkc/complete_scalar_quadratic_action_v1.json")


def test_inventory_rows_and_provenance():
    assert complete.FIELD_ORDER == total.VARIABLES
    assert complete.ACTION_COMPONENTS == (
        "Einstein-Hilbert plus Gibbons-Hawking-York (ADM)",
        "DFM-MKC scalar amplitude/phase",
        "pressureless baryon Schutz-Sorkin",
        "radiation Schutz-Sorkin",
    )
    assert complete.quadratic_action()["derivative_order"] == 1
    assert complete.euler_hessian() and len(complete.euler_hessian()) == 12
    assert all(complete.row_provenance()[name] for name in complete.FIELD_ORDER)
    assert all(complete.block_provenance().values())


def test_noncommuting_formal_adjoint_product_rule():
    a = sp.Symbol("a", positive=True)
    D = complete.DiffOp((0, 1))
    residual = (complete.DiffOp.scalar(a) * D).adjoint() - complete.DiffOp(
        (-complete.total_derivative(a), -a)
    )
    assert residual.is_zero()
    # Composition independently exercises D a = a D + D(a).
    assert (D * complete.DiffOp.scalar(a) -
            complete.DiffOp((complete.total_derivative(a), a))).is_zero()


def test_exact_full_matrix_adjoint_and_subblock_certificates():
    assert all(op.is_zero() for row in complete.formal_adjoint_residuals()
               for op in row)
    assert all(op.is_zero() for op in complete.lapse_shift_subblock_residuals())
    assert all(op.is_zero() for op in complete.lapse_shift_on_shell_residuals())
    assert all(x == 0 for x in complete.visible_sector_residuals())
    assert all(x == 0 for x in complete.dark_principal_residuals())


def test_no_constraint_kinetics_and_all_schutz_fields():
    cert = complete.certificate()
    assert cert["no_lapse_shift_time_kinetics"]
    assert not cert["F_zero_used"]
    assert not cert["gauge_fixing_used"]
    assert not cert["constraint_elimination_used"]
    assert set(complete.FIELD_ORDER[6:]) == {
        "delta_J_b_0", "delta_J_b_L", "delta_ell_b",
        "delta_J_r_0", "delta_J_r_L", "delta_ell_r",
    }
    source = inspect.getsource(complete)
    assert "metric_constraint_elimination_v1" not in source
    assert "scalar_constraint_variational_bridge_v1" not in source


def test_artifact_scope_and_completeness():
    data = json.loads(ARTIFACT.read_text())
    assert tuple(data["canonical_field_order"]) == complete.FIELD_ORDER
    assert data["quadratic_action_completeness"] == "complete"
    assert len(data["euler_row_coverage"]) == 12
    assert data["formal_adjoint_residuals"] == "all exact zero"
    assert data["F_zero_branch_classification"] == "unclassified"
    assert data["classification_ready"] is False
    assert data["noether_ready"] is True
    assert data["every_retained_Schutz_Sorkin_field_included"] is True
    assert data["no_imported_eliminator_certificate"] is True
