import json
import subprocess
from pathlib import Path

import numpy as np

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_extraction_harness_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

def test_official_best_fit_vector_extraction_harness_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_official_best_fit_vector_extraction_harness.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS_OK" in result.stdout

def test_harness_record_does_not_extract_or_promote_vector():
    data = json.loads(ART.read_text())
    assert data["status"] == "EXTRACTION_HARNESS_ONLY_NO_BASELINE_VECTOR_EXTRACTED"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR" in data["still_missing_objects_after_this_harness"]
    assert "baseline LCDM prediction vector has been extracted" in data["does_not_prove"]

def test_harness_can_extract_toy_shape_matching_vector(tmp_path):
    order = json.loads(ORDER.read_text())
    required_len = int(order["ordering_rule"]["required_prediction_vector_shape"][0])

    table = np.arange(required_len * 2, dtype=float).reshape(required_len, 2)
    best_fit = tmp_path / "toy_best_fit.txt"
    np.savetxt(best_fit, table)

    mapping = [
        {"target_index": i, "source_row": i, "source_col": 1}
        for i in range(required_len)
    ]
    mapping_file = tmp_path / "mapping.json"
    mapping_file.write_text(json.dumps({"row_mapping": mapping}, indent=2))

    output = tmp_path / "candidate.json"

    subprocess.run(
        [
            "python3",
            "tools/extract_act_dr6_baseline_lcdm_official_best_fit_vector.py",
            "--best-fit-file",
            str(best_fit),
            "--mapping",
            str(mapping_file),
            "--output",
            str(output),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    candidate = json.loads(output.read_text())
    assert candidate["status"] == "OFFICIAL_BEST_FIT_EXTRACTION_CANDIDATE_ONLY_NOT_BASELINE_VECTOR_PROMOTED"
    assert candidate["vector_shape"] == [required_len]
    assert candidate["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"

def test_harness_rejects_incomplete_mapping(tmp_path):
    order = json.loads(ORDER.read_text())
    required_len = int(order["ordering_rule"]["required_prediction_vector_shape"][0])

    table = np.arange(required_len * 2, dtype=float).reshape(required_len, 2)
    best_fit = tmp_path / "toy_best_fit.txt"
    np.savetxt(best_fit, table)

    mapping_file = tmp_path / "bad_mapping.json"
    mapping_file.write_text(json.dumps({"row_mapping": []}, indent=2))

    result = subprocess.run(
        [
            "python3",
            "tools/extract_act_dr6_baseline_lcdm_official_best_fit_vector.py",
            "--best-fit-file",
            str(best_fit),
            "--mapping",
            str(mapping_file),
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "mapping covers" in result.stderr

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
