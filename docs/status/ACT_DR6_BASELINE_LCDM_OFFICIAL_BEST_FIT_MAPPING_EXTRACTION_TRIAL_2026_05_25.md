# ACT DR6 Baseline LCDM Official Best-Fit Mapping Extraction Trial — 2026-05-25

Status: `OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_BLOCKED_NO_CERTIFIED_ROW_MAPPING` or `OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_RAN_VECTOR_CANDIDATE_NOT_PROMOTED`

## Added object

`ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL`

## Inputs supplied

- official NASA LAMBDA ACT DR6 LCDM best-fit spectra tarball;
- ACT DR6 CMB-only SACC row-order metadata when locally available;
- combined numeric best-fit table;
- explicit row-mapping trial artifact;
- extraction audit trial artifact.

## Row mapping rule

The trial may construct `row_mapping` only if every ACT DR6 CMB-only target row has:

- inferable spectrum label;
- inferable scalar ell;
- unique official best-fit source row;
- unique source column;
- full target-index coverage.

## Promotion rule

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR` is not promoted by this record.

## Boundary

This is a mapping/extraction trial only.

It does not prove a baseline LCDM prediction vector exists.
It does not promote a baseline LCDM prediction vector.
It does not prove a baseline LCDM prediction vector is fully row-audited.
It does not prove a baseline LCDM prediction vector is physically correct.
It does not provide a DFM-MKC prediction vector.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- baseline LCDM prediction vector exists;
- baseline LCDM prediction vector has been promoted;
- baseline LCDM prediction vector is fully row-audited;
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
