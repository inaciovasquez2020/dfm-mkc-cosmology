# ACT DR6 baseline-source recovery — 2026-10-15

## Status

`OFFICIAL_LIKELIHOOD_SOURCE_LOCATED := TRUE`

`TRUSTED_135_SLOT_LCDM_THEORY_VECTOR := NOT_YET_MATERIALIZED`

`EMPIRICAL_COMPARISON := NOT_EXECUTED`

This update narrows the source-provenance blocker. Official ACT DR6 likelihood code and release documentation are publicly available. That is not equivalent to possessing a validated Lambda-CDM theory-prediction vector aligned to this repository's frozen 135-slot data ordering.

## Primary source candidates

- ACT Collaboration, DR6 CMB-only likelihood code: https://github.com/ACTCollaboration/DR6-ACT-lite
- ACT Collaboration, DR6 parameter/configuration repository: https://github.com/ACTCollaboration/ACT-DR6-parameters
- NASA LAMBDA, ACT DR6.02 Pspipe SACC product details: https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_pspipe_sacc_info.html
- NASA LAMBDA ACT DR6.02 release landing page: https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/index.html
- ACT DR6 power spectra and likelihoods paper: https://arxiv.org/abs/2503.14452

The ACT-lite README documents the official `cobaya-run yamls/act-lcdm.yaml` workflow and notes that its bundled test data can be simulated. Therefore the bundled file must not be treated as empirical data without verifying the installed official data payload and its digest.

## Required execution receipt

The remaining object is a reproducible theory-vector receipt, not a guessed array. It must bind:

1. The exact official data product and SHA-256 digest.
2. The exact ACT likelihood/configuration commit and software versions.
3. The frozen cosmological and nuisance parameter vector, with provenance for the selected baseline point.
4. The theory-code configuration and output.
5. The mapping from the generated theory outputs to every slot in the repository's 135-element ordering certificate.
6. Shape, finite-value, and row-order checks, plus a rerun digest.

Only after those bindings pass can the baseline vector be promoted from candidate to trusted input. A DFM-MKC prediction vector and out-of-sample likelihood comparison remain separate missing objects.

## Boundary

This source recovery does not prove DFM-MKC, reject Lambda-CDM, establish empirical validation, or execute a likelihood. It only identifies official upstream source candidates and states the exact reproducibility receipt still required.
