from tools.verify_dfm_mkc_flrw_reduction_2026_10_29 import flrw_residuals


def test_action_derived_flrw_continuity_and_constraint_propagation():
    residuals = flrw_residuals()
    assert residuals["dark_sector_continuity"] == 0
    assert residuals["friedmann_constraint_propagation"] == 0
