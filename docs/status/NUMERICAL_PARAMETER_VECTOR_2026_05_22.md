# Numerical parameter vector

Status: `NUMERICAL_PARAMETER_VECTOR_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_FIT`

Required object filled:

- `NUMERICAL_PARAMETER_VECTOR`

Input objects:

- `FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL`
- `VARIATIONAL_DERIVATION_CHECK`
- `PARAMETER_DOMAIN_AND_UNITS_TABLE`
- `COSMOLOGICAL_REDUCTION_ANSATZ`
- `FROZEN_PREDICTION_VECTOR`
- `EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON`
- `DERIVED_REDUCED_BACKGROUND_EQUATIONS`
- `PERTURBATION_CLOSURE_EQUATIONS`

Root blocker removed:

- `NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED`

New root blocker:

- `INITIAL_CONDITIONS_NOT_SUPPLIED`

Check result:

- `PASS_REFERENCE_VECTOR_ONLY`

Boundary:

- supplies a numerical reference parameter vector
- checks domain compatibility against the parameter domain and units table
- does not claim the vector is fit to data
- does not claim physical calibration
- does not supply initial conditions
- does not supply an observable evaluation grid
- does not supply a data vector
- does not supply a covariance matrix
- does not supply a likelihood rule
- does not execute a likelihood comparison
- does not supply empirical evidence

Does not prove:

- DFM-MKC
- Lambda-CDM failure
- dark-energy resolution
- dark-matter resolution
- Nobel-level physical discovery
- any Clay problem

Next missing objects:

- `INITIAL_CONDITIONS`
- `OBSERVABLE_EVALUATION_GRID`
- `DATA_VECTOR_SCHEMA`
- `COVARIANCE_MATRIX`
- `LIKELIHOOD_RULE`
- `LAMBDA_CDM_BASELINE_VECTOR`
- `INDEPENDENT_EMPIRICAL_VALIDATION`
