#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/repo_status/dfm_mkc_external_validation_or_submission_handoff_2026_06_02.json"
STATUS_DOC = ROOT / "docs/status/EXTERNAL_VALIDATION_OR_SUBMISSION_HANDOFF_2026_06_02.md"
REQUEST_DOC = ROOT / "docs/submission/DFM_MKC_EXTERNAL_VALIDATION_REQUEST_2026_06_02.md"

REQUIRED_STATUS_PHRASES = [
    "EXTERNAL_VALIDATION_OR_SUBMISSION_HANDOFF_READY",
    "This file does not record completed external validation.",
    "This file records only that the repository is ready for the next external or submission-facing step.",
]

REQUIRED_REQUEST_PHRASES = [
    "Please independently validate the DFM-MKC cosmology repository",
    "commit hash",
    "commands run",
    "reproducibility conclusion",
    "It does not by itself establish a unique cosmological interpretation.",
]

def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8")

def main() -> None:
    post = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_post_closure_external_validation_packet.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if post.returncode != 0:
        raise AssertionError(post.stdout + post.stderr)

    data = json.loads(read(ARTIFACT))

    assert data["status"] == "EXTERNAL_VALIDATION_OR_SUBMISSION_HANDOFF_READY"
    assert data["input_status"] == "POST_CLOSURE_EXTERNAL_VALIDATION_PACKET_OK"
    assert data["repository_surface"] == "CLOSED_REPRODUCIBILITY_SURFACE_ONLY"
    assert data["decision"] == "PASS"
    assert data["boundary"] == "HANDOFF_ONLY_NO_EXTERNAL_VALIDATION_CLAIM"

    for item in [
        "ExternalIndependentLikelihoodValidation",
        "SubmissionToReviewerOrJournal",
        "IdentifiabilityGuaranteeOrDegeneracyTheorem",
        "Stop",
    ]:
        if item not in data["next_admissible_objects"]:
            raise AssertionError(f"missing next object: {item}")

    for item in [
        "completed_external_validation",
        "unconditional_cosmology_interpretation",
        "unique_parameter_reconstruction",
        "final_physical_correctness",
    ]:
        if item not in data["not_claimed"]:
            raise AssertionError(f"missing not_claimed item: {item}")

    status_text = read(STATUS_DOC)
    request_text = read(REQUEST_DOC)

    for phrase in REQUIRED_STATUS_PHRASES:
        if phrase not in status_text:
            raise AssertionError(f"missing status phrase: {phrase}")

    for phrase in REQUIRED_REQUEST_PHRASES:
        if phrase not in request_text:
            raise AssertionError(f"missing request phrase: {phrase}")

    print("DFM_MKC_EXTERNAL_VALIDATION_OR_SUBMISSION_HANDOFF_OK")
    print(json.dumps({
        "decision": data["decision"],
        "status": data["status"],
        "boundary": data["boundary"],
        "next_admissible_objects": data["next_admissible_objects"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
