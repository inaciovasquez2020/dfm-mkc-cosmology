from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from dfm_mkc_solver.averaged_matter_growth_suppression_v1 import (
    integrate_averaged_matter_growth_suppression,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (
    ROOT
    / "artifacts"
    / "dfm_mkc"
    / "averaged_matter_growth_suppression_v1.json"
)


def _run(wave_number: float, steps: int = 2048):
    return integrate_averaged_matter_growth_suppression(
        scale_factor_initial=0.25,
        scale_factor_final=1.0,
        steps=steps,
        wave_number=wave_number,
        mass_frequency=2.0,
        hubble_at_unit_scale_factor=1.0,
        gravitational_constant=1.0,
    )


def test_zero_wave_number_recovers_matter_growth():
    certificate = _run(0.0)

    assert math.isclose(
        certificate.final_cdm_growth,
        4.0,
        rel_tol=1.0e-11,
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        certificate.final_dfm_growth,
        certificate.final_cdm_growth,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        certificate.final_growth_ratio,
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )
    assert certificate.maximum_relative_density_scaling_error < 1.0e-10
    assert certificate.maximum_relative_hubble_scaling_error < 1.0e-10
    assert certificate.maximum_friedmann_residual < 1.0e-12
    assert certificate.maximum_cdm_growing_mode_error < 1.0e-10
    assert certificate.all_values_finite is True
    assert certificate.averaged_matter_background_evolved is True
    assert certificate.averaged_dfm_growth_evolved is True
    assert certificate.instantaneous_field_background_evolved is False
    assert certificate.observable_computed is True


def test_suppression_is_scale_dependent():
    certificates = tuple(
        _run(wave_number, steps=4096)
        for wave_number in (0.0, 0.5, 1.0, 1.5)
    )
    ratios = tuple(
        certificate.final_growth_ratio
        for certificate in certificates
    )
    suppressions = tuple(
        certificate.final_growth_suppression
        for certificate in certificates
    )

    assert math.isclose(ratios[0], 1.0, abs_tol=1.0e-12)
    assert ratios[0] > ratios[1] > ratios[2] > ratios[3]
    assert all(0.0 < ratio <= 1.0 for ratio in ratios)
    assert ratios[-1] < 0.8
    assert suppressions[0] == 0.0
    assert suppressions[1] < suppressions[2] < suppressions[3]
    assert suppressions[-1] > 0.25


def test_growth_ratio_has_rk4_refinement():
    coarse = _run(1.5, steps=256)
    medium = _run(1.5, steps=512)
    fine = _run(1.5, steps=1024)

    coarse_medium = abs(
        coarse.final_growth_ratio - medium.final_growth_ratio
    )
    medium_fine = abs(
        medium.final_growth_ratio - fine.final_growth_ratio
    )

    assert coarse_medium > 0.0
    assert medium_fine > 0.0
    assert medium_fine < coarse_medium
    assert math.log(coarse_medium / medium_fine, 2.0) > 3.5


def test_committed_artifact():
    payload = json.loads(ARTIFACT.read_text())

    assert (
        payload["object_id"]
        == "DFM_MKC_AVERAGED_MATTER_GROWTH_SUPPRESSION_V1"
    )
    assert (
        payload["status"]
        == "AVERAGED_MATTER_ERA_GROWTH_SUPPRESSION_COMPUTED"
    )

    cases = payload["cases"]
    assert [case["wave_number"] for case in cases] == [
        0.0,
        0.5,
        1.0,
        1.5,
    ]

    ratios = [case["final_growth_ratio"] for case in cases]
    assert math.isclose(ratios[0], 1.0, abs_tol=1.0e-12)
    assert ratios[0] > ratios[1] > ratios[2] > ratios[3]
    assert ratios[-1] < 0.8

    assert payload["claim_boundaries"] == [
        "The calculation uses the averaged quadratic oscillatory matter branch.",
        "The instantaneous phi/theta background is not evolved.",
        "No Boltzmann hierarchy or observational likelihood is computed.",
        "This is not empirical validation or a dark-matter replacement claim.",
    ]
