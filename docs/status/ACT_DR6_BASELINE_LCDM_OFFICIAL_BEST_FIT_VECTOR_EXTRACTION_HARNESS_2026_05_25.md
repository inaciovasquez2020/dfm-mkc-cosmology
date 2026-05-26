# ACT DR6 Baseline LCDM Official Best-Fit Vector Extraction Harness — 2026-05-25

Status: `EXTRACTION_HARNESS_ONLY_NO_BASELINE_VECTOR_EXTRACTED`

## Added object

`ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS`

## Harness script

`tools/extract_act_dr6_baseline_lcdm_official_best_fit_vector.py`

## Target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Required inputs to execute

- official NASA LAMBDA ACT DR6/P-ACT LCDM best-fit spectra text file;
- explicit JSON row mapping from best-fit spectra table entries to ACT DR6 CMB-only SACC row indices.

## Harness checks

- official best-fit file exists;
- mapping file exists;
- mapping covers every certified target row exactly once;
- source row and column indices are in range;
- extracted vector shape equals `required_prediction_vector_shape`;
- best-fit file digest is frozen;
- mapping file digest is frozen;
- extracted vector digest is frozen;
- candidate remains non-promoted pending row-order audit.

## Row-order binding status

`HARNESS_CAN_BIND_BY_EXPLICIT_MAPPING_ROW_AUDIT_STILL_REQUIRED`

## Not-observed-data-vector certificate status

`HARNESS_SOURCE_CLASS_SEPARATION_READY`

## Allowed next status after successful extraction

`BASELINE_LCDM_EXTRACTED_VECTOR_CANDIDATE_READY_FOR_ROW_ORDER_AUDIT`

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is an extraction harness only.

It does not provide a baseline LCDM prediction vector.
It does not extract a baseline LCDM prediction vector.
It does not prove a baseline LCDM prediction vector is row-aligned.
It does not prove a baseline LCDM prediction vector is physically correct.
It does not provide a DFM-MKC prediction vector.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- baseline LCDM prediction vector exists;
- baseline LCDM prediction vector has been extracted;
- baseline LCDM prediction vector is row-aligned;
- baseline LCDM prediction vector is physically correct;
- DFM-MKC prediction vector exists;
- DFM-MKC prediction vector is correct;
- ACT DR6 residual eigenspace empirical comparison has been run;
- DFM-MKC empirical validation;
- Lambda-CDM failure;
- dark matter resolution;
- dark energy resolution;
- dark matter is liquid;
- dark matter is solid;
- dark matter phase transition is physically real;
- ACT validation of DFM-MKC;
- CMB validation of DFM-MKC;
- independent empirical replication;
- gravity closure;
- Chronos-RR;
- H4.1/FGL;
- P vs NP;
- any Clay problem.
