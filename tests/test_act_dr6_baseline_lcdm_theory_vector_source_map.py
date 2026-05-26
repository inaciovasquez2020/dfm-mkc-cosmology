import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_theory_vector_source_map_2026_05_25.json")

def test_baseline_lcdm_theory_vector_source_map_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_theory_vector_source_map.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE_MAP_OK" in result.stdout

def test_official_source_route_found_but_vector_still_missing():
    data = json.loads(ART.read_text())
    assert data["status"] == "OFFICIAL_COBAYA_CAMB_SOURCE_MAP_ONLY_NO_VECTOR_ARTIFACT_FOUND"
    assert data["trusted_source_route_found"] is True
    assert data["standalone_official_row_aligned_npz_vector_found"] is False
    assert data["still_missing_objects_after_this_source_map"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]

def test_required_official_sources_are_recorded():
    data = json.loads(ART.read_text())
    sources = data["official_sources_found"]
    assert "ACT_DR6_ACT_LITE_LIKELIHOOD" in sources
    assert "ACT_DR6_PARAMETERS_AND_RUN_SETTINGS" in sources
    assert "NASA_LAMBDA_ACT_DR6_COBAYA_CHAINS" in sources
    assert sources["ACT_DR6_ACT_LITE_LIKELIHOOD"]["head_commit"]
    assert sources["ACT_DR6_PARAMETERS_AND_RUN_SETTINGS"]["head_commit"]

def test_minimal_next_object_is_binding_harness():
    data = json.loads(ART.read_text())
    assert data["minimal_next_object"]["id"] == "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS"
    assert data["minimal_next_object"]["status"] == "MISSING"

def test_no_prediction_or_empirical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "checked NPZ baseline vector artifact exists" in data["does_not_prove"]
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
