# ACT DR6 Baseline LCDM Official Source Provenance Readiness — 2026-05-25

Status: `BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY_NO_VECTOR_PROMOTION`

## Added object

`OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE`

## Promotion scope

Extraction readiness only.

Explicitly not promoted to:

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Official sources

- `NASA_LAMBDA_ACT_DR6_02_PSPIPE_BEST_FITS_INFO`
- `NASA_LAMBDA_ACT_DR6_02_PSPIPE_BEST_FITS_DOWNLOADS`
- `NASA_LAMBDA_ACT_DR6_02_CHAINS_INFO`
- `ACT_DR6_PARAMETERS_REPOSITORY`

## Digest-bound execution record

Status: `SOURCE_AND_CONFIGURATION_DIGEST_BOUND_EXECUTION_NOT_RUN_HERE`

The official source route records:

- CAMB best-fit generation source;
- CAMB version: `1.5.9`;
- ACT DR6 LCDM cosmological parameters;
- NASA LAMBDA Pspipe best-fit source digests;
- ACT DR6 Cobaya parameter repository HEAD commit.

## Row-order binding against ACT DR6 ordering

Status: `EXTRACTION_RULE_READY_BINDING_NOT_YET_APPLIED_TO_VECTOR`

An extraction script must map official best-fit spectra columns into the exact ACT DR6 CMB-only SACC row order before constructing `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`.

## Not-observed-data-vector certificate

Status: `SOURCE_CLASS_SEPARATION_CERTIFIED_FOR_OFFICIAL_SOURCE`

The official source class is LCDM best-fit power spectra generated with CAMB v1.5.9, not an observed ACT DR6 data-vector artifact.

The prior shape-compatible local candidate was rejected as data-vector-derived and remains non-promoted.

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Next admissible object

`ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS`

## Boundary

This is a source-provenance and extraction-readiness record only.

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
