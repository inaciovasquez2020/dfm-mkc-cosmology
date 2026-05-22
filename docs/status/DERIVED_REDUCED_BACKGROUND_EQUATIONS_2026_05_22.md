# Derived reduced background equations

Status: `DERIVED_REDUCED_BACKGROUND_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL`

Required object filled:

- `DERIVED_REDUCED_BACKGROUND_EQUATIONS`

Input objects:

- `FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL`
- `VARIATIONAL_DERIVATION_CHECK`
- `PARAMETER_DOMAIN_AND_UNITS_TABLE`
- `COSMOLOGICAL_REDUCTION_ANSATZ`
- `FROZEN_PREDICTION_VECTOR`
- `EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON`

Root blocker partially reduced:

- `NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED`

New root blocker:

- `PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED`

Check result:

- `PASS_STRUCTURAL_ONLY`

Boundary:

- supplies structural reduced background equation candidates
- maps each FLRW background target to a reduced equation candidate
- does not prove a full symbolic derivation
- does not supply numerical integration
- does not supply perturbation closure equations
- does not supply numerical parameter values
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

- `PERTURBATION_CLOSURE_EQUATIONS`
- `NUMERICAL_PARAMETER_VECTOR`
- `INITIAL_CONDITIONS`
- `DATA_VECTOR_SCHEMA`
- `COVARIANCE_MATRIX`
- `LIKELIHOOD_RULE`
- `LAMBDA_CDM_BASELINE_VECTOR`
- `INDEPENDENT_EMPIRICAL_VALIDATION`
