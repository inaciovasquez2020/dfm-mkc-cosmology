import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_data_comparison_protocol_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_DATA_COMPARISON_PROTOCOL_V1_2026_05_27.md")


def data():
    return json.loads(ART.read_text())


def test_comparison_protocol_status():
    assert data()["id"] == "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1"
    assert data()["status"] == "DATA_COMPARISON_PROTOCOL_SUPPLIED_NO_EMPIRICAL_RUN"
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in data()["source_dependencies"]


def test_datasets_and_contract_declared():
    blob = json.dumps(data(), sort_keys=True)
    assert "ACT DR6" in blob
    assert "Planck" in blob
    assert "DESI" in blob
    assert "LCDM baseline prediction vector" in blob
    assert "DFM-MKC prediction vector" in blob


def test_metrics_declared_without_values():
    metrics = data()["metrics"]
    assert "chi2" in metrics["primary"]
    assert "delta_chi2" in metrics["primary"]
    assert "AIC" in metrics["model_selection"]
    assert "BIC" in metrics["model_selection"]
    assert "whitened_residual_vector" in metrics["diagnostics"]
    assert "no metric values are computed" in metrics["status"].lower()


def test_comparison_acceptance_blocks_claims():
    acceptance = data()["acceptance_test_result"]
    assert acceptance["datasets_declared_present"] is True
    assert acceptance["comparison_contract_present"] is True
    assert acceptance["requires_prediction_vector"] is True
    assert acceptance["numerical_run_supplied"] is False
    assert acceptance["likelihood_values_supplied"] is False
    assert acceptance["empirical_status_promoted"] is False
    assert acceptance["lambda_cdm_failure_promoted"] is False


def test_comparison_boundaries():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC data comparison run" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "Boltzmann solver implementation" in blocked
    assert "any Clay problem" in blocked


def test_comparison_doc():
    text = DOC.read_text()
    assert "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1" in text
    assert "DATA_COMPARISON_PROTOCOL_SUPPLIED_NO_EMPIRICAL_RUN" in text
    assert "Does not prove" in text
