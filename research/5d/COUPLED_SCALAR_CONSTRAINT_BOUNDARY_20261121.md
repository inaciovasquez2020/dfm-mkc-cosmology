# DFM–MKC: nonzero-KK scalar constraint boundary (2026-11-21)

## Status

**Independent exact algebra:** `COMPUTATION_PASS` for the temporal Maxwell Gaussian elimination / Schur complement, given the previously stated perturbation ansatz. **Full ADM second variation:** `OPEN`. **Lapse and two gravitational shift eliminations:** `OPEN`. **Physical 3×3 kinetic matrix, gradient/mass operators, scalar stability:** `OPEN`. No Lean proof, spectral stability certificate, novelty claim or independent review. This file is a research checkpoint, not a claim of a viable cosmological model.

## Exact background, hypotheses, and limitations

Action in units `8πG5 = 1`:

`S = ∫ √(-g) [ R/2 - (∂φ)²/2 - V(φ) - f(φ)F²/4 ] d⁵x`.

Background: `a=t^(3/2)`, `b=b0 t^(3/4)`, `f=t^(-7)`, `F_ty=(sqrt(51)/4)b0 t^(13/4)`, with `t,b0>0`. Analyze real quadratures of a Fourier pair `exp(i(kx+ny))`, `k≠0`, `n≠0`; reality relates conjugate modes. The displayed Gaussian computation uses only the `u=δA_t`-dependent quadratic Maxwell block. Its linear metric source is inherited from the prior scalar-Gauss derivation; a full coupled ADM second variation is NOT certified.

For the gauge choices `δφ=0`, `δA_y=0` and a diagonal spatial scalar metric, check residual gauge fixing against the actual time-dependent background when constructing the full Hessian. These choices are valid only on an appropriate nondegenerate gauge patch; source and number of dynamical coordinates must be audited after enforcing Einstein constraints. An existing repository gauge-orbit theorem for a constant-radius *winding-scalar* background is not evidence for this distinct electric, time-dependent geometry.

## Temporal Maxwell constraint and exact Schur complement

Let `v` be the longitudinal Fourier coordinate (`δA_x=ik v`), `u=δA_t`, and define

- `Cx = a b f = b0 t^(-19/4)`;
- `Cy = a³ f/b = t^(-13/4)/b0`;
- `A = k² Cx`, `B = n² Cy`, `D = A+B`.

In real Fourier quadratures, let `J` denote the linear metric source (including the background flux). The `u`-dependent Lagrangian is

`Lu = A/2 (v_dot-u)² + B/2 u² + J u`.

Then `∂Lu/∂u = D u-A v_dot+J=0`, so

`u* = (A v_dot-J)/D`.

Eliminating `u` gives

`Lu_red = (AB/2D) v_dot² + (A J/D)v_dot - J²/(2D)`.

The Hessian of the unreduced `(v_dot,u)` quadratic form is `[[A,-A],[-A,D]]`. Its determinant is `AB>0`, and its Schur complement is

`Kvv(Maxwell)=AB/D = b0 k² n² t^(-13/4) / (b0² k²+n² t^(3/2)) > 0`.

This **does not** establish the sign of `Kvv` after eliminating the lapse and both gravitational shift scalars: their mixing may modify the physical Schur complement.

The old source convention in complex Fourier notation was `J ~ i n Q(3ζ-β-α)` with `Q=√51/4`, up to Fourier-phase conventions. The exact sign and any additional shift-source terms must be rederived from the *complete* ADM quadratic action before promoting this as a full gravitational constraint identity.

## Decisive unresolved obligation

Construct the complete quadratic expansion of the 5D ADM action (including spatial curvature, extrinsic curvature, scalar and electromagnetic terms) in a fixed consistent nonzero-`(k,n)` scalar gauge. Assemble all terms as a Hermitian quadratic form in velocities, dynamical coordinates and nondynamical lapse/shift/gauge variables. Check the rank of the nondynamical Hessian, respecting first-class gauge constraints; solve them in a nonsingular chart; and compute the full physical kinetic and gradient/mass matrices. Verify the result against the unreduced Einstein and Maxwell linearized equations.

**Stop conditions:** singular constraint chart, omitted gauge mode, mismatch with the linearized field equations, an indefinite kinetic eigenvalue, or an unverified symbolic identity. Do not label unresolved spectrum or full stability as PASS.

## Reproduction

`python3 -B research/5d/gauss_schur_exact_audit.py`  (SymPy preinstalled). This certificate tests algebraic elimination, positivity under positive symbols, normalization, and limiting coordinate degeneracies; it does NOT test the full gravitational action.

This checkpoint intentionally leaves `GRAVITATIONAL_SCALAR_CONSTRAINT_BLOCK`, `PHYSICAL_SCALAR_KINETIC_MATRIX`, `GRADIENT_MASS_EIGENVALUES`, and `GLOBAL_5D_SCALAR_STABILITY` all **OPEN**.
