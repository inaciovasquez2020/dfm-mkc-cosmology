# Cobaya Runtime Environment Certification Target

Status: `RUNTIME_ENVIRONMENT_CERTIFICATION_TARGET_ONLY_NOT_CERTIFIED`

Record ID: `COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_TARGET_2026_05_24`

Purpose: Define required runtime-environment fields before any Cobaya likelihood execution is admissible.

Required fields:
- python_version
- cobaya_version
- camb_version_or_null
- class_version_or_null
- numpy_version
- scipy_version
- platform
- pip_freeze_digest
- execution_command
- environment_log_digest

Pending outputs:
- runtime_environment_record
- pip_freeze_digest
- environment_log_digest

Negative use lock:
- runtime environment target only
- environment not certified
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
- does not certify Cobaya
- does not certify CAMB
- does not certify CLASS
- does not run a likelihood
- does not produce posterior chains
- does not reject Lambda-CDM
- does not validate DFM-MKC
- does not provide Chronos proof input
- does not prove R1/R2/R3
- does not prove NON_FACTORISATION
- does not prove Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
