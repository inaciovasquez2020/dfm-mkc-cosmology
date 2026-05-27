# DFM-MKC Matter Coupling Rule V1 — 2026-05-27

Status: `CONCRETE_MATTER_COUPLING_RULE_SUPPLIED_PHENOMENOLOGICAL_ONLY`

This file supplies `DFM_MKC_MATTER_COUPLING_RULE_V1`, the explicit visible-sector and photon coupling interface after `DFM_MKC_FIELD_EQUATIONS_V1`.

Source dependency:

```text
DFM_MKC_FIELD_EQUATIONS_V1
Source artifact:
artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json
Coupling principle
Visible matter and photons couple to the spacetime metric g_{mu nu}.
They do not directly couple to phi or theta in V1.
The DFM-MKC sector affects visible matter and light only through the metric equation:
G_{mu nu} + Lambda g_{mu nu}
  =
8 pi G (T_vis_{mu nu} + T_DFM_MKC_{mu nu})
V1 introduces:
direct_phi_visible_coupling = false
direct_theta_visible_coupling = false
dataset_tuned_couplings_allowed = false
Ordinary matter coupling
Visible matter is coupled by:
S_vis[psi_vis, g]
  =
int_M d^4x sqrt(-g) L_vis(psi_vis, g)
Visible stress-energy is:
T_vis_{mu nu}
  =
-(2/sqrt(-g)) delta(sqrt(-g) L_vis)/delta g^{mu nu}
Visible equations are:
delta S_vis / delta psi_vis = 0
In the freely falling massive test-particle limit:
u^mu nabla_mu u^nu = 0
Photon coupling
Photon coupling may be represented by the standard minimally coupled Maxwell action:
S_EM[A, g]
  =
int_M d^4x sqrt(-g) [-(1/4) F_{mu nu} F^{mu nu}]
with
F_{mu nu} = nabla_mu A_nu - nabla_nu A_mu
In the geometric-optics limit:
k^mu k_mu = 0
and
k^mu nabla_mu k^nu = 0
Thus photons follow null geodesics of g_{mu nu}.
V1 introduces:
direct_phi_photon_coupling = false
direct_theta_photon_coupling = false
Stress-energy exchange rule
Total conservation:
nabla^mu (T_vis_{mu nu} + T_DFM_MKC_{mu nu}) = 0
Visible conservation in V1:
nabla^mu T_vis_{mu nu} = 0
when the visible equations hold and L_vis is diffeomorphism invariant.
Dark-sector conservation in V1:
nabla^mu T_DFM_MKC_{mu nu} = 0
when the phi and theta equations hold.
Direct exchange current:
Q_nu = 0
Equivalence principle status
The weak equivalence principle is preserved at the V1 matter-coupling level through universal metric coupling for visible test bodies.
The Einstein equivalence principle is preserved for visible-sector local nongravitational physics under standard minimal-coupling assumptions.
V1 introduces no screening or environment-dependent visible-sector coupling.
Lensing rule
Lensing is metric lensing.
Photons follow null geodesics of g_{mu nu}.
DFM-MKC affects lensing only by changing the metric solution through T_DFM_MKC_{mu nu}.
Weak-lensing, strong-lensing, cluster-offset, and Bullet-Cluster-type comparisons require later solved backgrounds and prediction vectors.
Baryonic limit
Baryonic matter follows the visible-sector equations from:
L_vis(psi_vis, g)
Baryons feel the DFM-MKC sector only through the gravitational metric sourced by:
T_DFM_MKC_{mu nu}
Galaxy rotation curves are not predicted here; they require a solved metric and matter distribution in a later prediction object.
Radiation limit
Radiation uses standard minimally coupled photon stress-energy.
Photons remain null with respect to g_{mu nu}.
V1 introduces no direct dispersion modification and no frequency-dependent lensing.
Downstream pipeline targets
The next stages remain locked:
DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1
DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1
DFM_MKC_DATA_COMPARISON_PROTOCOL_V1
Acceptance result
This supplies:
DFM_MKC_MATTER_COUPLING_RULE_V1
The object contains:
ordinary_matter_coupling
photon_coupling
geodesic_or_optical_rule
stress_energy_exchange_rule
equivalence_principle_status
lensing_prediction_rule
baryonic_limit
radiation_limit
Boundary
Does not prove:
DFM-MKC linear perturbation system.
DFM-MKC ACT Planck DESI prediction vector.
DFM-MKC data comparison.
DFM-MKC empirical validation.
Lambda-CDM failure.
Dark matter replacement.
Dark matter is liquid.
Dark matter is solid.
Dark matter is a phase.
Galaxy rotation curve fit.
CMB fit.
BAO fit.
Weak lensing fit.
Bullet Cluster explanation.
Dark energy resolution.
Dark matter resolution.
Gravity closure.
Chronos-RR.
Unrestricted H4.1/FGL.
P vs NP.
Any Clay problem.
Next admissible step
Supply DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1 from the field equations and matter coupling rule.
