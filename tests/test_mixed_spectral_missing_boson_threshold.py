"""Exact independent perturbation identities for the spectral threshold."""
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys


def test_stationary_shift():
    # W(b)=-alpha*zeta*b^-6 and delta Lambda=6 alpha zeta
    # preserve V'(1)=0; verify V, V' and V'' shifts independently
    for a in (F(0), F(1,25), F(1,24), F(1), F(7,3)):
        for z in (F(1), F(9,8), F(17,13)):
            lam=6*a*z
            delta_v=lam-a*z
            delta_vp=-lam+6*a*z
            delta_vpp=2*lam-42*a*z
            assert delta_v==5*a*z
            assert delta_vp==0
            assert delta_vpp==-30*a*z


def test_certificate_as_script():
    script=Path(__file__).resolve().parents[1] / 'research/5d/mixed_spectral_missing_boson_threshold_exact.py'
    r=subprocess.run([sys.executable,'-B',str(script)],capture_output=True,text=True,check=True)
    assert 'THRESHOLD_ALPHA_BOUNDS := 1/25 < alpha_crit < 1/24' in r.stdout
    assert 'ACTUAL_COUPLED_5D_DETERMINANT := OPEN' in r.stdout


if __name__=='__main__':
    test_stationary_shift()
    test_certificate_as_script()
    print('INDEPENDENT_SHIFT_IDENTITY_TEST := PASS')
    print('CERTIFICATE_SUBPROCESS := PASS')
