#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from solver.background_solver import solve_background
from solver.distances import (
    angular_diameter_distance,
    comoving_distance,
    luminosity_distance,
)

OBJECT_ID = "DFM_MKC_FIVE_HOUR_VALIDATION_STRESS"
STATUS = "LONG_RUN_NUMERICAL_STRESS_CERTIFICATE_NO_THEOREM_CLOSURE"

DOES_NOT_PROVE = [
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "production Boltzmann solver correctness",
    "theorem-level closure",
    "any Clay problem",
]


def _case(seed: int, index: int) -> dict[str, Any]:
    rng = random.Random((seed << 32) + index)

    h0 = rng.uniform(62.0, 78.0)
    omega_m = rng.uniform(0.24, 0.36)
    omega_r = rng.uniform(6.0e-5, 1.2e-4)
    omega_l = rng.uniform(0.61, 0.76)
    alpha = rng.uniform(-0.035, 0.035)
    beta = rng.uniform(-0.02, 0.02)
    zmax = rng.choice([0.5, 1.0, 2.0, 3.0, 5.0])
    nz = rng.choice([128, 192, 256, 384])

    return {
        "params": (h0, omega_m, omega_r, omega_l, alpha, beta),
        "zmax": zmax,
        "nz": nz,
    }


def _hash_arrays(*arrays: np.ndarray) -> str:
    h = hashlib.sha256()
    for arr in arrays:
        h.update(np.asarray(arr, dtype=np.float64).tobytes())
    return h.hexdigest()


def run_case(seed: int, index: int) -> dict[str, Any]:
    spec = _case(seed, index)
    z, hubble, phi = solve_background(spec["zmax"], spec["params"], nz=spec["nz"])

    z = np.asarray(z, dtype=np.float64)
    hubble = np.asarray(hubble, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)

    if z.size != spec["nz"]:
        raise AssertionError(f"unexpected redshift grid size: {z.size} != {spec['nz']}")
    if not np.all(np.isfinite(z)):
        raise AssertionError("non-finite redshift grid")
    if not np.all(np.isfinite(hubble)):
        raise AssertionError("non-finite Hubble output")
    if not np.all(np.isfinite(phi)):
        raise AssertionError("non-finite Phi output")
    if not np.all(hubble > 0.0):
        raise AssertionError("non-positive Hubble output")
    if not np.all(np.diff(z) > 0.0):
        raise AssertionError("redshift grid is not strictly increasing")

    chi = comoving_distance(z, hubble)
    dl = luminosity_distance(z, chi)
    da = angular_diameter_distance(z, chi)

    if not np.all(np.isfinite(chi)):
        raise AssertionError("non-finite comoving distance")
    if not np.all(np.isfinite(dl)):
        raise AssertionError("non-finite luminosity distance")
    if not np.all(np.isfinite(da)):
        raise AssertionError("non-finite angular diameter distance")
    if not np.all(chi >= -1.0e-12):
        raise AssertionError("negative comoving distance")
    if not np.all(np.diff(chi) >= -1.0e-12):
        raise AssertionError("comoving distance is not monotone")
    if not np.all(dl + 1.0e-12 >= chi):
        raise AssertionError("luminosity distance below comoving distance")
    if not np.all(da <= chi + 1.0e-12):
        raise AssertionError("angular diameter distance above comoving distance")

    phi_ratio = np.abs(phi / np.maximum(hubble * hubble, 1.0e-30))
    max_phi_ratio = float(np.max(phi_ratio))
    if not math.isfinite(max_phi_ratio) or max_phi_ratio >= 100.0:
        raise AssertionError(f"unstable Phi/H^2 ratio: {max_phi_ratio}")

    return {
        "case_index": index,
        "zmax": spec["zmax"],
        "nz": spec["nz"],
        "params": [float(x) for x in spec["params"]],
        "hubble_min": float(np.min(hubble)),
        "hubble_max": float(np.max(hubble)),
        "phi_ratio_max": max_phi_ratio,
        "chi_final": float(chi[-1]),
        "result_hash": _hash_arrays(z, hubble, phi, chi, dl, da),
    }


def run_stress(
    *,
    duration_seconds: float,
    seed: int,
    report_path: Path,
    min_cases: int,
    max_cases: int | None,
) -> dict[str, Any]:
    start = time.monotonic()
    deadline = start + duration_seconds
    case_hashes: list[str] = []
    case_seconds: list[float] = []
    endpoints: list[dict[str, Any]] = []
    cases = 0
    interrupted = False

    try:
        while True:
            if max_cases is not None and cases >= max_cases:
                break
            if cases >= min_cases and time.monotonic() >= deadline:
                break

            case_start = time.monotonic()
            result = run_case(seed, cases)
            elapsed = time.monotonic() - case_start

            case_hashes.append(result["result_hash"])
            case_seconds.append(elapsed)
            if cases < 10 or cases % 100 == 0:
                endpoints.append(result)

            cases += 1

            if cases % 1000 == 0:
                print(
                    json.dumps(
                        {
                            "object_id": OBJECT_ID,
                            "cases_completed": cases,
                            "elapsed_seconds": round(time.monotonic() - start, 3),
                            "last_case_seconds": round(elapsed, 6),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    except KeyboardInterrupt:
        interrupted = True

    total_seconds = time.monotonic() - start
    digest = hashlib.sha256("\n".join(case_hashes).encode("utf-8")).hexdigest()

    certificate_status = STATUS
    if interrupted:
        certificate_status = STATUS + "_INTERRUPTED_PARTIAL"

    certificate = {
        "id": OBJECT_ID,
        "status": certificate_status,
        "duration_target_seconds": duration_seconds,
        "duration_observed_seconds": total_seconds,
        "seed": seed,
        "cases_completed": cases,
        "min_cases_required": min_cases,
        "interrupted": interrupted,
        "case_digest": digest,
        "case_seconds": {
            "min": min(case_seconds) if case_seconds else None,
            "mean": statistics.mean(case_seconds) if case_seconds else None,
            "max": max(case_seconds) if case_seconds else None,
        },
        "invariants_checked": [
            "finite redshift grid",
            "strictly increasing redshift grid",
            "finite positive Hubble output",
            "finite Phi output",
            "finite distance outputs",
            "nonnegative monotone comoving distance",
            "luminosity distance dominates comoving distance",
            "angular diameter distance bounded by comoving distance",
            "bounded Phi/H^2 ratio",
        ],
        "sampled_case_records": endpoints,
        "does_not_prove": DOES_NOT_PROVE,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    return certificate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration-seconds", type=float, default=18_000.0)
    parser.add_argument("--seed", type=int, default=20260614)
    parser.add_argument("--min-cases", type=int, default=1)
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path("artifacts/stress/dfm_mkc_five_hour_validation_stress.json"),
    )
    args = parser.parse_args()

    certificate = run_stress(
        duration_seconds=args.duration_seconds,
        seed=args.seed,
        report_path=args.report_path,
        min_cases=args.min_cases,
        max_cases=args.max_cases,
    )
    print(json.dumps(certificate, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
