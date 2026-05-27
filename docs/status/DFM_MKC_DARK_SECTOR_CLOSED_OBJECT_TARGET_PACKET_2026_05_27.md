# DFM-MKC Dark-Sector Closed Object Target Packet — 2026-05-27

Status: `TARGET_PACKET_ONLY_OBJECTS_NOT_SUPPLIED`

This packet records the five closed objects required before DFM-MKC/URF can become an experimentally testable dark-matter replacement candidate.

## Source dependency

`DARK_MATTER_REPLACEMENT_VALIDATION_TOOLKIT_2026_05_27`

## Target objects

### 1. `DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1`

Required contents:

- Spacetime domain.
- Field inventory.
- Dynamical variables.
- Action integral.
- Lagrangian density.
- Allowed parameters.
- Variation rules.
- Boundary terms.
- Units and dimensions.
- Reduction to known limits.

Acceptance test:

> The object must specify a closed action or equivalent variational principle from which field equations can be derived without adding post-hoc terms.

### 2. `DFM_MKC_FIELD_EQUATIONS_V1`

Required contents:

- Metric equation.
- Dark-sector equation.
- Constraint equations.
- Conservation laws.
- Stress-energy tensor.
- Gauge or coordinate conditions.
- Well-posedness assumptions.
- Known-limit recovery.

Acceptance test:

> The object must derive or state closed field equations compatible with the action functional and with ordinary gravitational observables.

### 3. `DFM_MKC_MATTER_COUPLING_RULE_V1`

Required contents:

- Ordinary-matter coupling.
- Photon coupling.
- Geodesic or optical rule.
- Stress-energy exchange rule.
- Equivalence-principle status.
- Lensing prediction rule.
- Baryonic limit.
- Radiation limit.

Acceptance test:

> The object must specify how visible matter and light interact with the DFM-MKC dark-sector structure without tuning per dataset.

### 4. `DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1`

Required contents:

- Background solution.
- Perturbation variables.
- Gauge choice.
- Linearized equations.
- Initial conditions.
- Transfer functions.
- Growth equation.
- Stability conditions.
- CMB observable mapping.
- Matter-power mapping.

Acceptance test:

> The object must produce a linear perturbation system suitable for CMB, lensing, BAO, and structure-growth predictions.

### 5. `DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1`

Required contents:

- Frozen parameter table.
- Dataset binding.
- Observable-vector definition.
- CMB TT/TE/EE prediction.
- CMB lensing prediction.
- BAO prediction.
- Matter-power prediction.
- Likelihood interface.
- Lambda-CDM baseline comparison rule.
- Blind holdout rule.

Acceptance test:

> The object must generate reproducible numerical predictions comparable against ACT, Planck, DESI, and baseline Lambda-CDM on the same data interface.

## Packet acceptance rule

All five targets must be supplied before any experimental-validation claim.

No single target promotes empirical status.

A replacement claim requires:

1. Frozen equations.
2. Frozen parameters.
3. Public reproducible prediction code.
4. Same-data comparison against Lambda-CDM.
5. Blind holdout success.
6. Independent reproduction.

## Boundary

Does not prove:

- DFM-MKC closed action functional.
- DFM-MKC field equations.
- DFM-MKC matter coupling law.
- DFM-MKC linear perturbation system.
- DFM-MKC ACT Planck DESI prediction vector.
- DFM-MKC empirical validation.
- Lambda-CDM failure.
- Dark matter replacement.
- Dark matter is liquid.
- Dark matter is solid.
- Dark matter is a phase.
- Dark energy resolution.
- Dark matter resolution.
- Gravity closure.
- Chronos-RR.
- Unrestricted H4.1/FGL.
- P vs NP.
- Any Clay problem.

## Next admissible step

Supply `DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1` as a concrete mathematical object.
