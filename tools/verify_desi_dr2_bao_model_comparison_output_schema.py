#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path('artifacts/cosmology/desi_dr2_bao_model_comparison_output_schema_2026_05_24.json')
DOC = Path('docs/status/DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_SCHEMA_2026_05_24.md')
SCHEMA = Path('schemas/cosmology/desi_dr2_bao_model_comparison_output_schema_2026_05_24.json')

REQUIRED_SCHEMA_FIELDS = [
    'lcdm_loglike',
    'dfm_mkc_loglike',
    'lcdm_chi2',
    'dfm_mkc_chi2',
    'delta_chi2',
    'AICc',
    'BICc',
    'posterior_predictive_distribution_p',
    'runtime_environment_record',
    'execution_log_digest',
    'boundary',
]

REQUIRED_LOCK = [
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
]

REQUIRED_BOUNDARY = [
    'does not run Cobaya',
    'does not certify Cobaya',
    'does not certify CAMB',
    'does not import the DESI DR2 BAO likelihood',
    'does not execute Lambda-CDM',
    'does not execute DFM-MKC',
    'does not produce lcdm_loglike or dfm_mkc_loglike',
    'does not compute delta_chi2',
    'does not compute AICc',
    'does not compute BICc',
    'does not compare Lambda-CDM against DFM-MKC',
    'does not reject Lambda-CDM',
    'does not validate DFM-MKC',
    'does not provide Chronos proof input',
    'does not prove R1/R2/R3',
    'NON_FACTORISATION',
    'Chronos-RR',
    'H4.1/FGL',
    'P vs NP',
    'Clay problem',
]

def main() -> None:
    data = json.loads(ART.read_text())
    schema = json.loads(SCHEMA.read_text())
    doc = DOC.read_text()

    assert data['record_id'] == 'DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_SCHEMA_2026_05_24'
    assert data['status'] == 'SCHEMA_ONLY_NO_LIKELIHOOD_EXECUTION'
    assert data['dataset_id'] == 'DESI_DR2_BAO'
    assert data['schema_path'] == str(SCHEMA)
    assert data['result_object_target'] == 'DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_RESULT'
    assert schema['$id'] == 'DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_SCHEMA_2026_05_24'
    assert schema['properties']['record_id']['const'] == 'DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_RESULT'

    for token in REQUIRED_SCHEMA_FIELDS:
        assert token in schema['required'], token
        assert token in schema['properties'], token

    for token in ['lcdm_loglike', 'dfm_mkc_loglike']:
        assert token in data['required_loglike_fields'], token
        assert token in doc, token

    for token in ['lcdm_chi2', 'dfm_mkc_chi2', 'delta_chi2']:
        assert token in data['required_chi2_fields'], token
        assert token in doc, token

    for token in ['AICc', 'BICc']:
        assert token in doc, token

    empty = data['example_empty_result']
    assert empty['lcdm_loglike'] is None
    assert empty['dfm_mkc_loglike'] is None
    assert empty['delta_chi2'] is None
    assert empty['AICc'] is None
    assert empty['BICc'] is None

    for token in REQUIRED_LOCK:
        assert token in data['negative_use_lock'], token
        assert token in doc, token
        assert token in empty['boundary'], token

    for token in REQUIRED_BOUNDARY:
        assert token in doc, token

    print('DESI_DR2_BAO_MODEL_COMPARISON_OUTPUT_SCHEMA_OK')

if __name__ == '__main__':
    main()
