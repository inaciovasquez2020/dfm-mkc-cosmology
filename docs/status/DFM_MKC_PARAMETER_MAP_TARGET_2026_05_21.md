# DFM-MKC Parameter Map Target — 2026-05-21

Status: `PARAMETER_MAP_TARGET_ONLY_NOT_SUPPLIED`

This target records the missing DFM parameter map required before observable prediction rules, frozen prediction vectors, or likelihood execution can be supplied.

## Upstream required object

- DFM field equations or action functional

## Required parameter object fields

- primitive parameter names
- parameter definitions
- dimensional units
- allowed domains
- prior ranges
- frozen values or free status
- physical interpretation
- degeneracy structure
- Lambda-CDM parameter correspondence or explicit noncorrespondence
- matter-sector parameters
- dark-sector parameters
- initial-condition parameters
- boundary-condition parameters
- nuisance-parameter separation
- observable-channel dependencies
- calibration parameters
- holdout-freeze certificate

## Prediction channels still blocked

- CMB TT/TE/EE
- CMB lensing
- BAO distances
- SN Ia distances
- weak-lensing and galaxy-clustering observables
- cluster abundance

## Root blocker

`DFM_PARAMETER_MAP_NOT_SUPPLIED`

## Downstream blocked objects

- DFM observable prediction rules
- DFM frozen prediction vector
- DFM likelihood rule
- DFM holdout split
- DFM-vs-Lambda-CDM comparison

## Boundary

Target schema only.

Does not supply DFM field equations.
Does not supply DFM action functional.
Does not supply DFM parameter map.
Does not supply parameter values.
Does not supply prior ranges.
Does not freeze DFM parameters.
Does not supply observable prediction rules.
Does not supply frozen predictions.
Does not execute any likelihood.
Does not produce empirical evidence.
Does not prove DFM.
Does not disprove Lambda-CDM.
Does not replace CDM.
