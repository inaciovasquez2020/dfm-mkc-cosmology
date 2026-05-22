# ACT_DR6_REPRODUCIBLE_DOWNLOAD_COMMAND_OR_EXTERNAL_SHA256_DIGEST — 2026-05-22

Status: REPRODUCIBLE_DOWNLOAD_COMMAND_BOUND_EXTERNAL_DIGEST_NOT_SUPPLIED_NOT_EXECUTED

This object binds the ACT DR6 official data-product reference and the DR6-ACT-lite reproducible download command target.

Reproducible command target:
- git clone https://github.com/ACTCollaboration/DR6-ACT-lite.git DR6-ACT-lite
- cd DR6-ACT-lite
- python3 -m pip install -e .
- cobaya-install act_dr6_cmbonly

Required next object:
- ACT_DR6_REPRODUCIBLE_DOWNLOAD_EXECUTION_AND_LOCAL_SHA256_COMPARISON

Does not prove:
- ACT DR6 public release digest certification
- ACT DR6 reproducible download execution
- ACT DR6 downloaded payload hash match
- ACT DR6 full SACC schema certification
- complete certified likelihood manifest
- executed multiprobe likelihood run
- Lambda-CDM rejection
- six-parameter flat Lambda-CDM rejection
- alternative-model validation
- DFM-MKC validation
- dark matter resolution
- dark energy resolution
- any Clay problem
