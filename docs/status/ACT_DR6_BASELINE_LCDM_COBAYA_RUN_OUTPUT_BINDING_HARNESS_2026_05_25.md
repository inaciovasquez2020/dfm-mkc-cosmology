# ACT DR6 Baseline LCDM Cobaya Run Output Binding Harness — 2026-05-25

Status: `BINDING_HARNESS_ONLY_NO_BASELINE_VECTOR_IMPORTED`

## Added object

`ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS`

## Target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Harness script

`tools/bind_act_dr6_baseline_lcdm_cobaya_run_output.py`

## Harness role

The harness validates a future Cobaya/CAMB baseline LCDM vector candidate against the frozen ACT DR6 CMB-only row order and emits a binding-candidate record.

## Accepted candidate formats

- `.npz` with `theory_vector`, `prediction_vector`, `baseline_lcdm_prediction_vector`, or explicit `--key`;
- `.npy` one-dimensional array;
- `.json` with `prediction_vector` or explicit `--key`.

## Harness checks

- candidate artifact exists;
- candidate vector is one-dimensional;
- candidate vector shape equals the certified ACT DR6 CMB-only data-vector shape;
- candidate digest is frozen;
- candidate row index `i` is bound to `ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE` row index `i`.

## Execution result

`NOT_EXECUTED_NO_CANDIDATE_VECTOR_SUPPLIED`

## Allowed next status after candidate passes harness

`BASELINE_LCDM_PREDICTION_VECTOR_READY_FOR_SOURCE_AUTHENTICITY_VALIDATION`

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is a binding harness only.

It does not import a baseline LCDM prediction vector.
It does not prove a baseline LCDM prediction vector is official.
It does not prove a baseline LCDM prediction vector is physically correct.
It does not provide a DFM-MKC prediction vector.
It does not run empirical comparison.

Physical dark-matter phase claims remain: `HYPOTHESIS_ONLY`

## Does not prove

This record does not prove:

- baseline LCDM prediction vector exists;
- baseline LCDM prediction vector is official;
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
