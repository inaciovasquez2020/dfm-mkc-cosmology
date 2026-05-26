# ACT DR6 Baseline LCDM Row Mapping Failure Analysis — 2026-05-25

Status: `ROW_MAPPING_FAILURE_ANALYSIS_*`

## Added object

`ACT_DR6_BASELINE_LCDM_ROW_MAPPING_FAILURE_ANALYSIS`

## Target missing object

`ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING`

## Ultimate target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Purpose

This record analyzes why the official best-fit mapping/extraction trial did not certify a complete row mapping.

## Minimal next object

`ACT_DR6_BASELINE_LCDM_SACC_TO_BEST_FIT_LABEL_BINDING_RULE`

## Blocked until

- SACC row metadata supplies or is supplemented with spectrum labels, ell/bin labels, and tracer labels for every target row;
- best-fit source-file labels are normalized against SACC tracer labels;
- each target row receives exactly one source-row/source-column assignment;
- the mapping is independently audited against `ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE`.

## Allowed next status after binding rule

`ROW_MAPPING_BINDING_RULE_READY_FOR_MAPPING_CONSTRUCTION`

## Promotion decision

`DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING`
- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is row-mapping failure analysis only.

It does not provide an official best-fit row-order mapping.
It does not provide a baseline LCDM prediction vector.
It does not extract a baseline LCDM prediction vector.
It does not prove a baseline LCDM prediction vector is row-aligned.
It does not prove a baseline LCDM prediction vector is physically correct.
It does not provide a DFM-MKC prediction vector.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- official best-fit row-order mapping exists;
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
