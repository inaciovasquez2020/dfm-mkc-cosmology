# DESI DR2 BAO Lambda-CDM Baseline Execution Target

Status: `EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN`

Record ID: `DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_2026_05_24`

Dataset dependency: `DESI_DR2_BAO_CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET_2026_05_24`

Config path: `configs/cosmology/desi_dr2_bao_lcdm_baseline_target.yaml`

Execution command: `cobaya run configs/cosmology/desi_dr2_bao_lcdm_baseline_target.yaml`

Certified inputs required before execution:
- DESI DR2 BAO digest-certified input packet
- Cobaya installed version
- CAMB installed version
- Cobaya likelihood import succeeds
- DESI DR2 BAO likelihood data path resolves

Pending outputs:
- best_fit_loglike
- best_fit_chi2
- derived_parameters
- runtime_environment_record
- execution_log_digest
- posterior_or_evaluate_output_path

Negative use lock:
- execution target only
- no likelihood execution
- no posterior chains
- no best-fit value
- no Lambda-CDM rejection
- no DFM-MKC comparison
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
This target defines only the intended DESI DR2 BAO Lambda-CDM baseline execution surface. It does not run Cobaya. It does not certify Cobaya. It does not certify CAMB. It does not import the DESI DR2 BAO likelihood. It does not produce a likelihood value. It does not produce posterior chains. It does not compare Lambda-CDM against DFM-MKC. It does not reject Lambda-CDM. It does not validate DFM-MKC. It does not provide Chronos proof input. It does not prove R1/R2/R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
