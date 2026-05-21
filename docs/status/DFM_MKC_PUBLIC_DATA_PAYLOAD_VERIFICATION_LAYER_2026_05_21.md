# DFM-MKC Public Data Payload Verification Layer

Status: `PAYLOAD_VERIFICATION_LAYER_ONLY_NO_DATA_IMPORTED`

Purpose:
- define local payload verification requirements before any ACTDR6 or independent public data slot can be promoted

Depends on:
- `artifacts/repo_intake/dfm_mkc_public_data_source_seek_registry_2026_05_21.json`
- `artifacts/repo_intake/dfm_mkc_terminal_blocker_exhaustion_certificate_2026_05_21.json`
- `artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_missing_object_target_2026_05_21.json`
- `artifacts/repo_intake/dfm_mkc_independent_public_data_missing_object_target_2026_05_21.json`

Payload classes:
- `ACTDR6_NumericalData_Unfixed`
- `IndependentPublicData`

Required verification fields:
- `source_name`
- `source_url`
- `download_timestamp_utc`
- `local_path`
- `file_size_bytes`
- `sha256`
- `license_or_terms_reference`
- `payload_role`
- `expected_schema`
- `checksum_verified`
- `schema_validated`
- `external_payload_verified`

Promotion requirements:
- `payload_exists_locally`
- `sha256_recorded`
- `file_size_recorded`
- `source_url_recorded`
- `checksum_verified_true`
- `schema_validated_true`
- `external_payload_verified_true`

Data is not imported.
Payload is not verified.
No protocol run is performed.
No evidence is supplied.
No slot is promoted.

Does not prove:
- DFM-MKC
- Lambda-CDM failure
- ACT/DES holdout survival
- independent empirical validation
- dark-energy resolution
- dark-matter resolution
- Nobel-level physical discovery
- any Clay problem
