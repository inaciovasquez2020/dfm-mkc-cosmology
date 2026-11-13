# Certified positive-energy radion minimum from a fixed mixed 5D periodic spectrum

**Date:** 2026-11-13. **Status:** PROVED for the explicitly defined one-loop 4D Einstein-frame radion effective potential, with exact rational enclosures of the full infinite spectral sums. **Lean:** NOT_RUN. **Full coupled 5D/quantum perturbations:** OPEN. **Novelty:** NOT CLAIMED; construction overlaps the 2026 Biswas–Juberi–Kamal mixed-spectrum mechanism.

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

## Prior literature, scope and blockers

This is a self-contained numerical-rigor reproduction of a known mechanism, **not a new 5D theory**. Biswas, Juberi and Kamal, *Quality Time in Extra Dimensions: Axion Quality and Radion Cosmology*, arXiv:2611.12765v1 (November 9, 2026), https://arxiv.org/abs/2611.12765, Section 4 and Appendix B, derive the massive periodic scalar determinant, reverse the sign for fermions, and obtain radion Minkowski/dS minima using mixed neutral spectra. The present configuration uses one specifically stated Dirac field and massless real scalar rather than asserting the physical benchmark values in that paper.

**Required independent follow-up:** Check all 5D gauge, graviton, scalar, fermion and mixed KK quadratic kinetic terms, their characteristics and mass matrices, and renormalization/loop validity at the chosen scale. A positive radion curvature is only a **zero-mode** stability condition, not proof of global, nonlinear or full 5D stability. Quantized winding period and bulk cosmological constant were selected to produce the minimum, and no naturalness or observational selection mechanism is established. The effective 4D geometry/causal-order distribution can be reproduced by an appropriately matched 4D model, so this provides **no Chronos discriminant** and no evidence of physical 5D necessity.

Reproduce without downloads using Python 3 standard library:

```bash
python3 -B research/5d/mixed_periodic_spectral_ds_certificate.py
```

At the exact PR revision require a successful dedicated GitHub Actions job plus other required status gates; a queued, failed or timed-out job is **NOT PASS**. Local Mac checkout and toolchains were not inspected.

**STATUS:** ONE_LOOP_RADION_DS_LOCAL_MINIMUM := PROVED; INFINITE_SERIES_SIGN := COMPUTATION_PASS only after verifier execution; COUPLED_5D_STABILITY := OPEN; PHYSICAL_5D := OPEN; LEAN_VERIFIED := NOT_RUN; NOVELTY := NOT_CLAIMED.
