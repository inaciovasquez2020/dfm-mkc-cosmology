#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path('artifacts/cosmology/desi_dr2_bao_lcdm_baseline_execution_target_2026_05_24.json')
DOC = Path('docs/status/DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_2026_05_24.md')
CFG = Path('configs/cosmology/desi_dr2_bao_lcdm_baseline_target.yaml')

REQUIRED_CONFIG_TOKENS = [
    'bao.desi_dr2.desi_bao_all',
    'camb:',
    'omegam:',
    'H0:',
    'omegab:',
    'sampler:',
    'evaluate:',
]

REQUIRED_LOCK = [
    'execution target only',
    'no likelihood execution',
    'no posterior chains',
    'no best-fit value',
    'no Lambda-CDM rejection',
    'no DFM-MKC comparison',
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
    'does not produce a likelihood value',
    'does not produce posterior chains',
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

    assert data['record_id'] == 'DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_2026_05_24'
    assert data['status'] == 'EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN'
    assert data['dataset_id'] == 'DESI_DR2_BAO'
    assert data['config_path'] == str(CFG)
    assert data['intended_likelihood'] == 'bao.desi_dr2.desi_bao_all'
    assert data['intended_theory_backend'] == 'camb'
    assert data['intended_sampler'] == 'evaluate'

    for token in REQUIRED_CONFIG_TOKENS:
        assert token in cfg, token

    for token in REQUIRED_LOCK:
        assert token in data['negative_use_lock'], token
        assert token in doc, token

    for token in REQUIRED_BOUNDARY:
        assert token in doc, token

    print('DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_OK')

if __name__ == '__main__':
    main()
