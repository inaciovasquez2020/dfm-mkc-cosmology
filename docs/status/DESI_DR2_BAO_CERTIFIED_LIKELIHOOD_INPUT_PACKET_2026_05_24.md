# DESI DR2 BAO Certified Likelihood Input Packet

Status: `DIGEST_CERTIFIED_INPUT_PACKET_ONLY_NO_LIKELIHOOD_EXECUTION`

Record ID: `DESI_DR2_BAO_CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET_2026_05_24`

Dataset: `DESI_DR2_BAO`

Source URL: `https://github.com/CobayaSampler/bao_data`

Source subdirectory: `desi_bao_dr2`

Release version: `v2.6`

Source commit SHA: `b7b8a36e9bccb063081f811f323cada21ab5fbdd`

Local source root: `external_data/desi_dr2_bao/bao_data/desi_bao_dr2`

File count: `16`

## Certified fields

- dataset_name
- source_url
- release_version
- source_commit_sha
- local_source_root
- file_manifest
- sha256 digests
- cross_covariance_policy
- boundary

## Pending fields

- Cobaya environment version
- CAMB or CLASS backend version
- exact ΛCDM YAML
- exact DFM-MKC YAML
- likelihood execution
- posterior chains
- delta_chi2
- AICc
- BICc
- posterior_predictive_distribution_p

## File manifest summary

| Role | Count |
|---|---:|
| covariance | 8 |
| data_vector_or_likelihood_table | 8 |
| likelihood_config_or_metadata | 0 |
| other | 0 |

## Negative use lock

- digest-certified input packet only
- no likelihood execution
- no posterior chains
- no Lambda-CDM rejection
- no DFM-MKC validation
- not Chronos proof input
- not evidence for R1
- not evidence for R2
- not evidence for R3
- not evidence for NON_FACTORISATION
- not evidence for Chronos-RR
- not evidence for H4.1/FGL
- not evidence for P vs NP
- not evidence for any Clay problem

## Boundary

This record certifies local source-file discovery and SHA-256 digests only. It does not run Cobaya. It does not certify a Python environment. It does not certify CAMB or CLASS. It does not define the DFM-MKC likelihood. It does not execute ΛCDM. It does not execute DFM-MKC. It does not compare ΛCDM against DFM-MKC. It does not reject Lambda-CDM. It does not validate DFM-MKC. It does not provide Chronos proof input. It does not prove R1/R2/R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
