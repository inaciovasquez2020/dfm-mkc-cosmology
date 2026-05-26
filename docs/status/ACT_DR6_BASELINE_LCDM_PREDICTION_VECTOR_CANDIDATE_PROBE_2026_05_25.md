# ACT DR6 Baseline LCDM Prediction Vector Candidate Probe — 2026-05-25

Status: `CANDIDATE_PROBE_ONLY_BASELINE_VECTOR_NOT_PROMOTED`

## Added object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE`

## Target missing object

`ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`

## Probe script

`tools/probe_act_dr6_baseline_lcdm_prediction_vector_candidates.py`

## Probe role

The probe searches local repository artifacts for a shape-compatible baseline LCDM prediction-vector candidate and routes any match through the binding harness.

## Probe result artifact

`artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_result.json`

## Promotion rule

Only a matched, bound, source-authenticated baseline LCDM candidate may later close `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`.

## Still missing objects

- `ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR`
- `ACT_DR6_DFM_MKC_PREDICTION_VECTOR`

## Boundary

This is a candidate probe only.

It does not provide a baseline LCDM prediction vector.
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
