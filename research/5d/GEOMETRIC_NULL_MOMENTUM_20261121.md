# Geometric null-direction ADM scalar momentum constraint

**Status:** PROVED algebraically; exact SymPy fixture PASS. **Scope:** geometric part of the linearized scalar momentum constraint for homogeneous spatially flat 5D anisotropic FLRW. Full Maxwell momentum source, lapse and shift elimination, physical scalar kinetic matrix and full stability are **OPEN**.

Background: `ds²=-dt²+a(t)² d x_3²+b(t)²dy²`. Let `H=a_dot/a`, `F=b_dot/b`, and physical scalar Fourier derivatives `kap=k/a`, `nu=n/b`, with `k,n != 0`. In orthonormal spatial components, use `zeta` (the three equal ordinary-space metric scalar perturbations), `beta` (circle metric scalar), `alpha` (lapse), and real Fourier shift quadratures `u,v`. Define `zd=zeta_dot`, `bd=beta_dot`.

The linear extrinsic curvature in an orthonormal frame has diagonal perturbations `(zd-H alpha-kap u, zd-H alpha, zd-H alpha, bd-F alpha-nu v)` and off-diagonal x-y entries `-(nu u+kap v)/2`. With `E^j_i=K^j_i-delta^j_i K`, the geometric linear momentum divergence `D_j E^j_i` includes the connection variations `kap(H-F)beta` for i=x and `3nu(F-H)zeta` for i=y.

Thus the shift-null projection `kap C_x + nu C_y` is exactly

```
C_null(g) = -kap²(2 zd + bd) - 3 nu² zd
  + [kap²(2H+F) + 3nu² H] alpha
  + kap²(H-F) beta + 3nu²(F-H) zeta.
```

Every occurrence of shift variables `u,v` cancels. The scalar shift Hessian is `[[nu²,-kap nu],[-kap nu,kap²]]`, of rank one and with null vector `(kap,nu)`. The complementary shift direction has positive Hessian `(kap²+nu²)²` before normalization. Consequently the null direction must impose a momentum constraint, not be inverted.

**Boundary:** The full equation is `C_null(g)=C_null(matter)` (up to consistently chosen sign and Fourier conventions). The matter-source term is *not* certified here, and neither the complete ADM quadratic action nor the physical kinetic/gradient/mass matrices has been computed. Do not substitute `C_null(g)=0` without checking the Maxwell stress perturbation. The formula assumes diagonal scalar spatial gauge and the specified orthonormal Fourier conventions; verify gauge fixing against all four 5D diffeomorphism generators when constructing the complete action.

Run `python3 -B research/5d/geometric_null_momentum_audit.py` with SymPy already installed. The executable verifies null projection, rank-one Hessian, and shift cancellation using exact algebra. This does not constitute independent review or Lean verification.

**Next:** derive the linear Maxwell momentum source, impose the null constraint together with the transverse shift equation, eliminate lapse in a nonsingular gauge, and compare to directly linearized field equations. **Stop** at any mismatch or singular chart; full 5D stability stays OPEN.