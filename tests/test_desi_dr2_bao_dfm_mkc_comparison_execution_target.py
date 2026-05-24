import json
import subprocess
from pathlib import Path

ART = Path('artifacts/cosmology/desi_dr2_bao_dfm_mkc_comparison_execution_target_2026_05_24.json')
DOC = Path('docs/status/DESI_DR2_BAO_DFM_MKC_COMPARISON_EXECUTION_TARGET_2026_05_24.md')
CFG = Path('configs/cosmology/desi_dr2_bao_dfm_mkc_comparison_target.yaml')

def test_dfm_mkc_comparison_target_status():
    data = json.loads(ART.read_text())
    assert data['status'] == 'COMPARISON_EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN'
    assert data['dataset_id'] == 'DESI_DR2_BAO'
    assert data['baseline_dependency'] == 'DESI_DR2_BAO_LCDM_BASELINE_EXECUTION_TARGET_2026_05_24'
    assert data['intended_likelihood'] == 'bao.desi_dr2.desi_bao_all'
    assert data['intended_theory_backend'] == 'camb'
    assert data['intended_sampler'] == 'evaluate'

def test_dfm_mkc_comparison_config_tokens():
    text = CFG.read_text()
    for token in ['bao.desi_dr2.desi_bao_all', 'camb:', 'omegam:', 'H0:', 'omegab:', 'dfm_mkc_alpha:', 'dfm_mkc_beta:', 'dfm_mkc_gamma:', 'sampler:', 'evaluate:']:
        assert token in text

def test_dfm_mkc_comparison_negative_lock():
    text = DOC.read_text()
    for token in [
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
    ]:
        assert token in text

def test_dfm_mkc_comparison_verifier_passes():
    out = subprocess.check_output(['python3', 'tools/verify_desi_dr2_bao_dfm_mkc_comparison_execution_target.py'], text=True)
    assert 'DESI_DR2_BAO_DFM_MKC_COMPARISON_EXECUTION_TARGET_OK' in out
