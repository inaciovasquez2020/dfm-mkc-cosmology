# Exact expanding-circle 5D Einstein example — research-only certificate

**Status:** mathematical construction with exact finite symbolic checks; **not** a viable cosmology or evidence for a physically necessary fifth dimension. No Lean proof or independent review is claimed.

## Hypotheses
Five-dimensional Lorentzian Einstein gravity with cosmological constant Λ5=6h², h>0; no other matter stress tensor. The fifth coordinate y is identified modulo 2π; all four spatial directions in the local metric share the same time-dependent scale factor. Consider

```
ds5² = -dt² + exp(2ht) (dx1² + dx2² + dx3² + dy²).
```

The coordinate-tensor certificate computes all components and checks `Ric5 = 4 h² g5` and `Scal5 = 20 h²`. Consequently the Einstein equation with Λ5=6h² holds. With the cosmological constant placed on the geometric side, material T_AB=0 obeys NEC, and the cosmological term vanishes on null contraction.

## Four-dimensional Einstein-frame reduction
The circle radius is `b(t)=exp(ht)`, the Jordan metric is `gJ=-dt²+exp(2ht) dᶋx²`, and the Einstein metric is `gE=b*gJ`. For `tau = (2/h)exp(ht/2)`,

```
b(tau)=(h*tau/2)²
aE(tau)=(h*tau/2)³
H_E=3/tau
phi=sqrt(3/2)*log(b)
V(phi)=6h²*exp(-sqrt(2/3)*phi)=24/tau².
```

With the reduced four-dimensional gravitational normalization fixed by the Einstein-frame action, `3H_E² = (1/2)phi_dot²+V`, `H_E_dot=-(1/2)phi_dot²`, and `phi_ddot+3H_E phi_dot+dV/dphi=0`. Thus `aE''(tau)>0` for `tau>0`.

## Failure boundary
The circle **is not stabilized**, since `b ∝ tau²`. In the chosen Einstein-frame normalization, `m1,E=b^(-3/2)`, so `m1,E/H_E=8/(3h³tau²)→0` at late times. This signals eventual failure of a zero-mode-only low-energy truncation. No full mode spectrum, perturbative stability, matter coupling, data comparison, or physical necessity claim is supplied.

## Reproduction and provenance
Run from the repository root, with its environment supplying SymPy:

```bash
python3 -B research/5d/expanding_circle_exact_audit.py
```

All checks are exact symbolic assertions. On an assertion failure or resource timeout, classify the run as **FAIL** or **INCOMPLETE**, never PASS. The starting mathematical model is the familiar flat-slicing higher-dimensional de Sitter metric, here with a compact coordinate. The research contribution is a reproducible scoped check, **not** a claim of novelty.

**Validation gate:** run the script and applicable repository CI at the exact PR HEAD, inspect the diff, and only merge after required checks complete. The local Mac working tree was not inspected. This addition is independent of the repository's cosmological data analyses.
