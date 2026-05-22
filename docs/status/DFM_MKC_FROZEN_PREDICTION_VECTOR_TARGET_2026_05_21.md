# DFM-MKC Frozen Prediction Vector Target — 2026-05-21

Status: `FROZEN_PREDICTION_VECTOR_TARGET_ONLY_NOT_SUPPLIED`

This target records the missing frozen prediction vector required before likelihood execution or DFM-vs-Lambda-CDM comparison can be supplied.

## Upstream required objects

- DFM field equations or action functional
- DFM parameter map
- DFM observable prediction rules

## Required frozen-vector fields

- freeze identifier
- freeze timestamp
- source commit
- DFM equation object reference
- DFM parameter map reference
- observable prediction rules reference
- frozen parameter values
- frozen prior ranges
- holdout split reference
- no-post-hoc-tuning certificate
- prediction channel vectors
- residual vector definitions
- covariance alignment metadata
- likelihood input format
- failure-mode thresholds
- Lambda-CDM baseline reference
- reproduction command

## Prediction channels still blocked

- CMB TT/TE/EE
- CMB lensing
- BAO distances
- SN Ia distances
- weak-lensing and galaxy-clustering observables
- cluster abundance

## Root blocker

`DFM_FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED`

## Downstream blocked objects

- DFM likelihood rule
- DFM holdout split execution
- DFM-vs-Lambda-CDM comparison
- empirical evidence claim

## Boundary

Target schema only.

Does not supply DFM field equations.
Does not supply DFM action functional.
Does not supply DFM parameter map.
Does not supply DFM observable prediction rules.
Does not supply frozen DFM prediction values.
Does not supply frozen parameter values.
Does not supply holdout split execution.
Does not execute any likelihood.
Does not produce empirical evidence.
Does not prove DFM.
Does not disprove Lambda-CDM.
Does not replace CDM.
