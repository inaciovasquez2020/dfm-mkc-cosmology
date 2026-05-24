import json
import subprocess
from pathlib import Path

CLUSTER = Path("artifacts/cosmology/desi_dr2_bao_execution_readiness_target_cluster_2026_05_24.json")

def test_execution_readiness_cluster_status():
    data = json.loads(CLUSTER.read_text())
    assert data["record_id"] == "DESI_DR2_BAO_EXECUTION_READINESS_TARGET_CLUSTER_2026_05_24"
    assert data["status"] == "TARGET_CLUSTER_ONLY_NO_EXECUTION"
    assert len(data["targets"]) == 5

def test_execution_readiness_cluster_contains_all_targets():
    data = json.loads(CLUSTER.read_text())
    expected = {
        "COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_TARGET_2026_05_24",
        "DFM_MKC_PARAMETER_TO_OBSERVABLE_MAP_TARGET_2026_05_24",
        "DESI_DR2_BAO_LIKELIHOOD_IMPORT_SMOKE_TEST_TARGET_2026_05_24",
        "DESI_DR2_BAO_LCDM_EVALUATE_RUN_OUTPUT_TARGET_2026_05_24",
        "DESI_DR2_BAO_DFM_MKC_EVALUATE_RUN_OUTPUT_TARGET_2026_05_24",
    }
    assert set(data["targets"]) == expected

def test_execution_readiness_cluster_negative_lock():
    data = json.loads(CLUSTER.read_text())
    for token in [
        "no runtime environment certified",
        "no DFM-MKC parameter-to-observable map supplied",
        "no likelihood import smoke test executed",
        "no Lambda-CDM evaluate run executed",
        "no DFM-MKC evaluate run executed",
        "no likelihood execution",
        "no posterior chains",
        "no Lambda-CDM rejection",
        "no DFM-MKC validation",
        "not Chronos proof input",
        "not evidence for P vs NP",
        "not evidence for any Clay problem",
    ]:
        assert token in data["negative_use_lock"]

def test_execution_readiness_targets_verifier_passes():
    out = subprocess.check_output(
        ["python3", "tools/verify_desi_dr2_bao_execution_readiness_targets.py"],
        text=True,
    )
    assert "DESI_DR2_BAO_EXECUTION_READINESS_TARGETS_OK" in out
