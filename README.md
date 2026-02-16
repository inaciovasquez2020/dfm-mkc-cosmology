# dfm-mkc-cosmology

Includes executable checks and CI-verified consistency under bounded locality and capacity.

This repository contains the research implementation and cosmological models associated with the DFM-MKC framework. It is an indexed component of the Vasquez research ecosystem.
Cosmology statement

The core cosmological claim supported by this repository is stated independently of the implementation details:

docs/COSMOLOGY_STATEMENT.md

Readers interested in the physics result should start there. This repository exists to make that claim checkable and reproducible.

## Overview
The `dfm-mkc-cosmology` module provides specialized analysis and data structures for cosmological applications within the Universal Reference Frame (URF) context.

## Canonical Registry
This repository is a registered module of the Vasquez Index. Stable references, archival DOIs, and reproducibility links are maintained at:
* [Vasquez Index Dashboard](https://inaciovasquez2020.github.io/vasquez-index/dashboard.html)

## Repository Status
* **Repository Handle:** inaciovasquez2020/dfm-mkc-cosmology
* **Stability:** Refer to the Vasquez Index for the latest stable DOI and version history.
* **Infrastructure:** [scientific-infrastructure](https://github.com/inaciovasquez2020/scientific-infrastructure)

## References
- Unified framework context: https://inaciovasquez2020.github.io
- Project index: https://inaciovasquez2020.github.io/vasquez-index/

---

## Technical Notes
* **Integration:** This module is designed to interface with `urf-core` and `urf-axioms`.
* **Reproducibility:** To ensure consistent computational results, utilize the environment configurations defined in the `scientific-infrastructure` module.
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

## Quickstart (60 seconds)

```bash
./scripts/cosmology check
```

## Status

![cosmology-check](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/actions/workflows/cosmology-check.yml/badge.svg)
