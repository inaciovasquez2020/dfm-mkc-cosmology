from pathlib import Path
import json
import subprocess
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_unfixed_2026_05_21.json")

def test_actdr6_numerical_data_unfixed_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_actdr6_numerical_data_unfixed.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DFM-MKC ACTDR6 numerical data unfixed verifier OK." in result.stdout
    assert "ACTDR6_NUMERICAL_DATA_UNFIXED_EXTRACTED_FROM_AUTHENTIC_PAYLOAD" in result.stdout

def test_vector_covariance_and_mask_dimensions():
    data = json.loads(ARTIFACT.read_text())
    assert data["data_vector"]["length"] == 127
    assert len(data["data_vector"]["values"]) == 127
    assert data["covariance_matrix"]["shape"] == [127, 127]
    assert len(data["covariance_matrix"]["values"]) == 127
    assert all(len(row) == 127 for row in data["covariance_matrix"]["values"])
    assert data["mask"]["length"] == 127
    assert data["mask"]["values"] == [True] * 127

def test_hdu_block_lengths_are_exact():
    data = json.loads(ARTIFACT.read_text())
    assert {block["hdu"]: block["length"] for block in data["data_blocks"]} == {
        "data:cl_00": 45,
        "data:cl_0e": 40,
        "data:cl_ee": 42,
    }

def test_boundary_preserves_no_evidence_and_no_promotion():
    data = json.loads(ARTIFACT.read_text())
    assert "numerical data extraction only" in data["boundary"]
    assert "does not bind a DFM-MKC likelihood rule" in data["boundary"]
    assert "does not execute the likelihood" in data["boundary"]
    assert "does not supply empirical evidence" in data["boundary"]
    assert "does not promote any empirical slot" in data["boundary"]
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
