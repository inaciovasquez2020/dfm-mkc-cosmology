"""Verify the dust reference shape; no physical calibration or model fit."""
from dfm_mkc_solver.desi_dr2_reference_bao_vector_v1 import _self_test


def test_desi_dr2_reference_bao_shape():
    _self_test()
