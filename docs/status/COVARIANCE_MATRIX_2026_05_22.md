# Covariance matrix

Status: `COVARIANCE_MATRIX_SUPPLIED_REFERENCE_DIAGONAL_ONLY_NOT_EMPIRICAL`

Required object filled:

- `COVARIANCE_MATRIX`

Root blocker removed:

- `COVARIANCE_MATRIX_NOT_SUPPLIED`

New root blocker:

- `LIKELIHOOD_RULE_NOT_SUPPLIED`

Check result:

- `PASS_REFERENCE_DIAGONAL_MATRIX_ONLY`

Boundary:

- supplies a reference diagonal covariance matrix
- checks covariance slot order against the data vector schema
- does not supply empirical covariance
- does not bind covariance to an external payload
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

- `LIKELIHOOD_RULE`
- `LAMBDA_CDM_BASELINE_VECTOR`
- `INDEPENDENT_EMPIRICAL_VALIDATION`
