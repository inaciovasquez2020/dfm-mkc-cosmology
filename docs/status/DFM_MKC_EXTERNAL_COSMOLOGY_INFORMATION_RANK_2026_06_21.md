# DFM-MKC external cosmology information rank — 2026-06-21

Status: `DFM_MKC_EXTERNAL_COSMOLOGY_INFORMATION_RANK_2026_06_21`

Answer: yes, there is newer external information that helps, but it does not solve DFM-MKC cosmology.

Solves: `false`

Weakest missing object: `DFM_MKC_parameter_to_observable_map_to_ACT_DR6_135_row_prediction_vector`

## Ranked external information

1. ACT DR6.02 LAMBDA data release
   Source: `https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/`
   Usefulness: strongest actionable external input surface.
   Helps by providing official ACT DR6.02 PSPIPE products, best-fit power spectra, sky masks, covariance matrices, likelihood SACC files, and MCMC chains.
   Does not supply the DFM-MKC forward model or ACT DR6 135-row DFM-MKC prediction vector.

2. DES Y6 cosmology results and data products
   Source: `https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/`
   Usefulness: multiprobe validation-target improvement.
   Helps by providing public DES Y6 cosmology papers, a Y6 data-products entry point, and a 3x2pt large-scale-structure validation surface.
   Does not supply the DFM-MKC parameter-to-observable map.

3. DESI DR2 cosmology chains and data products
   Source: `https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/`
   Usefulness: baseline reproducibility and late-time validation surface.
   Helps by providing published DR2 cosmology chains, best-fit parameter values, and an external BAO comparison surface.
   Does not supply the DFM-MKC forward solver or closure proof.

4. DESI DR2 publications index
   Source: `https://data.desi.lbl.gov/doc/papers/dr2/`
   Usefulness: publication and dataset locator.
   Helps by locating DR2 cosmology publications from DESI first-three-years data.
   Does not supply a DFM-MKC executable observable prediction.

## Classification

- External data surfaces improved: yes.
- External prior-art/usefulness surfaces improved: yes.
- Direct DFM-MKC solver found: no.
- ACT DR6 prediction vector found: no.
- Lambda-CDM rejection claim admissible: no.
- DFM-MKC validation claim admissible: no.

Boundary: external-information ranking only; no new theorem, no cosmology solution, no claim of Lambda-CDM rejection, no DFM-MKC validation, no ACT DR6 135-row prediction vector, and no parameter-to-observable forward-model construction.

Next bounded improvement: bind ACT DR6.02 PSPIPE/SACC/covariance products as an external input surface while keeping `DFM_MKC_parameter_to_observable_map_to_ACT_DR6_135_row_prediction_vector` as the weakest missing object.
