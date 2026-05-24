#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path('artifacts/cosmology/desi_dr2_bao_dfm_mkc_comparison_execution_target_2026_05_24.json')
DOC = Path('docs/status/DESI_DR2_BAO_DFM_MKC_COMPARISON_EXECUTION_TARGET_2026_05_24.md')
CFG = Path('configs/cosmology/desi_dr2_bao_dfm_mkc_comparison_target.yaml')

REQUIRED_CONFIG_TOKENS = [
    'bao.desi_dr2.desi_bao_all',
    'camb:',
    'omegam:',
    'H0:',
    'omegab:',
    'dfm_mkc_alpha:',
    'dfm_mkc_beta:',
    'dfm_mkc_gamma:',
    'sampler:',
    'evaluate:',
]

REQUIRED_LOCK = [
    'comparison execution target only',
    'no likelihood execution',
    'no posterior chains',
    'no best-fit value',
    'no delta_chi2',
    'no AICc',
    'no BICc',
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
    'does not define the DFM-MKC model implementation',
    'does not define the DFM-MKC parameter-to-observable map',
    'does not import the DESI DR2 BAO likelihood',
    'does not produce a likelihood value',
    'does not produce posterior chains',
    'does not compute delta_chi2, AICc, or BICc',
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
    doc = DOC.read_text()
    cfg = CFG.read_text()

    assert data['record_id'] == 'DESI_DR2_BAO_DFM_MKC_COMPARISON_EXECUTION_TARGET_2026_05_24'
    assert data['status'] == 'COMPARISON_EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN'
    assert data['dataset_id'] == 'DESI_DR2_BAO'
    assert data['baseline_dependency'] == 'DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_2026_05_24'
    assert data['config_path'] == str(CFG)
    assert data['intended_likelihood'] == 'bao.desi_dr2.desi_bao_all'
    assert data['intended_theory_backend'] == 'camb'
    assert data['intended_sampler'] == 'evaluate'

    for token in ['dfm_mkc_alpha', 'dfm_mkc_beta', 'dfm_mkc_gamma']:
        assert token in data['dfm_mkc_placeholder_parameters'], token
        assert token in doc, token

    for token in REQUIRED_CONFIG_TOKENS:
        assert token in cfg, token

    for token in REQUIRED_LOCK:
        assert token in data['negative_use_lock'], token
        assert token in doc, token

    for token in REQUIRED_BOUNDARY:
        assert token in doc, token

    print('DESI_DR2_BAO_DFM_MKC_COMPARISON_EXECUTION_TARGET_OK')

if __name__ == '__main__':
    main()
