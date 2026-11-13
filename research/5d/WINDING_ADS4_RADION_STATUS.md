# Exact compact axion winding and radion stabilization in 5D

**Date:** 2026-11-13. **Status:** PROVED algebraically for the model below, COMPUTATION_PASS for a complete 5D tensor example; LEAN_VERIFIED = NOT_RUN; full KK fluctuation stability and physical 5D necessity = OPEN. **Novelty: not established; the mechanism is known in literature.**

## Action and globally defined winding

Work in units where the five-dimensional Einstein-Hilbert coefficient is 1/2, with signature `(-,+,+,+,+)`:

```text
S5 = ∫ d5x sqrt(-g5) [ R5/2 - Lambda5 - (dchi)^2/4 ].
```

Take `w ~ w+2π` and a compact scalar `chi ~ chi+2π f` of fixed nonzero integer winding `n`, `chi = q w (mod 2π f)`, `q=n f`. Thus `dchi=q dw` is globally well-defined even though the circle-valued scalar has no globally single-valued real lift.

The field equations in Einstein form are

```text
Ric5_AB = (2/3) Lambda5 g5_AB + (1/2)(dchi)_A (dchi)_B,
Box5 chi = 0
```

where the latter is interpreted for local lifts of the compact scalar.

Use `ds5²=ds4²+b²dw²` with constant `b>0` and maximally symmetric `Ric4_munu=3k g4_munu`. The 5D tensor equations reduce **exactly** to

```text
3k = 2 Lambda5/3,
0 = 2 Lambda5 b²/3 + q²/2.
```

Consequently, for nonzero winding `q`, a fixed-radius solution exists precisely for `Lambda5<0`, with

```text
b² = -3 q²/(4 Lambda5),  k = 2 Lambda5/9 < 0.
```

The resulting geometry is **AdS4 × S1**, not an accelerating or de Sitter four-dimensional solution. The scalar equation holds because the winding gradient and metric are constant in `w`.

## Reduced Einstein-frame radion test

Set `gE=b*gJ` and canonically normalized `phi=sqrt(3/2) log b`. With the conventional action normalization above, the reduced four-dimensional zero-mode action (after factoring out the positive circle volume) has potential

```text
V_E(b) = Lambda5/b + q²/(4 b³).
```

At the unique positive stationary point:

```text
V'_E(b)=-(4 Lambda5 b²+3q²)/(4b⁴)=0,
V_E(b*)=2 Lambda5/(3b*) < 0,
V''_E(b*)=-2 Lambda5/b*³ > 0,
m_phi²=(db/dphi)² V''_E(b*) = -4 Lambda5/(3b*) > 0.
```

The AdS radius squared in Einstein frame is `L_E²=-9b*/(2 Lambda5)`, so `m_phi² L_E²=6`. This establishes a **positive homogeneous zero-mode radion mass**. It does not establish the full scalar-vector-tensor/KK perturbation spectrum or nonlinear stability.

The potential derivative is strictly negative for every `b>0` when `Lambda5>=0` and `q!=0`. Therefore **this minimal action has no finite-radius dS or Minkowski stationary vacuum**. The constructive result and its obstruction both depend on the stated minimal action and positive scalar kinetic term; they are not universal 5D no-go theorems.

## Explicit rational tensor example

Choose `Lambda5=-3/2`, `q=1`, `b²=1/2`, and Poincaré AdS4 coordinates `(t,x,y,z)`, `z>0`:

```text
ds5² = 3/z²(-dt²+dx²+dy²+dz²) + (1/2)dw²,
chi = w (mod 2π).
```

The verifier constructs the 5×5 metric, its Levi-Civita connection and the full 25-component Ricci tensor. It confirms

```text
Ric5_AB = -g5_AB + (1/2)delta_Aw delta_Bw.
```

It also verifies the general symbolic potential/Einstein equations, positive radion mass, `m_phi² L_E²=6`, and the nonnegative-`Lambda5` obstruction.

**Reproduction:** `python3 -B research/5d/winding_ads4_stabilization_exact_audit.py` using already installed SymPy, or dedicated PR CI. Do not run with optimized Python. A timeout, missing SymPy, or failed assertion is INCOMPLETE/FAIL, not PASS. The original expanding-circle positive-`Lambda5` model [#335](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/335) remains an independent non-stabilized example; its hypotheses were not altered.

## Connection and external prior art

This is a source-pinned mathematical benchmark for the Chronos–Cosmology comparison, **not** a new theory and **not** a verified link from 5D geometry to the Chronos event-first generation law. The 4D metric and causal order of a reduced model can also be posited in a purely 4D theory. To identify a physical extra dimension, one needs a distinguishing observable under matched hypotheses, and the stabilization result is AdS rather than the observed cosmological acceleration.

A directly overlapping treatment of scalar winding and radion stabilization appeared in Biswas, Juberi, Kamal, *Quality Time in Extra Dimensions: Axion Quality and Radion Cosmology*, arXiv:2611.12765 (submitted 2026-11-09), especially its scalar-winding subsection: winding plus negative bulk vacuum energy gives an AdS minimum, and further Casimir contributions are needed in their Minkowski/dS examples. Earlier winding and Scherk–Schwarz compactification mechanisms also exist. **Novelty of this construction is not claimed.** Reference: https://arxiv.org/abs/2611.12765

**OPEN:** A coefficient- and assumption-preserving observable map to Chronos; physical/dS compactification with fully audited matter and fluctuations; KK tower spectral stability; predictive distinction from a 4D comparator; observational tests and Lean formalization.
