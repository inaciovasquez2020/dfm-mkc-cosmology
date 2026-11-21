# Nonzero-KK electric source in the scalar momentum constraint — 2026-11-21

**Status:** Exact symbolic stress-tensor source and positive lapse coefficient: `COMPUTATION_PASS`. No claim of a fully gauge-consistent sourced ADM scalar constraint, physical kinetic matrix, or five-dimensional stability.

## Exact assumptions
Five-dimensional EMD solution with `a=t^(3/2)`, `b=b0 t^(3/4)`, `f=t^(-7)`, background `F_ty=sqrt(51)b0 t^(13/4)/4`; `t,b0>0`. Fourier perturbations `exp(i(kx+ny))`, with `k,n != 0`, `delta A_x=i k v`, `delta A_y=0`. The spatial metric is diagonal in the scalar gauge, and `delta phi=0`; gauge completeness and the full ADM Hessian are **not** established here.

The background electric flux is `Q=a³ f F_ty/b=sqrt(51)/4`. At first order `delta F_xy=k n v`. The matter momentum density measured against the ADM normal is

`delta T_(normal,x) = f F_ty delta F_xy / b² = Q k n v/(a³ b)`.

The `y`-momentum density from this purely electric background vanishes at this order in the stated perturbation chart; other sectors and gauge-dependent source terms need separate treatment. With `kap=k/a`, `nu=n/b`, the orthonormal x component is `delta T_(normal,xhat)=Q kap nu v/a³`. This tests the source's tensor and background scaling. The overall complex Fourier phases and precise ADM Codazzi sign must be matched to the geometric constraint from the previous certificate before an equality of full constraints is promoted.

## Lapse equation coefficient

For geometric null momentum expression `C_null(g)` documented in `GEOMETRIC_NULL_MOMENTUM_20261121.md`, the lapse coefficient is

`C_alpha = kap²(2H+F)+3 nu² H = (15 kap²/4+9 nu²/2)/t >0`

on the power-law solution. Thus for a *given correctly phased and normalized* source `S_null`, the equation `C_null(g)=S_null` has exactly one lapse solution. Writing the remaining geometric terms as

`R=-kap²(2 zeta_dot+beta_dot)-3nu² zeta_dot+kap²(H-F)beta+3nu²(F-H)zeta`,

it is `alpha=(S_null-R)/C_alpha`.

This is an algebraic solvability result, **not** proof that the lapse and both gravitational shifts can all be eliminated consistently. The Hamiltonian constraint is still to be imposed; the null shift combination remains a momentum constraint and must not be inverted as an ordinary Hessian block.

## Reproduction and stop conditions

Run `python3 -B research/5d/maxwell_normal_momentum_source_audit.py` with SymPy already available. It checks the stress-tensor source, orthonormal projection and positivity of `C_alpha` using exact rational arithmetic.

**OPEN:** independent full ADM second variation; relative Fourier phase/source normalization in the coupled momentum constraint; remaining gravitational shift equation and Hamiltonian constraint; rank and positive definiteness of the physical scalar kinetic matrix; physical gradient/mass eigenvalues; complete 5D scalar stability. Stop at the first mismatch or singular gauge. No Lean check or independent review. No novelty claim.

Source files: `research/5d/geometric_null_momentum_audit.py` and `research/5d/gauss_schur_exact_audit.py` are supporting scoped fixtures, not a full action certificate.
