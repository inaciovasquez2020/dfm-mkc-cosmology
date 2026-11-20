# Massive periodic bosonic Casimir spectrum: exact radion dS no-go

**Date:** 2026-11-13. **STATUS:** PROVED for the specified one-loop, circle-reduced zero-mode effective potential; polynomial certificate COMPUTATION_PASS when checked; LEAN NOT_RUN; full 5D fluctuation stability and physical extra dimension OPEN. **Novelty NOT CLAIMED.**

## Starting from the KK spectrum rather than chosen inverse powers

Consider a real, neutral 5D scalar of constant proper mass `m≥0` with standard positive kinetic term and periodic `w~w+2π` boundary conditions on a circle of physical radius `b>0`. Its Jordan-frame KK squared masses are `m²+n²/b²`, `n∈Z`.

The formally divergent one-loop Jordan-frame vacuum energy is `1/2 sum_n integral d⁴p/(2π)⁴ log[p²+m²+n²/b²]`. Use Schwinger proper time and subtract its zero-winding Poisson-resummed term (the local bulk cosmological-constant counterterm), retaining only nonzero winding sectors. Poisson summation and the standard Bessel integral give the **finite**, explicitly radius-dependent circle term

```text
V_J,Cas(b;m) = - m^(5/2)/(8 π⁴ b^(3/2))
                * sum_(n=1)^∞ K_(5/2)(2π n m b)/n^(5/2)
             = -3/(64 π⁶ b⁴) sum_(n=1)^∞ e^(-z_n) P(z_n)/n⁵,
z_n=2π n m b, P(z)=1+z+z²/3.
```

Here the massless expression is obtained by continuous limit at `m=0`; it equals `-3 ζ(5)/(64π⁶b⁴)`. In the 4D Einstein-frame metric `g_E=b g_J`, the potential is `V_E,Cas=V_J,Cas/b²`, so

```text
V_E,Cas(b;m) = -B b^(-6) S(mb),
B=3/(64π⁶)>0,
S(mb)=sum_(n≥1) e^(-z_n) P(z_n)/n⁵.
```

These expressions are for **one real periodic scalar** in the chosen flat-circle one-loop prescription. Every additional real periodic scalar with nonnegative multiplicity contributes with the same negative sign. This fixed spectrum is not a freely fitted sum of independent inverse powers. Arbitrary finite local bulk contributions are absorbed into the renormalized `Lambda`; curvature- or radius-dependent localized counterterms are outside the model.

## Theorem: massive periodic bosons cannot stabilize nonnegative vacuum energy in the winding model

Let `b>0`, `A>0` (positive canonical scalar winding), `Lambda∈R`, finitely many scalar masses `m_j≥0`, and positive degeneracies `d_j>0`. Define the 4D Einstein-frame zero-mode potential

```text
V(b)=Lambda/b+A/b³
     - sum_j [B_j/b⁶ * S_j(b)],
B_j=3d_j/(64π⁶)>0,
S_j(b)=sum_(n≥1) e^(-z_jn) P(z_jn)/n⁵,
z_jn=2π n m_j b.
```

**Claim:** At every positive-radius critical point `V'(b)=0` with `V(b)≥0`, the curvature `V''(b)<0`. Therefore the canonically normalized radion `phi=sqrt(3/2)log b` has **negative squared mass** at that point. No stable radion Minkowski or dS minimum exists in this precisely specified class.

**Proof.** Introduce `U(b)=sum_j B_j S_j(b)` and derivatives with respect to `b`. Differentiating `V=Lambda/b+A/b³-U/b⁶`, eliminating `Lambda` using `V'=0`, gives

```text
Lambda = -3A/b² + 6U/b⁵ - U'/b⁴,
V_* = -2A/b³ + 5U/b⁶ - U'/b⁵,
V''_* = 6A/b⁵ - 30U/b⁸ + 10U'/b⁷ - U''/b⁶.
```

Nonnegative `V_*` implies `2A/b³ ≤ 5U/b⁶-U'/b⁵`. Substitution yields

```text
V''_* ≤ -[15U - 7bU' + b²U'']/b⁸.
```

For a single spectral summand `h(z)=exp(-z)P(z)`, `z=2πnmb≥0`,

```text
15h(z)-7z h'(z)+z²h''(z)
  = exp(-z) [45+45z+21z²+6z³+z⁴]/3 > 0.
```

Every coefficient of the quartic is strictly positive. The `n` sum and any finite positive degeneracy sum preserve strict positivity, proving `V''_*<0`. At `m=0` the formula has a smooth limit with quartic value 15, recovering the exact massless `b^(-6)` case of [PR #341](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/341).

For each fixed positive `b`, the nonzero-winding spectral series and its needed derivatives converge absolutely, justifying termwise differentiation. At `m=0`, derivatives reduce to convergent zeta sums. No finite parameter mesh is used as the proof.

**Scope:** The result forbids only nonnegative-vacuum **positive radion curvature** for the *specified boson-only one-loop potential with winding and Lambda*. It does not forbid healthy minima once fermionic, twisted, gauge, nonminimal, brane-localized or other nonmonomial sources enter. It does not claim a complete quantum 5D effective action or physical light KK spectrum.

## Reproduction and independent tests

The no-dependency exact checker is `research/5d/massive_periodic_boson_casimir_no_ds_exact.py`. It derives the positive quartic through independent polynomial differentiation rules for `exp(-z)P(z)`, checks all five coefficients, and reproduces rational massless critical-point controls: unstable Minkowski, unstable dS, and a positive-curvature zero-mode *AdS* radion minimum. The proof applies to all real `z≥0` because positivity is coefficientwise, not because of finitely many test points.

```bash
python3 -B research/5d/massive_periodic_boson_casimir_no_ds_exact.py
```

**Primary prior work:** Biswas, Juberi and Kamal, *Quality Time in Extra Dimensions: Axion Quality and Radion Cosmology*, arXiv:2611.12765v1 (2026-11-09), https://arxiv.org/abs/2611.12765. Its Appendix B derives the massive neutral-scalar periodic Casimir determinant and its main text considers mixed neutral spectra which can exhibit Minkowski/dS minima. This note is an independent exact certificate for a narrower boson-only obstruction; novelty and superiority to that published analysis are **not established**.

**NEXT PHYSICAL BLOCKER:** Choose field content and boundary conditions independently of the desired solution, derive the *complete* mixed-sign spectral potential, identify any controlled 4D radion minimum with vacuum energy and KK hierarchy, then audit all kinetic modes and compare an observable against matched 4D Chronos. No proof of physical fifth-dimensional necessity exists.
