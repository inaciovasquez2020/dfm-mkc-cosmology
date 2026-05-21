#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_minimal_schema_validation_requirement_target_2026_05_21.json")
STATUS = Path("docs/status/DFM_MKC_MINIMAL_SCHEMA_VALIDATION_REQUIREMENT_TARGET_2026_05_21.md")

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
    "requirement target only",
    "acceptance predicates specified but not implemented as schema validation",
    "candidate protocol field map exists but is not validated",
    "numerical data vector not extracted",
    "covariance matrix not extracted",
    "full protocol execution not performed",
    "no evidence supplied",
    "no slot promoted",
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

def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing artifact: {ARTIFACT}")
    if not STATUS.exists():
        fail(f"missing status doc: {STATUS}")

    data = json.loads(ARTIFACT.read_text())
    text = STATUS.read_text()

    if data.get("status") != "REQUIREMENT_TARGET_ONLY_ACCEPTANCE_PREDICATES_NOT_IMPLEMENTED":
        fail("unexpected status")

    if data.get("hard_blocker") != "schema validation remains blocked":
        fail("missing hard blocker")

    predecessor = data.get("predecessor", {})
    if predecessor.get("pull_request") != 100:
        fail("missing predecessor PR #100")
    if predecessor.get("merge_commit") != "0923660":
        fail("missing predecessor merge commit 0923660")

    target = data.get("minimal_schema_validation_requirement_target", {})
    fields = target.get("required_protocol_fields")
    predicates = target.get("acceptance_predicates", {})

    if fields != REQUIRED_FIELDS:
        fail("required protocol fields mismatch")

    for field in REQUIRED_FIELDS:
        if field not in predicates:
            fail(f"missing acceptance predicates for {field}")
        if not isinstance(predicates[field], list) or not predicates[field]:
            fail(f"empty acceptance predicates for {field}")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in data.get("boundary", []):
            fail(f"missing artifact boundary: {boundary}")
        if boundary not in text:
            fail(f"missing status boundary: {boundary}")

    for nonclaim in REQUIRED_NONCLAIMS:
        if nonclaim not in data.get("does_not_prove", []):
            fail(f"missing artifact nonclaim: {nonclaim}")
        if nonclaim not in text:
            fail(f"missing status nonclaim: {nonclaim}")

    print("DFM-MKC minimal schema-validation requirement target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Required fields: {', '.join(REQUIRED_FIELDS)}")

if __name__ == "__main__":
    main()
