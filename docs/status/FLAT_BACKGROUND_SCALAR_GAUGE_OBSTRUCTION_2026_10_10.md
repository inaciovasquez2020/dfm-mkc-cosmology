# Flat-background scalar-gauge obstruction — 2026-10-10

Status: `SPATIAL_CURVATURE_MODE_CANNOT_BE_GAUGED_AWAY_ON_TESTED_BACKGROUND`

## Established input

The scalar metric convention in `src/dfm_mkc_solver/scalar_bardeen_weyl_observable_v1.py` uses the linear gauge transformation

```
psi -> psi + H T
E'  -> E' - L'
```

where `H = a'/a`, `T` is the scalar time-coordinate shift, and `L` is the scalar spatial-coordinate shift.

The on-shell auxiliary-rank regression in `tools/audit_generalized_proca_l4_scalar_sector_v1.py` specializes to the flat constant-scale-factor background `a=1`, with all background derivatives zero. Thus `H=0).

## Exact consequence

On this background,

```
delta psi -> delta psi
```

under the linearized time-coordinate shift. Therefore a general spatial-curvature perturbation `psi` cannot be set to zero by choosing `T`. For nonzero wavenumber, the spatial shift can remove the scalar shear variable `E`, but it does not remove `psi` when `H=0`.

Consequently, the perturbation ansatz with unperturbed spatial metric is not established as a complete gauge fixing on this flat background. The on-shell auxiliary matrix

```
diag(0, 0, k0**2/2)
```

and its rank-one/nullity-two result remain valid only for the restricted ansatz used to compute them. The null directions cannot yet be interpreted as physical modes or as gauge modes of the complete theory.

## Missing structural object

Derive the second-order scalar action and linearized constraint equations with the spatial-curvature perturbation retained, then impose the background equations and the legitimate gauge conditions. Only after this should the complete constrained system be reduced and its physical scalar degrees of freedom counted.

## Boundary

- `FLAT_BACKGROUND_GAUGE_FIXING_WITHOUT_PSI := NOT_VALIDATED`
- `SPATIAL_CURVATURE_PSI_REMOVABLE_BY_TIME_SHIFT_AT_H_ZERO := FALSE`
- `RESTRICTED_AUXILIARY_RANK_RESULT := VALID_FOR_RESTRICTED_ANSATZ_ONLY`
- `PHYSICAL_SCALAR_DOF_COUNT := OPEN`
- `STABILITY_OR_NEW_PHYSICAL_EFFECT := NOT_ESTABLISHED`
