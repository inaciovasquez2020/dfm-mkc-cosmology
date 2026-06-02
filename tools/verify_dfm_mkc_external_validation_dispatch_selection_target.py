#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_status/dfm_mkc_external_validation_dispatch_selection_target_2026_06_02.json"
STATUS_DOC = ROOT / "docs/status/EXTERNAL_VALIDATION_DISPATCH_SELECTION_TARGET_2026_06_02.md"
TEMPLATE_DOC = ROOT / "docs/submission/DFM_MKC_DISPATCH_SELECTION_TEMPLATE_2026_06_02.md"

def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8")

def run_required_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_external_validation_or_submission_handoff.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)

def main() -> None:
    run_required_verifier()
    data = json.loads(read(ARTIFACT))

    assert data["status"] == "DISPATCH_SELECTION_TARGET_OPEN"
    assert data["input_status"] == "EXTERNAL_VALIDATION_OR_SUBMISSION_HANDOFF_READY"
    assert data["missing_input"] == "external_validator_recipient_or_submission_venue"
    assert data["allowed_next_object_after_input"] == "ExternalValidationRequestSentOrSubmissionRecorded"
    assert data["decision"] == "PASS"
    assert data["boundary"] == "TARGET_ONLY_NO_DISPATCH_CLAIM"

    for item in ["ExternalValidatorRecipient", "SubmissionVenue", "ReviewerOrAdvisorRecipient"]:
        if item not in data["weakest_sufficient_next_inputs"]:
            raise AssertionError(f"missing weakest input: {item}")

    for item in ["completed_external_validation", "sent_email", "journal_submission", "physical_interpretation_promotion"]:
        if item not in data["not_claimed"]:
            raise AssertionError(f"missing not_claimed: {item}")

    status_text = read(STATUS_DOC)
    template_text = read(TEMPLATE_DOC)

    for phrase in [
        "DISPATCH_SELECTION_TARGET_OPEN",
        "external_validator_recipient_or_submission_venue",
        "No external-validation request may be recorded as sent until a recipient or venue is supplied.",
        "It does not record a sent email.",
        "It does not record a journal submission."
    ]:
        if phrase not in status_text:
            raise AssertionError(f"missing status phrase: {phrase}")

    for phrase in [
        "DISPATCH_ROUTE=external_validator",
        "DISPATCH_ROUTE=submission_venue",
        "DISPATCH_ROUTE=reviewer_or_advisor",
        "RECIPIENT_EMAIL=",
        "VENUE_URL="
    ]:
        if phrase not in template_text:
            raise AssertionError(f"missing template phrase: {phrase}")

    print("DFM_MKC_EXTERNAL_VALIDATION_DISPATCH_SELECTION_TARGET_OK")
    print(json.dumps({
        "decision": data["decision"],
        "status": data["status"],
        "missing_input": data["missing_input"],
        "boundary": data["boundary"],
        "allowed_next_object_after_input": data["allowed_next_object_after_input"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
