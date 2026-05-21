#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import importlib.util
import json
import sys

PREDICATE_MODULE = Path(__file__).with_name("dfm_mkc_schema_acceptance_predicates.py")

STATUS = "PREDICATE_TO_SCHEMA_VALIDATOR_BRIDGE_ONLY_NO_AUTHENTIC_PAYLOAD_VALIDATION"

def _load_predicates():
    spec = importlib.util.spec_from_file_location("dfm_mkc_schema_acceptance_predicates", PREDICATE_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load predicate module: {PREDICATE_MODULE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

_PREDICATES = _load_predicates()

REQUIRED_FIELDS = tuple(_PREDICATES.REQUIRED_FIELDS)

@dataclass(frozen=True)
class SchemaValidationReport:
    status: str
    accepted: bool
    missing_fields: tuple[str, ...]
    extra_fields: tuple[str, ...]
    rejected_fields: tuple[str, ...]
    field_missing_predicates: dict[str, tuple[str, ...]]

def validate_candidate_metadata_schema(candidate: dict[str, dict[str, Any]]) -> SchemaValidationReport:
    candidate_fields = set(candidate)
    required_fields = set(REQUIRED_FIELDS)

    missing_fields = tuple(field for field in REQUIRED_FIELDS if field not in candidate_fields)
    extra_fields = tuple(sorted(candidate_fields - required_fields))

    field_results = _PREDICATES.evaluate_candidate_field_map(candidate)
    field_missing_predicates = {
        field: tuple(result.missing_predicates)
        for field, result in field_results.items()
    }
    rejected_fields = tuple(
        field for field in REQUIRED_FIELDS
        if field_missing_predicates.get(field)
    )

    accepted = not missing_fields and not extra_fields and not rejected_fields

    return SchemaValidationReport(
        status=STATUS,
        accepted=accepted,
        missing_fields=missing_fields,
        extra_fields=extra_fields,
        rejected_fields=rejected_fields,
        field_missing_predicates=field_missing_predicates,
    )

def report_to_jsonable(report: SchemaValidationReport) -> dict[str, Any]:
    return {
        "status": report.status,
        "accepted": report.accepted,
        "missing_fields": list(report.missing_fields),
        "extra_fields": list(report.extra_fields),
        "rejected_fields": list(report.rejected_fields),
        "field_missing_predicates": {
            field: list(missing)
            for field, missing in report.field_missing_predicates.items()
        },
    }

def validate_candidate_metadata_schema_json(candidate_json: str) -> dict[str, Any]:
    candidate = json.loads(candidate_json)
    if not isinstance(candidate, dict):
        raise TypeError("candidate metadata schema input must be a JSON object")
    report = validate_candidate_metadata_schema(candidate)
    return report_to_jsonable(report)

def main() -> None:
    if len(sys.argv) != 2:
        print("usage: dfm_mkc_predicate_to_schema_validator_bridge.py <candidate-json-path>", file=sys.stderr)
        raise SystemExit(2)

    candidate_path = Path(sys.argv[1])
    report = validate_candidate_metadata_schema_json(candidate_path.read_text())
    print(json.dumps(report, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
