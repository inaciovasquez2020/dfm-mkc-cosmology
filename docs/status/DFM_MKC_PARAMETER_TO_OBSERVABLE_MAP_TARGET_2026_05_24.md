# DFM-MKC Parameter-to-Observable Map Target

Status: `PARAMETER_TO_OBSERVABLE_MAP_TARGET_ONLY_MAP_NOT_SUPPLIED`

Record ID: `DFM_MKC_PARAMETER_TO_OBSERVABLE_MAP_TARGET_2026_05_24`

Purpose: Define the missing model map required before DFM-MKC can be evaluated against DESI DR2 BAO.

Required fields:
- dfm_mkc_parameter_names
- parameter_priors
- observable_map_definition
- bao_observable_interface
- background_expansion_function
- sound_horizon_policy
- units_policy
- validity_domain
- implementation_path
- implementation_digest

Pending outputs:
- DFM-MKC parameter-to-observable map
- implementation_path
- implementation_digest
- unit tests for observable map

Negative use lock:
- parameter-to-observable map target only
- map not supplied
- no DFM-MKC implementation
- no likelihood execution
- no posterior chains
- no best-fit value
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

Boundary:
- does not define the DFM-MKC model
- does not define the DFM-MKC parameter-to-observable map
- does not implement DFM-MKC
- does not run Cobaya
- does not compute BAO observables
- does not compare Lambda-CDM against DFM-MKC
- does not reject Lambda-CDM
- does not validate DFM-MKC
- does not provide Chronos proof input
- does not prove R1/R2/R3
- does not prove NON_FACTORISATION
- does not prove Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
