# ACT DR6 Baseline LCDM Official Best-Fit Vector Row-Order Mapping Target — 2026-05-25

Status: `ROW_ORDER_MAPPING_TARGET_ONLY_NO_MAPPING_SUPPLIED`

## Added object

`ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET`

## Target missing object

`ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING`

## Ultimate target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Purpose

This record specifies the exact row-order mapping object required to run the official best-fit extraction harness.

## Required mapping schema

Format: `JSON`

Top-level key:

`row_mapping`

Each row-mapping item must contain:

- `target_index`
- `source_row`
- `source_col`
- `observable_label`
- `frequency_or_spectrum_label`

## Required mapping invariants

- Every `target_index` from `0` to `required_prediction_vector_shape[0]-1` appears exactly once.
- No duplicate `target_index` is allowed.
- Each `source_row` and `source_col` must be in range for the official best-fit spectra table.
- Each mapped table value must be numeric.
- The mapping must cite the official best-fit source file digest.
- The mapping must cite the `ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE`.
- The mapping must not use the observed ACT DR6 `data_vector` as a source.

## Blocked until mapping exists

- official best-fit vector extraction;
- baseline LCDM extracted-vector candidate;
- baseline LCDM row-order audit;
- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR` promotion.

## Allowed next status after mapping exists

`BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_READY_FOR_EXTRACTION_TRIAL`

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING`
- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is a row-order mapping target only.

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
