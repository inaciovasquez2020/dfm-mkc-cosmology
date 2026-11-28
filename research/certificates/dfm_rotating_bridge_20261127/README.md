# Controlled Einstein–Klein–Gordon to averaged matter-growth limit

2026-11-27. Public `dfm-mkc-cosmology`, remote base `ea4f548e5c9b3160ea0a4dde76cab74be6a4964f`. Source inspected: `src/dfm_mkc_solver/dark_sector_fourier_rhs_v1.py`, `metric_constraint_elimination_v1.py`, `dark_sector_stress_energy_perturbations_v1.py`, `averaged_full_field_matching_surface_v1.py`, and `averaged_matter_growth_suppression_v1.py`. Compare PRs #352–354. Analytic PROVED under the following hypotheses; standalone numerical and symbolic checks PASS; Lean and full repository CI NOT_RUN. No repository writes, Codex or Claude. Literature context: Suárez and Chavanis, Phys. Rev. D 92, 023510 (2015), DOI 10.1103/PhysRevD.92.023510; Salehian et al., JHEP 09 (2021) 050, DOI 10.1007/JHEP09(2021)050. Nonrelativistic reduction is established physics; independent novelty of this finite-mode estimate NOT_ESTABLISHED.

## 1. Existing matching obstruction

For the canonical quadratic branch alpha=beta=1 and rho_star=lambda_phi=0, the historical circular calibration has radial velocity zero and angular velocity m. In cosmic time, pressureless matching gives delta_p=phi^2 m delta_theta_dot-phi^2 m^2 Phi=0 (Psi=Phi). The existing normalized phase-current lock imposes delta_theta_dot+2m delta_phi/phi-4m Phi=0. Together they give delta_theta_dot=m Phi and delta_phi/phi=3Phi/2. Since delta_rho/rho=2 delta_phi/phi at delta_p=0, necessarily delta=3Phi. Hence arbitrary target density and growing-mode derivative cannot be specified under those conditions. In particular the current matching function explicitly divides by phi_prime and rejects zero phi_prime. A Cartesian rotating-envelope prescription avoids both the division and the unwarranted phase lock. It is a distinct choice of initial data, not a proof of equivalence to the historical matching prescription.

## 2. Exact relativistic system and constraint propagation

Assume a pure, minimally coupled canonical quadratic complex scalar on a spatially flat expanding FLRW solution, no visible species, no cosmological constant, positive m. Use units with a(0)=H(0)=rho(0)=1 and g=4 pi G=3/2. Write psi for the complex background, eta for one real spatial Fourier harmonic of its complex perturbation, and use cosmic time. Then

    psi_ddot+3H psi_dot+m^2 psi=0,
    rho=(|psi_dot|^2+m^2|psi|^2)/2, H=sqrt(rho), H_dot=-g |psi_dot|^2,
    a_dot=a H.

Initial circular field: psi(0)=1/m, psi_dot(0)=i (constant phase chosen zero). The positive Friedmann solution exists on every finite forward interval: rho_dot=-3H |psi_dot|^2, 0<H<=1, rho>=exp(-6T), and 1<=a<=exp(T). Thus |H_dot|<=3. All variables remain bounded for each fixed m.

Use the zero-anisotropic-stress Newtonian-gauge metric (1+2Phi,1-2Phi). Put p2=k^2/a^2, x=m psi, v=psi_dot, y=m eta, w=eta_dot. Define Akin=|v|^2, R=Re(conj(v)w), Xpot=Re(conj(x)y), q=Re(conj(v)y)/m, delta_rho=R+Xpot-Akin Phi, delta_p=R-Xpot-Akin Phi. The source-level constraints and perturbed Klein–Gordon equation are

    p2 Phi = -g(delta_rho+3H q),
    D=g q-H Phi,
    eta_ddot+3H eta_dot+(m^2+p2)eta=4 psi_dot D-2m^2 psi Phi.

The conformal-time q of the source file converts to cosmic q above. Solve algebraically Phi=-g(R+Xpot+3Hq)/(p2-g Akin). When the denominator is nonzero this is an ordinary linear evolution in (y,w) on the background. In fact D is its true time derivative: differentiate the constraint. The elementary identities from the field equations are

    Akin_dot=-6H Akin-2 C, C=m Re(conj(v)x),
    (R+Xpot)_dot=-6H R-p2 q+4 Akin D-2 C Phi,
    q_dot=-3H q+R-Xpot.

If one sets Phi_dot=D in the differentiated constraint, its residual equals -3H times the constraint itself, as shown by substitution of H_dot=-g Akin and D=gq-H Phi. The actual differentiated constraint differs from this expression by (p2-g Akin)(Phi_dot-D). Both residuals vanish, so Phi_dot=D. Differentiating the momentum constraint gives exactly Phi_ddot+4H Phi_dot+(2H_dot+3H^2)Phi=g delta_p. Thus the time, momentum, trace and traceless scalar Einstein equations are consistent with this linear closure in the pure-scalar setting; no assumption of slowly varying metric derivatives is needed. `constraint_check.py` independently verifies the two polynomial identities exactly in SymPy.

## 3. Theorem (uniform finite-interval Jeans-scaled limit)

Fix T>0 and kappa>0. Let the mass m tend to infinity with comoving k^2=m kappa. The finite interval is [0,T], not the entire history. Set

    X=m a^(3/2) psi, Y=m a^(3/2) eta,
    X=U exp(imt)+V exp(-imt), X_dot=im(U exp(imt)-V exp(-imt)),
    Y=A exp(imt)+B exp(-imt), Y_dot=im(A exp(imt)-B exp(-imt)).

These are invertible algebraic definitions, not slowly varying assumptions. Choose fixed complex A(0)=A0, B(0)=B0 (bounded independently of mass); B0=0 is the well-prepared co-rotating choice. The averaged initial density and derivative are d(0)=2 Re A0 and d_dot(0)=-kappa Im A0. Put a_d=(1+3t/2)^(2/3), H_d=(1+3t/2)^-1. Then the relativistic Newtonian-gauge density contrast obeys

    sup_[0,T] |delta_rho/rho - d(t)| <= C(T,kappa)(|A0|+|B0|)/m,

for sufficiently large m, where d solves

    d_ddot+2H_d d_dot + (kappa^2/(4 a_d^4)-3/(2 a_d^3))d=0.

This is exactly the averaged one-component EdS equation at k^2/m=kappa. One explicit (conservative) constant is given below. The estimate is uniform in time and does not require phase-cycle averaging of the density. It is not uniform for kappa approaching zero or infinity. No claim is made for fixed k, arbitrary primordial initial conditions, relativistic multi-species evolution, or nonlinear perturbations.

### Proof: background control

Define E=a^3 rho, J=a^3 Re(conj(psi) psi_dot), Q=a^3 Im(conj(psi) psi_dot). Direct differentiation gives Q constant, E^2>=m^2(J^2+Q^2), and (E+3HJ/2)_dot=3H_dot J/2. E(0)=m|Q|=1, J(0)=0. Let M=max E on [0,T]. Using monotonic H in the integrated identity gives M-1<=3 sqrt(M^2-1)/m (or use the weaker bound 2 max 3H/(2m) from the previous certificate). Hence for m>=6, 1<=E<=(1+9/m^2)/(1-9/m^2)<=1+24/m^2. Since (a^(3/2))_dot=(3/2)sqrt(E), |a-a_d|<=12T/m^2.

Let b=3H_dot/2+9H^2/4, |b|<=b_*=27/4. Rescaling gives X_ddot+m^2 X=b X. Thus U_dot=b(U+V exp(-2imt))/(2im), V_dot=-b(U exp(2imt)+V)/(2im). Initially U=1-3i/(4m), V=3i/(4m). For m>=1, let L_b=(5/2)exp(b_* T), C_b=3/2+b_* T L_b. Direct Gronwall and integration give |U|+|V|<=L_b and |U-1|+|V|<=C_b/m. All constants depend only on T (units fixed).

### Proof: perturbation and constraints in envelopes

Let n=|A|+|B|, h=3H/(2m), Z=X_dot/m, W=Y_dot/m. The physical variables satisfy x=a^(-3/2)X, v=a^(-3/2)(Z-hX), y=a^(-3/2)Y, w=a^(-3/2)(W-hY). The exact cancellation of cross terms is

    Re(conj(Z) W + conj(X) Y)=2 Re(conj(U)A+conj(V)B).

Consequently a^3(R+Xpot)=2 Re A+e_r, |e_r|<=(2C_b+21 L_b/4)n/m, and |q|<=(5/2)L_b n/m. More precisely the latter bound also holds for a^3|q|. Set L=3 exp(2T)/kappa. For m>=2L the fractional constraint correction lambda=g Akin/p2<=L/m<=1/2, so the exact denominator is bounded below by p2/2. Put c=3/(kappa a), omega=kappa/(2a^2), P0=-c Re A. The constraint yields

    m Phi=P0+e_phi,
    |e_phi|<=C_phi n/m,
    C_D=2C_b+51 L_b/4,
    C_phi=(3/(2kappa))(2 C_D+4L).

Indeed the source a^3(R+Xpot+3Hq)=2 Re A+e with |e|<=C_D n/m, and 1/(1-lambda)<=2. Thus with P=3/kappa+C_phi and D_*=15 L_b/4+P, |m Phi|<=P n and |Phi_dot|<=D_* n/m.

The rescaled perturbation equation is exact:

    Y_ddot+m^2Y=(-p2+b)Y+4(X_dot-3HX/2)Phi_dot-2m^2 X Phi.

The envelope equations are therefore

    A_dot=i(omega A-c Re A)+i omega B exp(-2imt)+r_A,
    B_dot=-i omega B-i(omega A-c Re A) exp(2imt)+r_B,

with |r_A|+|r_B|<=C_R n/m, where one valid constant is

    C_R=b_*+10 L_b D_*+2(L_b C_phi+(3/kappa)C_b).

To check this bound, the b terms contribute <=b_* n/m, the metric derivative terms <=4(1+h)L_b D_* n/m<=10 L_b D_* n/m, and each metric potential term differs from its leading value by <=(L_b C_phi+3 C_b/kappa)n/m. No derivative of r is used.

### Proof: averaging with explicit rate

View z=(A,B) as a real-linear four-component vector with norm n. Let L0(a)z=(i(omega A-c Re A),-i omega B), and Lfast(t,a)z be the two displayed oscillating terms. The two operator norms are each <=M0=kappa/2+3/kappa. A primitive K(t) of the fast oscillations with coefficients frozen is obtained by dividing the first fast term by -2im and the second by 2im. Then ||K||<=M0/(2m) and ||K_dot-Lfast||<=M2/(2m), M2=kappa+3/kappa, since |H|<=1. Let M=2M0+C_R. For m>=1, n(t)<=n(0)exp(MT), ||z_dot||<=M n(t). Integrating by parts,

    || integral_0^t Lfast z || <= n(0)exp(MT) [M0(2+MT)+M2 T]/(2m).

Compare to zbar'=L0(a)zbar with identical initial data, use the integral equation and Gronwall (not a formal dropping of fast terms):

    sup ||z-zbar|| <= n(0) C_A/m,
    C_A=exp((M+M0)T) ([M0(2+MT)+M2 T]/2+C_R T).

Replace a by a_d in the slow equation: ||L0(a)-L0(a_d)||<=M2 |a-a_d|<=12 M2 T/m^2. The additional uniform error is <=n(0) C_S/m^2, C_S=12 M2 T^2 exp(2M0 T). The resulting slow system decouples B entirely. Writing A_d=u+iv, u_dot=-omega_d v and v_dot=(omega_d-c_d)u. With d=2u and omega_d_dot=-2H_d omega_d, it follows exactly that d_dotdot+2H_d d_dot+(omega_d^2-omega_d c_d)d=0, where omega_d c_d=3/(2a_d^3). This proves the desired equation and initial conditions.

Finally the observed density is (R+Xpot-Akin Phi)/rho. Using E>=1, E-1<=24/m^2, a^3 Akin<=2E and the above cancellation gives |delta-2 Re A|<=(48+2C_b+21 L_b/4+2P)n/m. Combining all errors gives the theorem with

    m>=max(6,2L),
    C(T,kappa)=(48+2C_b+21 L_b/4+2P)exp(MT)+2 C_A+2 C_S.

Constants are deliberately crude, but finite and independent of m. This establishes a controlled pure-scalar linear relativistic averaging bridge. QED.

## 4. Reproducible numerical checks

`OPENBLAS_NUM_THREADS=1 python verify.py` (NumPy 2.3.5, SciPy 1.17.0). Run under a 90-second external timeout for hard enforcement. The internal 65-second and integration-count checks occur between integrations, and evaluation count is checked after each. Any guard or solver failure is INCOMPLETE. DOP853 and RK45 independently integrate the actual Cartesian field and source-level Einstein system for 16 cases, kappa in {1,2,4,8}, m in {32,64,128,256}, over T=1.5. Four averaged EdS integrations; 401 samples per case, charge conservation, regular denominator, solver agreement, and endpoint improvement checks. Density errors normalized by input amplitude 1e-5. The exact and limiting initial density differ by O(1/m) because the slow-envelope prescription matches the limiting density, not the full density at finite m. The exact initial contrast for this choice is delta0*(1+3/(m kappa)); no claim of second-order perturbation convergence. Numerical receipts are platform/version dependent. `python constraint_check.py` (SymPy 1.14.0) checks the metric propagation identities independently. Neither finite samples nor symbolic polynomial checks substitute for the proof above.

## 5. Remaining OPEN

Extend to baryons and radiation, a cosmological constant, gauge-invariant primordial initial data, and the actual historical calibration/regular matching selection. The kappa->0 horizon-scale regime is not covered. Full cosmological transfer functions and growth likelihood are not computed. Independent novelty is unestablished; Lean and full repo CI NOT_RUN.
