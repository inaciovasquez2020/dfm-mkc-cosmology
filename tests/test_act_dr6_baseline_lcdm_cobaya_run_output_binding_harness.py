import json
import subprocess
from pathlib import Path

import numpy as np

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_cobaya_run_output_binding_harness_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

def test_baseline_lcdm_cobaya_binding_harness_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_cobaya_run_output_binding_harness.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS_OK" in result.stdout

def test_harness_object_is_available_but_no_vector_imported():
    data = json.loads(ART.read_text())
    assert data["status"] == "BINDING_HARNESS_ONLY_NO_BASELINE_VECTOR_IMPORTED"
    assert data["execution_result"] == "NOT_EXECUTED_NO_CANDIDATE_VECTOR_SUPPLIED"
    assert data["object_added"]["id"] == "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS"

def test_harness_accepts_shape_matching_candidate(tmp_path):
    order = json.loads(ORDER.read_text())
    shape = tuple(order["ordering_rule"]["required_prediction_vector_shape"])
    candidate = tmp_path / "candidate.npy"
    output = tmp_path / "binding.json"
    np.save(candidate, np.zeros(shape, dtype=float))

    subprocess.run(
        [
            "python3",
            "tools/bind_act_dr6_baseline_lcdm_cobaya_run_output.py",
            "--candidate",
            str(candidate),
            "--output",
            str(output),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    bound = json.loads(output.read_text())
    assert bound["status"] == "SHAPE_AND_ORDER_BINDING_CANDIDATE_ONLY_NOT_VALIDATED"
    assert bound["candidate_shape"] == list(shape)
    assert bound["ordering_certificate_id"] == order["id"]

def test_harness_rejects_shape_mismatch(tmp_path):
    candidate = tmp_path / "bad_candidate.npy"
    np.save(candidate, np.zeros((3,), dtype=float))

    result = subprocess.run(
        [
            "python3",
            "tools/bind_act_dr6_baseline_lcdm_cobaya_run_output.py",
            "--candidate",
            str(candidate),
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "does not match required shape" in result.stderr

def test_no_prediction_or_empirical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "baseline LCDM prediction vector is official" in data["does_not_prove"]
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
