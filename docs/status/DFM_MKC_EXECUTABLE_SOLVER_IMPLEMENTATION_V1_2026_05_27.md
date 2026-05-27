# DFM-MKC Executable Solver Implementation V1 — 2026-05-27

Status: `EXECUTABLE_SOLVER_IMPLEMENTATION_CONTRACT_SUPPLIED_NO_NUMERICAL_RUN`

This supplies `DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1` as an executable implementation contract.

## Source dependencies

```text
DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1
DFM_MKC_FIELD_EQUATIONS_V1
DFM_MKC_MATTER_COUPLING_RULE_V1
DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1
DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1
DFM_MKC_DATA_COMPARISON_PROTOCOL_V1
DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1
Implementation units
background_solver_module
perturbation_solver_module
constraint_monitor_module
transfer_projection_module
diagnostics_module
artifact_writer_module
Entrypoints
dfm_mkc_solve_background(config_path)
dfm_mkc_solve_perturbations(background_artifact_path, config_path)
dfm_mkc_project_observables(transfer_artifact_path, config_path)
dfm_mkc_validate_solver_outputs(output_artifact_path, tolerance_config_path)
dfm_mkc_run_prediction_vector(config_path)
Entrypoint signatures are specified but no numerical run is performed here.
Boundary
Does not prove:
DFM-MKC production solver code
DFM-MKC numerical integration run
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
Supply DFM_MKC_PRODUCTION_SOLVER_CODE_V1 or run a trusted external solver binding before any numerical prediction-vector run.
