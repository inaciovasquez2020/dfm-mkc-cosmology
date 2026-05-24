# DESI DR2 BAO DFM-MKC Comparison Execution Target

Status: `COMPARISON_EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN`

Record ID: `DESI_DR2_BAO_DFM_MKC_COMPARISON_EXECUTION_TARGET_2026_05_24`

Dataset dependency: `DESI_DR2_BAO_CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET_2026_05_24`

Baseline dependency: `DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_2026_05_24`

Config path: `configs/cosmology/desi_dr2_bao_dfm_mkc_comparison_target.yaml`

Execution command: `cobaya run configs/cosmology/desi_dr2_bao_dfm_mkc_comparison_target.yaml`

DFM-MKC placeholder parameters:
- dfm_mkc_alpha
- dfm_mkc_beta
- dfm_mkc_gamma

Certified inputs required before execution:
- DESI DR2 BAO digest-certified input packet
- DESI DR2 BAO Lambda-CDM baseline execution target
- Cobaya installed version
- CAMB installed version
- DFM-MKC model implementation
- DFM-MKC parameter-to-observable map
- Cobaya likelihood import succeeds
- DESI DR2 BAO likelihood data path resolves

Pending outputs:
- dfm_mkc_best_fit_loglike
- dfm_mkc_best_fit_chi2
- lcdm_best_fit_loglike
- lcdm_best_fit_chi2
- delta_chi2
- AICc
- BICc
- posterior_predictive_distribution_p
- runtime_environment_record
- execution_log_digest
- posterior_or_evaluate_output_path

Negative use lock:
- comparison execution target only
- no likelihood execution
- no posterior chains
- no best-fit value
- no delta_chi2
- no AICc
- no BICc
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
This target defines only the intended DESI DR2 BAO DFM-MKC comparison execution surface. It does not run Cobaya. It does not certify Cobaya. It does not certify CAMB. It does not define the DFM-MKC model implementation. It does not define the DFM-MKC parameter-to-observable map. It does not import the DESI DR2 BAO likelihood. It does not produce a likelihood value. It does not produce posterior chains. It does not compute delta_chi2, AICc, or BICc. It does not compare Lambda-CDM against DFM-MKC. It does not reject Lambda-CDM. It does not validate DFM-MKC. It does not provide Chronos proof input. It does not prove R1/R2/R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
