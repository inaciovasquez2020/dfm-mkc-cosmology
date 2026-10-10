# Generalized-Proca L4 scalar-sector audit and stopping boundary — 2026-10-10

Status: `CORRECTED_ACTION_REBUILT; IDENTITY_AND_FOURIER_AUDITS_ADDED; PHYSICAL_DOF_COUNT_OPEN`

## Scope

This note records the bounded result of the symbolic scalar-perturbation work discussed on 2026-10-10. The source supplied for that calculation defines a scalar-dependent curvature coefficient
`F(phi) = M2 - xs*phi**2`, a vector background `A_0 = B(t)`, perturbations `u(t,z)` and `chi(t,z)`, a metric lapse perturbation `Phi(t,z)`, and a shift perturbation `beta(t,z)`. It includes `R_{μν} A^μ A^ν` and computes a second-order Lagrangian followed by a Fourier reduction.

The calculations in this note distinguish the original model from a generalized-Proca L4-completed model. The completion changes the action; it is not a proof that the original and completed models have the same dynamics.

## Curvature convention and identity

The supplied Ricci implementation uses
```
R_mn = d_r Gamma^r_mn - d_n Gamma^r_mr
       + Gamma^r_rl Gamma^l_mn - Gamma^r_nl Gamma^l_mr
```

With this convention, for
`J^mu = A^mu nabla_nu A^nu - A^nu nabla_nu A^mu`,
```
D := (nabla_mu A^mu)^2
     - (nabla_mu A^nu)(nabla_nu A^mu)

nabla_mu J^mu = D - R_mn A^m A^n
```
and hence
```
R_mn A^m A^n = D - nabla_mu J^mu.
```

Therefore, with constant `xi`,
```
-(xi/2) R_mn A^m A^n
  = -(xi/2) D + (xi/2) nabla_mu J^mu.
```
The last term is a boundary term in the action under boundary conditions that discard it.

## Explicit linear generalized-Proca L4 completion

For `X = -A_mu A^mu/2`, the standard L4 structure is
```
L4 = G4(X) R + G4_X(X) D.
```

Choosing `G4_X = -xi/2` gives `G4(X) = C - xi X/2`. Taking `C = 0` as a convention gives the explicit completion
```
L_curvature = (1/2) F(phi) R - (xi/2) X R - (xi/2) D.
```

The `F(phi) R/2` term is retained as a separate scalar-tensor coupling. Since it depends on the independent scalar `phi`, it is not itself the vector-dependent `G4(X) R` coefficient. Thus the original action with `F(phi)R/2 - xi R_mn A^m A^n/2` does not, for independent `phi` and `A_mu`, by itself establish the standard generalized-Proca L4 relation. The completion above is a specific extended model choice.

## Important implementation boundary

A reproducible implementation is now present at `tools/audit_generalized_proca_l4_scalar_sector_v1.py` and is wired into `.github/workflows/cosmology-check.yml`. In the working SymPy session, the same corrected-action construction was executed: the Ricci/divergence residual on the supplied truncated off-diagonal ansatz simplified to zero; `L2` and the Fourier-reduced `Lk` were built; five Euler–Lagrange equations were generated; and the kinetic Hessian reduced to `diag(0, 0, alpha*a(t)^3/2, 0, a(t)/2)`. Three rational background/parameter samples gave frozen-symbol determinant degree four, and the auxiliary algebraic block was nonsingular at those three samples. These are bounded symbolic/sample checks, not a generic determinant theorem. GitHub's available status endpoint returned no check statuses for the merge commit, so CI success is not claimed.

A valid computational continuation must:
1. construct `X`, `D`, and the linked `G4(X)R + G4_X D` term with consistent index conventions;
2. verify the identity residual symbolically before continuing;
3. regenerate the second-order Lagrangian and Fourier reduction from the corrected action;
4. derive the Euler–Lagrange equations from that corrected reduced Lagrangian;
5. inspect the kinetic Hessian and identify the actual constraints/gauge conditions before interpreting a characteristic determinant as a physical degree-of-freedom count.

The ansatz sets scalar spatial-curvature and scalar-shear perturbations to zero, consistent with a spatially flat scalar gauge for nonzero k. The supplied source does not explicitly name or justify that gauge fixing. Record the gauge choice and treat k=0 separately before interpreting the reduced system as the complete scalar sector.

## Result ledger

- `RICCI_DIVERGENCE_IDENTITY := ESTABLISHED_ALGEBRAICALLY`
- `STANDARD_L4_MATCH_FOR_ORIGINAL_ACTION := NOT_ESTABLISHED`
- `LINEAR_G4_COMPLETION := SPECIFIED`
- `CORRECTED_QUADRATIC_ACTION := REBUILT_SYMBOLICALLY; AUDIT_SCRIPT_IN_MAIN`
- `FOURIER_REDUCTION_FOR_COMPLETED_ACTION := BUILT_SYMBOLICALLY`
- `KINETIC_HESSIAN := DIAG(0,0,alpha*a(t)^3/2,0,a(t)/2); RANK_2_IF_ALPHA_AND_A_NONZERO`
- `AUXILIARY_ALGEBRAIC_BLOCK := NONSINGULAR_AT_3_RATIONAL_SAMPLES_ONLY`
- `REDUCED_KINETIC_SCHUR_COMPLEMENT := NONZERO_AT_3_RATIONAL_SAMPLES_ONLY; NO_POSITIVITY_CLAIM`
- `CI_STATUS := NOT_CONFIRMED_BY_AVAILABLE_STATUS_ENDPOINT`
- `PHYSICAL_SCALAR_DOF_COUNT := OPEN`

## Stopping decision

The corrected action has now been rebuilt symbolically, Fourier-reduced, and subjected to a bounded Hessian, auxiliary-block, and reduced-kinetic Schur-complement audit. This is a good stopping point for the current restricted ansatz. It is not a completed physical mode-count or stability result: the spatially flat gauge choice is implicit rather than documented, determinant degrees and reduced-block nonsingularity were sampled rather than proved on-shell, and CI success is not confirmed. The next admissible step is to document/fix the gauge and impose the background equations before making physical mode or stability claims.
