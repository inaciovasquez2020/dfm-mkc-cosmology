# Data vector schema

Status: `DATA_VECTOR_SCHEMA_SUPPLIED_SCHEMA_ONLY_NO_EMPIRICAL_VALUES`

Required object filled:

- `DATA_VECTOR_SCHEMA`

Input objects:

- `FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL`
- `VARIATIONAL_DERIVATION_CHECK`
- `PARAMETER_DOMAIN_AND_UNITS_TABLE`
- `COSMOLOGICAL_REDUCTION_ANSATZ`
- `FROZEN_PREDICTION_VECTOR`
- `EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON`
- `DERIVED_REDUCED_BACKGROUND_EQUATIONS`
- `PERTURBATION_CLOSURE_EQUATIONS`
- `NUMERICAL_PARAMETER_VECTOR`
- `INITIAL_CONDITIONS`
- `OBSERVABLE_EVALUATION_GRID`

Root blocker removed:

- `DATA_VECTOR_SCHEMA_NOT_SUPPLIED`

New root blocker:

- `COVARIANCE_MATRIX_NOT_SUPPLIED`

Check result:

- `PASS_SCHEMA_ONLY`

Boundary:

- supplies a data vector schema only
- checks slot coverage against the frozen prediction vector and observable evaluation grids
- does not supply empirical data values
- does not supply observational uncertainties
- does not bind slots to an external payload
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

- `COVARIANCE_MATRIX`
- `LIKELIHOOD_RULE`
- `LAMBDA_CDM_BASELINE_VECTOR`
- `INDEPENDENT_EMPIRICAL_VALIDATION`
