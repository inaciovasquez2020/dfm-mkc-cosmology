import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_row_order_mapping_target_2026_05_25.json")

def test_official_best_fit_vector_row_order_mapping_target_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_official_best_fit_vector_row_order_mapping_target.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET_OK" in result.stdout

def test_mapping_target_remains_open():
    data = json.loads(ART.read_text())
    assert data["status"] == "ROW_ORDER_MAPPING_TARGET_ONLY_NO_MAPPING_SUPPLIED"
    assert data["object_added"]["status"] == "OPEN_TARGET"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING"

def test_required_mapping_schema_is_explicit():
    data = json.loads(ART.read_text())
    fields = {item["id"] for item in data["required_mapping_schema"]["row_mapping_item_fields"]}
    assert {
        "target_index",
        "source_row",
        "source_col",
        "observable_label",
        "frequency_or_spectrum_label",
    } <= fields

def test_mapping_blocks_vector_promotion():
    data = json.loads(ART.read_text())
    assert data["still_missing_objects_after_this_target"] == [
        "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "baseline LCDM prediction vector is row-aligned" in data["does_not_prove"]

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
