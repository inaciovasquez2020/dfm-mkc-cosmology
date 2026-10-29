# DESI DR2 BAO Data Pin — 2026-10-29

Status: `OBSERVED_BAO_VECTOR_AND_COVARIANCE_PINNED; MODEL_COMPARISON_BLOCKED`

## Source provenance

- Distribution: `CobayaSampler/bao_data`, directory `desi_bao_dr2`.
- Pinned source commit: `b7b8a36e9bccb063081f811f323cada21ab5fbdd` (commit message: `add desi_bao_dr2`, 2025-03-20).
- Repository: https://github.com/CobayaSampler/bao_data
- Commit-pinned vector URL: https://raw.githubusercontent.com/CobayaSampler/bao_data/b7b8a36e9bccb063081f811f323cada21ab5fbdd/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt
- Commit-pinned covariance URL: https://raw.githubusercontent.com/CobayaSampler/bao_data/b7b8a36e9bccb063081f811f323cada21ab5fbdd/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt

The pinned commit is the Cobaya distribution commit adding the DESI DR2 directory; the distribution README identifies the files as DESI DR2 data and references the DESI DR2 BAO papers. This is a version-pinned public distribution, not a claim that the GitHub mirror is the original DESI-hosted file server.

## Files and hashes

| Object | Filename | Byte count | Git blob SHA-1 | SHA-256 of retrieved UTF-8 file text |
|---|---|---:|---|---|
| Observed mean vector with row metadata | `desi_gaussian_bao_ALL_GCcomb_mean.txt` | 472 | `8aff444fdb42c0946342aa0011ab287eda097c4c` | `9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585` |
| Observed covariance | `desi_gaussian_bao_ALL_GCcomb_cov.txt` | 2547 | `fd8e5697ab61379b07b52efb781ea6713417a4d9` | `252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509` |

The SHA-256 values were computed over the exact UTF-8 text returned by the commit-pinned raw-file fetch. The byte counts match the GitHub Contents API metadata. Git blob SHA-1 values are included separately and are not represented as SHA-256. A second independent byte-download/hash run remains desirable before final release certification.

## Vector shape, order, and units

- Mean-vector rows: 13 observations; covariance dimensions: (13\times13).
- All observables are dimensionless distance ratios normalized by the sound horizon (r_d); covariance entries therefore have squared dimensionless units.
- Exact order is inherited from the mean file and must be used unchanged for the prediction vector and covariance:

| Index (0-based) | Redshift | Observable |
|---:|---:|---|
| 0 | 0.295 | (D_V/r_d) |
| 1 | 0.510 | (D_M/r_d) |
| 2 | 0.510 | (D_H/r_d) |
| 3 | 0.706 | (D_M/r_d) |
| 4 | 0.706 | (D_H/r_d) |
| 5 | 0.934 | (D_M/r_d) |
| 6 | 0.934 | (D_H/r_d) |
| 7 | 1.321 | (D_M/r_d) |
| 8 | 1.321 | (D_H/r_d) |
| 9 | 1.484 | (D_M/r_d) |
| 10 | 1.484 | (D_H/r_d) |
| 11 | 2.330 | (D_H/r_d) |
| 12 | 2.330 | (D_M/r_d) |

The last two rows are deliberately ordered (D_H/r_d) then (D_M/r_d); do not reorder them into a more intuitive transverse/radial sequence.

## Numerical integrity checks

Checks performed on the retrieved covariance text:

- Parsed shape: (13\times13).
- Exact symmetry check: passed ((C=C^T) element-by-element).
- Minimum eigenvalue: approximately (5.78998687\times10^{-3}), positive.
- Positive-definite check: passed for the parsed matrix.
- Observed-vector row count: 13.

These checks establish numerical integrity of the pinned observed data representation, not any cosmological model fit.

## DFM-MKC boundary

No DFM-MKC prediction vector was produced. The repository's current parameter/solver artifact is explicitly an interface only, and the closed field-equation/action artifact remains target-only. The current `dfm_mkc/model.py` three-parameter background expression is not a validated DFM-MKC perturbation solver and does not supply the sound horizon, transfer functions, or frozen 13-slot prediction.

Therefore:
- No residual vector or χ² has been calculated.
- No ΛCDM-vs-DFM-MKC score has been calculated.
- No empirical status is promoted.
- Weak-lensing data pinning and numerical shear prediction remain open.

## Next gates

1. Supply a complete, internally consistent DFM-MKC field-equation/action object and parameter map with actual frozen numerical values.
2. Implement the required background and perturbation solver; verify synthetic limits, grid convergence, and reproducibility with input/output hashes.
3. Independently redownload the two pinned BAO files and reproduce the SHA-256 values above.
4. Select a specific public weak-lensing release and pin its vector, covariance, redshift distributions, bin ordering, units, and hashes.
5. Freeze the shared likelihood, nuisance treatment, parameter policy, and decision rule before running matched DFM-MKC and ΛCDM comparisons.
