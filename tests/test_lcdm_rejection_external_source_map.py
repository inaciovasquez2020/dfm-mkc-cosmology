import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_lcdm_rejection_external_source_map.py"
ARTIFACT = ROOT / "artifacts/cosmology/lcdm_rejection_external_source_map_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_lcdm_rejection_external_source_map", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_source_ids_are_registered():
    data = json.loads(ARTIFACT.read_text())
    ids = {source["id"] for source in data["sources"]}
    assert "KAMELI_BAGHRAM_2025_MODIFIED_INITIAL_POWER_SPECTRUM" in ids
    assert "SHIMON_2026_SMALL_PATCH_HYPOTHESIS" in ids
    assert "BULL_ET_AL_2016_BEYOND_LCDM_REVIEW" in ids

def test_no_promotion_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "EXTERNAL_SOURCE_MAP_ONLY_NO_LCDM_REJECTION"
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "six-parameter flat Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]

def test_next_object_is_likelihood_execution_plan():
    data = json.loads(ARTIFACT.read_text())
    assert data["required_next_object"] == "SOURCE_WEIGHTED_MULTIPROBE_LIKELIHOOD_EXECUTION_PLAN"
