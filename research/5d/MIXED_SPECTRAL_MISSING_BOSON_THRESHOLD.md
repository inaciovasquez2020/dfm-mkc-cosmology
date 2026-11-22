# Exact conditional missing-boson stability threshold

Status: **PROVED within the specified deformation of the truncated one-loop radion potential**, with exact rational infinite-series certificate. Full mixed gauge-fixed five-dimensional spectral determinant: **OPEN**. No Lean theorem, physical 5D stability, or novelty claim.

Baseline is `research/5d/MIXED_PERIODIC_SPECTRAL_DS_STATUS.md` on `main` commit `d4a8bfb768871f43ad061eded3f7fd30c1ef171b`. It prescribes

`V_0(b)=Lambda/b + (B/2)/b^3 + B[4S(mb)-zeta(5)]/b^6`, with `2*pi*m=5`, stationary at `b=1`, and rigorously `9/10 < V_0(1)/B < 91/100`, `5/4 < V_0''(1)/B < 13/10`.

Consider **a controlled mathematical perturbation** `Delta V_Cas(b)=-alpha B zeta(5)/b^6`, with `alpha>=0`. This is an additional independent free massless periodic real-boson determinant multiplied by a formal weight `alpha`; arbitrary fractional alpha is a sensitivity parameter, **not** a claim that a fractional physical particle exists. Keep the winding coefficient, fermion mass/content, and stationary radius fixed. Retune only `Lambda` by `Delta Lambda=6 alpha B zeta(5)` to retain `V_alpha'(1)=0`. Direct derivatives give

- `Delta V_alpha(1)/B=5 alpha zeta(5)`, so `V_alpha(1)>0`;
- `Delta V_alpha''(1)/B=-30 alpha zeta(5)`;
- exactly one curvature sign change at `alpha_crit=(V_0''(1)/B)/(30 zeta(5))`.

The exact rational infinite-sum enclosure (Taylor bounds for `exp(-5)`, spectral remainder and integral-test bounds for `zeta(5)`) proves

`1/25 < alpha_crit < 1/24`.

Thus the de Sitter stationary point retains positive radion curvature at `alpha=1/25`, but has negative curvature at `alpha=1/24`, **after retuning Lambda**. The canonical radion field is `sqrt(3/2) log b`, so the curvature sign is also the homogeneous canonical radion mass-squared sign at stationarity.

**Important scope:** This is not the graviphoton/winding-scalar/graviton/ghost spectral correction. Those fluctuate in a coupled system and need not have this spectral shape or multiplicity. The result is a precise adversarial threshold conditional on this deformation. It neither rules out nor proves a physically stable 5D de Sitter solution.

Reproduce from repository root, Python 3 standard library only:

```bash
python3 -B research/5d/mixed_spectral_missing_boson_threshold_exact.py
python3 -B tests/test_mixed_spectral_missing_boson_threshold.py
```

Validation: exact local execution PASS on 2026-11-22; repo-integrated CI NOT_RUN at publication; no Lean verification.
