# ACT DR6 Baseline LCDM Prediction Vector Execution Gate — 2026-05-25

Status: `BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_BLOCKED_SOURCE_MISSING`

This record adds an execution gate for the missing baseline Lambda-CDM prediction vector.

## Target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Minimal missing input

`TRUSTED_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE`

Acceptable forms:

- official ACT-compatible Lambda-CDM theory vector artifact;
- reproducible CAMB/Cobaya execution output with frozen cosmological parameters and ACT DR6 row-order binding;
- checked NPZ vector artifact whose shape equals the frozen extracted ACT DR6 CMB-only data-vector shape and whose row order is certified against `ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE`.

## Execution result

`NOT_EXECUTED`

## Blocking reason

No trusted baseline Lambda-CDM theory prediction vector source aligned to the frozen ACT DR6 CMB-only row ordering is present in repository artifacts.

## Blocked until

- trusted baseline LCDM theory source exists;
- source digest is frozen;
- vector shape equals the frozen ACT DR6 CMB-only data-vector shape;
- row-order binding is certified.

## Allowed next status after missing input exists

`BASELINE_LCDM_PREDICTION_VECTOR_READY_FOR_SHAPE_AND_ORDER_VALIDATION`

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is an execution gate only.

It does not provide a baseline LCDM prediction vector.
It does not provide a trusted baseline LCDM theory source.
It does not prove a baseline LCDM prediction vector is correct.
It does not provide a DFM-MKC prediction vector.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- baseline LCDM prediction vector exists;
- trusted baseline LCDM theory source exists;
- baseline LCDM prediction vector is correct;
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
