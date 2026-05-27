DFM-MKC Data Comparison Protocol V1 — 2026-05-27
Status: DATA_COMPARISON_PROTOCOL_SUPPLIED_NO_EMPIRICAL_RUN
This supplies DFM_MKC_DATA_COMPARISON_PROTOCOL_V1.
Source dependency
DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1
Declared datasets
ACT DR6
Planck
DESI BAO
matter power
weak lensing
Comparison contract
baseline_model = LCDM baseline prediction vector with matched dataset schema
candidate_model = DFM-MKC prediction vector with matched dataset schema
schema_requirement = shared observable names, ordering, units, masks, covariance convention, and redshift or ell indexing
covariance_requirement = explicit covariance matrix or likelihood object before scoring
blindness_requirement = frozen parameter choices and model-selection criteria before empirical scoring
reproducibility_requirement = recorded hashes, code versions, solver settings, and parameter files
Metrics
chi2
delta_chi2
log_likelihood
delta_log_likelihood
AIC
BIC
residual_vector
whitened_residual_vector
covariance_condition_number
pull_distribution
jackknife_or_split_stability
No metric values are computed here.
Boundary
Does not prove:
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
Supply DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1 or a trusted external solver-binding object before any likelihood run.
