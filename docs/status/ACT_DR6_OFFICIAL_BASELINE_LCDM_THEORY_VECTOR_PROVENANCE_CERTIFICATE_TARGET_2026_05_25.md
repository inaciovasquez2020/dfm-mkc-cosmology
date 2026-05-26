# ACT DR6 Official Baseline LCDM Theory Vector Provenance Certificate Target — 2026-05-25

Status: `PROVENANCE_CERTIFICATE_TARGET_ONLY_OFFICIAL_THEORY_VECTOR_SOURCE_MISSING`

## Added object

`OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE_TARGET`

## Target missing object

`OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE`

## Ultimate target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Purpose

This record specifies the exact provenance certificate required before any baseline LCDM prediction vector can be promoted.

## Required certificate fields

- `official_likelihood_source`
- `official_parameter_or_bestfit_source`
- `camb_or_cobaya_execution_record`
- `theory_vector_extraction_rule`
- `row_order_binding`
- `shape_digest_certificate`
- `not_observed_data_vector_certificate`

## Current blockers

- No official baseline LCDM theory-vector artifact is present.
- No official ACT/CAMB/Cobaya digest-bound execution output is present.
- The prior shape-compatible candidate was rejected as a data-vector candidate, not a baseline theory vector.

## Promotion rule

Only a completed provenance certificate with all required fields satisfied may allow construction of `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`.

## Allowed next status after certificate exists

`BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY`

## Still missing objects

- `OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE`
- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is a provenance-certificate target only.

It does not provide an official ACT DR6 baseline LCDM theory-vector provenance certificate.
It does not provide a baseline LCDM prediction vector.
It does not prove a baseline LCDM prediction vector is official.
It does not prove a baseline LCDM prediction vector is physically correct.
It does not prove the bound candidate is a baseline LCDM theory vector.
It does not prove the bound candidate is source-authenticated.
It does not provide a DFM-MKC prediction vector.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- official ACT DR6 baseline LCDM theory-vector provenance certificate exists;
- baseline LCDM prediction vector exists;
- baseline LCDM prediction vector is official;
- baseline LCDM prediction vector is physically correct;
- bound candidate is a baseline LCDM theory vector;
- bound candidate is source-authenticated;
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
