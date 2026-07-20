import importlib.util
import sys
from pathlib import Path


CODE = Path(
    "src/dfm_mkc_solver/dark_sector_principal_symbol_v1.py"
)

spec = importlib.util.spec_from_file_location(
    "dark_sector_principal_symbol_v1",
    CODE,
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_action_derived_dark_sector_principal_certificate():
    regular = module.dark_sector_principal_certificate(
        scale_factor=2.0,
        phi_background=3.0,
        alpha=5.0,
        beta=7.0,
    )

    assert regular.kinetic_matrix == (
        (20.0, 0.0),
        (0.0, 252.0),
    )
    assert regular.gradient_matrix == regular.kinetic_matrix
    assert regular.kinetic_eigenvalues == (20.0, 252.0)
    assert regular.gradient_eigenvalues == (20.0, 252.0)
    assert regular.principal_rank == 2
    assert regular.kinetic_positive_definite is True
    assert regular.gradient_positive_definite is True
    assert regular.phase_degenerate is False
    assert regular.principal_sound_speed_squared == (1.0, 1.0)

    degenerate = module.dark_sector_principal_certificate(
        scale_factor=2.0,
        phi_background=0.0,
        alpha=5.0,
        beta=7.0,
    )

    assert degenerate.kinetic_matrix == (
        (20.0, 0.0),
        (0.0, 0.0),
    )
    assert degenerate.principal_rank == 1
    assert degenerate.kinetic_positive_definite is False
    assert degenerate.gradient_positive_definite is False
    assert degenerate.phase_degenerate is True
    assert degenerate.principal_sound_speed_squared is None
