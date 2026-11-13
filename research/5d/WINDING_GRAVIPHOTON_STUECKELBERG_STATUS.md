# Winding scalar–graviphoton mixing: exact 5D-to-4D zero-mode reduction

**Date:** 2026-11-13. **RESULT:** PROVED from the explicitly specified zero-mode metric ansatz and classical 5D action, with rational 5×5 inverse-metric tests. **Scope:** ZERO MODES ONLY. **Full 5D one-loop determinant, nonzero KK mixing, ghosts and hyperbolicity:** OPEN. **Lean:** NOT_RUN. **Novelty:** NONE—standard Kaluza–Klein and Stückelberg mechanism, also explicitly discussed in Biswas–Juberi–Kamal (2026), §5.2.3.

## Model, gauge invariance, and metric identity

Work with fixed circle coordinate `w ~ w+2π`, positive radius `b(x)`, a Jordan-frame metric `gJ`, graviphoton `B_mu(x)`, and a compact scalar `chi ~ chi+2π f` with integer winding `q=nf≠0`:

```text
S5 = ∫d⁵x sqrt(-g5) [R5/2 - Lambda5 - (∂chi)²/4],
ds5² = gJ_munu dxmu dxnu + b²(dw+B_mu dxmu)²,
chi = q*w + theta(x)  mod 2π f.
```

The exact block inverse and determinant are

```text
g5^munu = gJ^munu,
g5^mu w = -B^mu,
g5^ww   = b^(-2)+B_mu B^mu,
sqrt(-g5) = b sqrt(-gJ).
```

Therefore

```text
(∂chi)²_5 = (dtheta-qB)²_gJ + q²/b².
```

The inverse-metric identity is checked directly for eight exact nontrivial 5×5 rational metrics, including Lorentzian signature, and 64 exact combined tests of metric, winding and scalar-gradient data. It also follows algebraically for arbitrary nondegenerate `gJ` by Schur complements; the finite checks are adversarial sanity tests, not the proof.

The five-dimensional coordinate transformation `w' = w-lambda(x)` induces `B'=B+d lambda`, `theta'=theta+q lambda`; therefore `dtheta-qB` is gauge invariant. A globally single-valued `lambda` gives an ordinary connected gauge transformation. One can use unitary gauge `theta=0` locally for `q≠0`, but this is not justification for deleting the longitudinal polarization: the vector acquires it.

## Reduced action and mass

Using the standard Einstein–Hilbert circle reduction up to a total derivative, and suppressing the positive overall circle coordinate factor `2π`, the relevant **Jordan-frame** terms are

```text
L4,J/sqrt(-gJ) = b R_J/2
  - b³ F_B,mn F_B^mn/8
  - b(dtheta-qB)²_gJ/4
  - Lambda5*b - q²/(4b) + (radion derivative/total-derivative terms).
```

After the four-dimensional Einstein-frame Weyl change `gE=b*gJ`, the two quadratic vector-sector terms become

```text
L4,E/sqrt(-gE) contains
  - b³ F_B²_gE/8 - (dtheta-qB)²_gE/4,
V_E,winding(b)=q²/(4b³).
```

At fixed `b`, the canonical vector normalization is `Z_B=b³/2` in `-Z_B F_B²/4`, and the Stückelberg vector mass term is `-q² B²/4` in unitary gauge. Thus the physical zero-mode graviphoton mass is

```text
m_B² = (q²/2)/(b³/2) = q²/b³ = 4 A/b³,
A=q²/4.
```

The classical zero-mode `theta` is **eaten by the graviphoton**: a nonzero winding yields one massive 4D vector with three physical polarizations rather than an independent massless 4D scalar plus a massless 4D vector. There is still a physical radion degree of freedom. This counting does not calculate a quantum determinant or show a fully stable background.

## Application to the truncated Casimir witness in PR #343

That constructed effective potential uses `b*=1`, `A=B_C/2`, where `B_C=3/(64π⁶)`, and its certified vacuum bounds are `9/10<V(1)/B_C<91/100`. With `H_E²=V(1)/3`, the **classical zero-mode** graviphoton-to-Hubble ratio is

```text
m_B²/H_E² = (4A)/(V/3) = 6/(V(1)/B_C).
600/91 < m_B²/H_E² < 20/3,
5/2 < m_B/H_E < 13/5.
```

This gives a graviphoton heavier than Hubble by a factor between 2.5 and 2.6, **not a parametrically decoupled vector**. The radion is likewise Hubble-scale. The positive spectator KK/H ratio from PR #343 is irrelevant to whether these light zero modes can be integrated out.

**Crucial limitation:** The coupled winding/graviphoton **nonzero KK levels** and the graviton-induced fluctuation operator are not derived here. The background-covariant one-loop spectrum is not equivalent to simply counting a free independent periodic scalar. In particular, the extra-free-boson destabilization check in PR #343 is a *sensitivity counterexample*, **not** the computed physical determinant of the winding scalar. The complete one-loop effective potential remains OPEN and cannot currently be certified as a physical dS vacuum.

## Reproduction

```bash
python3 -B research/5d/winding_graviphoton_stueckelberg_exact.py
```

Runs with Python 3 standard library and no downloads. Assertions disabled means INCOMPLETE, not PASS. Dedicated exact-HEAD CI required; no Mac state inspected. All source changes additive and the PR should remain draft pending tests and full-scoped review.

**Prior art:** Biswas, Juberi and Kamal, *Quality Time in Extra Dimensions: Axion Quality and Radion Cosmology*, arXiv:2611.12765v1, https://arxiv.org/abs/2611.12765, §5.2.3 explicitly exhibits winding scalar/graviphoton Stückelberg coupling. General canonical Kaluza–Klein graviphoton reduction is standard.

**NEXT MISSING OBJECT:** Build and diagonalize the full gauge-fixed 5D quadratic fluctuation operator about the specified background, including the graviton, winding scalar, nonzero Fourier levels and gauge ghosts. Derive the renormalized determinant and recheck the vacuum rather than substituting an assumed free scalar. **PHYSICAL_5D := OPEN.**
