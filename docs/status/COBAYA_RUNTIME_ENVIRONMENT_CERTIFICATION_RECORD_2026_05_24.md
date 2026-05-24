# Cobaya Runtime Environment Certification Record

Status: `RUNTIME_ENVIRONMENT_CERTIFIED_NO_LIKELIHOOD_EXECUTION`

Record ID: `COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_RECORD_2026_05_24`

Target dependency: `COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_TARGET_2026_05_24`

Certified runtime fields:
- python_executable
- python_version
- platform
- cobaya_version
- camb_version
- numpy_version
- scipy_version
- pip_freeze_path
- pip_freeze_digest
- environment_log_path
- environment_log_digest

Certified imports:
- cobaya
- camb
- numpy
- scipy

Runtime values:
- python_executable: `/Users/inaciof.vasquez/dfm-mkc-cosmology/.runtime_envs/cobaya_runtime_2026_05_24/bin/python`
- cobaya_version: `3.5.7`
- camb_version: `1.6.0`
- numpy_version: `2.0.2`
- scipy_version: `1.13.1`
- pip_freeze_digest: `464bd9e4d24c103f98994727e47a2d93f56bff53e722657ee32dd47f4bae12ab`
- environment_log_digest: `bf149268a329561c5425036de607aea4310f1076f498f2cb6e36b39c574c5f4f`

Pending outputs:
- DESI DR2 BAO likelihood import smoke test
- Lambda-CDM evaluate run
- DFM-MKC parameter-to-observable map
- DFM-MKC evaluate run
- model comparison result

Negative use lock:
- runtime environment certification only
- no DESI DR2 BAO likelihood import smoke test
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
This record certifies only the local Python/Cobaya/CAMB runtime environment. It does not import the DESI DR2 BAO likelihood. It does not execute Lambda-CDM. It does not execute DFM-MKC. It does not produce posterior chains. It does not produce a best-fit value. It does not compute delta_chi2. It does not compute AICc. It does not compute BICc. It does not compare Lambda-CDM against DFM-MKC. It does not reject Lambda-CDM. It does not validate DFM-MKC. It does not provide Chronos proof input. It does not prove R1/R2/R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
