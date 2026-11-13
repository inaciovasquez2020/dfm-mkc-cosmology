# Single-power Casimir cannot stabilize a Minkowski/de Sitter circle with positive scalar winding

**2026-11-13. STATUS:** PROVED for the specified 4D Einstein-frame zero-mode effective potential; independent exact-rational tests COMPUTATION_PASS once CI passes; Lean NOT_RUN; full 5D quantum/mixed KK spectrum NOT_RUN; novel contribution NOT CLAIMED. This reproduces a known restriction in radion stabilization.

## Model and theorem

For a 5D Einstein circle with physical radius `b>0`, a fixed positive canonical scalar winding energy coefficient `A>0`, bulk vacuum energy `Lambda`, and one additional Casimir contribution following a single inverse power, consider the **explicit** four-dimensional Einstein-frame effective potential

```text
V(b)=Lambda/b + A/b³ + C/b^p,
p>3, A>0, Lambda,C arbitrary real.
```

For the massless five-dimensional circle Casimir scaling, `p=6`. A positive canonical radion has `phi=sqrt(3/2) log b`; at any critical point the sign of its physical zero-mode mass squared is the sign of `V''(b)`, since `(db/dphi)^2=2b²/3>0`.

**Theorem:** For every `p>3`, **no critical radius** `b>0` has both `V(b)>=0` and `V''(b)>0`. Stronger: every such nonnegative-energy critical point has

```text
V''(b) <= -2(p-3) A/b^5 < 0.
```

**Proof:** At `V'(b)=0`,

```text
Lambda = -3A/b² - p C/b^(p-1),
V_* = -2 A/b³ - (p-1) C/b^p,
V''_* = 6 A/b^5 + p(p-1) C/b^(p+2).
```

If `V_*>=0`, then `C<=-2A b^(p-3)/(p-1)`. Substitute into the curvature to get `V''_*<=6A/b^5 - 2p A/b^5 = -2(p-3)A/b^5<0`. Therefore stable radion Minkowski/dS stationary points **cannot** arise from this three-monomial potential. This result is not a theorem about all Casimir spectra or all five-dimensional actions.

In the standard massless case `p=6`, three exact rational witnesses at `A=b=1` show the boundaries:

| C | Lambda (from stationarity) | V_* | V''_* | Interpretation |
|---|---|---|---|---|
| -2/5 | -3/5 | 0 | -6 | Minkowski critical point, unstable radion |
| -1/2 | 0 | +1/2 | -9 | dS critical point, unstable radion |
| -1/10 | -12/5 | -3/2 | +3 | stable *radion* minimum, but AdS |

The last row establishes **only zero-mode radion curvature**, not full KK perturbation stability.

## Exact adversarial two-power boundary

The single-power hypothesis is essential. As a **purely algebraic effective-potential counterexample**, consider

```text
V(b) = Lambda/b + A/b³ + C/b⁶ + D/b⁷,
Lambda=-1/10, A=1, C=-2, D=13/10, b*=1.
```

A direct exact-fraction calculation gives `V(b*)=1/5>0`, `V'(b*)=0`, and `V''(b*)=3/5>0`. Thus the four-dimensional canonical radion has positive mass curvature and de Sitter vacuum energy at this stationary point. **This is NOT a constructed five-dimensional quantum field theory:** the two coefficients/powers have not been derived from any consistent spectrum, boundary conditions, renormalization scheme or UV completion. It illustrates why the no-go is a theorem about one inverse-power correction and not a prohibition on all nonmonomial Casimir corrections. The independent test is included in the same exact verifier.

## Consequences for the active 5D program

1. **Winding breaks the scaling degeneracy** of the homogeneous electric Maxwell family in PR #340 because the winding term scales as `1/b` in the 5D Jordan homogeneous Lagrangian, while that family's other terms all scale linearly with `b`. Breaking the degeneracy is not itself evidence of a stable accelerating vacuum.
2. **One massless Casimir inverse-power contribution cannot fix the dS problem.** A more elaborate radius dependence, e.g. a mass-dependent Casimir spectral function with independently specified boundary conditions and field content, is necessary for this route; other alternatives such as warping or changing gravity remain logically possible.
3. **A radius-only effective potential is not enough** for physical 5D: radion and mixed scalar/graviphoton modes require a full fluctuation and energy-condition audit, and Chronos remains an observationally distinctness problem.

## Primary literature and novelty

Biswas, Juberi and Kamal, *Quality Time in Extra Dimensions: Axion Quality and Radion Cosmology*, submitted November 9, 2026, https://arxiv.org/abs/2611.12765, explicitly discuss winding stabilization, its AdS minimum with negative bulk vacuum energy, and the insufficiency of a purely massless Casimir spectrum for a stable Minkowski/dS minimum. Their paper includes further massive neutral field spectra that can admit dS extrema. The current note is a **minimal self-contained algebraic certificate of a known obstruction**, not a claim of independent novelty.

Related published examples of Casimir-based radion stabilization and phenomenological problems include Cui and Ning, *Casimir energy stabilization of Standard Model landscape in dark dimension*, JHEP 02 (2026) 156, https://doi.org/10.1007/JHEP02(2026)156.

## Exact audit

Run with Python 3 standard library, no package downloads:

```bash
python3 -B research/5d/single_power_casimir_no_ds_exact.py
```

The script checks the identities and contradictory critical-point inequalities in 261 rational adversarial parameter combinations across integer exponents 4 through 32, tests dS, Minkowski and AdS witnesses, and verifies the canonical radion sign relation. Finite parameter tests are **supporting evidence only**; the symbolic inequality above proves the general result for every real `p>3`.

**STOP BOUNDARY:** Physical/quantum spectral derivation of a multi-scale Casimir potential, existence of stable dS with healthy 5D kinetic terms, a scale separation, and predictive Chronos 5D discrimination remain **OPEN**. Do not merge this note into a claim of a complete 5D spacetime theory.
