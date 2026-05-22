import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_lcdm_execution_and_certificate_targets.py"

spec = importlib.util.spec_from_file_location("verify_lcdm_execution_and_certificate_targets", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_certificate_target_has_no_evidence_promoted():
    data = json.loads((ROOT / "artifacts/cosmology/out_of_sample_multiprobe_lcdm_rejection_certificate_target_2026_05_22.json").read_text())
    assert data["status"] == "CERTIFICATE_TARGET_ONLY_NO_REJECTION"
    assert all(value is False for value in data["current_evidence_status"].values())
    assert data["required_next_object"] == "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN"

def test_execution_plan_requires_global_comparison():
    data = json.loads((ROOT / "artifacts/cosmology/source_weighted_multiprobe_likelihood_execution_plan_2026_05_22.json").read_text())
    assert data["status"] == "EXECUTION_PLAN_ONLY_NO_LIKELIHOOD_RUN"
    assert "GLOBAL_PROFILED_LIKELIHOOD_COMPARISON" in data["execution_blocks"]
    assert "posterior_predictive_p_value" in data["required_outputs"]

def test_promotion_gate_promotes_nothing():
    data = json.loads((ROOT / "artifacts/cosmology/empirical_promotion_gate_for_lcdm_alternatives_2026_05_22.json").read_text())
    assert data["status"] == "PROMOTION_GATE_ONLY_NO_MODEL_PROMOTED"
    assert data["current_promoted_models"] == []
    assert "MODEL_SPECIFIC_FROZEN_PREDICTION_VECTOR_AND_LIKELIHOOD_RULE" == data["required_next_object"]

def test_boundaries_preserve_no_overclaim():
    paths = [
        ROOT / "artifacts/cosmology/source_weighted_multiprobe_likelihood_execution_plan_2026_05_22.json",
        ROOT / "artifacts/cosmology/out_of_sample_multiprobe_lcdm_rejection_certificate_target_2026_05_22.json",
        ROOT / "artifacts/cosmology/empirical_promotion_gate_for_lcdm_alternatives_2026_05_22.json"
    ]
    for path in paths:
        data = json.loads(path.read_text())
        assert "Lambda-CDM failure" in data["does_not_prove"]
        assert "six-parameter flat Lambda-CDM rejection" in data["does_not_prove"]
        assert "DFM-MKC validation" in data["does_not_prove"]
        assert "any Clay problem" in data["does_not_prove"]
