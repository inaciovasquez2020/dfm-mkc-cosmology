"""Ten measurement operators independently bound to the fixed scalar action."""

from __future__ import annotations

from dataclasses import dataclass
import math

import sympy as sp

from . import scalar_constraint_variational_bridge_v1 as bridge
from . import visible_sector_action_v1 as visible


DFM_VS_LCDM_SEPARATION_PROVED = False
OBSERVATIONAL_DETECTABILITY_PROVED = False
NOVEL_PHYSICS_ESTABLISHED = False


@dataclass(frozen=True)
class PredictionComponent:
    name: str
    symbolic_expression: sp.Expr
    measurement_channel: str
    action_provenance: tuple[str, ...]
    domain_assumptions: tuple[str, ...]
    units_or_convention: str
    exact_binding_established: bool
    provenance_residuals: tuple[sp.Expr, ...]
    background_substitutions: tuple[str, ...] = ()
    source_evolution_equations: tuple[str, ...] = ()
    measurement_operator: str = ""


@dataclass(frozen=True)
class ActionBoundPredictionVector:
    components: tuple[PredictionComponent, ...]
    prediction_names: tuple[str, ...]
    symbolic_vector: tuple[sp.Expr, ...]
    numeric_vector: tuple[float, ...] | None
    action_binding_established: bool


@dataclass(frozen=True)
class PredictionState:
    wave_number: float
    scale_factor: float
    conformal_hubble: float
    gravitational_constant: float
    delta_rho_total: float
    momentum_source: float
    baryon_velocity_divergence: float
    source_distance: float
    lens_distance: float
    transverse_wave_number: float

    def __post_init__(self):
        for field_name, value in self.__dict__.items():
            if not math.isfinite(value):
                raise ValueError(f"{field_name} must be finite")
        if self.wave_number == 0:
            raise ValueError("wave_number must be nonzero")
        if self.scale_factor <= 0:
            raise ValueError("scale_factor must be positive")
        if self.gravitational_constant <= 0:
            raise ValueError("gravitational_constant must be positive")
        if self.source_distance <= 0:
            raise ValueError("source_distance must be positive")
        if not 0 < self.lens_distance < self.source_distance:
            raise ValueError("lens_distance must satisfy 0 < lens_distance < source_distance")


def _build_components() -> tuple[PredictionComponent, ...]:
    certificate = bridge.fixed_action_source_domain_binding_certificate()
    k2, a, H, G, drho, mom = sp.symbols(
        "k2 a H G delta_rho_total momentum_source", nonzero=True
    )
    theta_b, chi_s, chi, k_perp = sp.symbols(
        "theta_b chi_s chi k_perp", nonzero=True
    )
    eliminator = bridge.symbolic_metric_constraint_elimination(
        wave_number_squared=k2, scale_factor=a, conformal_hubble=H,
        gravitational_constant=G, delta_rho_total=drho,
        momentum_source=mom, enthalpy_sigma_total=sp.Integer(0),
    )
    B, E_prime, sigma_prime = sp.symbols("B E_prime sigma_prime")
    definitions = bridge.bardeen_weyl_definitions(
        lapse_potential=eliminator.solution["Psi"],
        curvature_potential=eliminator.solution["Phi"],
        scalar_shift=B, spatial_shear_prime=E_prime,
        scalar_shear_prime=sigma_prime, conformal_hubble=H,
    )
    chart = {B: 0, E_prime: 0, sigma_prime: 0}
    psi_b = sp.cancel(definitions.bardeen_lapse_potential.xreplace(chart))
    phi_b = sp.cancel(definitions.bardeen_curvature_potential.xreplace(chart))
    weyl = sp.cancel(definitions.weyl_potential_sum.xreplace(chart))
    delta_comoving = drho + 3 * H * mom / k2
    slip = sp.cancel(phi_b / psi_b)
    response = sp.cancel(weyl / delta_comoving)
    # Use the production eliminator's canonical momentum-chart Phi_prime.
    isw = sp.cancel(eliminator.solution["Phi_prime"] * 2)
    euler = visible.pressureless_baryon_euler_equation(
        wave_number_squared=k2, conformal_hubble=H,
        bardeen_lapse_potential=psi_b, velocity_divergence=theta_b,
    )
    convergence = bridge.thin_plane_convergence_integrand(
        weyl_sum=weyl, source_distance=chi_s, lens_distance=chi,
        transverse_wave_number=k_perp,
    )
    # Preserve both independently constructed operands in the exported tree.
    joint = sp.Mul(
        convergence,
        sp.Pow(euler.gravitational_force, -1, evaluate=False),
        evaluate=False,
    )

    expected_lensing = sp.cancel(
        -sp.Rational(1, 2) * chi * (chi_s-chi) / chi_s * k_perp**2 * weyl
    )
    metric_residuals = tuple(certificate.normalized_row_residuals.values())
    bardeen_residuals = tuple(certificate.bardeen_identity_residuals.values())
    momentum_residuals = (
        certificate.phi_prime_action_row_residual,
        certificate.eliminator_momentum_identity_residual,
        certificate.momentum_chart_identity_residual,
    )
    euler_residuals = (
        euler.force_coefficient_residual,
        euler.hubble_drag_coefficient_residual,
    )
    lensing_residuals = (sp.cancel(convergence - expected_lensing),)
    poisson_residual = sp.cancel(
        k2 * weyl + 8 * sp.pi * G * a**2 * delta_comoving
    )
    shared_exact = bool(
        certificate.action_binding_established
        and all(x == 0 for x in metric_residuals + bardeen_residuals)
    )
    dynamics_exact = bool(
        shared_exact and euler.fourier_sign_and_normalization_proved
        and all(x == 0 for x in euler_residuals)
    )
    lensing_exact = bool(
        shared_exact and all(x == 0 for x in lensing_residuals)
    )
    common_provenance = (
        "fixed_action_source_domain_binding_certificate",
        "canonical metric Euler rows",
        "symbolic_metric_constraint_elimination",
        "bardeen_weyl_definitions",
    )
    domain = certificate.domain_assumptions + (
        "Newtonian scalar chart B=E=0",
        "fixed-action source image; enthalpy_sigma_total=0",
    )
    specs = (
        ("Psi_B", psi_b, "relativistic clustering", domain, "dimensionless",
         "production Bardeen lapse", shared_exact, metric_residuals+bardeen_residuals, ()),
        ("Phi_B", phi_b, "spatial curvature", domain, "dimensionless",
         "production Bardeen curvature", shared_exact, metric_residuals+bardeen_residuals, ()),
        ("W_plus", weyl, "weak/CMB lensing", domain, "dimensionless",
         "production Weyl sum", shared_exact, metric_residuals+bardeen_residuals, ()),
        ("eta_slip", slip, "gravitational slip", domain+("Psi_B != 0",),
         "dimensionless", "Phi_B/Psi_B", shared_exact and slip == 1,
         metric_residuals+bardeen_residuals+(sp.cancel(slip-1),), ()),
        ("Sigma_Weyl", response, "comoving lensing response",
         domain+("Delta_comoving != 0",), "potential / comoving density",
         "W_plus/Delta_comoving", shared_exact and poisson_residual == 0,
         metric_residuals+bardeen_residuals+(poisson_residual,), ()),
        ("S_ISW", isw, "ISW cross-correlations", domain,
         "inverse conformal time", "2*production Phi_prime",
         shared_exact and all(x == 0 for x in momentum_residuals),
         metric_residuals+bardeen_residuals+momentum_residuals,
         ("canonical momentum chart: Phi_B'=P-H*Psi_B",)),
        ("A_pec", euler.gravitational_force, "peculiar acceleration", domain,
         "inverse conformal-length squared", "fixed-action baryon Euler force",
         dynamics_exact, metric_residuals+bardeen_residuals+euler_residuals,
         ("theta_b'=-H*theta_b+k2*Psi_B",)),
        ("theta_b_prime", euler.velocity_divergence_prime, "velocity evolution",
         domain, "inverse conformal time squared", "fixed-action baryon Euler row",
         dynamics_exact, metric_residuals+bardeen_residuals+euler_residuals,
         ("theta_b'=-H*theta_b+k2*Psi_B; no collision in fixed action",)),
        ("K_kappa", convergence, "weak-lensing convergence",
         domain+("chi_s > 0", "0 < chi < chi_s"), "per comoving length",
         "production thin-plane lensing operator", lensing_exact,
         metric_residuals+bardeen_residuals+lensing_residuals, ()),
        ("K_kappa_over_A_pec", joint, "dynamics-lensing consistency",
         domain+("chi_s > 0", "0 < chi < chi_s", "A_pec != 0"),
         "convergence integrand / acceleration", "K_kappa/A_pec",
         dynamics_exact and lensing_exact,
         metric_residuals+bardeen_residuals+euler_residuals+lensing_residuals, ()),
    )
    return tuple(PredictionComponent(
        name=n, symbolic_expression=e, measurement_channel=c,
        action_provenance=common_provenance + (
            (euler.action_origin,) if n in ("A_pec", "theta_b_prime", "K_kappa_over_A_pec") else ()
        ), domain_assumptions=d, units_or_convention=u,
        exact_binding_established=bool(exact and all(r == 0 for r in residuals)),
        provenance_residuals=residuals,
        background_substitutions=certificate.background_equations_used,
        source_evolution_equations=source, measurement_operator=op,
    ) for n, e, c, d, u, op, exact, residuals, source in specs)


def action_bound_prediction_vector(state: PredictionState | None = None):
    components = _build_components()
    exact = len(components) == 10 and all(
        c.exact_binding_established and all(r == 0 for r in c.provenance_residuals)
        for c in components
    )
    numeric = None
    if state is not None:
        substitutions = {
            sp.Symbol("k2", nonzero=True): state.wave_number**2,
            sp.Symbol("a", nonzero=True): state.scale_factor,
            sp.Symbol("H", nonzero=True): state.conformal_hubble,
            sp.Symbol("G", nonzero=True): state.gravitational_constant,
            sp.Symbol("delta_rho_total", nonzero=True): state.delta_rho_total,
            sp.Symbol("momentum_source", nonzero=True): state.momentum_source,
            sp.Symbol("theta_b", nonzero=True): state.baryon_velocity_divergence,
            sp.Symbol("chi_s", nonzero=True): state.source_distance,
            sp.Symbol("chi", nonzero=True): state.lens_distance,
            sp.Symbol("k_perp", nonzero=True): state.transverse_wave_number,
        }
        values = []
        for component in components:
            value = component.symbolic_expression.subs(substitutions)
            if value.free_symbols:
                raise ValueError(f"missing numeric parameters: {sorted(map(str, value.free_symbols))}")
            number = float(value)
            if not math.isfinite(number):
                raise ValueError(f"{component.name} is undefined for supplied state")
            values.append(number)
        numeric = tuple(values)
    return ActionBoundPredictionVector(
        components=components, prediction_names=tuple(x.name for x in components),
        symbolic_vector=tuple(x.symbolic_expression for x in components),
        numeric_vector=numeric, action_binding_established=exact,
    )


_INITIAL_VECTOR = action_bound_prediction_vector()
prediction_names = _INITIAL_VECTOR.prediction_names
symbolic_vector = _INITIAL_VECTOR.symbolic_vector
PREDICTIONS_DERIVED = sum(c.exact_binding_established for c in _INITIAL_VECTOR.components)
TEN_ACTION_BOUND_PREDICTIONS_DERIVED = bool(
    PREDICTIONS_DERIVED == 10 and _INITIAL_VECTOR.action_binding_established
)
# Numeric evaluability is independently exercised before this is true.
_NUMERIC_PROBE = PredictionState(2, 1.5, .7, 1/(8*math.pi), .4, .2, .3, 10, 4, 1.5)
MEASURABLE_PREDICTION_VECTOR_COMPUTED = bool(
    TEN_ACTION_BOUND_PREDICTIONS_DERIVED
    and len(action_bound_prediction_vector(_NUMERIC_PROBE).numeric_vector or ()) == 10
)


def numeric_vector(state: PredictionState) -> tuple[float, ...]:
    result = action_bound_prediction_vector(state)
    assert result.numeric_vector is not None
    return result.numeric_vector
