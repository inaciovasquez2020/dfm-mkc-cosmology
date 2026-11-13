# Transient 4D Einstein-frame acceleration with a shrinking 5D circle and NEC/DEC matter

**DATE:** 2026-11-13. **STATUS:** PROVED as a local exact geometric Einstein–stress construction with rational interval inequalities; COMPUTATION_PASS of independent polynomial checks; LEAN_VERIFIED NOT_RUN; **physical matter action OPEN**. No novelty claim.

## Geometry and scope

Take five-dimensional standard Einstein gravity with `Lambda5=0` and `kappa5²=1` on a finite time interval `I=[-1/100,1/100]`. The smooth 5D Lorentzian metric is

```text
ds5² = -dt² + a(t)²(dx²+dy²+dz²) + b(t)²dw²,
w ~ w+2π,
a(t)=exp(t-3t²/5), b(t)=exp(-t/10+t²/2).
```

Let `H=dot(a)/a=1-6t/5`, `F=dot(b)/b=-1/10+t`. The stress-energy is **defined** by the five-dimensional Einstein tensor `T_AB=G_AB`. This specifies a mathematically exact Einstein–stress solution for a conserved diagonal fluid. It is **not yet** an independently specified covariant matter model or microscopic source Lagrangian.

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

For any polynomial `f(t)=sum c_i t^i`, on `|t|≤1/100` its exact lower bound is `c_0 - sum_(i≥1) |c_i|/100^i`. The independent verifier applies this bound, with no floating point, to `H,-F,rho,rho±p3,rho±pw` and the 4D Einstein-frame expansion and acceleration numerators. Every bound is **strictly positive**, so the effective source satisfies **both 5D NEC and 5D DEC** throughout `I`. This is stronger than checking sampled times.

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

**Conclusion:** The NEC **power-law** no-go from [Cosmology PR #339](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/339) is **not an unrestricted no-go theorem for arbitrary smooth time-dependent scale factors**. The two claims are consistent: the present time dependence is non-power-law and acceleration is transient. This model does not exhibit exact de Sitter expansion or a stabilized finite circle.

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
