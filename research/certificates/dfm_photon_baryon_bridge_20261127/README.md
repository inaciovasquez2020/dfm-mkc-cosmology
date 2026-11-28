# Controlled photon–baryon drag and joint Jeans/tight-coupling limit

2026-11-27. Public repository `inaciovasquez2020/dfm-mkc-cosmology`, inspected main `ea4f548e5c9b3160ea0a4dde76cab74be6a4964f`. Extends the analytical certificates PR #355 (pure scalar), #356 (scalar+dust+Lambda), #357 (independent perfect radiation, head `dc849dc8cf2b3c22bab117a6c36a998f5a0620db`). Independent standalone derivation, not a production solver modification. Standard Thomson drag conventions: Ma & Bertschinger, ApJ 455, 7 (1995), DOI 10.1086/176550, arXiv:astro-ph/9506072. No novelty claim for the fluid equations, sound speed or heat-conduction damping. Novelty of the scoped uniform error estimate NOT_ESTABLISHED. Lean and full repository CI NOT_RUN; no Codex or Claude.

## 1. Hypotheses and exact collision equations

Use cosmic time t, fixed interval [0,T], a(0)=H(0)=1, g=4 pi G=3/2, critical density initially 1. Positive scalar, dust and photon fractions s,b,r; ell>=0 and s+b+r+ell=1. The minimally coupled canonical quadratic complex scalar obeys psi_ddot+3H psi_dot+m²psi=0, with circular initial psi=sqrt(s)/m, psi_dot=i sqrt(s). Set rho_s=(|psi_dot|²+m²|psi|²)/2, K_s=|psi_dot|², rho_b=b/a³, rho_gamma=r/a⁴, H²=ell+rho_s+rho_b+rho_gamma, H_dot=-g(K_s+rho_b+4rho_gamma/3), a_dot=aH. Treat baryons as pressureless and photons as a perfect radiation fluid. No shear, polarization hierarchy, baryon temperature, energy exchange, recombination, neutrinos, or nonlinear perturbations. A nonnegative externally specified continuous conformal scattering rate Gamma_m(t) is allowed to depend on mass. Only elastic linear momentum exchange is included. Put R=3rho_b/(4rho_gamma)=3ba/(4r), L=k/a, G=Gamma_m/a, and use Newtonian gauge Phi=Psi.

For contrasts d=delta_b, e=delta_gamma and velocities v_j=theta_j/k, where theta_j is the usual conformal Fourier velocity divergence, the equations are

    d_dot=-L v_b+3D, e_dot=-4 L v_gamma/3+4D,
    v_b_dot=-H v_b+L Phi+G(v_gamma-v_b)/R,
    v_gamma_dot=L(e/4+Phi)-G(v_gamma-v_b),

where D=Phi_dot. The momenta q_b=rho_b a v_b/k and q_gamma=(4rho_gamma/3)a v_gamma/k are cosmic momentum potentials (delta T^t_i=-partial_i q). Their collision terms are +J and -J, respectively, with J=4rho_gamma Gamma_m(v_gamma-v_b)/(3k). Thus the total momentum exchange cancels exactly. For one real spatial Fourier harmonic eta of the complex scalar, let p=k²/a², Q_s=Re(conj(psi_dot)eta), X=m²Re(conj(psi)eta), Y=Re(conj(psi_dot)eta_dot), Q=Q_s+q_b+q_gamma. The exact Einstein constraint and Klein–Gordon equations are

    Delta_rho=Y+X-K_s Phi+rho_b d+rho_gamma e,
    Delta_p=Y-X-K_s Phi+rho_gamma e/3,
    p Phi+g(Delta_rho+3H Q)=0, D=gQ-H Phi,
    eta_ddot+3H eta_dot+(m²+p)eta=4psi_dot D-2m²psi Phi.

Solve Phi algebraically with denominator p-gK_s, as in #357. The constraint propagation and spatial trace identities from #357 are unchanged, because the derivative of total momentum contains +J-J=0, and neither linear continuity equation gains a collision term. Explicitly, the constraint derivative with Phi_dot=D equals -3H times the constraint; the actual derivative differs by (p-gK_s)(Phi_dot-D). The trace equation is Phi_ddot+4H Phi_dot+(2H_dot+3H²)Phi=g Delta_p. Thus the reconstructed metric is consistent on intervals with nonzero denominator. The symbolic check in verify.py independently expands both identities, allowing an arbitrary J.

## 2. Exact acoustic dissipation, entropy and tight coupling

Define slip w=v_gamma-v_b, weighted mean v=(R v_b+v_gamma)/(1+R), entropy sigma=d-3e/4, and gamma=HR/(1+R). Direct differentiation, using R_dot=HR, gives

    v_dot=-gamma v+L(Phi+e/(4(1+R))),
    w_dot=H v+L e/4-[G(1+1/R)+H/(1+R)]w,
    e_dot=-4L v/3-4LR w/(3(1+R))+4D,
    sigma_dot=L w.

The energy F=R v_b²+v_gamma²+3e²/16 obeys exactly

    F_dot=-HR v_b²-2G w²+2L Phi(R v_b+v_gamma)+(3/2)e D.

Hence the acoustic+drag subsystem is dissipative apart from metric forcing. The drag-free tight-coupling mean equations with w=0 have squared sound speed c_s²=1/[3(1+R)]. These identities are algebraic, not a formal truncation of the collision operator. In particular sigma need not initially vanish. Let lambda_m=inf_[0,T] G(1+1/R). If positive, variation of constants proves

    |w(t)| <= exp(-lambda_m t)|w0|+C k integral_0^t exp(-lambda_m(t-u)) n(u) du,
    integral_0^t k|w(u)| du <= k|w0|/lambda_m + C k²/lambda_m integral_0^t n(u) du,

where n controls |v| and |e| and k>=1. This explicitly includes the initial layer for unmatched velocities. The second inequality, not only small pointwise slip, controls entropy drift and cumulative acoustic error.

## 3. Joint scalar–plasma theorem (PROVED)

Fix T>0, kappa>0, s,b,r,ell as above. Let k²=m kappa, k>=1, m sufficiently large, and lambda_m>=k². Prescribe mass-independent bounded initial scalar envelopes A0,B0, and fluid data e0,v0,w0,sigma0. Define envelopes exactly as in #357:

    X_bg=m a^(3/2)psi/sqrt(s), Y_bg=m a^(3/2)eta/sqrt(s),
    X_bg=U exp(imt)+V exp(-imt), X_bg_dot=im(U exp(imt)-V exp(-imt)),
    Y_bg=A exp(imt)+B exp(-imt), Y_bg_dot=im(A exp(imt)-B exp(-imt)).

Let N0=|A0|+|B0|+|sigma0|+sqrt(F(0)); F(0) is equivalent to the squared norm of the initial fluid acoustic+slip data for fixed positive R(0). Define limiting background a_d by a_d(0)=1, H_d²=ell+(s+b)/a_d³+r/a_d⁴, a_d_dot=a_d H_d. Define R_d=3ba_d/(4r), L_d=k/a_d. Define the mass-dependent free tight-coupling acoustic reference e_*,v_* by

    e_*_dot=-4L_d v_*/3,
    v_*_dot=-H_d R_d v_*/(1+R_d)+L_d e_*/(4(1+R_d)),
    (e_*,v_*)(0)=(e0,v0).

It retains the fast acoustic phase, rather than purporting to be a pointwise limit. Define the slow scalar reference d_s by

    d_s_ddot+2H_d d_s_dot+kappa² d_s/(4a_d⁴)=g(s d_s+b sigma0)/a_d³,
    d_s(0)=2 Re A0, d_s_dot(0)=-kappa Im A0.

There exists C finite depending only on fixed T,kappa,fractions (not on m or the continuous drag profile above the floor) such that

    sup (|delta_s-d_s|+|e-e_*|+|v-v_*|+|d-(sigma0+3e_*/4)|+|sigma-sigma0|)
        <= C N0 (1/k+k²/lambda_m),
    |w(t)| <= |w0| exp(-lambda_m t)+ C N0 k/lambda_m,

where delta_s=(Y+X-K_s Phi)/rho_s. Thus lambda_m/k² -> infinity suffices for simultaneous high-mass and ideal tight-coupling convergence. Unlike the independently conserved dust theorem, the plasma's adiabatic baryon contrast is oscillatory at leading order, not a slow dust mode. The surviving baryon source in the scalar limit is its constant entropy offset sigma0. With sigma0=0 the baryon term in that slow gravitational source vanishes. This is not a claim of physical absence of baryons from the background, nor of vanishing photon or baryon density at each time.

### Proof

All C below are independent of m and opacity, for the fixed parameters. By the circular charge-energy inequality of #357, H<=1, |H_dot|<=3, 1<=a<=exp(T), E=a³rho_s/s satisfies 1<=E<=1+24/m² for m>=6. Comparing the uniformly Lipschitz background ODE with E=1 gives |a-a_d|+|H-H_d|<=C/m². The carrier rescaling has bounded coefficient beta=3H_dot/2+9H²/4, so |U|+|V|<=C and |U-1|+|V|<=C/m. As p-gK_s>=p/2 for m>=6 exp(2T)/kappa, the linear IVP is regular. These prior estimates use nonnegative background densities, not the independent evolution of perturbations; elastic collisions do not change the homogeneous equations.

Set n=|A|+|B|+|sigma|+sqrt(F). On the bounded interval R is bounded above and below by positive constants. Thus |d|,|e|,|v_b|,|v_gamma| are <=C n, and the scalar cancellation from #357 gives

    |a³(Y+X)/s-2Re A|<=C n/m,
    |Q_s|<=C n/m, |q_b|+|q_gamma|<=C n/k.

The algebraic Einstein constraint implies |m Phi|<=C n, |D|<=C n/k and

    |m Phi-P0|<=C n/k,
    P0=-g[2s Re A+b sigma+(3b/4+r/a)e]/(kappa a).

In particular the exact rescaled scalar envelope equations are

    A_dot=i(omega A+P0)+i omega B exp(-2imt)+r_A,
    B_dot=-i omega B-i(omega A+P0) exp(2imt)+r_B,
    omega=kappa/(2a²), |r_A|+|r_B|<=C n/k.

This follows by substituting the exact rescaled KG equation Y_bg_ddot+m²Y_bg=(-p+beta)Y_bg+4(X_bg_dot-3H X_bg/2)D-2m²X_bg Phi. The metric derivative remainder is O(n/k), not assumed slowly varying. Hence |A_dot|+|B_dot|<=C n. From the energy identity and Cauchy–Schwarz, (sqrt(F))_dot<=C n/k (valid at zero by regularization with sqrt(F+epsilon) and passage to the limit). Integrating these bounds and the slip integral inequality for sigma yields

    n(t)<=C N0 + C(1+k²/lambda_m) integral_0^t n(u) du.

Here k|w0|/lambda_m<=C N0 since lambda_m>=k², k>=1. Gronwall bounds sup n<=C N0. All these estimates hold for any finite continuous drag function on [0,T], independent of its upper bound. The slip and entropy estimates follow: sup |sigma-sigma0|<=C N0(k/lambda_m+k²/lambda_m)<=C N0 k²/lambda_m.

For the acoustic reference on the exact background, compare (e,v) with the solution of the zero-slip, zero-metric equations with the same initial pair. Its time-dependent energy F_tc=(1+R)v²+3e²/16 has homogeneous derivative -HR v², hence its propagator has uniformly bounded Euclidean norm independent of k by norm equivalence. The forcing of the difference is (-4LRw/(3(1+R))+4D,L Phi). Its integral norm is <=C N0(k²/lambda_m+1/k), by the slip integral and metric bounds. Duhamel gives this bound for the acoustic pair error. Replacing a,H by a_d,H_d perturbs the acoustic generator by O((1+k)/m²); both propagators have the same uniformly equivalent energy estimate. Thus the additional uniform error is O(N0 k/m²), which is absorbed in N0/k. Recover d from sigma+3e/4. This does not require bounding derivatives of opacity.

For scalar averaging, separate P0 into P_m=-g(2s Re A+b sigma0)/(kappa a), its entropy error O(N0 k²/lambda_m), and the acoustic term f(a)e. The entropy error remains bounded even when multiplied by the fast carrier exponentials. For the carrier terms with coefficients of A,B and sigma0, integrate exp(±2imt) by parts: their cumulative size is O(N0/m), using the derivative bound on A,B and bounded a_dot. The fast terms involving e have |e_dot|<=C k N0, so the same argument bounds them by O(N0 k/m)=O(N0/k). The slow acoustic term integrates to O(N0/k) by the exact mean equation:

    e=4(1+R)(v_dot+gamma v-L Phi)/L.

For any of the smooth coefficient factors f(a), integration by parts moves v_dot onto 4 f(a)(1+R)/L, whose magnitude and derivative are O(1/k); v is bounded and Phi=O(N0/m). Thus all cumulative scalar errors are O(N0(1/k+k²/lambda_m)). Comparing integral equations by Gronwall to A_dot=i(omega A+P_m), B_dot=-i omega B, then replacing a by a_d at cost O(N0/m²), gives the uniform envelope approximation. The physical density differs from 2Re A by O(N0/m), by the exact carrier cancellation, E>=1 and K_s/rho_s<=2. Taking twice the real part of the limiting A equation and differentiating, using omega_dot=-2H_d omega, yields the scalar reference IVP. This completes the proof.

## 4. Necessary caution: slip small does not imply ideal acoustic limit

For the auxiliary constant-coefficient, gravity-free fluid system (a=1,H=0,R>0 constant), set Gamma=alpha k² for fixed alpha>0. This is a frozen-background diagnostic, not a self-consistent expanding Einstein cosmology. Eliminating e,v,w yields the cubic dispersion equation

    (z²+c_s² k²)(z+Lambda_c)+d_c k² z=0,
    Lambda_c=Gamma(1+1/R), d_c=R/[3(1+R)].

Let epsilon=1/k, z=k mu, and D_c=alpha(1+1/R). The equation becomes (mu²+c_s²)(D_c+epsilon mu)+epsilon d_c mu=0. At epsilon=0 the roots mu=±i c_s are simple. The implicit function theorem gives mu=±i c_s-epsilon d_c/(2D_c)+O(epsilon²), hence

    z_±=±i c_s k-R²/[6 alpha(1+R)²]+O(1/k).

For these modes w/e=k/[4(z+Lambda_c)]=O(1/k), but the acoustic amplitude is damped by a nonvanishing factor on fixed positive time intervals. Choosing bounded real initial data from the real part of the complex acoustic eigenmode yields a counterexample to uniform ideal (undamped) acoustic approximation when only Gamma/k -> infinity is assumed. At fixed t>0 a continuous sequence of k with c_s k t an integer multiple of 2pi exhibits the nonzero error. The limiting damping coefficient is the familiar slip/heat-conduction contribution, not the full Silk damping coefficient (photon shear is absent). The theorem's stronger scale condition lambda_m/k² -> infinity is sufficient, and this example excludes weakening it to lambda_m/k -> infinity in general. No assertion of necessity for all nonconstant interacting cosmologies.

## 5. Decoupling boundary (not a recombination theorem)

At any exact switch from drag to zero drag, evolve the full finite-mass equations continuously with the terminal state of the first segment (piecewise continuous coefficients suffice). The previous independently conserved dust averaging theorem uses bounded u=m q_b/rho_b=m a v_b/k. For k²=m kappa this requires v_b=O(1/k), whereas a generic acoustic state has v_b=O(1). Tight coupling alone imposes no such bound. The obstruction is already visible in the frozen gravity-free post-switch dust equation d_dot=-k v_b, v_b_dot=0: a nonzero mass-independent release velocity produces density change of order k on a fixed interval. This is a counterexample to an unconditional uniform slow-dust handoff, not to physical finite-k decoupling; linearization can cease to be valid for fixed perturbation amplitude as k increases. A controlled full transition needs an explicit opacity history and phase/velocity matching or a different post-switch scaling. No such realistic transition is established here.

## 6. Computational validation and limits

Run `OPENBLAS_NUM_THREADS=1 python verify.py` with NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0. Use an external 100-second timeout for hard time enforcement; internal 90-second and call-count guards act between integrations, evaluation guard after solver return. Guard failure is INCOMPLETE. The script independently solves the full Cartesian scalar, algebraic Einstein constraints and interacting fluid variables and the reduced scalar/acoustic reference. Parameters s=.26,b=.05,r=.09,ell=.60, T=.8, kappa in {1,4}, m in {16,32,64,128}, matched or nonzero initial slip, nonzero entropy, counter-rotating scalar perturbation. The chosen opacity is G=lambda_m R/(1+R), lambda_m=k² sqrt(m). Two independent explicit ODE algorithms DOP853 and RK45. Initial run failed the slip comparison (kappa=4,m=16, normalized discrepancy 2.061476e-5, original tolerance 3e-6); repaired only the maximum step to min(.4/m,1/lambda_m), retaining the tolerance, then rebuilt/reran. The receipt includes five zero symbolic residuals and 36 cubic spectral cases across R, alpha and k. These checks do not prove the theorem or the optimal error rate. No Mac execution, Lean, full production solver tests or observational likelihood. OPEN: photon shear and polarization closure, neutrinos, realistic opacity/recombination, controlled post-decoupling matching, primordial/horizon-scale normalization and historical calibration equivalence. No repository writes; integration requires separate approval.
