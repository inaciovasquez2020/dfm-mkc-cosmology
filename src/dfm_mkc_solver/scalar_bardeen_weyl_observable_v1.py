"""Gauge-invariant scalar metric observables in one declared convention.

The scalar metric convention used by this module is

    ds^2 = a(eta)^2 [
        -(1 + 2 A) d eta^2
        + 2 partial_i B d eta dx^i
        + ((1 - 2 psi) delta_ij
           + 2 partial_i partial_j E) dx^i dx^j
    ].

Under the scalar coordinate change

    eta -> eta + T,
    x^i -> x^i + partial^i L,

the supplied variables transform as

    A       -> A - H T - T',
    psi     -> psi + H T,
    B       -> B + T - L',
    E'      -> E' - L'.

Therefore the scalar shear sigma := B - E' transforms as

    sigma  -> sigma + T,
    sigma' -> sigma' + T'.

The two Bardeen combinations encoded here are

    Phi_B := A + H sigma + sigma',
    Psi_B := psi - H sigma.

Their sum is the Weyl/lensing potential in this convention:

    W := Phi_B + Psi_B.

This module proves only the algebraic gauge cancellation in the declared
convention.  It does not claim that the current DFM source-level metric
constraint elimination has already been derived from the constrained
quadratic action, nor that a DFM-versus-LambdaCDM prediction vector has been
computed.
"""

from dataclasses import dataclass
import math


def _require_finite(name, value):
    if not math.isfinite(value):
        raise ValueError("{} must be finite".format(name))


@dataclass(frozen=True)
class ScalarMetricGaugeState:
    """Scalar metric perturbations and the derivative of B - E'."""

    lapse_potential: float
    curvature_potential: float
    scalar_shift: float
    spatial_shear_prime: float
    scalar_shear_prime: float

    def __post_init__(self):
        for name, value in (
            ("lapse_potential", self.lapse_potential),
            ("curvature_potential", self.curvature_potential),
            ("scalar_shift", self.scalar_shift),
            ("spatial_shear_prime", self.spatial_shear_prime),
            ("scalar_shear_prime", self.scalar_shear_prime),
        ):
            _require_finite(name, value)

    @property
    def scalar_shear(self):
        return self.scalar_shift - self.spatial_shear_prime


@dataclass(frozen=True)
class BardeenWeylObservable:
    """Fixed scalar gauge-invariant observable in the declared convention."""

    bardeen_lapse_potential: float
    bardeen_curvature_potential: float
    weyl_potential_sum: float
    weyl_potential_average: float
    scalar_shear: float
    gauge_invariant_by_algebra: bool
    action_binding_established: bool
    dfm_vs_lcdm_prediction_vector_computed: bool

    def __post_init__(self):
        for name, value in (
            (
                "bardeen_lapse_potential",
                self.bardeen_lapse_potential,
            ),
            (
                "bardeen_curvature_potential",
                self.bardeen_curvature_potential,
            ),
            ("weyl_potential_sum", self.weyl_potential_sum),
            ("weyl_potential_average", self.weyl_potential_average),
            ("scalar_shear", self.scalar_shear),
        ):
            _require_finite(name, value)


@dataclass(frozen=True)
class BardeenGaugeInvarianceCertificate:
    """Numerical identity certificate for one arbitrary scalar gauge change."""

    original: BardeenWeylObservable
    transformed: BardeenWeylObservable
    lapse_invariance_residual: float
    curvature_invariance_residual: float
    weyl_sum_invariance_residual: float
    tolerance: float
    gauge_invariance_verified: bool
    newtonian_gauge_reduction_verified: bool
    action_binding_established: bool
    dfm_vs_lcdm_prediction_vector_computed: bool

    def __post_init__(self):
        for name, value in (
            (
                "lapse_invariance_residual",
                self.lapse_invariance_residual,
            ),
            (
                "curvature_invariance_residual",
                self.curvature_invariance_residual,
            ),
            (
                "weyl_sum_invariance_residual",
                self.weyl_sum_invariance_residual,
            ),
            ("tolerance", self.tolerance),
        ):
            _require_finite(name, value)
        if self.tolerance <= 0.0:
            raise ValueError("tolerance must be positive")


def scalar_gauge_transform(
    *,
    state,
    conformal_hubble,
    time_shift,
    time_shift_prime,
    spatial_shift_prime,
):
    """Apply the declared scalar gauge transformation."""

    for name, value in (
        ("conformal_hubble", conformal_hubble),
        ("time_shift", time_shift),
        ("time_shift_prime", time_shift_prime),
        ("spatial_shift_prime", spatial_shift_prime),
    ):
        _require_finite(name, value)

    return ScalarMetricGaugeState(
        lapse_potential=(
            state.lapse_potential
            - conformal_hubble * time_shift
            - time_shift_prime
        ),
        curvature_potential=(
            state.curvature_potential
            + conformal_hubble * time_shift
        ),
        scalar_shift=(
            state.scalar_shift
            + time_shift
            - spatial_shift_prime
        ),
        spatial_shear_prime=(
            state.spatial_shear_prime
            - spatial_shift_prime
        ),
        scalar_shear_prime=(
            state.scalar_shear_prime
            + time_shift_prime
        ),
    )


def bardeen_weyl_observable(*, state, conformal_hubble):
    """Return the two Bardeen potentials and their Weyl sum."""

    _require_finite("conformal_hubble", conformal_hubble)

    scalar_shear = state.scalar_shear
    bardeen_lapse = (
        state.lapse_potential
        + conformal_hubble * scalar_shear
        + state.scalar_shear_prime
    )
    bardeen_curvature = (
        state.curvature_potential
        - conformal_hubble * scalar_shear
    )
    weyl_sum = bardeen_lapse + bardeen_curvature

    return BardeenWeylObservable(
        bardeen_lapse_potential=bardeen_lapse,
        bardeen_curvature_potential=bardeen_curvature,
        weyl_potential_sum=weyl_sum,
        weyl_potential_average=0.5 * weyl_sum,
        scalar_shear=scalar_shear,
        gauge_invariant_by_algebra=True,
        action_binding_established=False,
        dfm_vs_lcdm_prediction_vector_computed=False,
    )


def certify_bardeen_weyl_gauge_invariance(
    *,
    state,
    conformal_hubble,
    time_shift,
    time_shift_prime,
    spatial_shift_prime,
    tolerance=1.0e-12,
):
    """Certify algebraic invariance under one arbitrary scalar gauge change."""

    _require_finite("tolerance", tolerance)
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")

    original = bardeen_weyl_observable(
        state=state,
        conformal_hubble=conformal_hubble,
    )
    transformed_state = scalar_gauge_transform(
        state=state,
        conformal_hubble=conformal_hubble,
        time_shift=time_shift,
        time_shift_prime=time_shift_prime,
        spatial_shift_prime=spatial_shift_prime,
    )
    transformed = bardeen_weyl_observable(
        state=transformed_state,
        conformal_hubble=conformal_hubble,
    )

    lapse_residual = abs(
        transformed.bardeen_lapse_potential
        - original.bardeen_lapse_potential
    )
    curvature_residual = abs(
        transformed.bardeen_curvature_potential
        - original.bardeen_curvature_potential
    )
    weyl_residual = abs(
        transformed.weyl_potential_sum
        - original.weyl_potential_sum
    )

    newtonian_state = ScalarMetricGaugeState(
        lapse_potential=state.lapse_potential,
        curvature_potential=state.curvature_potential,
        scalar_shift=0.0,
        spatial_shear_prime=0.0,
        scalar_shear_prime=0.0,
    )
    newtonian = bardeen_weyl_observable(
        state=newtonian_state,
        conformal_hubble=conformal_hubble,
    )
    newtonian_reduction = (
        abs(
            newtonian.bardeen_lapse_potential
            - state.lapse_potential
        )
        <= tolerance
        and abs(
            newtonian.bardeen_curvature_potential
            - state.curvature_potential
        )
        <= tolerance
        and abs(
            newtonian.weyl_potential_sum
            - (
                state.lapse_potential
                + state.curvature_potential
            )
        )
        <= tolerance
    )

    verified = (
        lapse_residual <= tolerance
        and curvature_residual <= tolerance
        and weyl_residual <= tolerance
    )

    return BardeenGaugeInvarianceCertificate(
        original=original,
        transformed=transformed,
        lapse_invariance_residual=lapse_residual,
        curvature_invariance_residual=curvature_residual,
        weyl_sum_invariance_residual=weyl_residual,
        tolerance=tolerance,
        gauge_invariance_verified=verified,
        newtonian_gauge_reduction_verified=newtonian_reduction,
        action_binding_established=False,
        dfm_vs_lcdm_prediction_vector_computed=False,
    )
