import json
import subprocess
from pathlib import Path

ART = Path('artifacts/cosmology/desi_dr2_bao_model_comparison_output_schema_2026_05_24.json')
DOC = Path('docs/status/DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_SCHEMA_2026_05_24.md')
SCHEMA = Path('schemas/cosmology/desi_dr2_bao_model_comparison_output_schema_2026_05_24.json')

def test_model_comparison_schema_status():
    data = json.loads(ART.read_text())
    assert data['status'] == 'SCHEMA_ONLY_NO_LIKELIHOOD_EXECUTION'
    assert data['dataset_id'] == 'DESI_DR2_BAO'
    assert data['result_object_target'] == 'DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_RESULT'

def test_model_comparison_schema_required_fields():
    schema = json.loads(SCHEMA.read_text())
    for token in ['lcdm_loglike', 'dfm_mkc_loglike', 'delta_chi2', 'AICc', 'BICc']:
        assert token in schema['required']
        assert token in schema['properties']

def test_model_comparison_empty_result_is_null_only():
    data = json.loads(ART.read_text())
    empty = data['example_empty_result']
    assert empty['lcdm_loglike'] is None
    assert empty['dfm_mkc_loglike'] is None
    assert empty['delta_chi2'] is None
    assert empty['AICc'] is None
    assert empty['BICc'] is None

def test_model_comparison_negative_lock():
    text = DOC.read_text()
    for token in [
        'schema-only result object',
        'no likelihood execution',
        'no posterior chains',
        'no best-fit value',
        'no delta_chi2 result',
        'no AICc result',
        'no BICc result',
        'no Lambda-CDM rejection',
        'no DFM-MKC validation',
        'not Chronos proof input',
        'not evidence for R1',
        'not evidence for R2',
        'not evidence for R3',
        'not evidence for NON_FACTORISATION',
        'not evidence for Chronos-RR',
        'not evidence for H4.1/FGL',
        'not evidence for P vs NP',
        'not evidence for any Clay problem',
    ]:
        assert token in text

def test_model_comparison_schema_verifier_passes():
    out = subprocess.check_output(['python3', 'tools/verify_desi_dr2_bao_model_comparison_output_schema.py'], text=True)
    assert 'DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_SCHEMA_OK' in out
