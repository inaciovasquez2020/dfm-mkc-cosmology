#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def covariance_matrix(x: np.ndarray) -> np.ndarray:
    if x.ndim != 2:
        raise ValueError("residual matrix must be two-dimensional")
    if x.shape[0] < 2:
        raise ValueError("at least two samples are required")
    centered = x - x.mean(axis=0, keepdims=True)
    return centered.T @ centered / float(x.shape[0] - 1)


def eigensystem(cov: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    return vals[order], vecs[:, order]


def condition_number(vals: np.ndarray, eps: float = 1e-12) -> float:
    positive = vals[vals > eps]
    if positive.size == 0:
        return float("inf")
    return float(positive.max() / positive.min())


def projection_distance(a_vecs: np.ndarray, b_vecs: np.ndarray, k: int) -> float:
    a = a_vecs[:, :k] @ a_vecs[:, :k].T
    b = b_vecs[:, :k] @ b_vecs[:, :k].T
    return float(np.linalg.norm(a - b, ord="fro"))


def rank_from_eigenvalues(vals: np.ndarray, tol: float = 1e-10) -> int:
    return int(np.sum(vals > tol))


def boundary_guard(vals: np.ndarray, expected_dim: int, tol: float = 1e-10) -> bool:
    return rank_from_eigenvalues(vals, tol=tol) == expected_dim and float(vals.min()) > tol


def synthetic_inputs(seed: int = 145) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    baseline = rng.normal(size=(96, 12))
    candidate = baseline.copy()
    candidate[:, 0] += 0.35 * baseline[:, 1]
    candidate[:, 2] -= 0.20 * baseline[:, 3]
    singular = baseline.copy()
    singular[:, 11] = singular[:, 0] + singular[:, 1]
    return baseline, candidate, singular


def run(seed: int, top_k: int) -> dict[str, object]:
    baseline, candidate, singular = synthetic_inputs(seed)

    baseline_cov = covariance_matrix(baseline)
    candidate_cov = covariance_matrix(candidate)
    singular_cov = covariance_matrix(singular)

    baseline_vals, baseline_vecs = eigensystem(baseline_cov)
    candidate_vals, candidate_vecs = eigensystem(candidate_cov)
    singular_vals, _ = eigensystem(singular_cov)

    dim = baseline.shape[1]

    return {
        "status": "SYNTHETIC_HARNESS_ONLY_NO_EMPIRICAL_EVIDENCE",
        "seed": seed,
        "samples": int(baseline.shape[0]),
        "dimension": int(dim),
        "top_k": int(top_k),
        "baseline_rank": rank_from_eigenvalues(baseline_vals),
        "candidate_rank": rank_from_eigenvalues(candidate_vals),
        "singular_failure_rank": rank_from_eigenvalues(singular_vals),
        "baseline_min_eigenvalue": float(baseline_vals.min()),
        "candidate_min_eigenvalue": float(candidate_vals.min()),
        "singular_min_eigenvalue": float(singular_vals.min()),
        "baseline_condition_number": condition_number(baseline_vals),
        "candidate_condition_number": condition_number(candidate_vals),
        "top_eigenspace_projection_distance": projection_distance(
            baseline_vecs,
            candidate_vecs,
            top_k,
        ),
        "boundary_guard_passed": boundary_guard(candidate_vals, dim),
        "synthetic_singular_boundary_guard_passed": boundary_guard(singular_vals, dim),
        "physical_dark_matter_phase_claim_status": "HYPOTHESIS_ONLY",
        "does_not_prove": [
            "DFM-MKC empirical validation",
            "Lambda-CDM failure",
            "dark matter resolution",
            "dark energy resolution",
            "dark matter is liquid",
            "dark matter is solid"
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=145)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    if args.top_k <= 0:
        raise SystemExit("--top-k must be positive")

    result = run(seed=args.seed, top_k=args.top_k)
    text = json.dumps(result, indent=2, sort_keys=True)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
