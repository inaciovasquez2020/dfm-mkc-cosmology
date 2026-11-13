# Transient 4D Einstein-frame acceleration with a shrinking 5D circle and NEC/DEC matter

**DATE:** 2026-11-13. **STATUS:** PROVED as a local exact geometric Einstein–stress construction with rational interval inequalities; COMPUTATION_PASS of independent polynomial checks; LEAN_VERIFIED NOT_RUN; **locally inverse-engineered covariant matter action CONSTRUCTED; microphysical justification OPEN**. No novelty claim.

## Geometry and scope

Take five-dimensional standard Einstein gravity with `Lambda5=0` and `kappa5²=1` on a finite time interval `I=[-1/100,1/100]`. The smooth 5D Lorentzian metric is

```text
ds5² = -dt² + a(t)²(dx²+dy²+dz²) + b(t)²dw²,
w ~ w+2π,
a(t)=exp(t-3t²/5), b(t)=exp(-t/10+t²/2).
```

Let `H=dot(a)/a=1-6t/5`, `F=dot(b)/b=-1/10+t`. The stress-energy is **defined** by the five-dimensional Einstein tensor `T_AB=G_AB`. This independently specifies the effective stress tensor; a compatible local covariant canonical-scalar–Maxwell action is constructed in the later section. Its potential and gauge coupling are inverse-engineered from the geometry, not independently motivated by microphysics.

## Full effective stress tensor

With `rho=T_tt`, `p3=T_xx/a²=T_yy/a²=T_zz/a²`, and `pw=T_ww/b²`, the full Einstein equations give

```text
rho = 3H²+3HF
p3  = -(2 dot H + dot F +3H²+2HF+F²)
pw  = -(3 dot H +6H²).
```

The exact expansions are

```text
rho     = 27/10 -96t/25 +18t²/25
rho+p3  = 129/100 +33t/25 -11t²/5
rho+pw  = 3/10 +264t/25 -198t²/25
rho-p3  = 411/100 -9t +91t²/25
rho-pw  = 51/10 -456t/25 +234t²/25.
```

The conservation identity

```text
dot rho+3H(rho+p3)+F(rho+pw)=0
```

holds as a polynomial identity (also follows from Bianchi).

For any polynomial `f(t)=sum c_i t^i`, on `|t|≤1/100` its exact lower bound is `c_0 - sum_(i≥1) |c_i|/100^i`. The independent verifier applies this bound, with no floating point, to `H,-F,rho,rho±p3,rho±pw` and the 4D Einstein-frame expansion and acceleration numerators. Every bound is **strictly positive**, so the effective source satisfies **both 5D NEC and 5D DEC** throughout `I`. This is stronger than checking sampled times. The local scalar–Maxwell reconstruction below also produces these same stress components from a positive-sign covariant action.

## Four-dimensional reduction and acceleration

Use `gE=b gJ`, `d tau=sqrt(b)dt` and `aE=a sqrt(b)`. The Einstein-frame acceleration is

```text
(1/aE) d²aE/dtau² = [dot H +dot F/2 +H²+HF/2]/b
                  = [1/4 -46t/25 +21t²/25]/b.
```

Because `b>0` and the numerator is strictly positive throughout the interval, this is a genuine period of 4D Einstein-frame acceleration with an actually shrinking circle `F<0`. At `t=0`, `H=1, F=-1/10, rho=27/10, p3=-141/100, pw=-12/5`, hence

```text
rho+p3=129/100>0, rho+pw=3/10>0,
Einstein-frame acceleration numerator = 1/4>0.
```

**Conclusion:** The NEC **power-law** no-go from [Cosmology PR #339](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/339) is **not an unrestricted no-go theorem for arbitrary smooth time-dependent scale factors**. The two claims are consistent: the present time dependence is non-power-law and acceleration is transient. This model does not exhibit exact de Sitter expansion or a stabilized finite circle. The matter action constructed below is local and engineered; it does not establish a realistic cosmology.

## Exact verification and primary literature

Run with Python 3 standard library (no downloads):

```bash
python3 -B research/5d/nec_transient_accelerating_circle_exact.py
```

The certificate derives the stress tensor and expansion coefficients through independent `Fraction` polynomial operations, checks the Einstein/Bianchi identity, and proves all listed inequalities on the entire closed time interval by exact absolute-coefficient bounds. No enumerated finite grid is relied upon to establish positivity.

The **possibility of transient acceleration from time-dependent compactification is already established** in the literature. In particular, Daniel H. Wesley, *Oxidised cosmic acceleration*, JCAP 01 (2009) 041, DOI https://doi.org/10.1088/1475-7516/2009/01/041, derives much broader no-go and e-fold bounds for the one-dimensional compact case under NEC. This local stress-engineered example does not constitute a novel physical mechanism.

## Explicit remaining obstacles

- **MATTER_ACTION := CONSTRUCTED, LOCAL AND INVERSE-ENGINEERED** — a fully specified covariant Einstein–canonical-scalar–Maxwell action with a smooth positive scalar-dependent gauge coupling and scalar potential is exhibited below. Its arbitrary functional couplings are tuned to the chosen metric; microphysical naturalness and independent physical predictions remain OPEN.
- **LONG_DURATION_ACCELERATION := OPEN** — positivity is certified only on `I`. Existing higher-dimensional e-fold bounds must be respected.
- **RADION_STABILIZATION := OPEN** — the circle still shrinks and later turns around in this chosen extension; no stable compactification.
- **KK_AND_PERTURBATIVE_STABILITY := NOT_RUN** — no full spectrum/ghost/hyperbolicity audit.
- **CHRONOS_TRANSFER_AND_PHYSICAL_5D_NECESSITY := OPEN** — an ordinary 4D model with the same metric/order/sampling law remains observationally degenerate on causal-chain statistics.

No repo besides Cosmology is asserted to be required for the direct geometric test; Chronos remains the chosen eventual 4D event-observable counterpart, URF Core supporting, and other connections background.

## Exact local scalar–Maxwell matter action (2026-11-13)

**Result:** The preceding effective-stress solution is not limited to defining an arbitrary stress tensor by `T=G`. A local *covariant* matter action can be reconstructed from a canonical homogeneous scalar and a circle-directed Maxwell electric field, both with conventional positive kinetic signs. This is an **inverse-engineered model**: the potential and gauge coupling are prescribed by the desired geometry, so it is not a prediction or evidence that a fifth dimension is physically necessary.

Use a five-dimensional scalar `varphi` and U(1) connection `A`, with `F=dA` and

```text
S5 = ∫ d5x sqrt(-g5) [ R5/2 - (∂varphi)^2/2 - V(varphi)
                        - f(varphi) F_AB F^AB/4 ].
```

On the same `I=[-1/100,1/100]`, let `H=1-6t/5`, `F_c=-1/10+t`, `a=exp(t-3t²/5)`, `b=exp(-t/10+t²/2)`. To avoid confusing circle expansion `F_c` with Maxwell curvature `F_AB`, define polynomials in `t`:

```text
C(t) = rho(t) + pw(t) = 3/10 + (264/25)t - (198/25)t²,
D(t) = p3(t) - pw(t) = 99/100 - (231/25)t + (143/25)t²,
U(t) = (rho(t)-p3(t))/2 = 411/200 - (9/2)t + (91/50)t².
```

Exact coefficientwise interval bounds prove `C(t)>0`, `D(t)>0`, `U(t)>0` everywhere on `I`. Thus `varphi(t)=∫₀ᵗ sqrt(C(s))ds` is strictly monotone and has a smooth inverse `t=T(varphi)` on the scalar image (and locally beyond the interval endpoints). Fix the Maxwell flux charge to `Q=1`, and **define the action's functions** on that image by

```text
V(varphi) = U(T(varphi)),
f(varphi) = exp[-6T(varphi)+18T(varphi)²/5]/D(T(varphi)) > 0.
```

These are specified smooth scalar-only functions, not coefficients re-evaluated from the field equations during evolution. Set the globally defined 5D gauge potential `A=A_w(t)dw` with `A_w(0)=0` and

```text
dA_w/dt = b(t) a(t)^3 D(t).
```

Then the homogeneous Maxwell equation is identically satisfied:

```text
d/dt [a³ f(varphi) (dA_w/dt)/b] = d(1)/dt = 0.
```

The scalar kinetic and electric energies are `K=(dvarphi/dt)²/2=C/2` and `E=f(dA_w/dt)²/(2b²)=D/2`; all are nonnegative, and `f>0`. Their diagonal stress components obey the **full Einstein tensor equations**:

```text
rho = K+V+E,
p3  = K-V+E,
pw  = K-V-E.
```

The remaining scalar equation is

```text
ddot varphi+(3H+F_c)dot varphi+V_varphi-E f_varphi/f=0.
```

Multiplying it by `sqrt(C)>0` reduces it to the exact polynomial identity

```text
C'/2+(3H+F_c)C+U'+3HD+D'/2 = 0,
```

which the standalone exact-rational verifier checks coefficient by coefficient. This closes the **local source-action existence** obstruction for this chosen metric, not the global or predictive physics problem.

**Independent executable audit:** `python3 -B research/5d/nec_transient_scalar_maxwell_action_audit.py`, with no packages/downloads. It imports the original exact full-interval NEC/DEC certificate, checks strict positivity of `C,D,U`, the scalar/Maxwell stress decomposition, Maxwell flux normalization, and the polynomial scalar equation. The precise positive-sign action also demonstrates that the anisotropy cannot be generated by a homogeneous canonical scalar alone or by time-dependent scalar plus spatial winding with the opposite pressure ordering.

**Remaining OPEN:** Why the particular reconstructed `V,f` should be selected by independent physics; extension beyond the local interval; radion and full perturbative/KK mode stability; empirical 5D-specific predictions and an observationally distinguishing Chronos event-sample law. A local action admitting a given solution does not mean the solution is an attractor or a physical model of our universe.

**Prior-art context:** Scalar-dependent gauge kinetic functions and anisotropic Einstein–scalar–vector cosmologies are established constructions; see Do and Kao, *Anisotropic power-law inflation of the five dimensional scalar–vector and scalar-Kalb–Ramond model*, European Physical Journal C 78, 531 (2018), https://doi.org/10.1140/epjc/s10052-018-6008-5. Neither this source-reconstruction mechanism nor the locally engineered solution is presented as a novel physical result.


## Independent KK/Hubble separation audit (2026-11-13)

**COMPUTATION_PASS for the exact interval bound; physical EFT control NOT ESTABLISHED.** This audit concerns a *minimally coupled five-dimensional massless spectator scalar* with periodic coordinate `w ~ w+2π`, rather than the full coupled metric–scalar–Maxwell fluctuation spectrum. Its instantaneous Fourier mass for mode `n` in the 4D Einstein frame is `m_(n,E)=|n| b^(-3/2)`; this follows from the Jordan circle gradient contribution `n²/b²` and the conformal map `gE=b*gJ`. The Einstein-frame Hubble parameter is `HE=(H+F_c/2)/sqrt(b)`. Therefore the first Fourier mode obeys the **exact identity**

```text
m_(1,E)/HE = 1/[b(t)*(19/20-7t/10)].
```

At `t=0` the ratio is exactly `20/19 ≈ 1.05263`. For **all** `|t|≤1/100`, the logarithm `x=log b=-t/10+t²/2` satisfies `|x|≤21/20000`. Applying the elementary bounds `1-u≤exp(x)≤1/(1-u)` for `|x|≤u<1`, and `943/1000 ≤ H+F_c/2 ≤ 957/1000`, gives strict rational bounds

```text
19979/19140 < m_(1,E)/HE < 20000000/18840197 < 107/100.
```

The exact accumulated Einstein-frame e-fold count on the certified interval is only `Delta N_E = log[a_E(1/100)/a_E(-1/100)] = 19/1000 = 0.019`, because `log a_E(t)=19t/20-7t²/20`. Thus the result is a **short transient**, not a sustained inflationary phase.

Hence the first extra-dimensional Fourier excitation is **of the same order as the Hubble scale throughout the entire certified accelerating interval**. This is a decisive *lack of parametric separation*: the low-energy zero-mode truncation is **not justified by a large KK mass/Hubble ratio** in the constructed example. It does not by itself prove that any mode is a ghost, tachyon, or unstable, and a complete coupled fluctuation analysis remains NOT_RUN.

The standalone stdlib exact checker `research/5d/nec_transient_kk_hubble_gap_audit.py` verifies the rational inequalities without evaluating any floating-point functions. The compactification remains local and inverse-engineered. Do not interpret the additional action as a completed physical five-dimensional cosmology, or treat the background's acceleration as a distinctive Chronos observable. The zero-mode observables remain reproducible by an appropriately matched 4D effective theory.

**Current weakest obstruction:** construct a demonstrably healthy fluctuation spectrum with a controlled regime `m_KK/H_E ≫ 1` if an effectively 4D cosmology is intended, **and** find a measurable difference relative to an equally specified 4D comparator. For this exact background the first hierarchy condition already fails quantitatively; further fitting of its scalar potential cannot fix that fact without changing its geometry or normalization.


## Refined interval and tunable radius: corrected scope (2026-11-13)

**PROVED for this specific inverse-engineered local action family; not an observational or stability result.** The earlier `I=[-1/100,1/100]`, `0.019` e-fold and `m_{1,E}/H_E≈1` statements remain correct for the **particular unit-radius normalization** and originally checked interval. They are **not universal limitations** of the family.

### A rigorously longer interval

The analytic geometry and matter functions can be continued on the closed rational interval

```text
I_extended = [-1/50,9/100] = [-0.02,0.09].
```

A new independent standard-library certificate, `research/5d/nec_transient_extended_interval_radius_audit.py`, verifies strict positivity of all necessary quadratic (or lower-degree) polynomials on the **entire interval** using Bernstein coefficients, not grid sampling. The guarded quantities are: `H>0`, `-F_c>0`, `rho>0`, `rho±p3>0`, `rho±pw>0`, `C=rho+pw>0`, `D=p3-pw>0`, `V>0`, `H+F_c/2>0`, and the exact 4D acceleration numerator `A>0`. The scalar clock is strictly monotone and the reconstructed positive `f(varphi)` remains smooth; the field equations continue to hold as exact identities.

Since `log aE(t)=19t/20-7t²/20`, the complete certified extended episode accumulates

```text
Delta N_E = 20361/200000 = 0.101805 e-folds.
```

This is longer than the original 0.019-e-fold certificate, but remains **far from sustained inflation**; no arbitrary-duration acceleration is asserted.

### One-parameter exact circle-radius family

The background ansatz allows an arbitrary constant prefactor `b0>0`:

```text
b_(b0)(t)=b0 exp(-t/10+t²/2).
```

The logarithmic rates `H` and `F_c` and therefore the 5D Einstein tensor in an orthonormal frame are independent of `b0`. The *same* scalar clock `varphi(t)`, potential `V(varphi)`, and positive coupling `f(varphi)=a(t)^(-6)/D(t)` remain unchanged. Choose instead the circle-directed Maxwell field

```text
dot A_w = b_(b0)(t) a(t)^3 D(t).
```

Then the circle electric energy `f(dot A_w/b)^2/2=D/2`, and the conserved Maxwell flux `a³ f dot A_w/b=1`; hence the Einstein equations and scalar equation persist **exactly** for each `b0>0`. The action is held fixed, but this is a **continuous solution family**, not a dynamically fixed or selected circle size. Flux and compact-gauge Wilson-line quantum restrictions have not been independently audited.

For an explicitly named *minimally coupled massless 5D spectator scalar* on a unit coordinate circle, the first KK-to-Einstein-Hubble ratio is

```text
m_(1,E)/H_E = 1/[b0 exp(-t/10+t²/2)(19/20-7t/10)].
```

Taking `b0=1/100`, exact rational exponential inequalities certify throughout the extended interval:

```text
98695/964 < m_(1,E)/H_E < 2000000000/17508493,
100 < m_(1,E)/H_E < 120.
```

Thus **the previous order-one KK ratio is a normalization-dependent obstruction only for the original `b0=1` background**, and a large *spectator* KK/Hubble hierarchy can be arranged at a different radius with the same reconstructed functional action. This does **not** establish stabilization, full graviton–scalar–Maxwell perturbative stability, cosmological naturalness, quantum consistency, or any empirical fifth-dimension signature. It also changes the effective 4D Newton normalization/size of the compactification, which must be accounted for in any physical comparison.

**Corrected mathematical boundary:** For this local class, *existence of transient acceleration and a tunable spectator KK/Hubble gap* are established; **dynamical selection and stability of the radius, prolonged acceleration, the coupled KK spectrum and a discriminating Chronos observable remain OPEN**. Do not continue citing the original `20/19` as a no-go for every member of the family.

**Reproduction:** `python3 -B research/5d/nec_transient_extended_interval_radius_audit.py` from the PR HEAD, plus the source/action verifiers. If any step fails or times out, validation is FAIL/INCOMPLETE, never PASS.


### Radius-modulus Jacobi field (linearized degeneracy)

**PROVED, conditional on the exact family above.** Let `E(g,varphi,A)=0` denote the coupled Euler–Lagrange equations for the *single, fixed* reconstructed action (same `V` and `f`, same circle period). For every `b0>0`, the displayed metric, scalar and circle electric field solve `E=0`. Differentiating the smooth family at any `b0=b*` gives

```text
D E_(g*,varphi*,A*) [ d/db0(g_b0,varphi_b0,A_b0)|_(b*) ] = 0.
```

This is an exact on-shell solution of the **linearized coupled field equations**. In a parametrization by `s=log b0`, its circle-metric component is `delta g_ww=2g_ww`, while `delta varphi=0` and the circle Maxwell potential (fixed by `A_w(0)=0`) varies as `delta A_w=A_w`. The perturbation is nonzero and changes the physical circle circumference at fixed `w~w+2π`; a constant real rescaling of `w` is not a globally valid degree-one diffeomorphism of the fixed-period circle. Thus the background has a *genuine continuous radius-parameter degeneracy*: the field equations do not pick out `b0`.

**Qualification:** On a time-dependent background, a parametric Jacobi field is **not** automatically a Fourier normal mode with zero mass; its norm, boundary conditions, gauge constraints, linear energy, and coupled stability have not been assessed. The result excludes the claim that this exact reconstructed model uniquely *selects* a finite circle size, but does not independently prove nonlinear instability. A radius-fixing dynamical condition remains OPEN.


## Sharp maximal connected shrinking/NEC/accelerating episode

**PROVED for this exact background and inverse-engineered scalar–Maxwell action, not for all five-dimensional cosmologies.** Write the circle Hubble parameter `F_c(t)=t-1/10` and the scalar kinetic function `C(t)=rho+p_w=3/10+(264/25)t-(198/25)t²`. The lower root of `C` is exactly

```text
t_- = 2/3 - sqrt(2101)/66 ≈ -0.02782828.
```

The largest **connected open interval containing t=0** on which the three-space expands, the circle strictly shrinks, the 4D Einstein-frame scale factor expands and accelerates, the five-dimensional NEC/DEC hold, and the canonical scalar–Maxwell reconstruction has `C>0`, `D>0`, `V>0`, `f>0`, is

```text
t_- < t < 1/10.
```

**Exact boundary proof.** The rational values of `C` at `-7/250=-0.028` and `-27/1000=-0.027` have opposite signs, and `C'(t)>0` throughout `[-0.028,0.1]`; thus the unique lower root in that bracket is `t_-`. Every other required inequality has **strictly positive quadratic Bernstein coefficients** over the full *larger* interval `[-0.028,0.1]`, verified as exact Fractions. Therefore no other condition fails before the circle-contraction rate reaches `F_c=0` at `t=0.1`. For `t<t_-` close to the root, circle NEC fails; for `t>0.1`, the circle grows. At `t=t_-`, the canonical scalar speed `dot(varphi)=sqrt(C)` vanishes, so the inverse-scalar-clock construction ceases to be a local diffeomorphism; the strict physical-action interval excludes the endpoint.

The Einstein-frame logarithmic scale factor is `log a_E(t)=19t/20-7t²/20`. The supremum of accelerated e-folds within this **maximal connected episode** is

```text
N_max = 29*sqrt(2101)/3960 - 21529/99000
      ≈ 0.11820791157,
117/1000 < N_max < 119/1000 < 1.
```

The exact script `research/5d/nec_transient_maximal_window_audit.py` verifies the root bracket, monotonicity, full-interval Bernstein positivity, and a rigorous rational enclosure of the e-fold supremum. It does not use finite grid sampling to claim global positivity. This **sharpens** the previous 0.101805-e-fold closed subinterval: one may extend the construction slightly further, but **cannot obtain even one e-fold without changing the metric, action solution branch, or required properties**. Adjusting the free constant circle prefactor `b0` has no effect on `H,F_c,C,D,A` or `Delta N_E`.

### General circle-NEC acceleration identity

For an arbitrary smooth homogeneous metric `-dt²+a(t)² dvecx²+b(t)²dw²` in standard 5D Einstein gravity, with `H=dot a/a`, `F_c=dot b/b`, and `kappa5²=1`, the exact circle-null stress is

```text
rho+p_w = -3 [dot H+H²-H*F_c].
```

The Einstein-frame acceleration numerator `A=dot H+dot F_c/2+H²+H*F_c/2` consequently satisfies the **identity**

```text
A = (dot F_c+3H*F_c)/2 - (rho+p_w)/3.
```

Thus under the circle NEC, `A>0` requires `dot F_c+3H*F_c>0`; equivalently `d(a³ F_c)/dt>0`. With `F_c<0`, the contraction rate weighted by 3-volume must move toward zero. This is a **necessary** condition only, not a global no-go theorem; the transient counterexample in this PR meets it. The sharp 0.1182-e-fold result belongs solely to the constructed metric.
