#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_exhaustive_parameter_table_evidence_packet_2026_05_21.json"
TEMPLATE = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_single_slot_evidence_packet_template_2026_05_21.json"
GATE = ROOT / "artifacts" / "repo_intake" / "dfm_mkc_single_slot_promotion_gate_2026_05_21.json"

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

def main() -> None:
    packet = json.loads(PACKET.read_text())
    template = json.loads(TEMPLATE.read_text())
    gate = json.loads(GATE.read_text())

    if template.get("status") != "TEMPLATE_ONLY_NO_EVIDENCE_SUPPLIED":
        raise SystemExit("template status mismatch")

    if gate.get("status") != "PROMOTION_GATE_ONLY_NO_SLOT_PROMOTED":
        raise SystemExit("promotion gate status mismatch")

    if packet.get("slot_name") != "ExhaustiveParameterTable":
        raise SystemExit("slot mismatch")

    if packet.get("status") != "SUPPLIED_UNVERIFIED_INPUT":
        raise SystemExit("invalid packet status")

    if packet.get("classification_status") != "SUPPLIED_UNVERIFIED_INPUT":
        raise SystemExit("invalid classification status")

    if packet.get("promotion_status") != "NOT_PROMOTED_TO_FULL_CLOSURE":
        raise SystemExit("invalid promotion status")

    evidence = ROOT / packet.get("evidence_path", "")
    if not evidence.exists():
        raise SystemExit(f"missing evidence path: {evidence}")

    observed = hashlib.sha256(evidence.read_bytes()).hexdigest()
    if observed != packet.get("evidence_sha256"):
        raise SystemExit("evidence sha256 mismatch")

    if packet.get("verifier_path") != "tools/verify_dfm_mkc_exhaustive_parameter_table_evidence_packet.py":
        raise SystemExit("verifier path mismatch")

    if packet.get("test_path") != "tests/test_dfm_mkc_exhaustive_parameter_table_evidence_packet.py":
        raise SystemExit("test path mismatch")

    boundaries = set(packet.get("does_not_prove", []))
    if not REQUIRED_BOUNDARIES.issubset(boundaries):
        raise SystemExit(f"missing boundaries: {sorted(REQUIRED_BOUNDARIES - boundaries)}")

    print("DFM-MKC ExhaustiveParameterTable evidence packet verification OK.")
    print(f"Status: {packet['status']}")

if __name__ == "__main__":
    main()
