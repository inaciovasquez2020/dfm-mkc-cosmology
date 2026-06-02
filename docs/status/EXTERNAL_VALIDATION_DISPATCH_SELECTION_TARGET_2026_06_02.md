# DFM-MKC Cosmology — External Validation Dispatch Selection Target

## Status

`DISPATCH_SELECTION_TARGET_OPEN`

## Input State

The external validation or submission handoff packet is merged and verified.

## Missing Input

`external_validator_recipient_or_submission_venue`

## Weakest Sufficient Next Input

One of:

1. `ExternalValidatorRecipient`
2. `SubmissionVenue`
3. `ReviewerOrAdvisorRecipient`

## Dispatch Rule

No external-validation request may be recorded as sent until a recipient or venue is supplied.

No submission may be recorded as completed until a venue is supplied.

## Allowed Next Object After Input

`ExternalValidationRequestSentOrSubmissionRecorded`

## Boundary

This file records a missing dispatch-selection input only.

It does not record completed external validation.

It does not record a sent email.

It does not record a journal submission.

It does not promote the physical interpretation.
