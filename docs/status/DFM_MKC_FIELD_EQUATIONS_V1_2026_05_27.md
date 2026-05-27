# DFM-MKC Field Equations V1 — 2026-05-27

Status: `CONCRETE_FIELD_EQUATIONS_DERIVED_PHENOMENOLOGICAL_ONLY`

This file supplies `DFM_MKC_FIELD_EQUATIONS_V1`, the second closed object in the DFM-MKC dark-sector chain.

Source dependency:

```text
DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1
Source artifact:
artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json
Action recalled
L_total =
  (R - 2 Lambda)/(16 pi G)
  - (alpha/2) g^{mu nu} nabla_mu phi nabla_nu phi
  - (beta/2) phi^2 g^{mu nu} nabla_mu theta nabla_nu theta
  - U(phi)
  + L_vis(psi_vis, g)
U(phi) = rho_star + (1/2) m_phi_squared phi^2 + (1/4) lambda_phi phi^4
U_prime(phi) = m_phi_squared phi + lambda_phi phi^3
Metric equation
G_{mu nu} + Lambda g_{mu nu}
  =
8 pi G (T_vis_{mu nu} + T_DFM_MKC_{mu nu})
where
G_{mu nu} = R_{mu nu} - (1/2) R g_{mu nu}
and
T_vis_{mu nu}
  =
-(2/sqrt(-g)) delta(sqrt(-g) L_vis)/delta g^{mu nu}.
The DFM-MKC dark-sector stress-energy tensor is:
T_DFM_MKC_{mu nu}
  =
alpha nabla_mu phi nabla_nu phi
+ beta phi^2 nabla_mu theta nabla_nu theta
- g_{mu nu}[
    (alpha/2)(nabla phi)^2
    + (beta/2) phi^2 (nabla theta)^2
    + U(phi)
  ].
No post-hoc source terms are added.
Rigidity-amplitude equation
alpha Box_g phi - beta phi (nabla theta)^2 - U_prime(phi) = 0
with
Box_g phi = nabla_mu nabla^mu phi.
Structural-phase equation
nabla_mu(beta phi^2 nabla^mu theta) = 0
Equivalently, the phase current
J_theta^mu = beta phi^2 nabla^mu theta
satisfies
nabla_mu J_theta^mu = 0.
The phase theta is interpreted modulo 2 pi; the local field equation is written on a branch chart.
Constraint equations
The covariant conservation constraint is:
nabla^mu [T_vis_{mu nu} + T_DFM_MKC_{mu nu}] = 0.
The phase-current conservation law is:
nabla_mu(beta phi^2 nabla^mu theta) = 0.
A full Hamiltonian/momentum constraint decomposition requires a 3+1 foliation and is not expanded in this covariant V1 object.
Conservation laws
nabla^mu (T_vis_{mu nu} + T_DFM_MKC_{mu nu}) = 0
nabla_mu(beta phi^2 nabla^mu theta) = 0
In this V1 object, visible matter couples through the metric only. Direct non-gravitational exchange with phi or theta is not introduced.
Gauge or coordinate conditions
No coordinate gauge is fixed in the V1 covariant equations.
Metric signature:
(-,+,+,+)
Perturbation gauge choice is deferred to:
DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1
Classical well-posedness is not proved here; standard hyperbolic gauge choices are required for PDE analysis.
Known-limit recovery
Limit:
phi = 0 and rho_star absorbed into Lambda
Recovered equations:
Einstein equations with visible stress-energy and effective cosmological constant.
Limit:
theta constant
Recovered equations:
Einstein gravity coupled to one real scalar phi with potential U(phi).
Limit:
g_{mu nu} -> eta_{mu nu}
Recovered equations:
alpha Box phi - beta phi (partial theta)^2 - U_prime(phi) = 0
and
partial_mu(beta phi^2 partial^mu theta) = 0.
Limit:
alpha = beta = 0 and U(phi) constant
Recovered equations:
No propagating DFM-MKC field equations remain; the dark sector contributes only a vacuum-energy shift.
Derivation status
metric_variation_performed = true
phi_variation_performed = true
theta_variation_performed = true
visible_sector_equation_deferred_to_L_vis = true
derived_without_post_hoc_terms = true
derived_from_closed_action_functional_v1 = true
Acceptance result
This supplies:
DFM_MKC_FIELD_EQUATIONS_V1
The object contains:
metric_equation
dark_sector_equations
constraint_equations
conservation_laws
stress_energy_tensor
gauge_or_coordinate_conditions
known_limit_recovery
Downstream objects still required
DFM_MKC_MATTER_COUPLING_RULE_V1
DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1
DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1
Boundary
Does not prove:
DFM-MKC matter coupling law.
DFM-MKC linear perturbation system.
DFM-MKC ACT Planck DESI prediction vector.
DFM-MKC empirical validation.
Lambda-CDM failure.
Dark matter replacement.
Dark matter is liquid.
Dark matter is solid.
Dark matter is a phase.
Dark energy resolution.
Dark matter resolution.
Gravity closure.
Chronos-RR.
Unrestricted H4.1/FGL.
P vs NP.
Any Clay problem.
Next admissible step
Supply DFM_MKC_MATTER_COUPLING_RULE_V1 as the explicit visible-sector and photon coupling interface.
