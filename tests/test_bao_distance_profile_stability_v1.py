from dfm_mkc_solver.bao_distance_profile_stability_v1 import (
    exact_bao_distance_profile_stability_certificate,
)


def test_exact_bao_distance_profile_stability_certificate():
    residuals = exact_bao_distance_profile_stability_certificate()
    assert set(residuals) == {
        "hubble_distance_identity",
        "hubble_distance_majorant_remainder",
        "comoving_integrand_identity",
        "comoving_integrand_majorant_remainder",
        "linear_interpolation_majorant_identity",
        "volume_product_difference",
        "volume_cube_root_identity",
        "volume_product_majorant_remainder",
        "volume_distance_majorant_remainder",
        "thirteen_row_profile_candidate_scaling",
    }
    assert all(expression == 0 for expression in residuals.values())
