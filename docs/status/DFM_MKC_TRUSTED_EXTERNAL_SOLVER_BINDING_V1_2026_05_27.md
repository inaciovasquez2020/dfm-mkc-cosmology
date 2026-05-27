DFM-MKC Trusted External Solver Binding V1 — 2026-05-27
Status: TRUSTED_EXTERNAL_SOLVER_BINDING_CONTRACT_SUPPLIED_NO_EXTERNAL_RUN
This supplies DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1 as an external solver binding contract.
Source dependencies
DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1
DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1
Allowed external targets
CLASS-compatible external binding
CAMB-compatible external binding
custom first-party DFM-MKC solver
Binding contract
source_code_commit
environment_lock
input_schema
output_schema
unit_convention
observable_ordering
covariance_alignment
reproducibility_hashes
Adapter requirements
dfm_mkc_background_adapter
dfm_mkc_perturbation_adapter
observable_adapter
diagnostic_adapter
Trust gates
schema_gate
hash_gate
diagnostic_gate
reproducibility_gate
empirical_claim_gate
Boundary
Does not prove:
DFM-MKC external solver adapter implementation
DFM-MKC trusted external solver execution
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
Supply DFM_MKC_EXTERNAL_SOLVER_ADAPTER_IMPLEMENTATION_V1 or DFM_MKC_PRODUCTION_SOLVER_CODE_V1 before any numerical prediction-vector run.
