# ACT DR6 Source-Recovery Gate — 2026-10-15

## Status

**DOCUMENTATION/SOURCE DISCOVERY: MERGED.**
**CI FOR SOURCE-RECOVERY PR #317: PASS.**
**OFFICIAL 135-SLOT THEORY VECTOR: NOT MATERIALIZED.**
**ACT LIKELIHOOD COMPARISON: NOT RUN.**
**DFM-MKC EMPIRICAL CLAIM: NOT ESTABLISHED BY THIS RECEIPT.**

Merged PR: https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/317
Merge commit: `eb8758ffc04d3e08a9f8d3301f4c31447ad1e58f`

## Official source candidates recorded

- ACT DR6 CMB-only likelihood code: https://github.com/ACTCollaboration/DR6-ACT-lite
- ACT DR6 parameter/configuration repository: https://github.com/ACTCollaboration/ACT-DR6-parameters
- NASA LAMBDA DR6.02 SACC product information: https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_pspipe_sacc_info.html
- NASA LAMBDA DR6.02 product landing page: https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/index.html
- ACT DR6 paper: https://arxiv.org/abs/2503.14452

Source identification is not equivalent to verified payload acquisition. In particular, any bundled test payload must be checked for whether it is simulated or official.

## CI record

PR #317 head: `c7fb3a782b4781847631d6279a331e0644d34470`
Merge commit: `eb8758ffc04d3e08a9f8d3301f4c31447ad1e58f`

Recorded checks:
- Main CI workflow run `38665908756`: completed successfully.
- Cosmology check workflow run `38665908812`: completed successfully.
- External status lock `38665908766`: completed successfully.
- Lean CI is disabled; its green status is not evidence of a Lean build.

## Required execution gate

Before any ACT comparison or cosmology claim is upgraded, create a receipt binding all of the following:

1. Exact official data product and downloaded payload SHA-256.
2. Likelihood code commit/release and configuration provenance.
3. Trusted baseline parameter vector and its provenance.
4. Exact 135-slot mapping, ordering, units, and conventions.
5. Finite-value, shape, and ordering checks.
6. Reproducible likelihood run output and digest.
7. Comparison protocol and a claim-level result with explicit uncertainty and nonclaims.

## Nonclaims

This source-recovery status does not establish that the baseline vector has been reconstructed, that the likelihood was evaluated, or that DFM-MKC is supported or ruled out by ACT DR6.
