# DFM-MKC Linear Perturbation System V1 — 2026-05-27

Status: `CONCRETE_LINEAR_PERTURBATION_SYSTEM_SUPPLIED_PHENOMENOLOGICAL_ONLY`

This file supplies `DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1`.

Source dependencies:

```text
DFM_MKC_FIELD_EQUATIONS_V1
DFM_MKC_MATTER_COUPLING_RULE_V1
Source artifacts:
artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json
artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json
Background solution
Spatially flat FLRW background:
ds^2 = a(eta)^2[-deta^2 + delta_ij dx^i dx^j]
Field expansions:
phi(eta, x) = phi_bar(eta) + delta_phi(eta, x)
theta(eta, x) = theta_bar(eta) + delta_theta(eta, x)
rho_vis(eta, x) = rho_vis_bar(eta) + delta_rho_vis(eta, x)
rho_gamma(eta, x) = rho_gamma_bar(eta) + delta_rho_gamma(eta, x)
Conformal Hubble factor:
Hc = a_prime / a
The background equations are inherited from DFM_MKC_FIELD_EQUATIONS_V1 after imposing FLRW symmetry. Explicit numerical background solving is deferred to the prediction-vector object.
Gauge choice
Newtonian gauge:
ds^2 = a(eta)^2[-(1+2 Psi)deta^2 + (1-2 Phi)delta_ij dx^i dx^j]
Scalar metric variables:
Psi
Phi
Vector and tensor modes are not included in V1.
Perturbation variables
Metric variables:
Psi(k, eta)
Phi(k, eta)
DFM-MKC variables:
delta_phi(k, eta)
delta_theta(k, eta)
Visible matter variables:
delta_b(k, eta)
v_b(k, eta)
Radiation variables:
delta_gamma(k, eta)
v_gamma(k, eta)
Linearized equations
Poisson constraint:
k^2 Phi + 3 Hc(Phi_prime + Hc Psi) = -4 pi G a^2 delta_rho_total
Momentum constraint:
k^2(Phi_prime + Hc Psi) = 4 pi G a^2 sum_A[(rho_A + p_A) theta_A]
Anisotropy relation:
k^2(Phi - Psi) = 12 pi G a^2 (rho_total + p_total) sigma_total
DFM-MKC rigidity-amplitude perturbation equation:
alpha[
  delta_phi_double_prime
  + 2 Hc delta_phi_prime
  + (k^2 + a^2 U_double_prime(phi_bar))delta_phi
  - phi_bar_prime(Psi_prime + 3 Phi_prime)
  + 2 a^2 Psi U_prime(phi_bar)
]
- beta[
  delta_phi theta_bar_prime^2
  + 2 phi_bar theta_bar_prime delta_theta_prime
  - 2 phi_bar theta_bar_prime^2 Psi
]
= 0
DFM-MKC phase perturbation equation:
(beta phi_bar^2 delta_theta_prime)_prime
+ 2 beta phi_bar phi_bar_prime delta_theta_prime
+ beta phi_bar^2 k^2 delta_theta
+ metric_source_theta
+ amplitude_source_theta
= 0
Visible baryon continuity:
delta_b_prime = -k v_b + 3 Phi_prime
Visible baryon Euler equation:
v_b_prime + Hc v_b = k Psi + photon_baryon_drag_terms
Photon continuity:
delta_gamma_prime = -(4/3)k v_gamma + 4 Phi_prime
Photon Euler equation:
v_gamma_prime = k(delta_gamma/4 + Psi) + photon_higher_moment_terms
Boltzmann hierarchy closure, recombination physics, and numerical source functions are deferred to the prediction-vector object.
Source terms
delta_rho_total = delta_rho_vis + delta_rho_gamma + delta_rho_DFM_MKC
delta_p_total = delta_p_vis + delta_p_gamma + delta_p_DFM_MKC
delta_rho_DFM_MKC, delta_p_DFM_MKC, and the DFM-MKC momentum perturbation are computed by linearizing T_DFM_MKC_{mu nu} from DFM_MKC_FIELD_EQUATIONS_V1.
Initial conditions
Adiabatic mode template:
All species begin with common primordial curvature perturbation R_star,
with DFM-MKC perturbations initialized consistently with the linearized constraints.
Optional DFM-MKC isocurvature perturbations may be tracked but are not promoted as fit parameters in V1.
The initial-condition rule must be frozen before any data claim.
Transfer functions
Metric transfer functions:
T_Psi(k, eta)
T_Phi(k, eta)
DFM-MKC transfer functions:
T_delta_phi(k, eta)
T_delta_theta(k, eta)
Visible transfer functions:
T_delta_b(k, eta)
T_v_b(k, eta)
T_delta_gamma(k, eta)
T_v_gamma(k, eta)
CMB, lensing, BAO, and matter-power transfer-to-observable maps are downstream prediction-vector objects.
Growth equation
Generic growth form:
delta_m_double_prime + A(k, eta) delta_m_prime + B(k, eta) delta_m = S_DFM_MKC(k, eta)
No numerical f sigma_8 or P(k) prediction is supplied in V1.
Stability conditions
Kinetic signs:
alpha > 0
beta > 0
Principal scalar-sector gradient terms have positive sign under alpha > 0 and beta > 0.
Potential-dependent instabilities depend on U_double_prime(phi_bar) and are not globally ruled out here.
Full well-posedness is not proved here.
CMB observable mapping
Temperature source status: deferred to DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1.
Polarization source status: deferred to DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1.
CMB lensing status: deferred to DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1.
No CMB fit claim is made.
Matter-power mapping
Linear matter power status: deferred to DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1.
BAO mapping status: deferred to DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1.
Weak-lensing mapping status: deferred to DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1.
No matter-power fit claim is made.
Acceptance result
This supplies:
DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1
The object contains:
background_solution
perturbation_variables
gauge_choice
linearized_equations
initial_conditions
transfer_functions
growth_equation
stability_conditions
cmb_observable_mapping
matter_power_mapping
Downstream objects still required
DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1
DFM_MKC_DATA_COMPARISON_PROTOCOL_V1
Boundary
Does not prove:
DFM-MKC ACT Planck DESI prediction vector
DFM-MKC data comparison
DFM-MKC empirical validation
Lambda-CDM failure
dark matter replacement
dark matter is liquid
dark matter is solid
dark matter is a phase
galaxy rotation curve fit
CMB fit
BAO fit
weak lensing fit
Bullet Cluster explanation
linear perturbation numerical solution
Boltzmann solver implementation
matter power spectrum fit
cosmic shear fit
dark energy resolution
dark matter resolution
gravity closure
Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay problem
Next admissible step
Supply DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1 from the linear perturbation system.
