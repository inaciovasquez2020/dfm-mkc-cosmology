# DFM-MKC Likelihood Rule Target — 2026-05-21

Status: `LIKELIHOOD_RULE_TARGET_ONLY_NOT_SUPPLIED`

This target records the missing likelihood rule required before DFM holdout execution, empirical evidence claims, or DFM-vs-Lambda-CDM comparison can be supplied.

## Upstream required objects

- DFM field equations or action functional
- DFM parameter map
- DFM observable prediction rules
- DFM frozen prediction vector
- DFM external data manifest

## Required likelihood-rule fields

- likelihood identifier
- data vector reference
- frozen prediction vector reference
- covariance matrix reference
- inverse covariance rule
- residual vector definition
- probe likelihood blocks
- joint likelihood composition rule
- nuisance parameter handling
- prior application rule
- scale-cut rule
- masking rule
- calibration/systematics rule
- cross-probe covariance rule
- chi-square definition
- log-likelihood definition
- model-comparison metrics
- Lambda-CDM baseline reference
- holdout execution rule
- failure thresholds
- reproduction command

## Probe likelihood channels still blocked

- CMB TT/TE/EE
- CMB lensing
- BAO distances
- SN Ia distances
- weak-lensing and galaxy-clustering observables
- cluster abundance

## Root blocker

`DFM_LIKELIHOOD_RULE_NOT_SUPPLIED`

## Downstream blocked objects

- DFM holdout split execution
- DFM-vs-Lambda-CDM comparison
- DFM empirical evidence claim
- DFM CDM replacement claim

## Boundary

Target schema only.

Does not supply DFM field equations.
Does not supply DFM action functional.
Does not supply DFM parameter map.
Does not supply DFM observable prediction rules.
Does not supply frozen DFM prediction values.
Does not supply likelihood equations.
Does not supply covariance matrices.
Does not supply probe likelihoods.
Does not supply joint likelihood.
Does not execute any likelihood.
Does not produce empirical evidence.
Does not prove DFM.
Does not disprove Lambda-CDM.
Does not replace CDM.
