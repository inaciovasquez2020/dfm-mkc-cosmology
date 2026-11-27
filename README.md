## Status

![cosmology-check](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/actions/workflows/cosmology-check.yml/badge.svg)

# dfm-mkc-cosmology

Includes executable checks and CI-verified consistency under bounded locality and capacity.

This repository contains the research implementation and cosmological models associated with the DFM-MKC framework. It is an indexed component of the Vasquez research ecosystem.
Cosmology statement

The core cosmological claim supported by this repository is stated independently of the implementation details:

[Cosmology statement](docs/COSMOLOGY_STATEMENT.md)

Readers interested in the physics result should start there. This repository exists to make that claim checkable and reproducible.

## Overview
The `dfm-mkc-cosmology` module provides specialized analysis and data structures for cosmological applications within the Unified Rigidity Framework (URF) context.

## Canonical Registry
This repository is a registered module of the Vasquez Index. Stable references, archival DOIs, and reproducibility links are maintained at:
* [Vasquez Index Dashboard](https://inaciovasquez2020.github.io/vasquez-index/dashboard.html)

## Repository Status

## Current Status on Main

- Canonical repository status: `STATUS.md`
- Real-data integration state: `docs/REAL_DATA_INTEGRATION_READINESS.md`
- Next closure target: `docs/status/NEXT_CLOSURE_MOVE.md`

* **Repository Handle:** inaciovasquez2020/dfm-mkc-cosmology
* **Stability:** Refer to the Vasquez Index for the latest stable DOI and version history.

## References
- Unified framework context: https://inaciovasquez2020.github.io
- Project index: https://inaciovasquez2020.github.io/vasquez-index/

---

## Technical Notes
* **Integration:** This module is designed to interface with `urf-core` and `urf-axioms`.
* **Reproducibility:** See [Python dependencies](requirements.txt) and the [cosmology CI workflow](.github/workflows/cosmology-check.yml).
* **Access:** This is a public repository supporting open science and reproducibility.

## Citation
If you use this research or implementation in your work, please cite it as follows:

```bibtex
@manual{Vasquez_DFM_MKC_2026,
  author = {Vasquez, Inacio F.},
  title  = {dfm-mkc-cosmology: Cosmological Implementation and Analysis},
  year   = {2026},
  url    = {[https://github.com/inaciovasquez2020/dfm-mkc-cosmology](https://github.com/inaciovasquez2020/dfm-mkc-cosmology)}
}

## Quickstart

Run the repository integrity check from the checkout root. It checks required files, tracked generated artifacts, and script permissions.

```bash
./scripts/cosmology check
```

For the separate [expanding-circle model audit](research/5d/EXPANDING_CIRCLE_STATUS.md), install SymPy in your Python environment and run:

```bash
python3 research/5d/expanding_circle_exact_audit.py
```

The exact model has an evolving circle radius. Radion stabilization and the coefficient match to [Chronos](https://github.com/inaciovasquez2020/chronos-urf-rr) remain **OPEN**.

## External status

This repository is governed by [`docs/status/EXTERNAL_STATUS_LOCK.md`](docs/status/EXTERNAL_STATUS_LOCK.md). Build success, CI success, dashboards, ledgers, axioms, admits, `sorry`, or placeholder witnesses do not constitute theorem-level closure.

## Cross-domain information recovery — 2026-11-27 UTC

Three scoped mathematical connections: 52 distinct audited Lean theorem declarations across two standalone certificates (41 + 11; the original 33 are counted once).

- [Chronos–Biological Friction, BFF #116](https://github.com/inaciovasquez2020/biological-friction-framework/blob/799b41b4692c71589587cba037f26f0ad4bff7fb/proofs/hidden-dissipation/receipt/HiddenDissipation.lean): merged; 33/33 audited declarations, fresh Linux build PASS. In finite cyclic Markov models with the stated stationary and path-gauge observations, different entropy production can be indistinguishable; sharp absolute-error minimax equals half maximal dissipation in the bounded current family. `BFF.HiddenDissipation.ring_observation_minimax`.
- [Biology–Cosmology, BFF #117](https://github.com/inaciovasquez2020/biological-friction-framework/blob/c5c8b2f24a0d4de57c764c161ab29c3689bec62f/proofs/hidden-dissipation/receipt/HiddenDissipation.lean): merged; eight additional declarations, cumulative 41/41 audit and fresh Linux build PASS. One diagonal generator-square observable with the specified stationary observations identifies squared current and entropy production; the restricted cosmological mode coefficient is invertible for known positive radius and nonzero mode. `BFF.HiddenDissipation.entropy_identified_by_curvature`, `BFF.HiddenDissipation.mode_identifiable`.
- [Cosmology–Chronos, #1392 pinned PR revision](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/2ed7df1497824343fce34924501d42a220c3006f/research/certificates/cosmology_causal_projection/receipt/CausalProjection.lean): Mac 11/11 and dedicated Linux Lean CI PASS; wider integration CI pending at this dated checkpoint. Identical projected coordinates can conceal different causal comparability; strip-area algebra and optimal pointwise decision loss are verified. `Chronos.CosmologyBridge.no_perfect_visible_decoder`, `Chronos.CosmologyBridge.strip_optimal_decoder`.

Only permitted standard Lean axioms were audited. These are mathematical comparisons, not physical equivalence or software dependencies. Full semigroup derivative, covariant action/Fourier derivation, continuum measure formalization, empirical validation, physical 5D detection and independent novelty remain OPEN. No repository-wide status promotion.
