# Five-dimensional stability research checkpoint — 2026-11-21

**Status:** research checkpoint; **global 5D stability OPEN**.  
**Basis:** user-reported successful Mac/SymPy executions in the 2026-11-21 research session, plus repository source inspection. This note is not a fresh execution of every script, a Lean certificate, or independent peer review.  
**Scope:** three distinct models, which must not be conflated:
1. Power-law expanding-circle Einstein–Maxwell–dilaton (EMD).
2. Einstein–winding model with the explicitly **truncated** mixed-spectator one-loop radion potential.
3. An **alternative** local two-derivative Einstein–F(X) action, used as a non-uniqueness/instability counterexample, **not** identified with the actual quantum completion.

## 1. Expanding-circle EMD: checked restricted identities

For `a=t^(3/2)`, `b=b0*t^(3/4)`, `f=t^(-7)`, the background conserved electric flux is `Q_e=a^3*f*E/b=sqrt(51)/4`. User-reported Mac PASS receipts include restricted ADM lapse/shift and Maxwell Schur-complement identities, the homogeneous Hamiltonian and anisotropy residual checks, and positive high-frequency principal coefficients for five tensor, three Maxwell and one scalar polarization in Fourier modes `(1,1),(1,0),(0,1),(2,3)`. These finite checks are **not** a full nine-field finite-wavelength spectral proof.

Fixed-metric, fixed-flux scalar probe:
- `U_phiphi=391/(4*t^2)`;
- homogeneous mode exponents `-17/8 ± (3*sqrt(663)/8)*i`;
- decaying probe solutions **do not** furnish nontrivial solutions of the complete fixed-metric Einstein constraints: the anisotropy constraint forces `delta(phi)=0` if all metric perturbations are suppressed.

For the homogeneous diagonal metric `ds^2=-dt^2+a^2 dx_3^2+b^2 dw^2`, with `H=a_dot/a` and `F=b_dot/b`,
`R_AB l_time-circle^A l_time-circle^B = -3[H_dot+H(H-F)]`.
For the EMD powers `p=3/2,r=3/4`, the independently checked null contractions equal `9/(8*t^2)` and `69/(16*t^2)`; they match the stated scalar kinetic and electric stress, and are positive. **This does not prove global EMD stability.**

## 2. Einstein–winding and zero-mode Stückelberg vector

For the normalized zero-mode winding–graviphoton quadratic model at constant radius `b>0` and winding `q != 0`,
`Z=b^3/2`, `mu^2=q^2/2`, and, for `k != 0`,
`K_L=Z*mu^2*k^2/(Z*k^2+mu^2)>0`, `omega^2=k^2+q^2/b^3`. The longitudinal algebraic temporal constraint, reduced kinetic coefficient, and dispersion were user-reported Mac PASS. Quadratic radion–vector and metric–vector mixing vanish **around a zero-vector, zero-background-Stückelberg-derivative reference**; this does not establish nonzero-KK decoupling.

At nonzero integer KK level `n`, the compact gauge orbit is
`delta(theta_n)=q*xi_n`, `delta(r_n)=i*n*xi_n`, where `r=delta(g_ww)/(2*b^2)`. Hence `Z_n=theta_n-q*r_n/(i*n)` and the proper winding strain `delta X_n=i*n*Z_n/b` are gauge invariant at linear order. User Mac verified these algebraic identities and the winding-scalar second-variation/mixing block.

The restricted ADM Einstein–Hilbert quadratic extrinsic-curvature and spatial-curvature identities (modulo periodic boundary terms) were Mac checked. A 16-variable **formal flat-reference classical derivative symbol** comprising all 15 symmetric 5D metric components and the scalar was also Mac checked (symmetric 16x16 Hessian, selected mixing and gauge identities for its Einstein–Hilbert *derivative* block). **The nonzero-winding flat reference is OFF-SHELL**. Thus this matrix is not an on-shell gauge-reduced physical spectrum. The original transverse test erroneously used `h12`; it was repaired to the genuinely transverse `h23` before successful replay.

## 3. Truncated mixed-spectrum quantum radion

The repository's stated *truncated* potential is
`V_E(b)=Lambda/b+A/b^3+B*G(b)/b^6`, `A=B/2`; its published exact-series certificate gives at stationary `b*=1`:
`0.9 < V*/B < 0.91`, `1.25 < V''*/B < 1.30`.

With canonical 4D Einstein-frame radion `varphi=sqrt(3/2)*log(b)`, the mass/Hubble ratio obeys
`250/91 < m_varphi^2/H*^2 < 26/9`. This implies exponentially decaying **homogeneous radion perturbations within the stated truncated 4D EFT**, and the standard finite-wavelength scalar energy identity yields nonincreasing mode energy. User Mac verified the rational inequalities and algebraic energy identity. Metric–radion quadratic mixing vanishes at a constant-scalar stationary background of that Einstein-frame EFT.

**Crucial exclusions:** The potential omits coupled winding/graviphoton and gravitational determinants; its particle-content sensitivity includes a rigorous extra-independent-boson counterexample. EFT cutoff control, full quantum fluctuations, and physical 5D stability are **OPEN**. The repository's published spectral status explains that the reference radius and first KK level lie near the five-dimensional Planck scale.

## 4. Classical de Sitter and NEC no-go

For static-circle `dS4 x S1`, ordinary five-dimensional Einstein equations imply
`T_AB l_time-circle^A l_time-circle^B=-3H^2<0` for `H>0`. Thus **any** such geometry requires NEC-violating effective stress along that null direction (within the stated Einstein-gravity assumptions).

In the *classical* Einstein–winding–Lambda action, the independent equations are
`3H^2=Lambda+rho_w`, `6H^2=Lambda-rho_w`,
so `3H^2=-2rho_w<0` for nonzero positive-energy winding: no real static-circle de Sitter solution.

The *truncated* quantum potential's homogeneous anisotropic-pressure contribution is
`(T^w_w-T^x_x)_Q=B*(5G-bG')/b^5`; at its tuned stationary point total anisotropy is `-V*=-3H*^2`, algebraically matching the background Einstein anisotropy. User Mac checked this. This is **not** a reconstruction of the full momentum-dependent 5D quantum stress.

## 5. Local F(X) completion — conditional counterexample, not the source model

Consider separately `S=int sqrt(-g5) [R5/2-F(X)]`, `X=(partial chi)^2=q^2/b^2`, for a positive-energy stationary Einstein-frame potential `V_E(b)=F(X)/b`.

Stationarity `V_E'(b*)=0` forces
`F_X(X*)=-b*V*/(2X*)<0`.
The resulting zero-mode graviphoton has `m_B^2=-2V*=-6H*^2<0`; the transverse homogeneous equation has a growing solution `exp(2H*t)`. In the frozen-coefficient longitudinal model,
`K_L=-b^3*V* k^2/(k^2-2V*)`, negative when `k^2>2V*`. **Do not use the eliminated expression at `k^2=2V*`**, where its temporal constraint degenerates. The high-momentum ghost diagnosis requires those momenta to lie within the EFT validity range. The null stress equals `2X*F_X=-b*V*<0`. User Mac verified mass, five kinetic-sign instances, NEC identity, and the repaired SymPy frozen-scalar kinetic substitution.

**Classification:** Stable realization by this restricted local two-derivative F(X) completion **REFUTED** under stated assumptions. This does **not** refute other covariant completions nor identify the actual quantum-effective action.

## 6. Nonzero-KK Hessian non-identifiability

The alternative higher-derivative operator
`Delta S_lambda=(lambda/2)*int sqrt(-g5)*(Box_5 chi)^2`
vanishes along with its first variation on the specified circle-independent winding backgrounds, but changes the nonzero-KK quadratic action. A cosine lapse perturbation with **integer** `n != 0` produces
`Delta L^(2)=lambda*pi*a^3*q^2*n^2*A_lapse^2/(2*b^3)`
after circle integration. User Mac verified Fourier orthogonality and five integer modes. Initial symbolic test failed because `n` was only assumed positive real; this was repaired by imposing integer Fourier momentum.

The added operator is **not assumed to occur in the minimal action**; it proves that homogeneous background/potential information does not uniquely specify the inhomogeneous quadratic operator across different covariant completions.

## 7. Audit boundaries and next targets

- `MAC_COMPUTATION_PASS`: user-provided successful console outputs; full scripts/logs not added with this document.
- `LEAN_VERIFIED := NOT_RUN`; no independent mathematical peer review claimed.
- `COMPLETE_ON_SHELL_5D_QUANTUM_HESSIAN := OPEN`.
- `GAUGE_FIXED_COUPLED_NONZERO_KK_SPECTRUM := OPEN`.
- `COMPLETE_ONE_LOOP_FUNCTIONAL_DETERMINANT := OPEN`.
- `EFT_CUTOFF_AND_RENORMALIZATION_CONTROL := OPEN`.
- `GLOBAL_5D_STABILITY := OPEN`.
- `PHYSICAL_STABLE_5D_COMPACTIFICATION := NOT_ESTABLISHED`.

**Next substantive obstruction:** Specify the actual complete quantum-effective action for the fixed five-dimensional Einstein–winding–spectator content (including gauge fixing, all coupled fluctuation and ghost determinants, and a controlled cutoff), then derive and test its on-shell physical Hessian. Do not infer a physical spectrum from the off-shell classical 16-variable symbol or from homogeneous radion curvature.

**Preservation:** This research note is a checkpoint only. It does not modify established proofs, mathematical source files, or repository status locks.
