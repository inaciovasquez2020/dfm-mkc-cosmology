# Initial conditions

Status: `INITIAL_CONDITIONS_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_CONSTRAINT_SOLVED`

Required object filled:

- `INITIAL_CONDITIONS`

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

Root blocker removed:

- `INITIAL_CONDITIONS_NOT_SUPPLIED`

New root blocker:

- `OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED`

Check result:

- `PASS_REFERENCE_INITIAL_CONDITIONS_ONLY`

Boundary:

- supplies reference background and perturbation initial conditions
- checks finite-value and basic domain admissibility
- does not claim the initial conditions solve the background constraints
- does not claim the initial conditions solve perturbation mode constraints
- does not claim the initial conditions are fit to data
- does not claim physical calibration
- does not supply numerical integration
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

- `OBSERVABLE_EVALUATION_GRID`
- `DATA_VECTOR_SCHEMA`
- `COVARIANCE_MATRIX`
- `LIKELIHOOD_RULE`
- `LAMBDA_CDM_BASELINE_VECTOR`
- `INDEPENDENT_EMPIRICAL_VALIDATION`
