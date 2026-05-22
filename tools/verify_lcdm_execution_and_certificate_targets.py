#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "SOURCE_WEIGHTED_MULTIPROBE_LIKELIHOOD_EXECUTION_PLAN": (
        ROOT / "artifacts/cosmology/source_weighted_multiprobe_likelihood_execution_plan_2026_05_22.json",
        "EXECUTION_PLAN_ONLY_NO_LIKELIHOOD_RUN"
    ),
    "OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE": (
        ROOT / "artifacts/cosmology/out_of_sample_multiprobe_lcdm_rejection_certificate_target_2026_05_22.json",
        "CERTIFICATE_TARGET_ONLY_NO_REJECTION"
    ),
    "EMPIRICAL_PROMOTION_GATE_FOR_LCDM_ALTERNATIVES": (
        ROOT / "artifacts/cosmology/empirical_promotion_gate_for_lcdm_alternatives_2026_05_22.json",
        "PROMOTION_GATE_ONLY_NO_MODEL_PROMOTED"
    )
}

DOCS = [
    ROOT / "docs/status/SOURCE_WEIGHTED_MULTIPROBE_LIKELIHOOD_EXECUTION_PLAN_2026_05_22.md",
    ROOT / "docs/status/OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE_TARGET_2026_05_22.md",
    ROOT / "docs/status/EMPIRICAL_PROMOTION_GATE_FOR_LCDM_ALTERNATIVES_2026_05_22.md"
]

REQUIRED_DOES_NOT_PROVE = {
    "Lambda-CDM failure",
    "six-parameter flat Lambda-CDM rejection",
    "DFM-MKC validation",
    "empirical discovery",
    "any Clay problem"
}

FORBIDDEN_PROMOTION_TOKENS = {
    "LCDM_DISPROVED",
    "LAMBDA_CDM_DISPROVED",
    "EXECUTED_LCDM_REJECTION",
    "DFM_MKC_VALIDATED",
    "EMPIRICAL_DISCOVERY_CLOSED",
    "MODEL_VALIDATED_UNCONDITIONALLY"
}

def main():
    for expected_id, (path, expected_status) in FILES.items():
        assert path.exists(), path
        data = json.loads(path.read_text())
        assert data["id"] == expected_id
        assert data["status"] == expected_status
        assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))
        assert "boundary" in data
        body = json.dumps(data, sort_keys=True)
        for token in FORBIDDEN_PROMOTION_TOKENS:
            assert token not in body, (token, path)

    cert = json.loads(FILES["OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE"][0].read_text())
    assert all(value is False for value in cert["current_evidence_status"].values())
    assert cert["required_next_object"] == "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN"

    plan = json.loads(FILES["SOURCE_WEIGHTED_MULTIPROBE_LIKELIHOOD_EXECUTION_PLAN"][0].read_text())
    assert "GLOBAL_PROFILED_LIKELIHOOD_COMPARISON" in plan["execution_blocks"]
    assert "look_elsewhere_adjusted_sigma" in plan["required_outputs"]

    gate = json.loads(FILES["EMPIRICAL_PROMOTION_GATE_FOR_LCDM_ALTERNATIVES"][0].read_text())
    assert gate["current_promoted_models"] == []
    assert "phenomenological_DFM_MKC_candidate" in gate["candidate_models"]

    for doc in DOCS:
        assert doc.exists(), doc
        text = doc.read_text()
        assert "Does not prove" in text
        assert "Lambda-CDM failure" in text
        assert "any Clay problem" in text

    print("Lambda-CDM execution and certificate target verification OK.")
    print("Status: EXECUTION_AND_CERTIFICATE_TARGETS_ONLY_NO_EMPIRICAL_PROMOTION")
    print("Required next object: EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN")

if __name__ == "__main__":
    main()
