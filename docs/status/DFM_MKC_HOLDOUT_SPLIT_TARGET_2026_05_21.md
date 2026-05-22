# DFM-MKC Holdout Split Target — 2026-05-21

Status: `HOLDOUT_SPLIT_TARGET_ONLY_NOT_SUPPLIED`

This target records the missing holdout split required before DFM holdout execution, empirical evidence claims, or DFM-vs-Lambda-CDM comparison can be supplied.

## Upstream required objects

- DFM field equations or action functional
- DFM parameter map
- DFM observable prediction rules
- DFM frozen prediction vector
- DFM likelihood rule
- DFM external data manifest

## Required holdout-split fields

- split identifier
- split timestamp
- source commit
- registered data manifest reference
- frozen prediction vector reference
- likelihood rule reference
- training data sources
- validation data sources
- holdout data sources
- blind data sources
- data access status
- pre-unblinding allowed operations
- post-unblinding forbidden operations
- parameter freeze reference
- prediction freeze reference
- likelihood freeze reference
- no-post-hoc-tuning certificate
- failure thresholds
- model comparison metrics
- reproduction command

## Required probe coverage

- CMB TT/TE/EE
- CMB lensing
- BAO distances
- SN Ia distances
- weak-lensing and galaxy-clustering observables
- cluster abundance

## Root blocker

`DFM_HOLDOUT_SPLIT_NOT_SUPPLIED`

## Downstream blocked objects

- DFM holdout split execution
- DFM-vs-Lambda-CDM comparison
- DFM empirical evidence claim
- DFM CDM replacement claim

## Boundary

Target schema only.

Does not assign training data.
Does not assign validation data.
Does not assign blind holdout data.
Does not execute holdout evaluation.
Does not supply DFM field equations.
Does not supply DFM action functional.
Does not supply DFM parameter map.
Does not supply DFM observable prediction rules.
Does not supply frozen DFM prediction values.
Does not supply likelihood equations.
Does not execute any likelihood.
Does not produce empirical evidence.
Does not prove DFM.
Does not disprove Lambda-CDM.
Does not replace CDM.
