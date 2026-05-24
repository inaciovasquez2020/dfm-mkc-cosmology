# DESI DR2 BAO Model Comparison Output Schema

Status: `SCHEMA_ONLY_NO_LIKELIHOOD_EXECUTION`

Record ID: `DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_SCHEMA_2026_05_24`

Dataset dependency: `DESI_DR2_BAO_CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET_2026_05_24`

Baseline dependency: `DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_2026_05_24`

Comparison dependency: `DESI_DR2_BAO_DFM_MKC_COMPARISON_EXECUTION_TARGET_2026_05_24`

Schema path: `schemas/cosmology/desi_dr2_bao_model_comparison_output_schema_2026_05_24.json`

Result object target: `DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_RESULT`

Required loglike fields:
- lcdm_loglike
- dfm_mkc_loglike

Required chi-square fields:
- lcdm_chi2
- dfm_mkc_chi2
- delta_chi2

Required information-criteria fields:
- AICc.lcdm
- AICc.dfm_mkc
- AICc.delta_AICc
- BICc.lcdm
- BICc.dfm_mkc
- BICc.delta_BICc

Required diagnostic fields:
- posterior_predictive_distribution_p
- runtime_environment_record
- execution_log_digest

Negative use lock:
- schema-only result object
- no likelihood execution
- no posterior chains
- no best-fit value
- no delta_chi2 result
- no AICc result
- no BICc result
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
This record defines only the DESI DR2 BAO model-comparison output schema. It does not run Cobaya. It does not certify Cobaya. It does not certify CAMB. It does not import the DESI DR2 BAO likelihood. It does not execute Lambda-CDM. It does not execute DFM-MKC. It does not produce lcdm_loglike or dfm_mkc_loglike. It does not compute delta_chi2. It does not compute AICc. It does not compute BICc. It does not compare Lambda-CDM against DFM-MKC. It does not reject Lambda-CDM. It does not validate DFM-MKC. It does not provide Chronos proof input. It does not prove R1/R2/R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
