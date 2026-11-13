# Certified positive-energy radion minimum from a fixed mixed 5D periodic spectrum

**Date:** 2026-11-13. **Status:** PROVED for a deliberately **truncated one-loop 4D radion potential**, with exact rational enclosures of every included infinite spectral sum. **NOT A COMPLETE 5D ONE-LOOP VACUUM:** the winding scalar's mixed fluctuations, graviphoton, gravitons, and their spectral shifts have not been included. A single additional independent periodic bosonic determinant destabilizes this candidate. **Lean:** NOT_RUN. **Full coupled 5D/quantum perturbations:** OPEN. **Novelty:** NOT CLAIMED; construction overlaps the 2026 Biswas–Juberi–Kamal mixed-spectrum mechanism.

## 5D spectrum and prescribed action data

Consider a five-dimensional Einstein theory with a circle `w~w+2π`, physical radius `b>0`, renormalized bulk vacuum energy `Lambda`, and a **positive-kinetic compact scalar** with fixed integer winding `n=1`, producing `A/b³` in the 4D Einstein-frame potential (`A=q²/4>0` in the canonical scalar normalization). Include **one real periodic massless neutral scalar** and **one periodic massive neutral 5D Dirac fermion** (four fermionic physical degrees of freedom) of fixed proper mass `m=5/(2π)`, both minimally coupled to the 5D metric. The Dirac fermion's Grassmann determinant reverses the scalar Casimir sign.

Poisson resummation of the periodic KK determinants, with the local zero-winding bulk term subtracted into renormalized `Lambda`, yields the single-real-boson normalization `B=3/(64π⁶)>0` and full Einstein-frame potential

```text
V(b)=Lambda/b+A/b³+B/b⁶ [4 S(mb)-zeta(5)],
S(mb)=sum_(n=1)^infty e^(-2π n m b)
                     [1+2π n m b+(2π n m b)²/3]/n⁵.
```

The field content, spin multiplicity, periodic boundary conditions and `m` are fixed before the vacuum calculation. The winding amplitude and bulk cosmological constant are **tuned** to exhibit a stationary minimum: choose reference radius `b*=1`, `A=B/2` (equivalently the compact scalar's winding slope `q=sqrt(2B)`, adjustable by its period for `n=1`). Define

```text
G(b)=4 S(mb)-zeta(5),
G0=G(1), G1=G'(1), G2=G''(1),
Lambda=B[-3/2 + G1 - 6 G0].
```

The last relation enforces `V'(1)=0` **exactly**; the remaining questions are the signs of `Lambda`, `V(1)`, `V''(1)`.

## Rigorous infinite-series certificate

Set `z_n=5n`, `P(z)=1+z+z²/3`, `h(z)=e^(-z)P(z)`. Then

```text
P_1(z)=P'(z)-P(z)=-(z+z²)/3,
P_2(z)=P_1'(z)-P_1(z)=(z²-z-1)/3.
S(1)=sum h(5n)/n⁵,
S'(1)=sum e^(-5n)*(5n)*P_1(5n)/n⁵,
S''(1)=sum e^(-5n)*(5n)²*P_2(5n)/n⁵.
```

All sums are absolutely convergent. The accompanying **standard-library Python 3 exact certificate** establishes the full infinite sums' intervals with no floating-point arithmetic:

- Bounds `r=e^-5` using reciprocals of the first 61 nonnegative Taylor terms of `e^5`, with an explicit geometric upper bound on the Taylor tail.
- Includes the first 12 spectral winding terms and bounds every remaining absolute summand of each of `S,S',S''` by `260 r^n`; the remaining tail is at most `260 r^13/(1-r)`, with `0<r<1/100`.
- Bounds `zeta(5)` by its first 100 terms and the positive decreasing integral-test tail `1/[4(101)^4]<tail<1/[4(100)^4]`.
- Uses interval arithmetic for `G0,G1,G2` and the following **exact identities**:

```text
Lambda/B = -3/2 + G1 - 6 G0,
V(1)/B   = -1 + G1 - 5 G0,
V''(1)/B = 3 + G2 - 10 G1 + 30 G0.
```

The certified strict rational bounds are

```text
1 < Lambda/B < 11/10,
9/10 < V(1)/B < 91/100,
5/4 < V''(1)/B < 13/10.
```

Thus `V'(1)=0`, `V(1)>0` and `V''(1)>0` for the **full infinite spectrum**. For canonical 4D radion `phi=sqrt(3/2)log b`, the squared zero-mode radion mass at the stationary point is `m_phi²=(2/3)V''(1)>0`. By ordinary second-derivative calculus, this is a strict local minimum and an effective de Sitter radion vacuum. No truncated-sum sign assumption is used.

For one minimally coupled 5D massless **spectator** with unit coordinate circle and reference radius `b*=1`, the nominal Einstein-frame first KK mass equals one and `H_E²=V(1)/3`. Since `B=3/(64π⁶)<1/10000` (using `π>3`), the certified vacuum bound gives `m_KK/H_E>100` in the chosen normalization. This is not a full gravitational/matter spectral gap or a controlled one-loop expansion test.

The same interval certificate also fixes the **radion/Hubble ratio**:
`(m_phi/H_E)^2=2V''(1)/V(1)` and therefore `33/20<m_phi/H_E<17/10` (approximately 1.68). The **radion is not parametrically decoupled** at the Hubble scale despite the heavy spectator KK excitation. A matched four-dimensional effective theory must retain the radion as a light dynamical scalar; eliminating it would not be justified by this certificate.

**EFT scale qualification:** The normalization `b*=1` and 5D Einstein coefficient `R5/2` puts the circle radius at the reference five-dimensional Planck length. Therefore the statement `m_KK/H_E>100` alone **does not show the KK level is well below the gravitational cutoff** or that the one-loop Casimir approximation is perturbatively controlled. A hierarchy involving the 5D Planck scale, field masses, compactification radius and higher loops remains to be established.

## Prior literature, scope and blockers

This is a self-contained numerical-rigor reproduction of a known mechanism, **not a new 5D theory**. Biswas, Juberi and Kamal, *Quality Time in Extra Dimensions: Axion Quality and Radion Cosmology*, arXiv:2611.12765v1 (November 9, 2026), https://arxiv.org/abs/2611.12765, Section 4 and Appendix B, derive the massive periodic scalar determinant, reverse the sign for fermions, and obtain radion Minkowski/dS minima using mixed neutral spectra. The present configuration uses one specifically stated Dirac field and massless real scalar rather than asserting the physical benchmark values in that paper.

**Required independent follow-up:** Check all 5D gauge, graviton, scalar, fermion and mixed KK quadratic kinetic terms, their characteristics and mass matrices, and renormalization/loop validity at the chosen scale. A positive radion curvature is only a **zero-mode** stability condition, not proof of global, nonlinear or full 5D stability. Quantized winding period and bulk cosmological constant were selected to produce the minimum, and no naturalness or observational selection mechanism is established. The effective 4D geometry/causal-order distribution can be reproduced by an appropriately matched 4D model, so this provides **no Chronos discriminant** and no evidence of physical 5D necessity.

Reproduce without downloads using Python 3 standard library:

```bash
python3 -B research/5d/mixed_periodic_spectral_ds_certificate.py
```

At the exact PR revision require a successful dedicated GitHub Actions job plus other required status gates; a queued, failed or timed-out job is **NOT PASS**. Local Mac checkout and toolchains were not inspected.

**STATUS:** ONE_LOOP_RADION_DS_LOCAL_MINIMUM := PROVED; INFINITE_SERIES_SIGN := COMPUTATION_PASS only after verifier execution; COUPLED_5D_STABILITY := OPEN; PHYSICAL_5D := OPEN; LEAN_VERIFIED := NOT_RUN; NOVELTY := NOT_CLAIMED.


## Independent completeness and EFT cutoff audit — decisive qualification

The exact series certificate proves a **mathematical property of the included determinant terms**. It does **not** establish that these terms form the entire one-loop spectrum of the purported five-dimensional action. In particular, the winding scalar is itself dynamical, and its fluctuations can mix with the Kaluza–Klein graviphoton. Gravitational fluctuations also contribute quantum determinants. The primary treatment explicitly warns that free-field Casimir formulas need not apply where winding-induced splittings and mixings matter (Biswas–Juberi–Kamal, arXiv:2611.12765v1, Section 4.2.2, note 6).

A **quantified adversarial sensitivity test**, rigorously certified using the same existing infinite-series interval bounds, adds only **one extra independent free periodic massless real bosonic determinant** to the truncated potential:

```text
Delta V(b) = -B*zeta(5)/b^6,  B=3/(64*pi^6).
```

Keep the winding parameter `A=B/2`, the massive fermion content, and the stationary reference `b*=1` fixed, but readjust the bulk cosmological constant to restore `V'(1)=0`. The exact changes in units of `B` are

```text
Delta Lambda/B = +6*zeta(5),
Delta V(1)/B   = +5*zeta(5),
Delta V''(1)/B = -30*zeta(5).
```

Since `zeta(5)>1` and the **truncated** spectral certificate has `V''(1)/B<1.30`, the modified stationary point obeys `V''(1)/B< -28` while retaining **positive vacuum energy**. Thus **one additional independent massless boson destroys this particular local radion minimum**. This is an exact counterexample to treating the result as robust under completion of its particle content. It does **not** imply the true mixed winding-scalar–graviphoton determinant equals an independent free scalar: that is precisely the missing calculation.

The reference Einstein–Hilbert action is `M5^3 R5/2`, with the selected numerical example using `M5=1`, `b*=1`. In the five-dimensional local/Jordan frame,

```text
b* M5 = 1,
m_1,KK / M5 = 1,
m_Dirac / M5 = 5/(2*pi), strictly between 35/44 and 5/6,
M4²/M5² = 2*pi  (at b*=1/M5).
```

Therefore **the first KK excitation is at the nominal 5D Planck scale**, and the massive Dirac field is also of the same order. The previously certified `m_KK/H>100` is a hierarchy relative to curvature, **not a hierarchy below the gravitational cutoff**. Without further parameter scaling and control of gravitational loops, this concrete numerical example does not establish a reliable five-dimensional EFT.

These two objections are independently audited in `research/5d/mixed_spectral_completeness_cutoff_audit.py` (Python stdlib, exact interval arithmetic), now required by the dedicated workflow. **A stable physical de Sitter compactification is NOT ESTABLISHED.** The credible result is a stable local radion minimum in the explicitly truncated one-loop potential, plus a demonstrated lack of robustness to an extra bosonic determinant. Before promotion as a physical source, the complete coupled determinant and a parameter regime with `1/b\ll M5`, `m_f\ll M5`, and controlled quantum corrections must be constructed.


## Constructive large-radius scaling: solves the reference cutoff issue, not spectral completeness

The cutoff issue `b*M5=1` is a limitation of the **numerical reference normalization**, not a universal no-go for the truncated one-loop spectral shape. In units `M5=1`, put `b=R x`, fix `R>0`, and scale the microscopic input parameters as

```text
m_Dirac(R)=5/(2*pi*R),
A(R)=B/(2 R³),   Lambda(R)=Lambda0/R^5,
Lambda0/B=-3/2+G1-6G0.
```

The integer winding remains `n=1`, but its scalar period/kinetic coefficient must be tuned so that the winding slope `q²=4A(R)` scales as `R^-3`. These choices **change the microscopic couplings across the family**; they do not follow dynamically from the action's equations.

At fixed dimensionless `x=b/R`, the complete **included** one-loop potential satisfies exactly

```text
V_R(R*x)=V_1(x)/R^6,
V'_R(R*x)=V'_1(x)/R^7,
V''_R(R*x)=V''_1(x)/R^8.
```

The stationary point and positive zero-mode curvature of the **truncated** model therefore persist, with `H_E²~R^-6` and `m_radion²~R^-6`. The Einstein-frame first spectator KK mass scales as `R^-3/2`, so `m_KK/H_E~R^(3/2)`. In the local 5D Jordan frame, `m_KK/M5=R^-1`, and `m_Dirac/M5=5/(2πR)`. Thus `R≫1` can put the KK tower and Dirac mass well below the nominal 5D gravitational scale while retaining a large KK/H ratio **in this tuned potential family**.

For a rigorous example, `R=100` yields `m_KK/M5=1/100`, `m_Dirac/M5<1/100`, and `m_KK/H_E>100000`, using the exact previously certified spectral energy bound and `π>3`. The independent stdlib checker `research/5d/mixed_spectral_large_radius_scaling_audit.py` tests the exact scaling identity at bounded rational inputs and checks these inequalities without floats.

**However, the missing-spectrum instability is scale-invariant:** adding the independent free massless bosonic determinant and readjusting `Lambda(R)` gives
```text
V''_(extra)(R)/[B R^-8] = V''_(truncated)(1)/B - 30*zeta(5) < -28
```
for every `R>0`. The corresponding canonical radion mass squared remains negative for all radii. Thus merely increasing the circle radius **does not repair the actual missing-field-content question**.

**Scope of achievement:** A formal *parametrically scale-separated region* exists for the explicitly **truncated and tuned one-loop potential**, so the reference cutoff problem is avoidable. This does not prove higher-loop suppression for the complete action, quantum consistency, the correct winding/graviphoton determinant, or a viable de Sitter state. The smallest physical blocker remains computing and auditing the full coupled five-dimensional fluctuation spectrum, not further tuning the radius.
