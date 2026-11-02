"""DESI DR2 13-row BAO shape for the DFM-MKC zero-field dust reference slice.

SOURCE BOUNDARY: This is the reference solution with A_0=phi=0, Lambda_0=0,
gamma_m=0, k=0, dust only, H(z)=H_0*(1+z)**(3/2). It is a
GR/Einstein-de Sitter limit of the supplied DFM-MKC scalar-vector action,
NOT a distinct DFM-MKC prediction, dark-energy fit, or validation.

The file exposes only dimensionless observable *shapes*. Physical predictions
require the independent positive quantity scale=c/(H_0*r_d), which is NOT
specified by the reference parameters or the existing sound-horizon solver.
No data fitting or statistical inference occurs here.

DESI DR2 order: CobayaSampler/bao_data, desi_bao_dr2,
desi_gaussian_bao_ALL_GCcomb_mean.txt (blob 8aff444fdb42c0946342aa0011ab287eda097c4c).
"""

from __future__ import annotations

import math
from typing import Tuple


# Order and observable labels are supplied by the public DESI DR2 13-row file.
DESI_DR2_BAO_ORDER: Tuple[Tuple[float, str], ...] = (
    (0.295, "DV_over_rs"),
    (0.510, "DM_over_rs"),
    (0.510, "DH_over_rs"),
    (0.706, "DM_over_rs"),
    (0.706, "DH_over_rs"),
    (0.934, "DM_over_rs"),
    (0.934, "DH_over_rs"),
    (1.321, "DM_over_rs"),
    (1.321, "DH_over_rs"),
    (1.484, "DM_over_rs"),
    (1.484, "DH_over_rs"),
    (2.330, "DH_over_rs"),
    (2.330, "DM_over_rs"),
)


def dust_reference_bao_shape(z: float, observable: str) -> float:
    """Dimensionless coefficient multiplying c/(H_0*r_d)."""
    if not math.isfinite(z) or z <= 0:
        raise ValueError("redshift must be finite and strictly positive")
    inv_root = 1.0 / math.sqrt(1.0 + z)
    d_m = 2.0 * (1.0 - inv_root)
    d_h = inv_root**3
    if observable == "DM_over_rs":
        return d_m
    if observable == "DH_over_rs":
        return d_h
    if observable == "DV_over_rs":
        return (z * d_m * d_m * d_h) ** (1.0 / 3.0)
    raise ValueError("unknown DESI BAO observable")


def dust_reference_shape_vector() -> Tuple[float, ...]:
    """13 shape coefficients, NOT absolute model predictions."""
    return tuple(dust_reference_bao_shape(z, name) for z, name in DESI_DR2_BAO_ORDER)


def dust_reference_vector_at_scale(c_over_H0_rd: float) -> Tuple[float, ...]:
    """Conditional 13-vector; caller must independently justify scale."""
    if not math.isfinite(c_over_H0_rd) or c_over_H0_rd <= 0:
        raise ValueError("c/(H_0*r_d) must be positive and finite")
    return tuple(c_over_H0_rd * x for x in dust_reference_shape_vector())


def _self_test() -> None:
    # One independent quadrature check of the analytical radial distance.
    # This does not depend on any fitted model or a user-supplied r_d.
    for z in (0.295, 0.706, 1.484, 2.330):
        steps = 4000  # even, for composite Simpson quadrature
        h = z / steps
        weighted_sum = 1.0 + (1.0 + z) ** (-1.5)
        for j in range(1, steps):
            weighted_sum += (4 if j % 2 else 2) * (1 + j * h) ** (-1.5)
        quadrature = weighted_sum * h / 3
        analytic = dust_reference_bao_shape(z, "DM_over_rs")
        assert math.isclose(analytic, quadrature, rel_tol=1e-12, abs_tol=1e-12)
    assert len(DESI_DR2_BAO_ORDER) == len(dust_reference_shape_vector()) == 13
    assert all(math.isfinite(x) and x > 0 for x in dust_reference_shape_vector())
    assert all(math.isclose(a, 2 * b) for a, b in zip(dust_reference_vector_at_scale(2.0), dust_reference_shape_vector()))
    for invalid in (0.0, -1.0, float("nan"), float("inf")):
        try:
            dust_reference_vector_at_scale(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid physical scale accepted")
    print("DESI_DR2_ORDER := 13_ROWS_VERIFIED")
    print("DUST_REFERENCE_DISTANCE_QUADRATURE := PASS")
    print("UNSPECIFIED_SOUND_HORIZON_SCALE := FAIL_CLOSED")
    print("MODEL_VALIDATION := NOT_ESTABLISHED")


if __name__ == "__main__":
    _self_test()
