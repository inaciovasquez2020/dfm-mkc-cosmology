#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys

OBJECTS = [
    {
        "slug": "authentic_payload_schema_validation_blocker_certificate",
        "status": "AUTHENTIC_PAYLOAD_SCHEMA_VALIDATION_BLOCKED_NO_PAYLOAD_SUPPLIED",
        "hard_blocker": "authentic ACT DR6 payload bytes are not supplied",
        "next_admissible_object": "authentic_payload_validation_target",
    },
    {
        "slug": "authentic_payload_validation_target",
        "status": "AUTHENTIC_PAYLOAD_VALIDATION_TARGET_ONLY_NO_PAYLOAD_VALIDATION",
        "hard_blocker": "authentic ACT DR6 payload validation remains unexecuted",
        "next_admissible_object": "payload_field_binding_requirement_surface",
    },
    {
        "slug": "payload_field_binding_requirement_surface",
        "status": "FIELD_BINDING_REQUIREMENT_SURFACE_ONLY_NO_FIELD_EXTRACTION",
        "hard_blocker": "protocol fields are not bound to authenticated payload locations",
        "next_admissible_object": "payload_digest_freeze_lock_target",
    },
    {
        "slug": "payload_digest_freeze_lock_target",
        "status": "DIGEST_FREEZE_LOCK_TARGET_ONLY_NO_DIGEST_VERIFICATION",
        "hard_blocker": "immutable authentic payload digest is not verified",
        "next_admissible_object": "schema_validation_execution_gate",
    },
    {
        "slug": "schema_validation_execution_gate",
        "status": "SCHEMA_VALIDATION_EXECUTION_GATE_ONLY_NOT_EXECUTED",
        "hard_blocker": "schema validation gate is not executed against authentic payload",
        "next_admissible_object": "authentic_payload_schema_validation_run",
    },
]

REQUIRED_FIELDS = [
    "data_vector",
    "covariance_matrix",
    "mask",
    "likelihood_rule",
    "statistical_threshold",
    "protocol_hash",
    "actdr6_release_date",
    "data_freeze_lock",
]

REQUIRED_BOUNDARIES = [
    "frontier object only",
    "does not validate authentic ACT DR6 payload bytes",
    "does not extract a numerical data vector",
    "does not extract a covariance matrix",
    "does not execute the likelihood",
    "does not supply evidence",
    "does not promote any empirical slot",
]

REQUIRED_NONCLAIMS = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    for index, spec in enumerate(OBJECTS, start=1):
        artifact = Path(f"artifacts/repo_intake/dfm_mkc_{spec['slug']}_2026_05_21.json")
        status_doc = Path(f"docs/status/DFM_MKC_{spec['slug'].upper()}_2026_05_21.md")

        if not artifact.exists():
            fail(f"missing artifact: {artifact}")
        if not status_doc.exists():
            fail(f"missing status doc: {status_doc}")

        data = json.loads(artifact.read_text())
        text = status_doc.read_text()

        if data.get("object_index") != index:
            fail(f"{spec['slug']}: wrong object index")
        if data.get("status") != spec["status"]:
            fail(f"{spec['slug']}: wrong status")
        if data.get("hard_blocker") != spec["hard_blocker"]:
            fail(f"{spec['slug']}: wrong hard blocker")
        if data.get("next_admissible_object") != spec["next_admissible_object"]:
            fail(f"{spec['slug']}: wrong next admissible object")
        if data.get("predecessor", {}).get("pull_request") != 103:
            fail(f"{spec['slug']}: missing predecessor PR #103")
        if data.get("predecessor", {}).get("merge_commit") != "11a518b":
            fail(f"{spec['slug']}: missing predecessor merge commit 11a518b")
        if data.get("required_fields") != REQUIRED_FIELDS:
            fail(f"{spec['slug']}: required fields mismatch")

        for field in REQUIRED_FIELDS:
            if field not in text:
                fail(f"{spec['slug']}: missing field in status doc: {field}")

        for boundary in REQUIRED_BOUNDARIES:
            if boundary not in data.get("boundary", []):
                fail(f"{spec['slug']}: missing artifact boundary: {boundary}")
            if boundary not in text:
                fail(f"{spec['slug']}: missing status boundary: {boundary}")

        for nonclaim in REQUIRED_NONCLAIMS:
            if nonclaim not in data.get("does_not_prove", []):
                fail(f"{spec['slug']}: missing artifact nonclaim: {nonclaim}")
            if nonclaim not in text:
                fail(f"{spec['slug']}: missing status nonclaim: {nonclaim}")

    print("DFM-MKC next five validation frontier verification OK.")
    print("Objects verified: 5")
    for spec in OBJECTS:
        print(f"- {spec['status']}")

if __name__ == "__main__":
    main()
