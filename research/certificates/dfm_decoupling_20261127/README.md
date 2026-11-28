# Opacity-uniform scalar–photon–baryon transition and sharp dust handoff

2026-11-27. Public repository `inaciovasquez2020/dfm-mkc-cosmology`, inspected main `ea4f548e5c9b3160ea0a4dde76cab74be6a4964f`. Extends the proof at PR #358, `fb8a8b4a30b051aba8dfd28deff94ee7b37832df`, and PR #357. PROVED analytically within the following perfect-fluid model. Standalone COMPUTATION_PASS_SCOPED. No Lean, Mac or repository CI execution. No repository writes, Codex or Claude. Standard photon–baryon equations and cosmological approximation regimes: Ma & Bertschinger (1995), arXiv:astro-ph/9506072; Blas, Lesgourgues & Tram (2011), arXiv:1104.2933. Independent novelty of the estimate not established.

## 1. Hypotheses and exact model

Use cosmic time [0,T], a(0)=H(0)=1, g=4 pi G=3/2, initial critical density 1. Fix s,b,r>0, ell>=0, s+b+r+ell=1. Canonical quadratic minimally coupled complex scalar psi has circular initial data psi(0)=sqrt(s)/m, psi_dot(0)=i sqrt(s), and obeys psi_ddot+3H psi_dot+m²psi=0. Write rho_s=(|psi_dot|²+m²|psi|²)/2, K_s=|psi_dot|², rho_b=b/a³, rho_gamma=r/a⁴. The background obeys H²=ell+rho_s+rho_b+rho_gamma, H_dot=-g(K_s+rho_b+4rho_gamma/3), a_dot=aH. Baryons are pressureless; photons form a perfect fluid with no anisotropic stress, polarization or background energy exchange. Linear drag is the only interaction. Fix kappa>0 and k²=m kappa, k>=1. Prescribe any finite piecewise continuous nonnegative cosmic slip relaxation rate lambda_m(t) on [0,T], with no bound on its mass dependence, amplitude, lower bound or time derivative. The equivalent conformal opacity is Gamma_m=a lambda_m R/(1+R), where R=3ba/(4r). The reduced comparison uses the SAME relaxation rate, not necessarily the same conformal opacity evaluated on a different background.

Let L=k/a, p=L², d=delta_b, e=delta_gamma, v_j=theta_j/k, w=v_gamma-v_b, v=(R v_b+v_gamma)/(1+R), gamma=HR/(1+R). Newtonian gauge potentials coincide, Phi=Psi. For the scalar harmonic eta, set X=m²Re(conj(psi)eta), Y=Re(conj(psi_dot)eta_dot), q_s=Re(conj(psi_dot)eta), q_b=rho_b a v_b/k, q_gamma=4rho_gamma a v_gamma/(3k), Q=q_s+q_b+q_gamma. Use the exact algebraic constraints and KG equation from #358:

    Phi=-g(X+Y+rho_b d+rho_gamma e+3H Q)/(p-gK_s), D=gQ-H Phi,
    eta_ddot+3H eta_dot+(m²+p)eta=4psi_dot D-2m²psi Phi.

Constraint propagation and trace consistency follow from #358 because the two momentum exchange terms cancel, independently of lambda_m. The exact fluid equations in mean-slip coordinates are

    d_dot=-L(v-w/(1+R))+3D,
    e_dot=-4L(v+Rw/(1+R))/3+4D,
    v_dot=-gamma v+L Phi+L e/[4(1+R)],
    w_dot=H v+L e/4-[lambda_m+H/(1+R)]w.

The identity F=R v_b²+v_gamma²+3e²/16=(1+R)v²+Rw²/(1+R)+3e²/16 gives

    F_dot=-HR v_b²-2lambda_m Rw²/(1+R)+2L Phi(1+R)v+3eD/2.

It holds for all nonnegative relaxation rates, including zero and through every finite switch. The IVP has continuous state at coefficient jumps. These equations and the energy identity were established in #358; verify.py independently checks five algebraic identities.

## 2. Opacity-uniform scaled approximation theorem

Introduce the exact rotating envelopes as in #358: X_bg=m a^(3/2)psi/sqrt(s), Y_bg=m a^(3/2)eta/sqrt(s), X_bg=U exp(imt)+V exp(-imt), X_bg_dot=im(U exp(imt)-V exp(-imt)), Y_bg=A exp(imt)+B exp(-imt), Y_bg_dot=im(A exp(imt)-B exp(-imt)). Define Ahat=A/k, Bhat=B/k, dhat=d/k, and retain e,v,w unscaled. Initial state may depend on m; put N0=|Ahat(0)|+|Bhat(0)|+|dhat(0)|+sqrt(F(0)). No phase locking or small slip is assumed. The comparison background a_d has H_d²=ell+(s+b)/a_d³+r/a_d⁴, a_d(0)=1, a_d_dot=a_d H_d.

For the reference variables (Ahat_*, Bhat_*, dhat_*, e_*, v_*, w_*), evaluate a,H,R,L,gamma on a_d,H_d. Set omega=kappa/(2a²) and P=-g(2s Re Ahat_*+b dhat_*)/(kappa a). Use the same initial state and the exact prescribed lambda_m(t):

    Ahat_*dot=i(omega Ahat_*+P), Bhat_*dot=-i omega Bhat_*,
    dhat_*dot=-(v_*-w_*/(1+R))/a,
    e_*dot=-4L(v_*+Rw_*/(1+R))/3,
    v_*dot=-gamma v_*+kappa P/a+L e_*/[4(1+R)],
    w_*dot=H v_*+L e_*/4-[lambda_m+H/(1+R)]w_*.

There exist C,m0 depending on the fixed fractions, T,kappa only such that m>=m0 implies sup norm of the state difference <= C N0/k, with complex modulus and real absolute value sum norm. The same holds after adjoining delta_s/k and 2 Re Ahat_* respectively, where delta_s=(X+Y-K_s Phi)/rho_s. Neither the rate nor C depends on opacity amplitude, its derivatives or its positive lower bound. This is a mass-dependent reduced IVP retaining acoustic and collision frequencies. It is not strong convergence of all unscaled contrasts or a photon free-streaming approximation.

### Proof

C denotes finite positive constants depending only on the fixed parameters, not m or opacity. The background proof of #357 is unchanged: H<=1, |H_dot|<=3, 1<=a<=exp(T), E=a³rho_s/s satisfies 1<=E<=1+24/m² for m>=6 by the comoving charge-energy inequality, and sup(|a-a_d|+|H-H_d|)<=C/m² by Gronwall. U,V obey |U|+|V|<=C, |U-1|+|V|<=C/m. The denominator p-gK_s>=p/2 for m>=6 exp(2T)/kappa. Thus the exact system has a regular linear IVP for every allowed rate. These estimates are global on [0,T] and can also be used for perturbation IVPs started at any later fixed time on the same background.

Let n=|Ahat|+|Bhat|+|dhat|+sqrt(F), equivalent to the state norm uniformly on the interval. The carrier cancellation of #357 gives |a³(X+Y)/s-2k Re Ahat|<=C k n/m. Also |q_s|<=C k n/m, and |q_b|+|q_gamma|<=C n/k. Since k²=m kappa, Q=O(n/k). The scaled density source is a³(X+Y+rho_b d+rho_gamma e)/k=2s Re Ahat+b dhat+O(n/k). The constraint then implies

    |m Phi/k-P0|<=C n/k, P0=-g(2s Re Ahat+b dhat)/(kappa a),
    |Phi|+|D|<=C n/k.

Indeed the denominator correction is O(1/m), and the contribution of Q to the scaled source is O(n/k²). The exact rescaled perturbation equation is Y_bg_ddot+m²Y_bg=(-p+beta)Y_bg+4(X_bg_dot-3HX_bg/2)D-2m²X_bg Phi, with |beta|<=27/4. Substituting the envelopes and dividing by k yields

    Ahat_dot=i(omega Ahat+P0)+i omega Bhat exp(-2imt)+r_A,
    Bhat_dot=-i omega Bhat-i(omega Ahat+P0) exp(2imt)+r_B,
    |r_A|+|r_B|<=C n/k.

For example the beta term costs Cn/m, the metric derivative term C|D|/k, and the carrier error in X_bg costs Cn/m; the leading metric approximation costs Cn/k. Hence |Ahat_dot|+|Bhat_dot|+|dhat_dot|<=C n. The fluid energy gives (sqrt(F))_dot<=C n because L Phi=O(n) and D=O(n/k), discarding both negative terms. The inequality at F=0 follows by regularizing with sqrt(F+epsilon) and taking epsilon down to zero in the integral bound. Gronwall gives sup n<=C N0. No derivative of opacity or of the fast fluid state is needed.

First take the reference operator on the exact background. Its homogeneous propagator has norm <=C on any subinterval: use the same sum of slow moduli and sqrt(F), the energy identity with D=0 and L Phi replaced by kappa P0/a, and bounded coefficients of the slow equations. In particular this bound is independent of k and lambda_m. The full scaled system is this linear operator plus the two displayed carrier terms plus a remainder of norm <=C n/k. In the fluid entries this follows from 3D/k, 4D, and L Phi-kappa P0/a=O(n/k). The slip equation has no remainder from gravity, and the same lambda_m exactly.

For the carrier terms, integrate exp(±2imt) by parts with coefficients (Ahat,Bhat,dhat) and smooth bounded background factors. Their derivatives are O(N0) even when the fluid collision rate is very large. Their cumulative primitive f(t) has norm <=C N0/m and is supported ONLY in the two complex scalar entries. If M(t) is the reference operator on the exact background, the restriction of M(t) to this scalar subspace has bounded norm independent of k and lambda_m (its only fluid contribution is through the bounded force kappa P0/a). Therefore the full state minus f(t) obeys the reference equation with forcing M(t)f(t) plus the ordinary remainder. Duhamel and the uniform propagator bound give sup error <=C N0/k. This argument avoids an invalid integration by parts involving the unbounded full propagator derivative.

Replace the reference background by a_d,H_d. In mean-slip coordinates the coefficient of lambda_m is exactly the same constant diagonal slip projection for both backgrounds. All remaining coefficient differences are O((1+k)/m²), from the smooth bounded functions of a,H and their acoustic factors k. Both reference propagators have the above energy estimate. A second Duhamel comparison costs C N0(1+k)/m², absorbed by C N0/k. Finally delta_s/k-2 Re Ahat=O(N0/m) by the carrier cancellation, E>=1, E-1=O(m^-2), K_s/rho_s<=2, and Phi/k=O(N0/k²). QED.

## 3. Sharp ordinary-dust handoff condition

Fix a release time t_*<T, with lambda_m=0 thereafter. Suppose A(t_*),B(t_*),d(t_*),e(t_*),v_b(t_*),v_gamma(t_*) are bounded uniformly in mass. These hypotheses can be tested on the incoming finite-mass IVP; they are not guaranteed by tight coupling across an arbitrary transition. Start the above theorem at t_* with the same full state. The reduced scalar and dust sector closes independently of the photon variables once lambda_m=0, because v_b*=v_*-w_*/(1+R_d) solves v_b*dot=-H_d v_b*+kappa P/a_d. Writing S=2Re Ahat_* and B_d=dhat_*, the two equations are

    S_ddot+2H_d S_dot+kappa² S/(4a_d⁴)=g(sS+b B_d)/a_d³,
    B_d_ddot+2H_d B_d_dot=g(sS+b B_d)/a_d³.

Initial S, S_dot, B_d are O(1/k); B_d_dot(t_*)=-v_b(t_*)/a_d(t_*)+O(m^-2) because the definition of the reduced v_b uses R_d rather than R. Define J(t) to be the baryon component of this coupled IVP with S=S_dot=B_d=0 and B_d_dot=-1/a_d(t_*) at t_*. It is independent of mass. By smoothness and its nonzero initial derivative there exists t1 in (t_*,T] with J(t1) nonzero. Linearity, bounded propagation, and the opacity-uniform estimate imply

    d_m(t)=k v_b(t_*) J(t)+O(1) uniformly on [t_*,T].

The O(1) bound depends on the uniform incoming data bound and fixed parameters, not mass. Therefore uniform boundedness of both unscaled matter contrasts on that interval is equivalent to k|v_b(t_*)|=O(1): necessity follows by evaluation at t1; sufficiency follows from the same reduced system and scaled error bound for both contrasts. In particular nonzero limiting release velocity forces unscaled density of order k at some fixed later time. This is an exact linear-IVP obstruction, not a claim that linear cosmology remains physically valid at arbitrarily large k with fixed initial amplitudes. It strengthens the frozen-background counterexample in #358 to the expanding self-gravitating model. For bounded k v_b(t_*), the ordinary unscaled dust+radiation approximation of #357 can be applied starting at t_*: its proof requires bounded A,B,d,u=m a v_b/k,e,h, the regular background bounds and zero collisions, all available here. Its reference uses A(t_*),d(t_*),u(t_*) and the limiting background, and its error is O(1/k) for bounded data, not a statement of convergence of unspecified mass-dependent initial data. The incoming photon acoustic data are not required to vanish.

## 4. Short transition estimate without a derivative of opacity

Let I=[t_-,t_+] have duration Delta. Assume incoming unscaled norm N_-=|A|+|B|+|d|+sqrt(F) at t_-. For sufficiently large m the same constraint and envelope estimates, now unscaled, give |m Phi|<=C N, |D|<=C N/k, |A_dot|+|B_dot|<=C N, |d_dot|<=C k N, (sqrt(F))_dot<=C N/k. Thus sup_I N<=C N_- exp(C k Delta). The mean, photon contrast and density derivatives are bounded by C k N independently of opacity. The slip variation-of-constants formula yields

    w_+=exp(-integral_I lambda_m) w_- + O(k Delta N_- exp(C k Delta)),
    (A,B,d,e,v)_+=(A,B,d,e,v)_- + O(k Delta N_- exp(C k Delta)).

Here the H/(1+R) slip damping can be included as bounded forcing, or integrated exactly. The release velocity is consequently

    v_b(t_+)=v_- - exp(-integral_I lambda_m)w_-/(1+R(t_+))
               + O(k Delta N_- exp(C k Delta)).

This is a quantitative interface map in the short layer k Delta << 1, including arbitrarily large integrated opacity. For bounded incoming N_-, k Delta=O(1) already preserves bounded unscaled incoming densities and envelopes. If v_-,w_-=O(1/k) and Delta=O(k^-2), the displayed estimate suffices for the sharp dust handoff condition. Conversely, if w_-=o(1), k Delta=o(1) and v_- tends to a nonzero constant, then v_b(t_+) has the same nonzero limit; a short drag-release layer cannot produce the ordinary dust approximation. The sharp handoff theorem applies directly at a fixed t_+ (or varying release times converging strictly inside the interval, by continuous dependence of the unit-response IVP). Long/phase-resolved transitions instead require the retained-opacity reduced system. QED.

## 5. Reproduction and diagnostics

Run `OPENBLAS_NUM_THREADS=1 python verify.py` using NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0. External 100-second timeout for hard wall enforcement; internal guards check logical IVP and segment counts and wall time between integrations, and RHS evaluation cap after each solver segment. Guard failure is INCOMPLETE. Fixed fractions (.26,.05,.09,.60), T=.6, 241 time samples, kappa in {1,4}, m in {16,32,64}, five profiles (smooth decay, rapid decay, reentrant, free generic velocity, free matched velocity), two full solvers DOP853/RK45, independent reduced reference and two unit-response IVPs. Smooth/rapid/reentrant profiles test scaled data; free handoff pairs test bounded unscaled incoming data at t_*=0 and differing velocity only. All calculations are finite floating-point checks, not a proof of the estimates. The initial run failed rapid profile (kappa=1,m=32) normalized slip disagreement 6.661286090694357e-6, tolerance 3e-6; the single solver repair split integrations at the two known opacity knots, retaining tolerances. A separate proposed monotonic maximum-absolute-density diagnostic was false: for kappa=1, m=16,32,64 the generic maximum remained 0.8 (amplitude units) while terminal contrasts were approximately .3010,.04566,-.30416. Replaced that unjustified diagnostic with the exact linear response identity for paired velocities. The six paired cases check reduced difference against the independently integrated unit-response coefficient; the full-field response is also recorded. This is not a universal monotonic growth claim. The final script passes 30 cases, 92 logical IVPs, 128 solver segments, 279436 RHS evaluations and five zero exact symbolic residuals. Receipt bytes can vary with platforms. No realistic recombination, Boltzmann hierarchy, baryon pressure, shear, primordial matching, horizon-scale modes, empirical likelihood, novelty or Lean result claimed. The sharp handoff is conditional on incoming data, not a theorem that physical recombination selects those data.
