# GWTC-5.0 polarization reproduction — evidence and open boundary

**Date:** 2026-11-05  
**Type:** Bounded external-data reproducibility note (not a new DFM-MKC result)  
**Status:** `SUMMARY_REPRODUCTION_REPORTED_PASS; ORIGINAL_INFERENCE_NOT_REPRODUCED; X_FIELD_NOT_ESTABLISHED`

## Purpose and provenance

This note records a bounded check of published gravitational-wave polarization artifacts as potential external evidence for an additional property of spacetime, denoted `X`. It **does not** establish an additional gravitational-wave polarization, an extra field, a nonzero curvature coupling, a new physical law, or validation of the DFM-MKC model.

Verified public source locations:

- Official LVK GWTC-5.0 POL summary release: https://zenodo.org/records/21454847 (`POL.tar.gz`).
- Official archive expected MD5: `0d22392a176237dcf6959f4e8ac6cc6e`.
- Public inference-package repository: https://github.com/isaac-cf-wong/nullpol. **A GWTC-5.0 POL-specific pinned revision has not been verified.**
- Request for missing original inference inputs: https://github.com/isaac-cf-wong/nullpol/issues/263 (created 2026-11-05).

## Reported local reproduction receipts (2026-11-05)

The operator reported the following Mac Terminal outputs. These are conversation-provided execution receipts, **not independently archived execution logs inside this repository**.

| Check | Result reported | Limit |
| --- | --- | --- |
| `md5 -q POL.tar.gz` equals the official MD5 | `CHECKSUM := PASS` | Confirms local archive identity if the quoted output is accurate; does not rerun inference |
| `tar -tzf POL.tar.gz` | `ARCHIVE := PASS` | Confirms archive can be listed |
| Inspect `POL/README.md` and `POL/summary.py` | `SOURCE_INSPECTION := PASS` | Source inspection only |
| Run unchanged `python3 summary.py` in `POL/` | `SCRIPT_EXECUTION := PASS`; outputs present | Recreates summaries, not event-level sampling |
| Compare generated `POL/pol_macro.tex` byte-for-byte with the archived file using `cmp -s` | `PUBLISHED_MACRO_REPRODUCTION := PASS` | Exact macro reproduction is **not** independent Bayesian evidence reproduction |

A missing Times/Nimbus Roman/FreeSerif font-family warning appeared during script execution but was nonfatal. No byte-for-byte reproduction of the generated PDF is claimed.

Archive contents listed in the reported command: `POL/README.md`, `POL/summary.py`, `POL/pol_macro.tex`, `POL/pol_logB.pdf`, `POL/pre_o4a_pol_log_bayes_factor.json`, `POL/o4a_pol_log_bayes_factor.json`, `POL/o4b_pol_log_bayes_factor.json`, `POL/paper.style`.

## Verification boundary

The released POL summaries are *downstream artifacts*. They do not, by themselves, certify that the original Bayesian inference has been reproduced. The exact upstream source objects have not been obtained:

1. Original per-event POL input configurations, selected event list, and hypothesis/likelihood definitions.
2. Strain, PSD, calibration, and GR waveform **references/versions**; event-level time–frequency selections.
3. Priors, sampler settings, random seeds, executable workflow manifest, and pinned `nullpol`/dependency revisions.
4. Per-event inference outputs/evidences and comparison tolerances.

These inputs have been requested from the authors in [issue #263](https://github.com/isaac-cf-wong/nullpol/issues/263); this note does not assert that they have been supplied or that the issue has been resolved.

## Mathematical and physical claim boundaries

- `POL_ARCHIVE_MD5 := PASS (operator-reported)`
- `PUBLISHED_POL_SUMMARY := PASS (operator-reported)`
- `ORIGINAL_BAYESIAN_INFERENCE := NOT_REPRODUCED`
- `INDEPENDENT_ADDITIONAL_POLARIZATION := NOT_ESTABLISHED`
- `FIELD_X_PHYSICAL_EXISTENCE := NOT_ESTABLISHED`
- `CURVATURE_SPECIFIC_COUPLING := NOT_DERIVED`
- `NOVEL_PHYSICS := NOT_ESTABLISHED`
- `DFM_MKC_EXTERNAL_VALIDATION_FROM_THIS_WORK := NONE`

A hypothetical `X` and an assumed interaction such as `X\mathcal{G}` do not prove that an additional field or coupling exists. Reproducing a summary cannot be promoted into confirmation of an unexplained gravitational-wave signal.

## Next admissible actions

1. Obtain, authenticate, and pin the exact authors' event-level POL inputs and software revision from issue #263 or another independently verified release.
2. If complete, rerun the original inference **unchanged** and compare its Bayes factors against the original outputs and documented tolerances.
3. Advance beyond this audit only if independent reproduction establishes an unexplained signal and a noncircular physical mechanism. Until then, **keep `X`-field modeling halted**.

This dated note is an audit artifact, not a theorem, manuscript proving a new law, or a replacement for the external collaboration's results.
