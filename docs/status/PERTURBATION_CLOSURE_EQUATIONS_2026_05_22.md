# Perturbation closure equations

Status: `PERTURBATION_CLOSURE_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL`

Required object filled:

- `PERTURBATION_CLOSURE_EQUATIONS`

Input objects:

- `FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL`
- `VARIATIONAL_DERIVATION_CHECK`
- `PARAMETER_DOMAIN_AND_UNITS_TABLE`
- `COSMOLOGICAL_REDUCTION_ANSATZ`
- `FROZEN_PREDICTION_VECTOR`
- `EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON`
- `DERIVED_REDUCED_BACKGROUND_EQUATIONS`

Root blocker removed:

- `PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED`

New root blocker:

- `NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED`

Check result:

- `PASS_STRUCTURAL_ONLY`

Boundary:

- supplies structural perturbation closure equation candidates
- maps growth and CMB symbolic observables to perturbation closure dependencies
- does not prove a full symbolic linearization
- does not supply numerical integration
- does not supply a Boltzmann solver
- does not supply recombination closure
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

- `NUMERICAL_PARAMETER_VECTOR`
- `INITIAL_CONDITIONS`
- `DATA_VECTOR_SCHEMA`
- `COVARIANCE_MATRIX`
- `LIKELIHOOD_RULE`
- `LAMBDA_CDM_BASELINE_VECTOR`
- `INDEPENDENT_EMPIRICAL_VALIDATION`
