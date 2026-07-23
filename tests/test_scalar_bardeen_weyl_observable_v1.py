import math

import pytest

from dfm_mkc_solver.scalar_bardeen_weyl_observable_v1 import (
    ScalarMetricGaugeState,
    bardeen_weyl_observable,
    certify_bardeen_weyl_gauge_invariance,
    scalar_gauge_transform,
)


def test_scalar_shear_cancels_spatial_gauge_shift():
    state = ScalarMetricGaugeState(
        lapse_potential=0.12,
        curvature_potential=-0.07,
        scalar_shift=0.031,
        spatial_shear_prime=-0.014,
        scalar_shear_prime=0.005,
    )

    transformed = scalar_gauge_transform(
        state=state,
        conformal_hubble=2.4,
        time_shift=0.0,
        time_shift_prime=0.0,
        spatial_shift_prime=0.19,
    )

    assert transformed.scalar_shear == pytest.approx(
        state.scalar_shear,
        abs=1.0e-15,
    )


def test_bardeen_weyl_observable_is_invariant():
    state = ScalarMetricGaugeState(
        lapse_potential=0.12,
        curvature_potential=-0.07,
        scalar_shift=0.031,
        spatial_shear_prime=-0.014,
        scalar_shear_prime=0.005,
    )

    certificate = certify_bardeen_weyl_gauge_invariance(
        state=state,
        conformal_hubble=2.4,
        time_shift=-0.023,
        time_shift_prime=0.017,
        spatial_shift_prime=0.041,
        tolerance=1.0e-13,
    )

    assert certificate.gauge_invariance_verified is True
    assert certificate.lapse_invariance_residual <= 1.0e-13
    assert certificate.curvature_invariance_residual <= 1.0e-13
    assert certificate.weyl_sum_invariance_residual <= 1.0e-13
    assert certificate.newtonian_gauge_reduction_verified is True


def test_newtonian_gauge_reduces_to_metric_potentials():
    state = ScalarMetricGaugeState(
        lapse_potential=1.25e-6,
        curvature_potential=-0.75e-6,
        scalar_shift=0.0,
        spatial_shear_prime=0.0,
        scalar_shear_prime=0.0,
    )

    observable = bardeen_weyl_observable(
        state=state,
        conformal_hubble=3.7,
    )

    assert observable.bardeen_lapse_potential == state.lapse_potential
    assert (
        observable.bardeen_curvature_potential
        == state.curvature_potential
    )
    assert observable.weyl_potential_sum == pytest.approx(0.5e-6)
    assert observable.weyl_potential_average == pytest.approx(0.25e-6)


def test_scientific_boundaries_remain_explicit():
    state = ScalarMetricGaugeState(
        lapse_potential=1.0e-6,
        curvature_potential=2.0e-6,
        scalar_shift=3.0e-7,
        spatial_shear_prime=-1.0e-7,
        scalar_shear_prime=2.0e-8,
    )

    certificate = certify_bardeen_weyl_gauge_invariance(
        state=state,
        conformal_hubble=1.5,
        time_shift=0.02,
        time_shift_prime=-0.03,
        spatial_shift_prime=0.04,
    )

    assert certificate.gauge_invariance_verified is True
    assert certificate.action_binding_established is False
    assert certificate.dfm_vs_lcdm_prediction_vector_computed is False
    assert certificate.original.action_binding_established is False
    assert (
        certificate.original.dfm_vs_lcdm_prediction_vector_computed
        is False
    )


def test_nonfinite_inputs_are_rejected():
    with pytest.raises(ValueError, match="lapse_potential must be finite"):
        ScalarMetricGaugeState(
            lapse_potential=math.inf,
            curvature_potential=0.0,
            scalar_shift=0.0,
            spatial_shear_prime=0.0,
            scalar_shear_prime=0.0,
        )
