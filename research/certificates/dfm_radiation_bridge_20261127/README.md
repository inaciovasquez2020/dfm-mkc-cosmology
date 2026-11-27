# Controlled perfect-radiation extension of the scalar–baryon–Lambda averaging bridge

2026-11-27. Public base `inaciovasquez2020/dfm-mkc-cosmology` at `ea4f548e5c9b3160ea0a4dde76cab74be6a4964f`; extends PR #356 at `5d19292958d4991ea8e2983ab468e25a1f809c21` and PR #355 at `580e3f6c3b68cbc952554d7351de690b15634935`. Analytic PROVED for independently conserved perfect radiation and pressureless dust coupled to a canonical quadratic complex scalar and nonnegative cosmological constant, in the finite-forward-interval Jeans scaling. Not a photon–baryon collision model, Boltzmann hierarchy, anisotropic stress model, primordial transfer function, or observational likelihood. Lean, full repository CI and independent novelty NOT_RUN/NOT_ESTABLISHED. No Codex or Claude. This is a standalone proof and IVP calculation, not a change to the production solver.

## 1. Exact relativistic system

Normalize initial a=H=1, critical density=1, g=4 pi G=3/2. Fix fractions s,b,r>0, ell>=0, s+b+r+ell=1. The background scalar is psi with initial psi=sqrt(s)/m, psi_dot=i sqrt(s); rho_s=(|psi_dot|^2+m^2|psi|^2)/2, K=|psi_dot|^2. Write rho_b=b/a^3, rho_r=r/a^4. The flat FLRW equations are psi_ddot+3H psi_dot+m^2 psi=0, a_dot=aH, H^2=ell+rho_s+rho_b+rho_r, H_dot=-g(K+rho_b+4rho_r/3). Radiation is a perfect fluid with p_r=rho_r/3, no shear or energy/momentum exchange.

For a real spatial Fourier harmonic eta of the complex scalar, set p=k^2/a^2, R=Re(conj(psi_dot) eta_dot), X=m^2 Re(conj(psi) eta), q_s=Re(conj(psi_dot) eta). Use Newtonian gauge with equal potentials Phi=Psi, cosmic momentum potentials delta T^t_i=-partial_i q_j, contrasts d=delta_b, e=delta_r, total momentum Q=q_s+q_b+q_r. The exact system is

    L=R+X-K Phi+rho_b d+rho_r e,
    P=R-X-K Phi+rho_r e/3,
    p Phi+g(L+3H Q)=0, D=g Q-H Phi,
    eta_ddot+3H eta_dot+(m^2+p)eta=4 psi_dot D-2m^2 psi Phi,
    d_dot=-p q_b/rho_b+3D, q_b_dot=-3H q_b+rho_b Phi,
    e_dot=-p q_r/rho_r+4D, q_r_dot=-3H q_r+rho_r e/3+4rho_r Phi/3.

Here Phi=-g(R+X+rho_b d+rho_r e+3H Q)/(p-gK). Derivative identities K_dot=-6HK-2C, (R+X)_dot=-6HR-p q_s+4KD-2C Phi, (q_s)_dot=-3H q_s+R-X, C=m^2 Re(conj(psi_dot)psi), imply that differentiation of the constraint with Phi_dot=D yields -3H times the constraint. The actual differentiation differs by (p-gK)(Phi_dot-D). Therefore Phi_dot=D wherever the denominator is nonzero. Also Q_dot=-3HQ+P+(K+rho_b+4rho_r/3)Phi. Differentiating the momentum constraint gives Phi_ddot+4H Phi_dot+(2H_dot+3H^2)Phi=gP. These identities, including radiation, are verified by exact symbolic expansion in verify.py; zero scalar anisotropic stress supplies the traceless spatial equation.

## 2. Theorem and data

Fix T>0, kappa>0, k=sqrt(m kappa), m tending to infinity. Define X_bg=m a^(3/2) psi/sqrt(s), Y=m a^(3/2) eta/sqrt(s) and the invertible rotating envelope definitions

    X_bg=U exp(imt)+V exp(-imt), X_bg_dot=im(U exp(imt)-V exp(-imt)),
    Y=A exp(imt)+B exp(-imt), Y_dot=im(A exp(imt)-B exp(-imt)).

Let u=m q_b/rho_b, h=sqrt(3) k q_r/(a rho_r). Prescribe A0,B0,d0,u0,e0,h0 independent of m and bounded. Let N0=|A0|+|B0|+|d0|+|u0|+sqrt(e0^2+h0^2). Define the limiting background a_d by a_d(0)=1 and H_d^2=ell+(s+b)/a_d^3+r/a_d^4. Write rho_sd=s/a_d^3, rho_bd=b/a_d^3. The limiting contrasts obey

    delta_s_ddot+2H_d delta_s_dot+kappa^2 delta_s/(4a_d^4)=g(rho_sd delta_s+rho_bd delta_b),
    delta_b_ddot+2H_d delta_b_dot=g(rho_sd delta_s+rho_bd delta_b),
    delta_s(0)=2 Re A0, delta_s_dot(0)=-kappa Im A0,
    delta_b(0)=d0, delta_b_dot(0)=-kappa u0.

There exist finite C and m0 depending only on T,kappa and fixed background fractions such that for m>=m0

    sup_[0,T] ( |(R+X-K Phi)/rho_s-delta_s| + |d-delta_b| ) <= C N0/sqrt(m).

In addition define theta_d(t)=k integral_0^t ds/(sqrt(3) a_d(s)). For the radiation acoustic vector, the corresponding bound is

    sup_[0,T] ||(e,h)-Rot(theta_d)(e0,h0)||_2 <= C N0/sqrt(m),
    Rot(theta)=[[cos(theta),-sin(theta)],[sin(theta),cos(theta)]].

If e0=h0=0, the matter bound improves to C N0/m, and the acoustic vector remains O(N0/sqrt(m)). All bounds are on fixed forward intervals and fixed positive kappa. In particular the full radiation density does not generally converge pointwise as m tends to infinity: the correct description retains its oscillatory phase. The statement is not uniform at kappa=0, or for time intervals growing with m.

## 3. Proof

Throughout, C denotes a finite positive constant depending only on the fixed fractions, T and kappa; it can change between inequalities. Operator norms are induced by the sum of complex moduli and absolute values on scalar/baryon variables and the Euclidean norm on the acoustic pair. Every O estimate below has this same uniform-in-m meaning; none asserts a derivative bound on an unspecified remainder.

### Background and regular denominator

H is positive and nonincreasing with H<=1, |H_dot|<=3, 1<=a<=exp(T), rho_s>=s exp(-6T). These bounds follow from the continuity equation rho_s_dot=-3HK and K<=2rho_s, the positive fractions and Friedmann. They ensure existence on every fixed finite forward interval. The normalized comoving E=a^3 rho_s/s, J=a^3 Re(conj(psi)psi_dot)/s, Q_bg=a^3 Im(conj(psi)psi_dot)/s satisfy E(0)=m Q_bg=1, J(0)=0, E^2>=m^2(J^2+Q_bg^2), Q_bg constant and (E+3HJ/2)_dot=3H_dot J/2. With M=max E, integration and monotonic H give M-1<=3 sqrt(M^2-1)/m. Consequently 1<=E<=1+24/m^2 for m>=6 (as in PR #356). The background equation is a_dot=a sqrt(ell+(sE+b)/a^3+r/a^4). On the compact rectangle a in [1,exp(T)], E in [1,2], the square root is bounded away from zero because s+b>0. The right hand side is uniformly Lipschitz in a and E. Comparison with E=1 and Gronwall imply sup |a-a_d|<=C/m^2. Also sup |H-H_d|<=C/m^2.

The rescaled background obeys X_bg_ddot+m^2 X_bg=beta X_bg, beta=3H_dot/2+9H^2/4, |beta|<=27/4. The exact envelope equations are U_dot=beta(U+V exp(-2imt))/(2im), V_dot=-beta(U exp(2imt)+V)/(2im). Initially U=1-3i/(4m), V=3i/(4m). Gronwall and integration yield |U|+|V|<=C, |U-1|+|V|<=C/m. Since K<=2 and g=3/2, gK/p<=3 exp(2T)/(m kappa). For m>=max(6,6 exp(2T)/kappa), p-gK>=p/2; the exact linear perturbation IVP is well defined.

### Radiation oscillator and uniformly bounded amplitudes

Put omega_r=k/(sqrt(3)a), z=(A,B,d,u), w=(e,h), n=||z||+||w||. The exact radiation equations in these coordinates are

    e_dot=-omega_r h+4D,
    h_dot=omega_r e+4 omega_r Phi.

Indeed q_r/rho_r has derivative H q_r/rho_r+e/3+4Phi/3, so the derivative of the factor 1/a cancels H exactly. These equations exhibit a skew-symmetric acoustic generator, not a growing norm bound of order k.

The exact scalar carrier cancellation from PR #356, Re(conj(Z)W+conj(X_bg)Y)=2 Re(conj(U)A+conj(V)B) with Z=X_bg_dot/m and W=Y_dot/m, gives |a^3(R+X)/s-2Re A|<=C ||z||/m, |q_s|+|q_b|<=C ||z||/m. Radiation momentum is exactly rho_r a h/(sqrt(3)k). Thus

    P0=-g(2s Re A+b d+r e/a)/(kappa a),
    |m Phi-P0|<=C(||z||/m+||w||/k),
    |m Phi|<=C n,
    |D|<=C(||z||/m+||w||/k).

The estimate follows directly from the constraint, the carrier cancellation and 1/(1-gK/p)<=2, including the radiation density in P0 and its momentum in the remainder. Constants can absorb 1/m<=C/k for large m. The rescaled scalar equation is Y_ddot+m^2 Y=(-p+beta)Y+4(X_bg_dot-3HX_bg/2)D-2m^2 X_bg Phi. Hence, with omega=kappa/(2a^2),

    A_dot=i(omega A+P0)+i omega B exp(-2imt)+r_A,
    B_dot=-i omega B-i(omega A+P0) exp(2imt)+r_B,
    d_dot=-kappa u/a^2+3D, u_dot=m Phi,
    |r_A|+|r_B|<=C(||z||/m+||w||/k).

To see the last bound, beta terms cost C||z||/m, the derivative metric term costs C|D| (because X_bg_dot/m is bounded), and replacing m X_bg Phi by exp(imt)P0 costs C(n/m+||w||/k), absorbed into the stated estimate. The dust equations follow from the exact momentum conservation. In particular ||z_dot||<=C n. Rotate w by angle minus theta(t)=-integral omega_r dt. The derivative of the rotated vector has norm at most 4|D|+4 omega_r |Phi|<=C n/k. For the combined rotated state, Gronwall gives sup n<=C N0. Integrating the rotated radiation equation gives sup ||w-Rot(theta)w0||<=C N0/k. Since |theta-theta_d|<=C k/m^2, the acoustic estimate follows. No derivative of the metric remainder is taken.

### Two-frequency averaging

Write z_dot=L0(a)z+Lfast(t,a)z+G0(a)e+Gfast(t,a)e+R_z, where L0 is the slow operator of PR #356, Lfast consists of exp(+/-2imt) terms, and G0,Gfast are the corresponding terms from -g r e/(kappa a^2) in P0. Their coefficients and their time derivatives with oscillatory factors removed are uniformly bounded, since a in [1,exp(T)] and |a_dot|<=exp(T). R_z has norm <=C(||z||/m+||w||/k). For Lfast, use a frozen-coefficient primitive dividing exp(+/-2imt) by +/-2im. Integration by parts, using ||z_dot||<=C N0, gives ||integral_0^t Lfast z||<=C N0/m. For Gfast e the same primitive is used, but e_dot=O(k N0) from its acoustic equation; the integral is <=C N0(1+k)/m<=C N0/k. For G0 e use h_dot=omega_r(e+4Phi), so

    integral_0^t G0 e = [G0 h/omega_r]_0^t - integral_0^t (G0/omega_r)_dot h -4 integral_0^t G0 Phi.

Both G0/omega_r and its derivative are O(1/k) on this interval. Thus the integral is O(N0/k). These are uniform cumulative estimates, not a pointwise assertion that radiation density vanishes. Comparing the integral equations with zbar_dot=L0(a)zbar, Gronwall yields sup ||z-zbar||<=C N0/k. Replacing a by a_d in the slow operator costs O(N0/m^2) by the background estimate and Lipschitz continuity. The limit equations for A,d,u are A_dot=i(omega A+P_m), d_dot=-kappa u/a_d^2, u_dot=P_m, where P_m=-g(2s Re A+b d)/(kappa a_d). The counter-rotating B decouples. Differentiating with delta_s=2 Re A and delta_b=d gives exactly the theorem, using omega_dot=-2H_d omega. The physical density differs from 2Re A by O(N0/m) using the cancellation, E>=1, E-1=O(m^-2), K/rho_s<=2 and Phi=O(N0/m). This proves the stated rate because k=sqrt(m kappa).

### Zero initial acoustic amplitude and nonconvergence of general radiation

If w0=0, the rotated acoustic estimate implies ||w||<=C N0/k, and the exact radiation equation gives ||w_dot||<=C N0. The remainder R_z now costs O(N0/m+N0/k^2)=O(N0/m), and Gfast e integrates to O(N0/m) using the improved derivative bound. The displayed integration by parts for G0 e costs O(N0/k^2+N0/m)=O(N0/m). The rest of the proof is unchanged. This proves the improved matter rate for initially vanishing acoustic data, without setting radiation background density to zero.

For w0 nonzero and any fixed t>0, theta_d(t)=sqrt(m kappa) c(t), c(t)>0. Taking continuous positive masses along sequences with theta_d(t)=2pi n+alpha gives distinct limiting radiation density values as alpha varies, by the acoustic estimate. Thus generally no pointwise radiation density limit exists. For fixed smooth test functions, integration by parts against the free rotation instead gives weak vanishing of the oscillatory radiation density on [0,T]. This distinction prevents a false strong multi-species limit. QED.

## 4. Reproduction and scope

`OPENBLAS_NUM_THREADS=1 python verify.py` (NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0). Use an external 90-second timeout for hard enforcement; script guards between integrations and after solver return are not a hard per-solver resource limit. Guard failure is INCOMPLETE. Two compositions, kappa in {1,4}, initial normalized acoustic data (1,.4) or (0,0), masses 32,64,128,256; independent DOP853 and RK45 full Cartesian solutions and four limiting reference solutions. Both density and acoustic components are compared at 301 samples, and charge, scalar comoving energy and denominator are checked. Numerical samples do not establish the unrestricted theorem or the optimal asymptotic rate. The script also checks the earlier pressureless-baryon Jeans determinant identity, separately from the two radiation-inclusive Einstein identities. Receipt bytes can vary across platforms. The fresh run uses the available container, not the Mac. No claim about observational growth, realistic photons, neutrino anisotropic stress, recombination, primordial initial conditions, historical calibration equivalence, or the superhorizon limit. Independent novelty not established. Repository integration requires approval.
