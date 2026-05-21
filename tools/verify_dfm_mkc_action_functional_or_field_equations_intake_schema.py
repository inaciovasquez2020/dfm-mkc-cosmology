#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "dfm_mkc_action_functional_or_field_equations_intake_schema_v1.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_action_functional_or_field_equations_intake_schema_2026_05_21.json"
BLOCKER = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_full_closure_blocker_certificate_2026_05_21.json"

TARGET_SLOT = "ActionFunctional_or_PrimitiveClosedFormFieldEquations"
REQUIRED_STATUS = "INTAKE_SCHEMA_ONLY_NO_EVIDENCE_SUPPLIED"

REQUIRED_BOUNDARIES = {
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
}

NULL_FIELDS = {
    "representation_kind",
    "action_functional",
    "primitive_closed_form_field_equations",
    "state_variables",
    "independent_variables",
    "units_or_normalization",
    "domain_of_validity",
    "derivation_of_model_H_z",
    "parameter_dependencies",
    "source_terms_dependency",
    "boundary_condition_dependency",
    "evidence_path",
    "evidence_sha256",
    "verifier_path",
    "test_path",
    "classification_status",
}

def main() -> None:
    schema = json.loads(SCHEMA.read_text())
    artifact = json.loads(ARTIFACT.read_text())
    blocker = json.loads(BLOCKER.read_text())

    if schema.get("status") != REQUIRED_STATUS:
        raise SystemExit("schema status mismatch")

    if artifact.get("status") != REQUIRED_STATUS:
        raise SystemExit("artifact status mismatch")

    if blocker.get("status") != "FULL_CLOSURE_BLOCKED_CERTIFICATE":
        raise SystemExit("blocker status mismatch")

    if schema.get("target_slot") != TARGET_SLOT:
        raise SystemExit("schema target slot mismatch")

    if artifact.get("target_slot") != TARGET_SLOT:
        raise SystemExit("artifact target slot mismatch")

    if TARGET_SLOT not in blocker.get("missing_required_slots", []):
        raise SystemExit("target slot is not recorded as missing in blocker")

    required = schema.get("required_fields_for_future_packet", {})
    if required.get("slot_name") != TARGET_SLOT:
        raise SystemExit("future packet slot mismatch")

    for key in NULL_FIELDS:
        if required.get(key) is not None:
            raise SystemExit(f"field must remain null in intake schema: {key}")

    if schema.get("currently_supplied") is not False:
        raise SystemExit("schema unexpectedly supplies evidence")

    if schema.get("currently_promoted") is not False:
        raise SystemExit("schema unexpectedly promotes evidence")

    if artifact.get("currently_supplied") is not False:
        raise SystemExit("artifact unexpectedly supplies evidence")

    if artifact.get("currently_promoted") is not False:
        raise SystemExit("artifact unexpectedly promotes evidence")

    boundaries = set(schema.get("does_not_prove", [])) & set(artifact.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing shared boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    print("DFM-MKC action functional / field equations intake schema verification OK.")
    print(f"Status: {schema['status']}")

if __name__ == "__main__":
    main()
