# Parameter domain and units table

Status: `PARAMETER_DOMAIN_AND_UNITS_TABLE_SUPPLIED_STRUCTURAL_ONLY`

Required object filled:

- `PARAMETER_DOMAIN_AND_UNITS_TABLE`

Input objects:

- `FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL`
- `VARIATIONAL_DERIVATION_CHECK`

Root blocker removed:

- `PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED`

New root blocker:

- `COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED`

Check result:

- `PASS_STRUCTURAL_ONLY`

Boundary:

- supplies parameter domains and mass-dimension units structurally
- checks that supplied action couplings are represented in the parameter table
- does not prove physical correctness of the parameter choices
- does not supply numerical parameter values
- does not supply a cosmological reduction ansatz
- does not supply a frozen prediction vector
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

- `COSMOLOGICAL_REDUCTION_ANSATZ`
- `FROZEN_PREDICTION_VECTOR`
- `EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON`
- `INDEPENDENT_EMPIRICAL_VALIDATION`
