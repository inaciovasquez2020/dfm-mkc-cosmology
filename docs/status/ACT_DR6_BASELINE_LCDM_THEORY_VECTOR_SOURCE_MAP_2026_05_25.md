# ACT DR6 Baseline LCDM Theory Vector Source Map — 2026-05-25

Status: `OFFICIAL_COBAYA_CAMB_SOURCE_MAP_ONLY_NO_VECTOR_ARTIFACT_FOUND`

This record maps the official source route for constructing a baseline Lambda-CDM prediction vector compatible with the frozen ACT DR6 CMB-only data-vector row order.

## Added object

`ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE_MAP`

## Target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Official sources found

- `ACT_DR6_ACT_LITE_LIKELIHOOD`
- `ACT_DR6_PARAMETERS_AND_RUN_SETTINGS`
- `NASA_LAMBDA_ACT_DR6_COBAYA_CHAINS`

## Source conclusion

An official ACT-compatible Cobaya/CAMB source route was found.

A standalone official row-aligned `.npz` baseline LCDM prediction-vector artifact was not found.

## Admissible route

1. Use `ACTCollaboration/DR6-ACT-lite` as the ACT DR6 CMB-only likelihood source.
2. Use `ACTCollaboration/ACT-DR6-parameters` as the ACT DR6 Cobaya/CAMB run-settings source.
3. Run or reconstruct a baseline LCDM Cobaya/CAMB theory output.
4. Extract a one-dimensional theory vector matching the certified ACT DR6 CMB-only data-vector shape.
5. Bind row index `i` to `ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE` row index `i`.
6. Freeze digest.
7. Promote only to `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_READY_FOR_SHAPE_AND_ORDER_VALIDATION`.

## Minimal next object

`ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS`

## Allowed next status

`BASELINE_LCDM_OFFICIAL_SOURCE_ROUTE_FOUND_VECTOR_STILL_MISSING`

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is a source map only.

It does not provide a baseline LCDM prediction vector.
It does not provide a checked NPZ baseline vector artifact.
It does not prove the baseline LCDM prediction vector is correct.
It does not provide a DFM-MKC prediction vector.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- baseline LCDM prediction vector exists;
- checked NPZ baseline vector artifact exists;
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
