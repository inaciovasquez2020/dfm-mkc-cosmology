# ACT DR6 Source-Recovery Gate — 2026-10-15

## Status

**SOURCE DISCOVERY: MERGED.**
**PROMOTED, LIKELIHOOD-BOUND 135-SLOT BASELINE: NOT ESTABLISHED.**
**HISTORICAL 135-SLOT NUMERIC CANDIDATE: EXISTS; NOT PROMOTED.**
**REPRODUCIBLE ACT-LITE LIKELIHOOD RUN FOR THE CURRENT COMPARISON: NOT ESTABLISHED.**
**DFM-MKC EMPIRICAL CLAIM: NOT ESTABLISHED BY THIS RECEIPT.**

Merged source-recovery PR: https://github.com/inaciovasquez2020/dfm-mkc-cosmology/pull/317  
Merge commit: `eb8758ffc04d3e08a9f8d3301f4c31447ad1e58f`

## Official source candidates

- ACT DR6 CMB-only likelihood code: https://github.com/ACTCollaboration/DR6-ACT-lite
- ACT DR6 parameter/configuration repository: https://github.com/ACTCollaboration/ACT-DR6-parameters
- NASA LAMBDA DR6.02 SACC product information: https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_pspipe_sacc_info.html
- NASA LAMBDA DR6.02 product landing page: https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/index.html
- ACT DR6 paper: https://arxiv.org/abs/2503.14452

Source identification is not equivalent to verified acquisition of the exact payload used by a particular run. The ACT-lite repository explicitly distinguishes its simulated test dataset from the installed official likelihood data.

## Deeper source audit — 2026-10-15

The repository already contains a historical candidate and partial audit dated 2026-06-17:

- Candidate source file: `dr6_lcdm_best_fits/cmb.dat`
- Recorded parent payload SHA-256: `f63d900ac986bd5b5bd3f523556e42b7b4743c13a81547697675432590514992`
- Recorded `cmb.dat` SHA-256: `8a83622627c48b925f01c8f14347f7a6877f11e87a4a7cedd086366af96f82b1`
- Candidate shape: `[135]`, split into 45 TT-like, 45 TE-like, and 45 EE-like rows.
- Historical materialization matched stored sample outputs within `9.094947017729282e-13`; its raw-byte vector digest did not match the original candidate digest. A canonical decimal digest was recorded, but the candidate was not promoted.
- Historical internal quadratic-form value: `153.61808801048306`. This number is not a verified ACT-lite likelihood result or a DFM-MKC comparison.

The official ACT-lite likelihood source provides a more precise convention for this 135-row CMB-only route. Its `chi_square` implementation obtains `Cl` with `ell_factor=True`, applies the SACC bandpower windows, scales spectra by `A_act^{-2}`, and applies `P_act^{-1}` for each E-mode leg. Its code exposes calibration and polarization-efficiency nuisance parameters. Therefore the earlier generic “foreground comparison” blocker is too broad when applied to this specific ACT-lite route: the operative unresolved binding is the exact ACT-lite configuration, nuisance-parameter point or fit rule, source-data provenance, and proof that the chosen `cmb.dat` spectrum is the intended baseline for this likelihood. The multifrequency MFLike route is a different likelihood path and must not be silently substituted for the 135-row CMB-only route.

This is a source-code convention audit only. It does not rerun ACT-lite, authenticate a fresh download, or promote the candidate.

## CI record for source-recovery PR #317

- Main CI workflow run `38665908756`: completed successfully.
- Cosmology check workflow run `38665908812`: completed successfully.
- External status lock `38665908766`: completed successfully.
- Lean CI was disabled; its green status is not evidence of a Lean build.

## Required execution gate

Before any ACT comparison or cosmology claim is upgraded, bind and verify:

1. Exact official SACC data payload and SHA-256, plus the exact likelihood code commit/release.
2. The baseline `cmb.dat` source and digest, with a justification that it is the intended spectrum for the ACT-lite comparison.
3. Frozen cosmological parameters and the ACT-lite nuisance-parameter point or explicit fit/marginalization rule for `A_act` and `P_act`.
4. Exact 135-slot mapping, ordering, units, D-ell convention, and SACC window projection.
5. Finite-value, shape, and ordering checks for the actual materialized vector.
6. Reproducible ACT-lite likelihood output and digest, distinguishing it from the historical internal quadratic-form number.
7. A separately materialized DFM-MKC prediction vector under the same row mapping and projection convention.
8. A comparison protocol and claim-level result with explicit uncertainty and nonclaims.

## Nonclaims

This receipt does not establish that a trusted baseline vector has been promoted, that ACT-lite has been rerun with a frozen configuration, that the historical internal quadratic form is an official likelihood result, or that DFM-MKC is supported or ruled out by ACT DR6.
