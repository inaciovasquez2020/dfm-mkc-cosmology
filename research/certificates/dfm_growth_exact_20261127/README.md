# Exact transfer and uniform bounds for the averaged EdS growth IVP

2026-11-27. Public repository base: `inaciovasquez2020/dfm-mkc-cosmology` at `ea4f548e5c9b3160ea0a4dde76cab74be6a4964f`. Existing implementation: `src/dfm_mkc_solver/averaged_matter_growth_suppression_v1.py`. Existing receipt: `artifacts/dfm_mkc/averaged_matter_growth_suppression_v1.json`. Analytic results PROVED for that averaged equation; standalone numerical checks COMPUTATION_PASS_SCOPED. Lean and full repo CI NOT_RUN. No quantum, observational or novelty claim.

## 1. Exact IVP solution

Assume a_i>0, m>0, H_1>0, k>=0, EdS H=H_1 a^(-3/2), and the averaged one-component perturbation equation

    delta_NN + (1/2)delta_N + [k^4/(4m^2 H_1^2 a) - 3/2]delta=0,
    delta(a_i)=1, delta_N(a_i)=1.

Define t=ln(a/a_i), q=k^4/(4m^2 H_1^2 a_i), S=exp(-t)delta. The normalized IVP is

    S''+(5/2)S'+q exp(-t) S=0, S(0)=1, S'(0)=0.

For q>0 set x_i=2 sqrt(q), x=x_i exp(-t/2). The change of variables yields delta_xx+(1-6/x^2)delta=0. Let j_l,y_l be spherical Bessel functions. A fundamental pair is x j_2(x), x y_2(x), with Wronskian 1. At x_i the initial conditions are delta=1, delta_x=-2/x_i. Using f_l'=f_{l-1}-(l+1)f_l/x for either family, the two coefficients are x_i y_1(x_i) and -x_i j_1(x_i), respectively. Thus

    S(t)=x^3/x_i [y_1(x_i) j_2(x)-j_1(x_i) y_2(x)].

The zero-q case has S=1. As x->0, x^3 j_2(x)->0 and x^3 y_2(x)->-3, so

    S_infinity=3 j_1(x_i)/x_i=3(sin x_i-x_i cos x_i)/x_i^3.

Equivalently S_infinity=3 integral_0^1 u^2 sinc(x_i u) du, using sinc(v)=sin(v)/v with sinc(0)=1. This is the spherical top-hat transform evaluated at x_i, not an identification of physical smoothing or of a primordial transfer function. For q->0, S_infinity=1-(2/5)q+(2/35)q^2+O(q^3). The exact coefficient may be negative or vanish for large q; the signed ratio is not the power spectrum. For x_i>0 its zeros satisfy tan(x_i)=x_i (cos x_i=0 cannot be a zero). At such a zero the growing-mode coefficient vanishes. Absolute late transfer is bounded by 3(1+x_i)/x_i^3, hence O(q^-1) as q->infinity.

The instantaneous Jeans balance is k_J(a)^4=6 m^2 H_1^2 a, i.e. k_J=6^(1/4) sqrt(m H_1) a^(1/4). This is coefficient balance, not a claim about the sign of an individual solution's time derivative. Standard context: Hu, Barkana, Gruzinov (2000), Fuzzy Cold Dark Matter, doi:10.1103/PhysRevLett.85.1158; Chavanis (2012), Growth of perturbations in an expanding universe with Bose-Einstein condensate dark matter, doi:10.1051/0004-6361/201116905. Bessel solutions and the Jeans scale are established literature; novelty of this scoped IVP analysis NOT_ESTABLISHED.

## 2. Global amplitude bound and explicit finite-time error

For q>0 define V=S^2+exp(t) S'^2/q. Direct substitution gives V'=-4 exp(t) S'^2/q <=0. Since V(0)=1, |S(t)|<=1 for every t>=0, all q. For q>0 and t>0 strict inequality holds: S''(0)=-q<0 so the dissipated integral is positive. For q=0 the equality case is S=1.

Integrating the normalized ODE twice yields the Volterra equation

    S(t)=1-q integral_0^t K(t-s) exp(-s) S(s) ds,
    K(v)=(2/5)(1-exp(-5v/2)).

The kernel is nonnegative. Its integral against exp(-s) is

    F(t)=2/5-(2/3)exp(-t)+(4/15)exp(-5t/2).

Thus 0<=1-S(t)<=q F(t)<=2q/5. Substituting S(s)>=1-q F(s)>=1-q F(t) back into the integral proves

    q F(t)(1-q F(t)) <= 1-S(t) <= q F(t).

The lower bound is useful when q F(t)<1. This proves an explicit O(q^2) error for the linearized suppression, uniform in t>=0. For q<=3/2 (initial wavenumber at or below Jeans), S>=2/5>0. Then the first integrated equation for S' gives strict decrease for q>0,t>0. In particular the relative suppression is bounded by (2/5)q=(3/5)(k/k_J(a_i))^4. This controls the IVP for arbitrary duration, without numerical time stepping. It does not establish monotonic dependence on q in the oscillatory regime.

## 3. Verification

`OPENBLAS_NUM_THREADS=1 python verify.py` with NumPy 2.3.5 and SciPy 1.17.0. Two independent solve_ivp methods (DOP853, RK45), 63 q values from 0 through 400, 641 time samples per case on [0,16], independent quadrature of the limit formula and comparison to the four frozen repository examples. Numerical checks do not replace the proofs. 150-integration guard, 40-second between-integration guard and post-solver evaluation limit; use an external process timeout for a hard time cap. Any guard or solver failure is INCOMPLETE, not PASS. Floating-point receipt may vary across versions/platforms. Full field evolution, relativistic modes, baryon/radiation perturbations, metric transfer, gauge normalization, actual primordial initial conditions, likelihood and observational validity remain OPEN. No Codex or Claude used; no repository writes.
