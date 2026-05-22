import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_external_data_manifest_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_external_data_manifest.py"

def test_manifest_is_source_only():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "EXTERNAL_DATA_MANIFEST_CONSOLIDATED_TARGET_ONLY"
    assert data["claim_level"] == "source_manifest_only"
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False

def test_registered_sources_exist():
    data = json.loads(ARTIFACT.read_text())
    assert data["registered_source_count"] == 3
    ids = {source["id"] for source in data["registered_sources"]}
    assert "DES_SN5YR_0_DATA" in ids
    assert "DES_Y3_MAGNIFICATION_SYSTEMATICS" in ids
    assert "PANTHEON_PLUS_SHOES_1_DATA" in ids
    for source in data["registered_sources"]:
        assert (ROOT / source["path"]).exists()

def test_frozen_prediction_target_is_registered_but_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    target = data["registered_target"]
    assert target["id"] == "DFM_MKC_FROZEN_PREDICTION_MAP_TARGET"
    assert target["status"] == "FROZEN_PREDICTION_MAP_TARGET_ONLY_PREDICTIONS_NOT_SUPPLIED"
    assert data["root_blocker"] == "DFM_FROZEN_PREDICTION_MAP_NOT_SUPPLIED"

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not import numerical data vectors.",
        "Does not validate external payloads.",
        "Does not supply DFM equations.",
        "Does not supply frozen DFM predictions.",
        "Does not execute any likelihood.",
        "Does not produce empirical evidence.",
        "Does not prove DFM.",
        "Does not disprove Lambda-CDM.",
        "Does not replace CDM.",
    ]:
        assert token in boundary

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
