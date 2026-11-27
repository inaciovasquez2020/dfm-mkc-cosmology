# Controlled scalar–baryon–Lambda relativistic averaging bridge

2026-11-27. Public DFM-MKC repository base `ea4f548e5c9b3160ea0a4dde76cab74be6a4964f`. Extends the pure-scalar proof at PR #355, `580e3f6c3b68cbc952554d7351de690b15634935`. The baryon Euler sign is consistent with `tests/test_visible_sector_pressureless_baryon_euler_v1.py` at base. This is a standalone mathematical and computational certificate, not a modification or execution of the repository's production solver. Analytic PROVED under the specified hypotheses. Standalone computation PASS. Lean, full repository CI, radiation, primordial matching and observational growth likelihood NOT_RUN/OPEN. No Codex or Claude. Standard coupled nonrelativistic perturbation equations are established literature (e.g. Marsh, Phys. Rev. D 91, 123520, 2015, DOI 10.1103/PhysRevD.91.123520); novelty of the quantitative estimate is not established.

## Exact equations and constraint propagation

Normalize a(0)=H(0)=1, critical density at the initial point to 1, g=4 pi G=3/2. Fix s>0, b>0, ell>=0, s+b+ell=1. Use a spatially flat expanding FLRW solution with a canonical minimally coupled complex scalar psi of quadratic mass m, separately conserved pressureless baryons r=b/a^3, and Lambda/3=ell. No radiation, anisotropic stress or collision terms. Initial circular scalar psi(0)=sqrt(s)/m, psi_dot(0)=i sqrt(s). Equations:

    psi_ddot+3H psi_dot+m^2 psi=0,
    rho_s=(|psi_dot|^2+m^2|psi|^2)/2,
    H^2=ell+rho_s+r, H_dot=-g(|psi_dot|^2+r), a_dot=aH.

For a real spatial Fourier harmonic with complex scalar amplitude eta, define p=k^2/a^2, K=|psi_dot|^2, R=Re(conj(psi_dot) eta_dot), X=m^2 Re(conj(psi) eta), q_s=Re(conj(psi_dot) eta). Newtonian gauge has equal potentials Phi. Denote baryon contrast d and cosmic momentum potential q_b by delta T^t_i=-partial_i q_b. Total perturbed density L=R+X-K Phi+r d, total pressure perturbation P=R-X-K Phi, total momentum q=q_s+q_b. The constraint equations and evolution are

    p Phi+g(L+3H q)=0, D=g q-H Phi,
    eta_ddot+3H eta_dot+(m^2+p)eta=4 psi_dot D-2m^2 psi Phi,
    d_dot=-p q_b/r+3D, q_b_dot=-3H q_b+r Phi.

Solve Phi=-g(R+X+r d+3H q)/(p-gK). The dust Euler equation in conformal time is theta_b'+Hc theta_b=k^2 Phi, with theta_b=k^2 q_b/(a r); this recovers the repository test sign and normalization. This is a pressureless dust idealization, not photon-coupled baryon evolution.

Let C=m^2 Re(conj(psi_dot)psi). Exact derivatives of K, R+X and q_s are

    K_dot=-6HK-2C,
    (R+X)_dot=-6HR-p q_s+4KD-2C Phi,
    q_s_dot=-3H q_s+R-X.

Putting Phi_dot=D in the derivative of the constraint gives exactly -3H times that constraint, using H_dot=-g(K+r), r_dot=-3Hr and the dust equations. The actual derivative differs by (p-gK)(Phi_dot-D), so Phi_dot=D wherever p-gK is nonzero. In particular q_dot=-3Hq+P+(K+r)Phi. Differentiating D yields

    Phi_ddot+4H Phi_dot+(2H_dot+3H^2)Phi=gP.

Hence the full scalar Einstein constraints and trace propagate in this system. `verify.py` checks both polynomial identities by exact SymPy expansion.

## Theorem: coupled finite-interval limit

Fix T>0, kappa>0, and set k^2=m kappa. Rescale

    X_bg=m a^(3/2) psi/sqrt(s), Y=m a^(3/2) eta/sqrt(s),
    X_bg=U exp(imt)+V exp(-imt), X_bg_dot=im(U exp(imt)-V exp(-imt)),
    Y=A exp(imt)+B exp(-imt), Y_dot=im(A exp(imt)-B exp(-imt)).

These are invertible algebraic definitions. Let u=m q_b/r, and prescribe mass-independent A(0)=A0, B(0)=B0, d(0)=d0, u(0)=u0, all finite. Write n0=|A0|+|B0|+|d0|+|u0|. The nonzero B0 fast mode is allowed. Let a_d solve a_d_dot=a_d H_d with H_d^2=ell+(s+b)/a_d^3, a_d(0)=1. Put rho_sd=s/a_d^3 and rho_bd=b/a_d^3. Then, for sufficiently large m,

    sup_[0,T] ( |(R+X-K Phi)/rho_s - delta_s|+|d-delta_b| ) <= C(T,kappa) n0/m,

where the limit satisfies

    delta_s_ddot+2H_d delta_s_dot+kappa^2 delta_s/(4a_d^4)
        =g(rho_sd delta_s+rho_bd delta_b),
    delta_b_ddot+2H_d delta_b_dot=g(rho_sd delta_s+rho_bd delta_b).

Initial conditions: delta_s(0)=2 Re A0, delta_s_dot(0)=-kappa Im A0, delta_b(0)=d0, delta_b_dot(0)=-kappa u0. The bound is not uniform in kappa near zero or infinity; no fixed-k or primordial/horizon-scale convergence is asserted. All densities and H in the limiting equations belong to the limiting dust-plus-Lambda background, not the instantaneous background.

### Proof: background estimates

H is positive and nonincreasing, H<=1 and |H_dot|<=3. The density derivative is rho_s_dot=-3HK; K<=2rho_s. On a finite forward interval rho_s>=s exp(-6T), 1<=a<=exp(T); the expanding solution exists there. For normalized E=a^3 rho_s/s, J=a^3 Re(conj(psi) psi_dot)/s and Q=a^3 Im(conj(psi) psi_dot)/s, E(0)=mQ=1, J(0)=0, E^2>=m^2(J^2+Q^2), Q conserved. As in PR #355, (E+3HJ/2)_dot=3H_dot J/2, hence E>=1 and M-1<=3 sqrt(M^2-1)/m with M=max E. For m>=6 this yields E<=1+24/m^2. This step uses only monotonic H, not pure scalar domination.

Let v=a^(3/2). It solves v_dot=(3/2)sqrt(ell v^2+sE+b); the limiting v_d replaces E by 1. The right-hand side with E=1 is Lipschitz with constant <=3/2 on v>=1. Its change from E=1 to E(t) is <=(3/2)s(E-1)/(2 sqrt(s+b))<=18/m^2. Gronwall gives |a-a_d|<=|v-v_d|<=C_bg/m^2 with C_bg=18 T exp(3T/2). Here a=v^(2/3) is Lipschitz on v>=1.

Write h=3H/(2m), beta=3H_dot/2+9H^2/4, |beta|<=beta_*=27/4. X_bg_ddot+m^2 X_bg=beta X_bg. The equations for U,V are the same as in PR #355, with initial U=1-3i/(4m), V=3i/(4m). Thus for m>=1, |U|+|V|<=L=(5/2)exp(beta_* T) and |U-1|+|V|<=C_b/m, C_b=3/2+beta_* TL, by Gronwall and direct integration.

### Proof: uniform coefficient estimates

Set n=|A|+|B|+|d|+|u|, Z=X_bg_dot/m, W=Y_dot/m. Exact cancellation of the fast cross terms gives Re(conj(Z)W+conj(X_bg)Y)=2 Re(conj(U)A+conj(V)B). In physical variables

    a^3(R+X)/s=Re(conj(Z-hX_bg)(W-hY)+conj(X_bg)Y),
    a^3 q_s/s=Re(conj(Z-hX_bg)Y)/m.

Hence |a^3(R+X)/s-2 Re A|<=C_r n/m, C_r=2C_b+21L/4, and a^3 |q_s|<=s(5/2)L n/m. Also a^3 |q_b|=b|u|/m. Define C_q=(5/2)L+1, C_D=C_r+3C_q, so

    |a^3(R+X+r d+3Hq)-(2s Re A+b d)|<=C_D n/m.

Let L_c=3 exp(2T)/kappa. Since K<=2, gK/p<=L_c/m, and for m>=2L_c the denominator is at least p/2. Set omega=kappa/(2a^2), P0=-g(2s Re A+b d)/(kappa a). Then

    |m Phi-P0|<=C_phi n/m,
    C_phi=(g/kappa)(2C_D+4L_c),
    |m Phi|<=P_* n, P_*=3/kappa+C_phi,
    |D|<=D_* n/m, D_*=g C_q+P_*.

The first estimate follows by expanding 1/(1-gK/p) and using |2s Re A+b d|<=2n; the other two follow directly. No slow-metric assumption is used.

The exact rescaled perturbation equation is

    Y_ddot+m^2 Y=(-p+beta)Y+4(X_bg_dot-3HX_bg/2)D-2m^2 X_bg Phi.

Consequently the rotating and baryon equations take the form

    A_dot=i(omega A+P0)+i omega B exp(-2imt)+r_A,
    B_dot=-i omega B-i(omega A+P0) exp(2imt)+r_B,
    d_dot=-kappa u/a^2+r_d,
    u_dot=P0+r_u.

The remainder norm is <=C_R n/m with, for example,

    C_R=beta_*+10 L D_*+2(L C_phi+3 C_b/kappa)+3D_*+C_phi.

Indeed the beta term, D term, and error of replacing m X_bg Phi by exp(imt)P0 contribute the first three terms, exactly as in the pure scalar proof. The last two terms are the dust continuity correction 3D and dust Euler correction mPhi-P0. No differentiation of a remainder is needed.

### Proof: controlled averaging and limiting equation

Let z=(A,B,d,u) with the above sum norm (a real six-dimensional vector). Denote the nonoscillatory operator by L0(a), and the two fast oscillatory entries by Lf(t,a). Both have operator norm <=M0=4kappa+12/kappa+1 on a>=1. Their slowly varying coefficients have a-derivatives bounded by M0 (for L0 and for the combined fast terms), since omega_a=-kappa/a^3 and (P0)_a=-P0/a, and (kappa/a^2)_a=-2kappa/a^3. Time derivatives of the fast coefficients alone are also bounded by M0 since H<=1 and a times the a-derivatives obey the same bound. Integrating the exponentials with the coefficients frozen defines a real-linear primitive Kf with ||Kf||<=M0/(2m), ||Kf_dot-Lf||<=M0/(2m). Let M=2M0+C_R. Then n(t)<=n0 exp(MT), ||z_dot||<=M n(t), and integration by parts gives

    ||integral_0^t Lf z|| <= n0 exp(MT) M0 (2+MT+T)/(2m).

Comparing the integral equations to zbar_dot=L0(a)zbar with the same initial data, Gronwall yields sup ||z-zbar||<=n0 C_A/m, where

    C_A=exp((M+M0)T)[M0(2+MT+T)/2+C_R T].

Replacing a by a_d in the slow operator costs at most n0 C_S/m^2, C_S=M0 C_bg T exp(2M0 T), by the Lipschitz bound and Gronwall. The resulting slow equation is A_dot=i(omega A+P0), B_dot=-i omega B, d_dot=-kappa u/a_d^2, u_dot=P0, with coefficients evaluated at a_d. Thus B decouples from the slow density. Define delta_s=2 Re A, delta_b=d. With omega_dot=-2H_d omega, differentiate these equations to obtain the two stated coupled equations and initial conditions.

Finally |(R+X-K Phi)/rho_s-2 Re A| <= (C_r+48+2P_*)n/m, since E>=1, E-1<=24/m^2 and K/rho_s<=2. Both physical contrasts are thus controlled by the explicit constant

    C(T,kappa)=(C_r+48+2P_*)exp(MT)+2C_A+2C_S,
    m>=max(6,2L_c).

All constants are finite, independent of m, and deliberately conservative. The proof is uniform in s,b,ell within the stated positive-density normalization; b>0 and s>0 are required for the normalized contrasts. QED.

## Coupled Jeans obstruction (PROVED)

At fixed time, define Qp=kappa^2/(4a_d^4)>0. The coefficient matrix in the second-order density equations (apart from common Hubble damping) is

    J=[[Qp-g rho_sd, -g rho_bd],[-g rho_sd,-g rho_bd]].

It is similar to a real symmetric matrix by the positive diagonal scaling diag(sqrt(rho_sd),sqrt(rho_bd)). Its determinant is -Qp g rho_bd<0. Hence its two eigenvalues have opposite signs at every nonzero wavenumber if the baryon density is positive. No finite total-matter Jeans threshold stabilizes both instantaneous modes in this pressureless-baryon idealization. The negative eigenvalue tends to -g rho_bd as Qp->infinity (trace and determinant, or the quadratic formula); its scalar-to-baryon eigenvector ratio is g rho_bd/(Qp-g rho_sd-lambda_minus)=O(Qp^-1). A frozen-coefficient spectral statement is not a theorem of unbounded late-time growth in an expanding Lambda background. Real baryon pressure and radiation can change this conclusion. No physical prediction beyond the stated model.

## Reproduction and limits

Run `OPENBLAS_NUM_THREADS=1 python verify.py` (NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0). Use an external timeout of 90 seconds for hard enforcement; internal 70-second/count checks occur between integrations and evaluation cap is post-solver. Guard failure is INCOMPLETE. Tests use normalized interval [0,1], 301 samples, three matter/vacuum compositions, kappa in {1,4,8}, m in {32,64,128,256}, a nonzero counter-rotating B0 and independent initial baryon contrast and velocity. Two full-field solvers (DOP853 and RK45) per case and nine independent averaged references. All 36 cases pass the energy, charge and solver checks, with decreasing endpoint mass-error trend for each composition/wavenumber. Symbolic identities are separate exact polynomial checks. The receipt is not an exhaustive parameter proof, nor a cosmological transfer function or likelihood. Floating-point bytes may depend on library/platform. No Mac build was performed. OPEN: radiation and collisions, primordial/horizon-scale normalization, calibration branch equivalence, full integration and empirical likelihood. No public repository writes made for this certificate.
