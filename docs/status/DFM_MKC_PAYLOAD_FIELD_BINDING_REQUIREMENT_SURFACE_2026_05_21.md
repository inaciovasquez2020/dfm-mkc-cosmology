# DFM-MKC Payload Field Binding Requirement Surface — 2026-05-21

Status: FIELD_BINDING_REQUIREMENT_SURFACE_ONLY_NO_FIELD_EXTRACTION

Object index:
- 3 of 5

Predecessor:
- PR #103
- merge commit: 11a518b
- prior status: PREDICATE_TO_SCHEMA_VALIDATOR_BRIDGE_ONLY_NO_AUTHENTIC_PAYLOAD_VALIDATION

Hard blocker:
- protocol fields are not bound to authenticated payload locations

Purpose:
- Record the requirement that each protocol field must be bound to authenticated payload locations before validation.

Required protocol fields:
- data_vector
- covariance_matrix
- mask
- likelihood_rule
- statistical_threshold
- protocol_hash
- actdr6_release_date
- data_freeze_lock

Next admissible object:
- payload_digest_freeze_lock_target

Boundary:
- frontier object only
- does not validate authentic ACT DR6 payload bytes
- does not extract a numerical data vector
- does not extract a covariance matrix
- does not execute the likelihood
- does not supply evidence
- does not promote any empirical slot

Does not prove:
- DFM-MKC
- Lambda-CDM failure
- ACT/DES holdout survival
- independent empirical validation
- dark-energy resolution
- dark-matter resolution
- Nobel-level physical discovery
- any Clay problem
