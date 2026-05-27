# DFM-MKC Numerical Boltzmann Solver V1 — 2026-05-27

Status: `SOLVER_INTERFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION`

This supplies `DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1` as a solver interface and implementation contract.

## Source dependencies

```text
DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1
DFM_MKC_FIELD_EQUATIONS_V1
DFM_MKC_MATTER_COUPLING_RULE_V1
DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1
DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1
DFM_MKC_DATA_COMPARISON_PROTOCOL_V1
Solver inputs
a(eta)
Hc(eta)
phi_bar(eta)
theta_bar(eta)
rho_vis_bar(eta)
rho_gamma_bar(eta)
rho_DFM_MKC_bar(eta)
Psi(k, eta)
Phi(k, eta)
delta_phi(k, eta)
delta_theta(k, eta)
delta_b(k, eta)
v_b(k, eta)
delta_gamma(k, eta)
v_gamma(k, eta)
k_grid
eta_grid
ell_grid
redshift_grid
Equation blocks
background_ode_block
metric_constraint_block
dfm_mkc_scalar_block
visible_matter_block
radiation_block
closure_block
Required numerical methods
adaptive ODE integrator
constraint residual monitoring
hierarchy truncation rule
transfer-function interpolation rule
grid refinement stability checks
ell_max convergence checks
k_grid convergence checks
eta_grid convergence checks
Required solver outputs
T_Psi(k, eta)
T_Phi(k, eta)
T_delta_phi(k, eta)
T_delta_theta(k, eta)
T_delta_b(k, eta)
T_v_b(k, eta)
T_delta_gamma(k, eta)
T_v_gamma(k, eta)
C_ell_TT_ACT
C_ell_TE_ACT
C_ell_EE_ACT
C_ell_lensing_ACT
C_ell_TT_Planck
C_ell_TE_Planck
C_ell_EE_Planck
C_ell_lensing_Planck
D_M_over_r_d
D_H_over_r_d
D_V_over_r_d
P_k_linear
sigma8
f_sigma8
C_ell_shear
constraint_residuals
stability_summary
grid_convergence_summary
solver_version
input_hashes
output_hashes
No numerical outputs are produced here.
External solver binding option
Allowed targets:
CLASS-compatible external binding
CAMB-compatible external binding
custom first-party DFM-MKC solver
Required binding fields:
source_code_commit
environment_lock
input_schema
output_schema
unit_convention
observable_ordering
covariance_alignment
reproducibility_hashes
No trusted external solver binding is supplied here.
Boundary
Does not prove:
DFM-MKC executable Boltzmann solver
DFM-MKC trusted external solver binding
DFM-MKC numerical prediction vector
DFM-MKC data comparison run
DFM-MKC likelihood improvement
DFM-MKC empirical validation
Lambda-CDM failure
dark matter replacement
dark matter is liquid
dark matter is solid
dark matter is a phase
galaxy rotation curve fit
CMB fit
ACT fit
Planck fit
DESI fit
BAO fit
weak lensing fit
Bullet Cluster explanation
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
Supply DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1 or DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1 before any numerical prediction-vector run.
