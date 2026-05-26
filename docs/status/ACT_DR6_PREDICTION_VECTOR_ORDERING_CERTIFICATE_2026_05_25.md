# ACT DR6 Prediction Vector Ordering Certificate — 2026-05-25

Status: `ORDERING_CERTIFICATE_FOR_EXTRACTED_DATA_VECTOR_ONLY_PREDICTIONS_STILL_MISSING`

This record closes the missing ordering-certificate object for the extracted ACT DR6 CMB-only official data vector.

## Closed missing object

`ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE`

## Ordering rule

Any future baseline LCDM or DFM-MKC prediction vector must be a one-dimensional array with exactly the same shape as the frozen extracted ACT DR6 CMB-only official data vector.

Entry `i` of any future prediction vector must correspond to row index `i` of the frozen extracted ACT DR6 CMB-only official data vector.

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Allowed next status after prediction vectors exist

`RESIDUAL_EIGENSPACE_COMPARISON_READY_NOT_VALIDATED`

## Boundary

This is an ordering certificate for the extracted data-vector row index only.

It does not provide a baseline LCDM prediction vector.
It does not provide a DFM-MKC prediction vector.
It does not prove either prediction vector is correct.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- baseline LCDM prediction vector exists;
- DFM-MKC prediction vector exists;
- baseline LCDM prediction vector is correct;
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
