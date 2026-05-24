#!/usr/bin/env python3
import json
from pathlib import Path

TARGETS = [
    ("COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_TARGET_2026_05_24", Path("artifacts/cosmology/cobaya_runtime_environment_certification_target_2026_05_24.json"), Path("docs/status/COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_TARGET_2026_05_24.md")),
    ("DFM_MKC_PARAMETER_TO_OBSERVABLE_MAP_TARGET_2026_05_24", Path("artifacts/cosmology/dfm_mkc_parameter_to_observable_map_target_2026_05_24.json"), Path("docs/status/DFM_MKC_PARAMETER_TO_OBSERVABLE_MAP_TARGET_2026_05_24.md")),
    ("DESI_DR2_BAO_LIKELIHOOD_IMPORT_SMOKE_TEST_TARGET_2026_05_24", Path("artifacts/cosmology/desi_dr2_bao_likelihood_import_smoke_test_target_2026_05_24.json"), Path("docs/status/DESI_DR2_BAO_LIKELIHOOD_IMPORT_SMOKE_TEST_TARGET_2026_05_24.md")),
    ("DESI_DR2_BAO_LCDM_EVALUATE_RUN_OUTPUT_TARGET_2026_05_24", Path("artifacts/cosmology/desi_dr2_bao_lcdm_evaluate_run_output_target_2026_05_24.json"), Path("docs/status/DESI_DR2_BAO_LCDM_EVALUATE_RUN_OUTPUT_TARGET_2026_05_24.md")),
    ("DESI_DR2_BAO_DFM_MKC_EVALUATE_RUN_OUTPUT_TARGET_2026_05_24", Path("artifacts/cosmology/desi_dr2_bao_dfm_mkc_evaluate_run_output_target_2026_05_24.json"), Path("docs/status/DESI_DR2_BAO_DFM_MKC_EVALUATE_RUN_OUTPUT_TARGET_2026_05_24.md")),
]

CLUSTER = Path("artifacts/cosmology/desi_dr2_bao_execution_readiness_target_cluster_2026_05_24.json")
CLUSTER_DOC = Path("docs/status/DESI_DR2_BAO_EXECUTION_READINESS_TARGET_CLUSTER_2026_05_24.md")

REQUIRED_LOCK = [
    "no likelihood execution",
    "no posterior chains",
    "no Lambda-CDM rejection",
    "no DFM-MKC validation",
    "not Chronos proof input",
    "not evidence for R1",
    "not evidence for R2",
    "not evidence for R3",
    "not evidence for NON_FACTORISATION",
    "not evidence for Chronos-RR",
    "not evidence for H4.1/FGL",
    "not evidence for P vs NP",
    "not evidence for any Clay problem",
]

def main() -> None:
    cluster = json.loads(CLUSTER.read_text())
    cluster_doc = CLUSTER_DOC.read_text()

    assert cluster["record_id"] == "DESI_DR2_BAO_EXECUTION_READINESS_TARGET_CLUSTER_2026_05_24"
    assert cluster["status"] == "TARGET_CLUSTER_ONLY_NO_EXECUTION"

    for record_id, artifact_path, doc_path in TARGETS:
        data = json.loads(artifact_path.read_text())
        doc = doc_path.read_text()

        assert data["record_id"] == record_id
        assert data["strand"] == "DFM-MKC / cosmology"
        assert data["dataset_id"] == "DESI_DR2_BAO"
        assert data["required_fields"], record_id
        assert data["pending_outputs"], record_id
        assert data["negative_use_lock"], record_id
        assert data["boundary"], record_id
        assert record_id in cluster["targets"], record_id
        assert record_id in cluster_doc, record_id

        for token in REQUIRED_LOCK:
            assert token in data["negative_use_lock"], (record_id, token)
            assert token in doc, (record_id, token)

    for token in [
        "no runtime environment certified",
        "no DFM-MKC parameter-to-observable map supplied",
        "no likelihood import smoke test executed",
        "no Lambda-CDM evaluate run executed",
        "no DFM-MKC evaluate run executed",
        "no likelihood execution",
        "not Chronos proof input",
    ]:
        assert token in cluster["negative_use_lock"], token
        assert token in cluster_doc, token

    print("DESI_DR2_BAO_EXECUTION_READINESS_TARGETS_OK")

if __name__ == "__main__":
    main()
