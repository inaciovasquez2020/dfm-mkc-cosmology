#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/remaining_empirical_execution_closeout_chain_2026_05_22.json"
DOC = ROOT / "docs/status/REMAINING_EMPIRICAL_EXECUTION_CLOSEOUT_CHAIN_2026_05_22.md"

OBJECT = "REMAINING_EMPIRICAL_EXECUTION_CLOSEOUT_CHAIN"
STATUS = "TERMINAL_CLOSEOUT_CHAIN_MATERIALIZED_EXECUTION_BLOCKED_BY_MISSING_REAL_PAYLOADS"
NEXT = "REAL_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_DIGESTS_SCHEMA_PATHS_AND_POLICY_VALUES"

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["object"] == OBJECT
    assert data["status"] == STATUS
    assert data["required_next_object"] == NEXT
    assert data["finish_for_day_status"] == "structural_closeout_complete_empirical_execution_not_started"

    objects = [step["object"] for step in data["closeout_steps"]]
    for obj in [
        "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS",
        "ACTUAL_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS",
        "CERTIFIED_SUPPLIED_RECORDS_COMPATIBLE_WITH_PER_PROBE_TABLE_COVARIANCE_POLICY_AND_MANIFEST",
        "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS",
        "ACTUAL_LIKELIHOOD_EXECUTION",
        "ACTUAL_DFM_MKC_VS_LAMBDA_CDM_COMPARISON",
        "OUT_OF_SAMPLE_REJECTION_OR_VALIDATION_CERTIFICATE",
    ]:
        assert obj in objects

    for payload in [
        "external nuisance-prior source identifiers",
        "release/version tags",
        "SHA-256 digests",
        "schema field paths",
        "cross-covariance policy records",
        "real data paths",
        "executed likelihood outputs",
    ]:
        assert payload in data["terminal_missing_payloads"]

    for phrase in [
        "complete certified multiprobe manifest",
        "likelihood execution",
        "DFM-MKC versus Lambda-CDM comparison",
        "Lambda-CDM rejection",
        "DFM-MKC validation",
        "empirical validation",
        "any Clay problem",
    ]:
        assert phrase in data["does_not_prove"]
        assert phrase in doc

    assert STATUS in doc
    assert NEXT in doc
    print("Remaining empirical execution closeout chain verification OK.")
    print(f"Status: {STATUS}")
    print(f"Required next object: {NEXT}")

if __name__ == "__main__":
    main()
