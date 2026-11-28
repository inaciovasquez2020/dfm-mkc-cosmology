# Uniform low-block metric feedback and self-consistent scalar–Einstein–Boltzmann averaging

2026-11-27. Public DFM-MKC base `ea4f548e5c9b3160ea0a4dde76cab74be6a4964f`. Extends PR #359 (`b8ecf585d5c94692e04c6990091335c77fa4b3f6`) and PR #360 (`0fb25fe24f29b7a4539ed4d67db334ffe7c4fdd5`). Inspected `src/dfm_mkc_solver/{metric_constraint_elimination_v1,dark_sector_fourier_rhs_v1,radiation_species_coupled_fourier_rhs_v1,photon_scalar_polarization_hierarchy_v1}.py`. Uses the standard physical Legendre photon polarization brightness hierarchy, not a claim of spin-2 equivalence for the repository's E recurrence. Standard references: Ma and Bertschinger, ApJ 455, 7 (1995), DOI 10.1086/176550, arXiv:astro-ph/9506072; Blas, Lesgourgues, Tram, CLASS II, DOI 10.1088/1475-7516/2011/07/034, arXiv:1104.2933. The equations and hierarchy methods are established physics; novelty of the estimates is NOT_ESTABLISHED. Analytic PROVED within the stated linear model; standalone COMPUTATION_PASS, Lean/Mac/full production tests NOT_RUN. No production code change, Codex or Claude.

## 1. Background, conventions, exact constrained dynamics

Cosmic time t in [0,T], normalized a(0)=H(0)=1, initial critical density 1, g=4 pi G=3/2. Fractions s,b,r,n>0, ell>=0, s+b+r+n+ell=1: canonical minimally coupled quadratic complex scalar, pressureless baryons, photons, collisionless massless neutrinos, cosmological constant. Scalar mass m>0; circular initial psi=sqrt(s)/m, psi_dot=i sqrt(s). Define rho_s=(|psi_dot|^2+m^2|psi|^2)/2, K=|psi_dot|^2, rho_b=b/a^3, rho_g=r/a^4, rho_n=n/a^4. Equations:

    psi_ddot+3H psi_dot+m^2 psi=0,
    a_dot=aH, H^2=ell+rho_s+rho_b+rho_g+rho_n,
    H_dot=-g Wtot, Wtot=K+rho_b+4(rho_g+rho_n)/3.

Prescribe a nonnegative integrable cosmic scattering rate G_c(t) (conformal opacity a G_c), allowed to depend on m and k, with no bound uniform in m assumed. Only elastic linear Thomson momentum exchange; no nonlinear perturbations, baryon pressure, massive neutrinos, recombination law or ionization/temperature evolution. Linear scalar metric convention is lapse Psi, spatial curvature Phi, Newtonian gauge. Let eta be the complex scalar perturbation of one real spatial Fourier harmonic. Put p=k^2/a^2, L=k/a, k>0. Define the exact lapse-corrected velocity

    chi=eta_dot-psi_dot Psi.

Then the conventional perturbed Klein-Gordon equation

    eta_ddot+3H eta_dot+(m^2+p)eta=psi_dot(Psi_dot+3Phi_dot)-2m^2 psi Psi

is equivalent to

    eta_dot=chi+psi_dot Psi,
    chi_dot=-3H chi-(m^2+p)eta+3psi_dot D-m^2 psi Psi,
    D=Phi_dot.

Differentiate chi and use the background field equation. The transformation is algebraic and invertible on the constrained states when the metric is reconstructed below. It avoids differentiating the opacity or the anisotropic stress. In particular the lapse perturbation disappears from the stress-energy formulas:

    Rk=Re(conj(psi_dot)chi), Xp=m^2 Re(conj(psi)eta),
    delta_rho_s=Rk+Xp, delta_p_s=Rk-Xp, q_s=Re(conj(psi_dot)eta).

Use baryon contrast delta_b and velocity v_b=theta_b/k. Photon temperature Theta_l=F_gamma,l/4, polarization brightness P_l=G_gamma,l/4 (NOT spin-weighted E_l), and massless-neutrino brightness N_l=F_nu,l/4. Thus delta_g=4Theta_0, delta_n=4N_0, v_g=3Theta_1, v_n=3N_1, sigma_g=2Theta_2, sigma_n=2N_2. Cosmic momentum q_j=(rho_j+p_j)a v_j/k; use delta T^t_i=-partial_i q. Set

    Q=q_s+q_b+q_g+q_n,
    Delta=Rk+Xp+rho_b delta_b+4rho_g Theta_0+4rho_n N_0,
    Ptot=Rk-Xp+4(rho_g Theta_0+rho_n N_0)/3,
    Sstress=4(rho_g sigma_g+rho_n sigma_n)/3.

The three Einstein constraints now solve directly:

    Phi=-g(Delta+3H Q)/p,
    Psi=Phi-3g Sstress/p,
    D=g Q-H Psi.

There is no denominator p-gK; the only division is by p>0. At a fixed k the map from chi to eta_dot is eta_dot=chi+psi_dot Psi with Psi already reconstructed from chi. At a singular p-gK the inverse map from freely specified eta_dot need not exist; the regular constrained IVP uses chi as independent data, and does not assert arbitrary coordinate-velocity data are admissible there. No k=0 assertion.

Baryons:

    delta_b_dot=-L v_b+3D,
    v_b_dot=-H v_b+L Psi+G_c(3Theta_1-v_b)/R,
    R=3rho_b/(4rho_g), R_dot=H R.

Each of Theta,P,N streams by L[l X_(l-1)-(l+1)X_(l+1)]/(2l+1). Add D to Theta_0 and N_0; add L Psi/3 to Theta_1 and N_1. Photon dipole gets G_c(v_b/3-Theta_1); intensity l>=2 gets -G_c Theta_l and source G_c Pi/10 at l=2. Polarization brightness all l gets -G_c P_l and sources G_c Pi/2 at l=0, G_c Pi/10 at l=2, Pi=Theta_2+P_0+P_2. No other terms for massless neutrinos. This is the Ma–Bertschinger Legendre brightness convention, not the repository E-chain convention. Physical polarization E-mode output conversion and observable line-of-sight integrals are not supplied.

### Constraint propagation (exact)

Individual scalar identities from the chi equations:

    (Rk+Xp)_dot=-6H Rk-p q_s+3K D,
    (q_s)_dot=-3H q_s+Rk-Xp+K Psi.

The fluid monopole/dipole equations give the total conservation identities, with arbitrary equal-and-opposite Thomson momentum transfer J:

    Delta_dot=-3H(Delta+Ptot)-p Q+3 Wtot D,
    Q_dot=-3H Q+Ptot+Wtot Psi-Sstress.

The finite hierarchy with N_cut>=2 has the same conservation identities (only monopole and dipole derivatives enter). Write F=p Phi+g(Delta+3H Q), A=p(Phi-Psi)-3g Sstress. Differentiating F with Phi_dot temporarily set to D gives Fdot|D=-3H F+H A. The actual derivative differs by p(Phi_dot-D), and F=A=0 by reconstruction. Thus Phi_dot=D identically. Differentiating D and using H_dot=-g Wtot gives the spatial trace equation

    Phi_ddot+3H Phi_dot+H Psi_dot+(2H_dot+3H^2)Psi+g Sstress=g Ptot.

This holds almost everywhere for integrable prescribed opacity; all reconstructed potentials are absolutely continuous at fixed m,k. The traceless equation is A=0. Thus all scalar Einstein equations propagate, including shear, without computing Psi_dot in the evolution equations. The exact symbolic checks independently expand these identities, the change of variable and the scalar energy equation. These are identities of the specified perturbation system; no equivalence to every production RHS is claimed.

## 2. Uniform metric-feedback theorem

Fix T>0, kappa>0 and fractions above. Jeans scaling k^2=m kappa, m sufficiently large (k>=1). The following estimates use a constant C depending only on T,kappa,fractions, not on m, the hierarchy cutoff, or the opacity. Different occurrences of C may denote different finite constants. Normalize matter contrasts by k; this permits bounded incoming fluid velocities even at decoupling, as in #359. Let

    x=m psi/sqrt(s), v=psi_dot/sqrt(s),
    y=m eta/(k sqrt(s)), w=chi/(k sqrt(s)),
    X=a^(3/2)x, Z=a^(3/2)v,
    Y=a^(3/2)y, W=a^(3/2)w,
    h=3H/(2m), Vp=W+hY,
    A=(Y-i Vp)exp(-imt)/2, B=(Y+i Vp)exp(imt)/2,
    d=delta_b/k.

These are exact invertible rotating coordinates, not definitions using the true Y_dot (which includes a metric term). Put c_b=sqrt(R/3)v_b, and weight each brightness moment by sqrt(2l+1). Let z be the real Hilbert state (A,B,d,c_b,weighted Theta,P,N), with standard squared norm |A|^2+|B|^2+d^2+c_b^2+sum_l(2l+1)(|Theta_l|^2+|P_l|^2+|N_l|^2). Finite or infinite weighted square-summable data allowed; initially A,B,d and c_b are arbitrary finite, independent of m for a limiting comparison, and all brightness data have uniformly bounded norm. Define N0=||z(0)||. Place the extra scalar and baryon variables in degrees <=2, c_b in degree 1, streaming zero on them. All comparisons use the same prescribed initial rotating and brightness data. These choices are a rescaled linear perturbation limit, not a uniform bound on unscaled physical contrasts.

### Background estimates

The circular energy-charge calculation of #357 and #359 applies with two radiation species because H is nonincreasing. With E=a^3 rho_s/s, J_bg=a^3 Re(conj(psi)psi_dot)/s, Q_bg=a^3 Im(conj(psi)psi_dot)/s, E^2>=m^2(J_bg^2+Q_bg^2), m Q_bg=1 and (E+3HJ_bg/2)_dot=3H_dot J_bg/2. Since E(0)=1 and J_bg(0)=0, M=max E satisfies M-1<=3 sqrt(M^2-1)/m. Thus 1<=E<=1+24/m^2 for m>=6. Also 1<=a<=exp(T), 0<H<=1, |H_dot|<=3. The background exists on [0,T] since rho_s>=s exp(-6T) and the fields and derivatives remain bounded for fixed m. Compare a_dot=a sqrt(ell+(sE+b)/a^3+(r+n)/a^4) to the dust-plus-radiation-plus-Lambda solution a_d,H_d obtained by E=1. The RHS is uniformly Lipschitz in a,E on the compact domain with positive lower bound on the radicand; hence |a-a_d|+|H-H_d|<=C/m^2. The rescaled X solves X_ddot+m^2 X=beta X, beta=3H_dot/2+9H^2/4 uniformly bounded. Its exact background envelopes satisfy U_dot=beta(U+V exp(-2imt))/(2im), V_dot=-beta(U exp(2imt)+V)/(2im), U0=1-3i/(4m), V0=3i/(4m). Gronwall yields |X-exp(imt)|+|Z-i exp(imt)|<=C/m (Z=X_dot/m-hX). All constants independent of m.

### Feedback estimate

Uniformly in all state coordinates, the matter density source satisfies

    a^3 (Rk+Xp)/(s k) = Re(conj(Z)(Vp-hY)+conj(X)Y)
                       = 2 Re A + O(||z||/m).

The second equality uses the preceding two background estimates and Y=A exp(imt)+B exp(-imt), Vp=i(A exp(imt)-B exp(-imt)). The fast cross terms cancel. Scalar momentum is s k/(m a^3) Re(conj(Z)Y); baryon and radiation momenta are O(||z||/k), since k/m=kappa/k and each low moment is bounded by its weighted norm. Thus

    |Delta|<=C k||z||, |Q|<=C||z||/k, |Sstress|<=C||z||,
    |Phi|+|Psi|+|D|<=C||z||/k,
    |Phi-Psi|<=C||z||/k^2,
    |(m/k)Psi-P_m|<=C||z||/k,
    P_m=-g(2s Re A+b d)/(kappa a).

For the last estimate insert the density cancellation into the algebraic constraints; the radiation density is O(||z||) and the shear likewise, and the momentum correction is O(||z||/k). The denominators are p=k^2/a^2, with a bounded. No opacity enters the estimates.

The exact rescaled chi equations give

    Y_dot=m Vp+(m/k) Z Psi,
    Vp_dot=-mY+(-p+beta)Y/m+3 Z D/k+(m/k)(-X+h Z)Psi.

So with omega=kappa/(2a^2), differentiating the rotating variables gives

    A_dot=i omega(A+B exp(-2imt))+i P_m+epsilon_A,
    B_dot=-i omega(B+A exp(2imt))+epsilon_B,
    |epsilon_A|+|epsilon_B|<=C||z||/k.

Indeed the potential contribution to A_dot is (m/(2k))exp(-imt)(Z+iX-i h Z)Psi, to B_dot is (m/(2k))exp(imt)(Z-iX+i h Z)Psi. The first equals i(m/k)Psi+O(||z||/m), the leading contribution to the second cancels. The beta and D terms are bounded by C||z||/m and C||z||/k^2 respectively. This cancellation uses the lapse-corrected coordinate; the previous coordinate-velocity envelopes have different fast terms. In particular ||A_dot||+||B_dot||<=C||z|| without differentiating opacity or higher multipoles. Also d_dot=-v_b/a+3D/k is bounded by C||z||.

The exact generator on z is therefore L S + C_col(t) + B_low(t). S is the direct sum Legendre skew streaming matrix of norm<=1 (zero on other variables), C_col is the Thomson collision block plus baryon Hubble damping. It is dissipative in the fixed weighted Hilbert norm by the energy calculation of #360: the dipole/baryon block contributes -(2G_c/3)(v_g-v_b)^2-H R v_b^2/3; the symmetric polarization collision block has eigenvalues -1,-1,-3/10 times G_c, and other multipoles have negative diagonal or zero collisions. B_low contains the scalar rotated RHS, d_dot and metric forcing. All its inputs and outputs lie in degrees <=2. Its norm is bounded by C independent of m,k,opacity and cutoff: the scalar and density bounds were just proved; metric forcing on fluid dipoles and c_b has size O(L|Psi|)=O(||z||), monopoles have D=O(||z||/k). Thus the symmetric part of the full generator is <=C I. For every fixed m, integrability of G_c gives bounded integrable generator on this Hilbert space; the integral equation gives unique absolutely continuous solutions (also for finite projections). Energy and Gronwall yield

    ||z(t)||<=exp(Ct) N0

uniformly in cutoff and opacity. This verifies, rather than assumes, the conditional low-block hypothesis of #360.

## 3. Self-consistent truncation theorem (PROVED)

Let initial data be supported on degrees <=p0, p0>=2, let N_cut>=p0, and observe the projection to degrees <=q0, 2<=q0<=N_cut. Compare the full hierarchy and its zero-terminal truncation on the same exact background, with their own algebraically reconstructed metric. They are compressions of the same bounded integrable generator in the normalized state. Rescaling by exp(-Ct) makes the generator dissipative; all nonstreaming terms commute with projections at degrees >=2. The upper-tail and adjoint two-way propagation argument of #360 therefore applies verbatim with streaming size L<=k. In particular

    ||P_q0(z-z_Ncut)(t)|| <= exp(Ct) N0 (kt)^D/D!, D=2N_cut+2-p0-q0,
    ||z-z_Ncut|| <= exp(Ct) N0 (kt)^(N_cut+1-p0)/(N_cut+1-p0)!.

The same bound holds with kt replaced by integral_0^t L(s)ds (streaming optical length), by changing the integration variable in the beta-integral proof. To recall that proof: tail above j is forced only by streaming from degree j; its contractive rescaled propagator gives inductive factorial tail bounds. The error in the retained section is forced only through the omitted boundary link. By adjoint reverse-time propagation, reaching low degree q0 from degree N_cut costs a second factorial factor. Convolution gives exponent D. The full-state bound follows instead from the residual of the zero-extended truncated solution. For arbitrary weighted square-summable data, split into low data and initial tail, adding at most 2 exp(Ct) times the tail norm to the bound. No finite numerical reference needed in the proof.

All scaled matter contrasts, k Phi, k Psi, k D and k^2(Phi-Psi) are bounded linear outputs on degrees <=2, with operator norms independent of m,k,opacity. Consequently their errors have the same low factorial bound up to a constant factor. This includes quadrupole anisotropic stress, and both self-consistent metric potentials, not just prescribed forcing. For fixed T and k^2=m kappa, N_cut=ceil(c sqrt(m))+O(1) with c sufficiently large (e.g. c> e T sqrt(kappa)/2 for the low bound, c>e T sqrt(kappa) for full-state) is sufficient for exponentially small truncation error with fixed p0 and q0. This is not an optimal or necessary cutoff formula.

## 4. Joint scalar averaging with exact interacting radiation hierarchy (PROVED)

A mass-dependent reduced reference must retain the actual radiation hierarchy and opacity; in general it has no pointwise limit as k grows. First use the exact background a,H in the reference. Drop the exp(±2imt) terms from the displayed scalar envelope equations and set remainders to zero. Evolve

    Abar_dot=i(omega Abar+Pbar), Bbar_dot=-i omega Bbar,
    dbar_dot=-vbar_b/a,
    Pbar=-g(2s Re Abar+b dbar)/(kappa a).

Use all original photon and neutrino streaming/collision rows, and baryon Euler row, but replace D by zero and L Psi by kappa Pbar/a. This removes subleading radiation density/shear and momentum sources from the leading slow matter potential while retaining their full streaming, collision and velocity dynamics. Radiation effects on baryon velocity and hence density remain. In particular one has NOT replaced radiation by a perfect fluid or used a slip-only approximation. For the leading potential define Phibar=Psibar=k Pbar/m. The reference is a linear evolution with the same bounded low block and dissipative high generator, so its propagator has the same uniform energy estimate.

The full vs reduced generators differ by a low oscillatory operator L_fast with just i omega B exp(-2imt), -i omega A exp(2imt) in the scalar rows and a uniformly bounded remainder of norm <=C/k. A frozen-coefficient primitive K_fast is obtained by dividing those two entries by -2im and +2im respectively. Its operator norm <=C/m, and ||K_fast_dot-L_fast||<=C/m since omega_dot=-2H omega. Along the exact solution, derivative of K_fast z is L_fast z+O(N0/m), because only A_dot,B_dot appear, and these are uniformly bounded. Crucially the primitive is supported in scalar coordinates where the radiation streaming and all collision terms are zero. Subtract K_fast z from the full-minus-reduced error: the reduced generator applied to K_fast z is also O(N0/m), not O(G_c/m). Initial correction is O(N0/m). Duhamel with the uniform reduced propagator proves

    sup_[0,T] ||z-zbar||<=C N0/k.

This avoids differentiating a fast or opacity-dependent remainder and is uniform in hierarchy depth. The exact scaled matter contrast differs from 2Re A by O(||z||/m) since E=1+O(m^-2). The scaled potentials k Phi,k Psi differ from k Phibar=k Psibar=kappa Pbar by O(N0/k). The result includes all weighted radiation moments in the error norm, at each fixed m,k. It compares two mass-dependent solutions, not convergence of radiation to a mass-independent function.

### Replacing the exact background by a_d without an opacity upper bound

Naively comparing collision matrices at R and R_d costs G_c |R-R_d|; this is not uniformly small for unbounded opacity. The following argument avoids that loss. In the weighted velocity pair (c_b,c_g)=(sqrt(R/3)v_b,sqrt(3)Theta_1), rotate by the orthogonal matrix with rows (sqrt(R),1)/sqrt(1+R) and (-1,sqrt(R))/sqrt(1+R). The first coordinate is the collision kernel, the second the slip. Collision in this basis is diagonal (0,-lambda), lambda=G_c(1+1/R). All other collision blocks are unchanged, including the brightness quadrupole/polarization matrix and high diagonal. Use the same rotation with R_d=3ba_d/(4r) in the dust-background reference, and prescribe the same cosmic G_c(t) in both systems. The two rotation matrices differ by O(m^-2), their time derivatives likewise, by the uniform estimates for a,H and R_dot=H R. Streaming conjugation preserves skew-adjointness; its difference in norm, including L-L_d, is O(k/m^2). All bounded low coefficients and baryon Hubble terms differ by O(m^-2). Only the slip collision coefficient needs separate control, and |lambda-lambda_d|<=C m^-2 lambda with lambda and lambda_d comparable uniformly (both zero when G_c=0).

Let e be the difference of the two reduced solutions in their respective rotated coordinates, with identical initial data. All noncollision generator differences yield forcing of norm <=C(1+k)N0/m^2. The extra term in the slip coordinate has size |lambda-lambda_d| |v_slip,d|. The squared energy inequality, using Young's inequality to absorb lambda |e_slip|^2, is

    (||e||^2)_dot <= C||e||^2+C N0^2 (1+k)^2/m^4
                        +C m^-4 lambda_d |v_slip,d|^2.

The reference dissipative energy estimate, integrated in time with its bounded low block, gives integral lambda_d |v_slip,d|^2 <= C N0^2. This holds independently of the integral or maximum opacity. Gronwall yields ||e||<=C N0(1+k)/m^2, and reversing the rotations costs O(N0/m^2). Thus replacing a,H throughout the reduced system by a_d,H_d preserves the O(N0/k) joint error bound. If a different conformal opacity is specified in the reference rather than the same cosmic opacity, analogous relative coefficient control must be verified; no unconditional comparison of unrelated opacity histories is claimed.

Combine Sections 3–4: the dust-background rotating scalar reference with full physical brightness/polarization and massless neutrino hierarchies, prescribed cosmic opacity and scaled baryon density, is uniformly accurate to O(N0/k), plus the controlled finite-section truncation error. The theorem is finite-time, fixed positive kappa, linear, and with the specified normalization. The unscaled density errors may remain O(1); no assertion of ordinary unscaled slow dust convergence or adiabatic primordial initialization. QED.

## 5. Computational reproduction and limitations

`OPENBLAS_NUM_THREADS=1 timeout 120 python verify.py` with NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0. The script additionally uses SIGALRM at 115 s, a 100-second between-call guard, 140 integration cap and post-solver 150000 RHS evaluation cap. Any guard or failed solver is INCOMPLETE. Finite tests use s=.26,b=.05,r=.06,n=.03,ell=.60, T=.6, 161 samples, kappa in {1,4}, m in {16,32,64,128}, profiles zero, smooth release, reentrant G_c of order k^2. Nonzero initial polarization, neutrino shear, scalar counter-rotating envelope and baryon velocity. Two explicit ODE methods DOP853/RK45 solve the regular full Cartesian system at cutoff 32; independent averaged dust-background reference per case. All three hierarchies retain physical Legendre brightness rows and their self-consistent metric sources. Twelve additional cutoff comparisons at {4,8,16} against 48, at m=32,128 and kappa=4, for free and reentrant profiles. Numerical agreement alone cannot certify an error smaller than the solver tolerance; the factorial bound is analytic, and the logged factorial factor omits the unspecified analytic feedback prefactor. Maximum errors use finite samples and include scaled metric outputs; not rigorous interval arithmetic. The receipt reports 24 main cases, 12 cutoff cases, 88 integrations, 323033 RHS evaluations, six zero symbolic residuals and exact collision eigenvalues. No proof of optimal rates or cutoff, no production code execution, Mac build or Lean kernel. All fractions fixed and positive as specified; arbitrary nonnegative integrable prescribed opacity, not a derivation of recombination. Primordial/superhorizon mode matching, actual spin-2 convention binding for repository E variables, physical opacity, Boltzmann production implementation, CMB and matter likelihood, independent novelty remain OPEN. Repository integration requires approval.
