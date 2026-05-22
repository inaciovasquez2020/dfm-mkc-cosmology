import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_lcdm_rejection_frontier_bundle.py"

spec = importlib.util.spec_from_file_location("verify_lcdm_rejection_frontier_bundle", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_registry_contains_required_blocks():
    path = ROOT / f"artifacts/cosmology/multiprobe_lcdm_rejection_dataset_registry_{module.STAMP}.json"
    data = json.loads(path.read_text())
    assert {"CMB", "BAO", "SN", "GROWTH", "H0", "NEUTRINO_MASS"}.issubset(set(data["dataset_blocks"]))

def test_scorecard_is_not_validated():
    path = ROOT / f"artifacts/cosmology/alternative_model_stability_scorecard_{module.STAMP}.json"
    data = json.loads(path.read_text())
    assert data["status"] == "SCORECARD_ONLY_NO_ALTERNATIVE_VALIDATED"
    assert "phenomenological_DFM_MKC_candidate" in data["candidate_models"]

def test_boundaries_block_overclaim():
    for slug in module.SLUGS:
        data = json.loads((ROOT / "artifacts" / "cosmology" / f"{slug}_{module.STAMP}.json").read_text())
        assert "Lambda-CDM failure" in data["does_not_prove"]
        assert "six-parameter flat Lambda-CDM rejection" in data["does_not_prove"]
        assert "no Lambda-CDM rejection certificate" in data["boundary"]
