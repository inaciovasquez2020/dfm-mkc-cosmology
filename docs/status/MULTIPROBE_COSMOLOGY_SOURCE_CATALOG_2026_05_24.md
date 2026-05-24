# Multiprobe Cosmology Source Catalog

Status: `SOURCE_CATALOG_RECORD_ONLY_DIGESTS_AND_LIKELIHOOD_RUNS_PENDING`

Record ID: `MULTIPROBE_COSMOLOGY_SOURCE_CATALOG_2026_05_24`

Strand: `DFM-MKC / cosmology`

Purpose: organize external cosmology datasets and likelihood frameworks for later certified ΛCDM vs DFM-MKC comparison.

## Dataset records

| Dataset ID | Probe | Recommendation | Role |
|---|---|---:|---|
| `DESI_DR2_BAO` | BAO / expansion history | USE | primary expansion-history anchor |
| `PLANCK_2018_PLIK_LOWELL` | CMB / early-time constraints | USE | CMB gold-standard baseline |
| `ACT_DR6_CMB_LENSING` | CMB / high-ell and lensing | USE | ground-based CMB extension and lensing cross-check |
| `SPT_3G_DR1` | CMB / complementary ground-based spectra | DEVELOPING | complementary CMB consistency check |
| `DES_Y6_3X2PT` | weak lensing + galaxy clustering | AVAILABLE_REGISTRATION_OR_WRAPPER_REQUIRED | late-time growth and S8 comparison |
| `PANTHEON_PLUS` | supernovae / distance ladder | USE | low-redshift distance baseline |
| `ROMAN_MOCK_SN` | future high-redshift supernova forecast | FORECAST_ONLY | future-data high-redshift discriminator reference |
| `ESGB_SCALAR_DARK_SECTOR_COMPARATOR_2507_05207_V3` | external dark-sector modified-gravity comparator | COMPARATOR_ONLY | Gauss-Bonnet scalar dark-sector benchmark |

## First certified packet target

`CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET`

Minimal first dataset choice: `DESI_DR2_BAO`.

Required fields:
- dataset_name
- source_url
- release_version
- data_vector_path
- covariance_path
- nuisance_prior_path_or_null
- likelihood_config_path
- data_vector_sha256
- covariance_sha256
- nuisance_priors_sha256_or_null
- likelihood_config_sha256
- cross_covariance_policy
- lcdm_baseline_command
- dfm_mkc_comparison_command
- boundary

## Negative use lock

- source catalog only
- no downloaded data vectors certified
- no covariance digests certified
- no likelihood execution
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

This record is a source-catalog and packet-schema target only. It does not certify that any listed data vector has been downloaded. It does not certify covariance matrices. It does not certify nuisance priors. It does not run Cobaya. It does not produce posterior chains. It does not compare ΛCDM against DFM-MKC. It does not reject Lambda-CDM. It does not validate DFM-MKC. It does not provide Chronos proof input. It does not prove R1/R2/R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
