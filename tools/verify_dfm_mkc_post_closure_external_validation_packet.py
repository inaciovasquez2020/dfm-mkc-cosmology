#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/repo_status/dfm_mkc_post_closure_external_validation_packet_2026_06_02.json"

DOCS = [
    ROOT / "docs/status/POST_CLOSURE_EXTERNAL_VALIDATION_PACKET_2026_06_02.md",
    ROOT / "docs/status/PAPER_FACING_INFERENCE_PACKET_2026_06_02.md",
    ROOT / "docs/status/EXTERNAL_INDEPENDENT_LIKELIHOOD_VALIDATION_TARGET_2026_06_02.md",
    ROOT / "docs/status/IDENTIFIABILITY_GUARANTEE_OR_DEGENERACY_FRONTIER_2026_06_02.md",
]

RECONCILED = [
    ROOT / "STATUS.md",
    ROOT / "docs/status/NEXT_CLOSURE_MOVE.md",
    ROOT / "docs/REAL_DATA_INTEGRATION_READINESS.md",
]

FORBIDDEN_PROMOTIONS = [
    "Lambda-CDM falsified",
    "dark energy resolved",
    "dark matter resolved",
    "final cosmological truth",
    "Nobel-level discovery",
    "Clay problem solved",
]

REQUIRED_ARTIFACT_KEYS = {
    "artifact",
    "status",
    "repository_surface",
    "reconciled_status_files",
    "created_files",
    "next_admissible_objects",
    "missing_external_objects",
    "forbidden_interpretations",
    "decision",
    "boundary",
}

def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text(encoding="utf-8")

def main() -> None:
    data = json.loads(read(ARTIFACT))
    missing = REQUIRED_ARTIFACT_KEYS - set(data)
    if missing:
        raise AssertionError(f"missing artifact keys: {sorted(missing)}")

    assert data["status"] == "POST_CLOSURE_EXTERNAL_VALIDATION_PACKET"
    assert data["repository_surface"] == "CLOSED_REPRODUCIBILITY_SURFACE_ONLY"
    assert data["decision"] == "PASS"
    assert data["boundary"] == "NO_NEW_PHYSICS_CLAIM"

    for item in [
        "ExternalIndependentLikelihoodValidation",
        "IdentifiabilityGuaranteeOrDegeneracyTheorem",
        "PreparePaperFacingInferencePacket",
        "ArchiveReleaseAndDashboardSync",
        "Stop",
    ]:
        if item not in data["next_admissible_objects"]:
            raise AssertionError(f"missing next object: {item}")

    for item in [
        "independent_likelihood_reproduction",
        "prior_sensitivity_report",
        "degeneracy_or_identifiability_analysis",
        "third_party_validation_note",
    ]:
        if item not in data["missing_external_objects"]:
            raise AssertionError(f"missing external object: {item}")

    for path in DOCS + RECONCILED:
        text = read(path)
        for phrase in FORBIDDEN_PROMOTIONS:
            if phrase in text and "not" not in text[max(0, text.find(phrase)-80):text.find(phrase)+len(phrase)+80].lower():
                raise AssertionError(f"possible forbidden promotion in {path}: {phrase}")

    next_text = read(ROOT / "docs/status/NEXT_CLOSURE_MOVE.md")
    if "Canonical Remaining Repository Object" not in next_text or "None" not in next_text:
        raise AssertionError("NEXT_CLOSURE_MOVE.md not reconciled to none")

    readiness_text = read(ROOT / "docs/REAL_DATA_INTEGRATION_READINESS.md")
    if "## Status" not in readiness_text or "Closed" not in readiness_text:
        raise AssertionError("REAL_DATA_INTEGRATION_READINESS.md not reconciled to closed")

    packet_text = read(ROOT / "docs/status/POST_CLOSURE_EXTERNAL_VALIDATION_PACKET_2026_06_02.md")
    for phrase in [
        "Independent likelihood reproduction",
        "Degeneracy and identifiability analysis",
        "No new scientific claim",
    ]:
        if phrase not in packet_text:
            raise AssertionError(f"missing packet phrase: {phrase}")

    print("DFM_MKC_POST_CLOSURE_EXTERNAL_VALIDATION_PACKET_OK")
    print(json.dumps({
        "decision": data["decision"],
        "status": data["status"],
        "repository_surface": data["repository_surface"],
        "next_admissible_objects": data["next_admissible_objects"],
        "boundary": data["boundary"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
