# DFM-MKC Observable Prediction Rules Target — 2026-05-21

Status: `OBSERVABLE_PREDICTION_RULES_TARGET_ONLY_NOT_SUPPLIED`

This target records the missing rules that must map DFM equations and parameters into observable cosmological prediction channels before frozen predictions or likelihood execution can be supplied.

## Upstream required objects

- DFM field equations or action functional
- DFM parameter map

## Required prediction-rule fields

- observable channel name
- input parameter dependencies
- input initial-condition dependencies
- input boundary-condition dependencies
- forward-model equations
- projection from DFM state to observable
- units and normalization
- redshift domain
- scale domain
- nuisance-parameter separation
- calibration rule
- covariance compatibility rule
- residual vector definition
- Lambda-CDM baseline comparison rule
- holdout-freeze rule
- failure-mode definition

## Observable channels still blocked

- CMB TT/TE/EE
- CMB lensing
- BAO distances
- SN Ia distances
- weak-lensing and galaxy-clustering observables
- cluster abundance

## Root blocker

`DFM_OBSERVABLE_PREDICTION_RULES_NOT_SUPPLIED`

## Downstream blocked objects

- DFM frozen prediction vector
- DFM likelihood rule
- DFM holdout split
- DFM-vs-Lambda-CDM comparison

## Boundary

Target schema only.

Does not supply DFM field equations.
Does not supply DFM action functional.
Does not supply DFM parameter map.
Does not supply DFM observable prediction rules.
Does not supply channel projection rules.
Does not supply residual vector rules.
Does not supply covariance compatibility rules.
Does not supply frozen predictions.
Does not execute any likelihood.
Does not produce empirical evidence.
Does not prove DFM.
Does not disprove Lambda-CDM.
Does not replace CDM.
