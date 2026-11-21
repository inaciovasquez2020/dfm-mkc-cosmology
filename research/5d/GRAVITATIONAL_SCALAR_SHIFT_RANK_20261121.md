# Time-dependent 5D EMD scalar-shift rank obstruction

Status: **PROVED algebraically**, with an executed exact SymPy fixture for the *principal extrinsic-curvature quadratic block*. **Not** a full 5D second variation, dynamical scalar kinetic matrix, or stability theorem.

Background: spatially flat 5D metric `-dt²+a(t)² dx_3²+b(t)² dy²`, with the proposed accelerating `a=t^(3/2), b=b0 t^(3/4)`. For a nonzero Fourier pair `(k,n)`, define physical wave numbers `kap=k/a`, `nu=n/b`.

Choose orthonormal spatial indices `(x,z1,z2,y)` and diagonal scalar spatial metric fluctuations `delta gamma_xx=delta gamma_z1z1=delta gamma_z2z2=2 zeta` and `delta gamma_yy=2 beta` at the principal kinetic level. With scalar shift components `(u,v)`, the linearized extrinsic-curvature contribution (omitting background Hubble and lapse terms irrelevant to the *pure shift Hessian*) can be written

`Kxx=zeta_dot-kap*u; Kz1z1=Kz2z2=zeta_dot; Kyy=beta_dot-nu*v; Kxy=-(kap*v+nu*u)/2`.

The ADM gravitational kinetic structure is `F=tr(K²)-(tr K)²`. Direct exact differentiation gives

`H_shift = Hessian_(u,v)(F) = [[nu²,-kap*nu],[-kap*nu,kap²]]`.

Its eigenvalues are `0` and `kap²+nu²>0`. Its determinant vanishes identically; its null direction is `(kap,nu)`. Its shift-quadratic form equals `(nu*u-kap*v)²`. This is a **constraint degeneracy**, not a negative-energy direction.

The null projection of the principal shift equations is

`(kap,nu)·grad_(u,v)F = 2 [kap² beta_dot + (2 kap²+3 nu²) zeta_dot]`.

In the full linearized theory this combination receives background and matter-source terms; it must not be set equal to zero without the remaining ADM terms. Background homogeneous matter (dilaton and purely time-circle electric field) has no background spatial scalar gradient or spatial Maxwell field strength, so its principal quadratic `u,v` Hessian does not remove this rank-one degeneracy. This does **not** establish the full lapse/shift Hessian rank, which depends on the treatment of temporal Maxwell and lapse variables.

**Consequence:** a naive inverse of the two gravitational scalar-shift Hessian cannot exist for generic nonzero `k,n`. A correct coupled reduction must retain the null-direction momentum constraint, fix residual gauge consistently, and only invert the nondegenerate subblock. The prior Maxwell temporal Schur complement alone is insufficient.

Reproduction: `python3 -B research/5d/gravitational_scalar_shift_rank_audit.py` (requires SymPy). This confirms the algebra, rank, null direction and perfect-square identity.

**OPEN:** complete ADM scalar Hessian including lapse, both shifts, dilaton, electric flux and spatial Ricci terms; matter-sourced momentum constraint; correct gauge quotient; physical kinetic and gradient/mass matrices; complete 5D scalar stability and observational viability.

**Novelty:** not claimed. **Lean:** NOT_RUN. **Local Mac:** NOT_INSPECTED.