# Exact Einstein–Gauss–Bonnet winding de Sitter × circle background

**Status (2026-11-13):** PROVED product-background equations by exact curvature contraction; COMPUTATION_PASS independently for all 25 tensor components. Linearized radion mass is a **formal restricted zero-mode result**. Full ghost, hyperbolicity, KK, and nonlinear stability OPEN. Lean NOT_RUN; no physical fifth dimension or novelty claimed.

## Specified source and solution

In units with gravitational coefficient 1/2 and signature (-,+,+,+,+), use the 5D action

S5 = integral sqrt(-g5) [R5/2 - Lambda5 + alpha GB5/2 - (dchi)^2/4],

where GB5 = Riem^2 - 4 Ric^2 + R^2. The compact winding scalar is chi = q*w (mod 2pi), w ~ w+2pi, q integer; its differential is global and its equation Box5 chi = 0 holds. Let ds5^2 = ds4_dS(k)^2 + b^2 dw^2, with Ric4 = 3k g4 and k,b>0. Put Q=q^2/(4b^2).

Independent full curvature contraction yields R5=12k, GB5=24k^2 and Lanczos tensor H_mu_nu=0, H_ww/g_ww=-12k^2. The Einstein–Lanczos equations are

G_AB + Lambda5*g_AB + alpha*H_AB = (1/2)(dchi)_A(dchi)_B - (1/4)g_AB(dchi)^2.

They reduce exactly to 3k=Lambda5+Q and -6k+Lambda5-12alpha*k^2=Q, or equivalently

Q=-(3/2)k-6alpha*k^2, Lambda5=(9/2)k+6alpha*k^2.

**Exact rational witness:** alpha=-1, k=1/3, Lambda5=5/6, q=1, b^2=3/2, Q=1/6. The independent stdlib verifier constructs all Riemann/Ricci/Lanczos components in a 5D orthonormal frame and checks every field-equation residual equals zero.

**Important sign boundary:** Q>0 with k>0 requires alpha<0. This negative Gauss–Bonnet coupling may be associated with problematic perturbation sectors. Exact background existence alone does not prove a physically viable compactification.

## Restricted zero-mode radion calculation

The 4D Jordan-frame reduction for the block-diagonal varying circle radius b(x), after dropping total divergences, is

S4/(2pi) = integral sqrt(-g4) [ b(R4+alpha GB4)/2 - Lambda5*b - q^2/(4b) ].

For a 4D maximally symmetric background, delta GB4=4k delta R4. With C=1+4alpha*k, the linearized radion and trace equations read

(C/2) delta R4 - (2Q/b) delta b=0,
-b delta R4 -8Q delta b+3C Box4 delta b=0.

For C!=0 they give (Box4-m_J^2)delta b=0 with m_J^2=4Q(1+2C)/(3C^2). For the rational witness C=-1/3 and m_J^2=2/3>0, yielding m_J^2/k=2. This is a formal mass calculation only: **it does not establish positive kinetic energy, absence of tensor/vector/scalar ghosts, full perturbative stability, or well-posedness.**

More generally alpha=-a<0 and a>0. The open interval 1/(4a)<k<3/(8a) gives Q>0, Lambda5>0, C!=0 and m_J^2>0. The endpoints are excluded. This is an algebraic interval, not a physically certified stable phase. The separate spin-2 principal-symbol audit below identifies a decisive high-KK instability on the entire winding-supported dS branch.

## Literature and research boundary

Related established approaches include Canfora, Giacomini & Pavluchenko, *Dynamical compactification in Einstein–Gauss–Bonnet gravity from geometric frustration*, Phys. Rev. D 88, 064044 (2013), DOI https://doi.org/10.1103/PhysRevD.88.064044; and *General relativity from Einstein–Gauss–Bonnet gravity*, Phys. Rev. D 104, 044026 (2021), DOI https://doi.org/10.1103/PhysRevD.104.044026. Neither is asserted to use this exact model; novelty is NOT ESTABLISHED.

Unlike the minimal Einstein–winding construction [PR #336](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/336), which has a stabilized AdS rather than dS background, a higher-curvature source admits an exact dS background. This does **not** imply that the model describes our universe or has a distinctive observable against a matched 4D theory.

**Next decisive obstruction:** derive the complete gauge-fixed quadratic 5D perturbation action, determine kinetic signatures/characteristics and KK spectrum. Chronos observable transfer, observational necessity and Lean validation remain OPEN.

Reproduce with Python standard library: python3 -B research/5d/egb_winding_ds4_exact_audit.py. Do not optimize Python; assertions must be active. No Mac worktree or local-only research was inspected.

## Decisive new obstruction: transverse spin-2 circle principal symbol

**PROVED for the classical full 5D Einstein–Gauss–Bonnet–winding action above.** The product equations give the identity Q = -(3k/2)(1+4alpha*k). Thus any positive-curvature dS4 solution with nonzero winding Q>0 forces C:=1+4alpha*k<0. This is stronger than the merely necessary condition alpha<0.

The separate exact verifier research/5d/egb_winding_kk_tensor_symbol.py perturbs the five-dimensional algebraic Riemann tensor by an off-diagonal transverse polarization with unit component delta R_(1,4,2,4). It differentiates **every curvature term** in the Lanczos tensor and checks delta Ric_12=1 and delta H_12=4k. Consequently the coefficient of the second derivative of h_12 along the circle in the linearized 5D equation is C=1+4alpha*k, while its four-dimensional propagation coefficient is positive: the reduced constant-radius Einstein term is bR4/2 and the 4D GB4 term at constant b is topological.

For Fourier index n around a circle of radius b, the high-n spin-2 dispersion has principal contribution omega^2=|spatial momentum|^2+C*n^2/b^2+O(k). At fixed 4D momentum and k, arbitrarily large n make omega^2 negative. The explicit rational witness has C=-1/3 and circle contribution -2n^2/9. This is a **classical unrestricted Kaluza–Klein tensor gradient/tachyon obstruction**. It rules out treating this particular dS4×S1 solution as linearly stable across its entire classical KK tower, despite the positive restricted radion mass. It is not a claim about a UV-cutoff effective theory, possible modified actions, or all 5D models.

**Revised status:** exact dS background = PROVED/COMPUTATION_PASS; healthy full classical 5D compactification = REFUTED for this winding-supported product branch by the negative spin-2 circle principal coefficient; stable accelerating physical universe = OPEN for different actions. Full tensor kinetic and hyperbolicity analysis should independently cross-check this principal symbol; it does not repair the identified sign.
