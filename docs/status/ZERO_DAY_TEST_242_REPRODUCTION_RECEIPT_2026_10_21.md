# Zero Day Test 242 — Independent Numerical Reproduction Receipt

Date: 2026-10-21

Status: **Conditional — numerical reproduction and finite-range endpoint scaling supported.**

## Scope

The independent script `tools/reproduce_zero_day_test_242.py` implements the proposed six-variable closed-FLRW system in `docs/status/ZERO_DAY_TEST_242_NUMERICAL_ROBUSTNESS.tex`. The JSON receipt is `artifacts/status/zero_day_test_242_reproduction_2026_10_21.json`.

The initial values are internally consistent:
[
\rho_0=0.5(0)^2+U(1)+0.1+0.1=0.95,\qquad
a_0=\sqrt{3/(8\pi\rho_0)}=0.3544695181296627\ldots
]

## Event-time comparison

| Method | Event | Previously reported | Reproduced | Absolute difference |
|---|---|---:|---:|---:|
| DOP853, rtol (10^{-10}) | Maximum expansion | 397.749693853 | 397.749693737 | (1.16\times10^{-7}) |
| DOP853, rtol (10^{-10}) | Contracting to (a=0.1) | 792.771209639 | 792.771207927 | (1.71\times10^{-6}) |
| DOP853, rtol (10^{-12}) | Maximum expansion | 397.749689824 | 397.749689992 | (1.68\times10^{-7}) |
| DOP853, rtol (10^{-12}) | Contracting to (a=0.1) | 792.771145029 | 792.771147486 | (2.46\times10^{-6}) |
| RK45, rtol (10^{-10}) | Maximum expansion | 397.750427766 | 397.750427667 | (9.90\times10^{-8}) |
| RK45, rtol (10^{-10}) | Contracting to (a=0.1) | 792.782148826 | 792.782147360 | (1.47\times10^{-6}) |

The reproduction used `atol = 0.01 × rtol`. The original note does not preserve the original absolute tolerances, so this is a close independent reproduction, not an exact replay of the original runs.

## Endpoint study

After reaching the contracting branch at (a=0.1), the script integrates independently using (x=\ln a) and enforces the Friedmann constraint algebraically to determine the negative contracting value of (H). It samples the Kretschmann scalar
[
K=12\left[(\dot H+H^2)^2+\left(H^2+\frac{1}{a^2}\right)^2\right]
]
at smaller scale factors.

| (a) | Time | (K) | (K a^{12}) |
|---:|---:|---:|---:|
| 0.1 | 792.7712079273 | (2.99244\times10^{23}) | (2.99244\times10^{11}) |
| 0.05 | 792.7712090248 | (1.22570\times10^{27}) | (2.99244\times10^{11}) |
| 0.02 | 792.7712091716 | (7.30577\times10^{31}) | (2.99244\times10^{11}) |
| 0.01 | 792.7712091804 | (2.99244\times10^{35}) | (2.99244\times10^{11}) |

Across these samples, (K a^{12}) varies by about (2.5\times10^{-9}) relative to its value at (a=0.01). Tightening the log-scale integration tolerance from (10^{-11}) to (10^{-12}) changes (K) at (a=0.01) by about (5.1\times10^{-12}) relatively. The constraint-reduced formulation has a normalized Friedmann residual near floating-point precision; absolute residuals alone become misleading because the terms are extremely large.

## Result and boundary

- **Reproduced:** the reported turnaround and (a=0.1) event times to close numerical tolerance under the stated equations.
- **Supported over the sampled range:** (K\propto a^{-12}) during the final contracting segment, with a rapidly converging finite endpoint time.
- **Not proved:** a mathematical curvature-singularity classification, geodesic incompleteness, or any derivation of this closed-FLRW system from the DFM–MKC action.
- **Not claimed:** empirical cosmological validation or rejection of \(\Lambda\)CDM.

The result is conditional on the assumed equations, potential, initial data, units, and numerical formulation. The finite-range scaling is evidence for divergence under this model, not a substitute for an analytic endpoint argument.

## Reproduction

Run from the repository root with Python, NumPy, and SciPy installed:

`python3 tools/reproduce_zero_day_test_242.py`

The committed JSON is a concise receipt of the run. The script prints a fuller JSON record to stdout, including event states and normalized endpoint residuals.
