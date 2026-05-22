#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/results/dfm_background_solver_synthetic_sanity_check_2026_05_22.csv"


@dataclass(frozen=True)
class DFMParams:
    H0: float = 70.0
    Omega_b0: float = 0.05
    Omega_c0: float = 0.25
    Omega_r0: float = 9.0e-5
    V0: float = 0.69991
    lam: float = 0.0
    beta: float = 0.0
    Phi_i: float = 0.0
    dot_Phi_i: float = 0.0


@dataclass(frozen=True)
class SolverConfig:
    N_initial: float = -3.0
    N_final: float = 0.0
    steps: int = 600
    sanity_tolerance: float = 1.0e-5


State = tuple[float, float, float, float, float]


def potential(phi: float, p: DFMParams) -> float:
    return p.V0 * math.exp(-p.lam * phi)


def hubble_dimensionless(phi: float, pi: float, rho_b: float, rho_c: float, rho_r: float, p: DFMParams) -> float:
    h2 = (rho_b + rho_c + rho_r + 0.5 * pi * pi + potential(phi, p)) / 3.0
    if h2 <= 0.0 or not math.isfinite(h2):
        raise ValueError(f"invalid H^2={h2}")
    return math.sqrt(h2)


def rhs(_N: float, y: State, p: DFMParams) -> State:
    phi, pi, rho_b, rho_c, rho_r = y
    H = hubble_dimensionless(phi, pi, rho_b, rho_c, rho_r, p)
    v = potential(phi, p)

    dphi = pi / H
    dpi = (-3.0 * H * pi + p.lam * v + p.beta * rho_c) / H
    drho_b = -3.0 * rho_b
    drho_c = -3.0 * rho_c - p.beta * rho_c * pi / H
    drho_r = -4.0 * rho_r

    return dphi, dpi, drho_b, drho_c, drho_r


def rk4_step(
    f: Callable[[float, State, DFMParams], State],
    N: float,
    y: State,
    h: float,
    p: DFMParams,
) -> State:
    k1 = f(N, y, p)
    y2 = tuple(yi + 0.5 * h * ki for yi, ki in zip(y, k1))
    k2 = f(N + 0.5 * h, y2, p)
    y3 = tuple(yi + 0.5 * h * ki for yi, ki in zip(y, k2))
    k3 = f(N + 0.5 * h, y3, p)
    y4 = tuple(yi + h * ki for yi, ki in zip(y, k3))
    k4 = f(N + h, y4, p)

    return tuple(
        yi + (h / 6.0) * (a + 2.0 * b + 2.0 * c + d)
        for yi, a, b, c, d in zip(y, k1, k2, k3, k4)
    )


def initial_state(p: DFMParams, cfg: SolverConfig) -> State:
    N = cfg.N_initial
    rho_b = 3.0 * p.Omega_b0 * math.exp(-3.0 * N)
    rho_c = 3.0 * p.Omega_c0 * math.exp(-3.0 * N)
    rho_r = 3.0 * p.Omega_r0 * math.exp(-4.0 * N)
    return p.Phi_i, p.dot_Phi_i, rho_b, rho_c, rho_r


def solve_background(p: DFMParams, cfg: SolverConfig) -> list[dict[str, float]]:
    h = (cfg.N_final - cfg.N_initial) / cfg.steps
    N = cfg.N_initial
    y = initial_state(p, cfg)
    rows: list[dict[str, float]] = []

    for i in range(cfg.steps + 1):
        phi, pi, rho_b, rho_c, rho_r = y
        H = hubble_dimensionless(phi, pi, rho_b, rho_c, rho_r, p)
        a = math.exp(N)
        z = (1.0 / a) - 1.0

        rows.append(
            {
                "step": float(i),
                "N": N,
                "a": a,
                "z": z,
                "Phi": phi,
                "dot_Phi": pi,
                "rho_b": rho_b,
                "rho_c": rho_c,
                "rho_r": rho_r,
                "V": potential(phi, p),
                "H_dimensionless": H,
            }
        )

        if i < cfg.steps:
            y = rk4_step(rhs, N, y, h, p)
            N += h

    return rows


def lambda_cdm_sanity(rows: list[dict[str, float]], p: DFMParams, cfg: SolverConfig) -> dict[str, float | bool]:
    final = rows[-1]
    final_H2 = final["H_dimensionless"] ** 2

    expected_rho_b = 3.0 * p.Omega_b0
    expected_rho_c = 3.0 * p.Omega_c0
    expected_rho_r = 3.0 * p.Omega_r0
    expected_H2 = (expected_rho_b + expected_rho_c + expected_rho_r + p.V0) / 3.0

    abs_H2_error = abs(final_H2 - expected_H2)
    density_error = max(
        abs(final["rho_b"] - expected_rho_b),
        abs(final["rho_c"] - expected_rho_c),
        abs(final["rho_r"] - expected_rho_r),
    )

    return {
        "expected_H2": expected_H2,
        "final_H2": final_H2,
        "abs_H2_error": abs_H2_error,
        "density_error": density_error,
        "final_dot_Phi_abs": abs(final["dot_Phi"]),
        "tolerance": cfg.sanity_tolerance,
        "lambda_cdm_limit_passed": (
            abs_H2_error < cfg.sanity_tolerance
            and density_error < cfg.sanity_tolerance
            and abs(final["dot_Phi"]) < cfg.sanity_tolerance
        ),
    }


def write_csv(rows: list[dict[str, float]], path: Path = OUT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    params = DFMParams()
    cfg = SolverConfig()
    rows = solve_background(params, cfg)
    write_csv(rows)
    sanity = lambda_cdm_sanity(rows, params, cfg)

    payload = {
        "status": "EXECUTABLE_SYNTHETIC_SANITY_CHECK_ONLY_NO_EMPIRICAL_VALIDATION",
        "model": "MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1",
        "parameters": asdict(params),
        "solver_config": asdict(cfg),
        "output_csv": str(OUT.relative_to(ROOT)),
        "sanity": sanity,
        "does_not_prove": [
            "DFM-MKC validation",
            "Lambda-CDM failure",
            "dark matter resolution",
            "dark energy resolution",
            "gravity closure",
            "empirical validation",
            "ACT validation",
            "DESI validation",
            "DES validation",
            "P vs NP",
            "any Clay problem"
        ],
    }

    print(json.dumps(payload, indent=2, sort_keys=True))

    if not sanity["lambda_cdm_limit_passed"]:
        raise SystemExit("Lambda-CDM synthetic sanity check failed")


if __name__ == "__main__":
    main()
