# ACT DR6 Empirical Payload Candidate — 2026-05-25

Status: `EMPIRICAL_PAYLOAD_CANDIDATE_ONLY_NO_DATA_IMPORTED`

This record adds ACT DR6 as the first empirical payload candidate for future DFM-MKC residual eigenspace and covariance/spectral validation.

## Added object

`ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE`

## Source pointers

- ACT DR6 data products: `https://act.princeton.edu/act-dr6-data-products`
- NASA LAMBDA ACT DR6.02: `https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/`
- NASA LAMBDA ACT DR6.02 chains info: `https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_chains_info.html`
- ACT DR6 full likelihood code: `https://github.com/ACTCollaboration/act_dr6_mflike`
- ACT DR6 CMB-only likelihood code: `https://github.com/ACTCollaboration/DR6-ACT-lite`
- ACT DR6 notebooks: `https://github.com/ACTCollaboration/DR6_Notebooks/tree/main`
- ACT DR6 NERSC chains: `https://portal.nersc.gov/project/act/dr6.02/chains/`

## Payload slots to fill later

- `dataset_id`
- `dataset_release`
- `source_url_or_release_doi`
- `payload_sha256`
- `data_vector_path`
- `covariance_matrix_path`
- `baseline_prediction_vector_path`
- `candidate_prediction_vector_path`
- `nuisance_parameter_table_path`
- `likelihood_configuration_path`
- `reproduction_command`
- `schema_validation_report_path`

## Candidate validation checks to run later

- `source_payload_downloaded_or_bound`
- `payload_sha256_verified`
- `data_vector_loaded`
- `covariance_matrix_loaded`
- `data_covariance_dimensions_match`
- `covariance_is_symmetric`
- `covariance_is_positive_semidefinite_or_regularized_with_certificate`
- `baseline_lcdm_prediction_vector_loaded_or_generated`
- `dfm_mkc_candidate_prediction_vector_loaded_or_generated`
- `residual_vectors_constructible`
- `residual_eigenspace_diagnostic_runnable`
- `boundary_covariance_failure_guard_passed`
- `independent_reproduction_command_supplied`

## Promotion boundary

Even after payload binding, the strongest allowed status is:

`EMPIRICAL_TEST_READY_NOT_VALIDATED`

Physical dark-matter phase claims remain:

`HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- ACT DR6 data has been downloaded;
- ACT DR6 payload has been verified;
- ACT DR6 likelihood has been executed;
- DFM-MKC empirical validation;
- Lambda-CDM failure;
- dark matter is liquid;
- dark matter is solid;
- dark matter phase transition is physically real;
- dark matter resolution;
- dark energy resolution;
- CMB validation;
- ACT validation;
- independent empirical replication;
- gravity closure;
- Chronos proof input;
- Chronos-RR;
- H4.1/FGL;
- P vs NP;
- any Clay problem.
