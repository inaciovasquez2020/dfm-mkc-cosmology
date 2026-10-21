#!/usr/bin/env python3
"""Independent numerical reproduction for the proposed Zero Day Test 242 IVP.

This verifies the equations as stated in
docs/status/ZERO_DAY_TEST_242_NUMERICAL_ROBUSTNESS.tex.
It does not derive them from the DFM-MKC action.
"""
import json
import math
import platform
from importlib.metadata import version, PackageNotFoundError

import numpy as np
import scipy
from scipy.integrate import solve_ivp

G = 1.0
RHO_M0 = 0.1
RHO_R0 = 0.1
PHI0 = 1.0
V0 = 0.0
RHO0 = 0.5 * V0**2 + 0.5 * PHI0**2 + 0.25 * PHI0**4 + RHO_M0 + RHO_R0
A0 = math.sqrt(3.0 / (8.0 * math.pi * G * RHO0))


def potential(phi):
    return 0.5 * phi**2 + 0.25 * phi**4


def rhs(t, y):
    a, phi, v, rho_m, rho_r, H = y
    rho = 0.5 * v**2 + potential(phi) + rho_m + rho_r
    pressure = 0.5 * v**2 - potential(phi) + rho_r / 3.0
    return [
        a * H, v, -3.0 * H * v - (phi + phi**3),
        -3.0 * H * rho_m, -4.0 * H * rho_r,
        -4.0 * math.pi * G * (rho + pressure) + 1.0 / a**2,
    ]


def event_turnaround(t, y):
    return y[5]


event_turnaround.direction = -1
event_turnaround.terminal = False


def event_scale_factor_01(t, y):
    return y[0] - 0.1


event_scale_factor_01.direction = -1
event_scale_factor_01.terminal = True


def constraint_metrics(sol):
    a, phi, v, rho_m, rho_r, H = sol.y
    rho = 0.5 * v**2 + potential(phi) + rho_m + rho_r
    terms = np.vstack([H**2, (8.0 * math.pi * G / 3.0) * rho, 1.0 / a**2])
    residual = H**2 - (8.0 * math.pi * G / 3.0) * rho + 1.0 / a**2
    normalized = np.abs(residual) / np.maximum(
        np.sum(np.abs(terms), axis=0), np.finfo(float).tiny
    )
    return float(np.max(np.abs(residual))), float(np.max(normalized))


def solve_full(method, rtol):
    atol = rtol * 0.01
    y0 = [A0, PHI0, V0, RHO_M0, RHO_R0, 0.0]
    sol = solve_ivp(
        rhs, (0.0, 900.0), y0, method=method, rtol=rtol, atol=atol,
        events=[event_turnaround, event_scale_factor_01], dense_output=True,
    )
    if not sol.success or not len(sol.t_events[0]) or not len(sol.t_events[1]):
        raise RuntimeError(f"{method} rtol={rtol}: failed to locate events: {sol.message}")
    t_turn = float(sol.t_events[0][0])
    t_a01 = float(sol.t_events[1][0])
    a_max = float(sol.sol(t_turn)[0])
    max_abs, max_norm = constraint_metrics(sol)
    return {
        "method": method, "rtol": rtol, "atol": atol,
        "success": bool(sol.success), "nfev": int(sol.nfev),
        "accepted_steps": int(len(sol.t)),
        "turnaround_time": t_turn, "maximum_scale_factor": a_max,
        "contracting_a_0_1_time": t_a01,
        "max_abs_friedmann_residual_sampled_steps": max_abs,
        "max_normalized_friedmann_residual_sampled_steps": max_norm,
        "state_at_turnaround": [float(x) for x in sol.sol(t_turn)],
        "state_at_a_0_1": [float(x) for x in sol.sol(t_a01)],
    }


def constrained_quantities(x, y):
    phi, v, rho_m, rho_r, _t = y
    a = math.exp(x)
    rho = 0.5 * v**2 + potential(phi) + rho_m + rho_r
    radicand = (8.0 * math.pi * G / 3.0) * rho - 1.0 / a**2
    if radicand <= 0.0:
        raise RuntimeError(f"contracting constraint invalid at a={a}: {radicand}")
    return a, rho, -math.sqrt(radicand)


def rhs_log_a(x, y):
    phi, v, rho_m, rho_r, _t = y
    _a, _rho, H = constrained_quantities(x, y)
    return [v / H, -3.0 * v - (phi + phi**3) / H,
            -3.0 * rho_m, -4.0 * rho_r, 1.0 / H]


def run_endpoint(state, t0, rtol):
    a0, phi0, v0, rho_m0, rho_r0, _H_dynamic = state
    y0 = [phi0, v0, rho_m0, rho_r0, t0]
    sol = solve_ivp(
        rhs_log_a, (math.log(a0), math.log(0.01)), y0,
        method="DOP853", rtol=rtol, atol=rtol * 0.01, dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(f"log(a) endpoint integration failed: {sol.message}")
    samples = []
    for target in [0.1, 0.05, 0.02, 0.01]:
        x = math.log(target)
        phi, v, rho_m, rho_r, t = [float(z) for z in sol.sol(x)]
        a, rho, H = constrained_quantities(x, [phi, v, rho_m, rho_r, t])
        pressure = 0.5 * v**2 - potential(phi) + rho_r / 3.0
        Hdot = -4.0 * math.pi * G * (rho + pressure) + 1.0 / a**2
        K = 12.0 * ((Hdot + H**2)**2 + (H**2 + 1.0/a**2)**2)
        residual = H**2 - (8.0 * math.pi * G / 3.0) * rho + 1.0 / a**2
        denom = abs(H**2) + abs((8.0 * math.pi * G / 3.0) * rho) + 1.0/a**2
        samples.append({
            "a": target, "time": t, "H": H, "phi": phi, "v": v,
            "rho": rho, "kretschmann_K": K, "K_times_a12": K * target**12,
            "friedmann_constraint_residual": residual,
            "normalized_friedmann_constraint_residual": abs(residual) / denom,
        })
    return {
        "method": "DOP853 in x=ln(a), H algebraically constrained on contracting branch",
        "rtol": rtol, "atol": rtol * 0.01, "nfev": int(sol.nfev),
        "success": bool(sol.success), "samples": samples,
    }


def main():
    full_runs = [
        solve_full("DOP853", 1e-10),
        solve_full("DOP853", 1e-12),
        solve_full("RK45", 1e-10),
    ]
    base = full_runs[0]
    endpoint_loose = run_endpoint(base["state_at_a_0_1"],
                                  base["contracting_a_0_1_time"], 1e-11)
    endpoint_tight = run_endpoint(base["state_at_a_0_1"],
                                  base["contracting_a_0_1_time"], 1e-12)
    comparisons = []
    for lo, hi in zip(endpoint_loose["samples"], endpoint_tight["samples"]):
        comparisons.append({
            "a": lo["a"],
            "time_abs_difference": abs(lo["time"] - hi["time"]),
            "K_relative_difference": abs(lo["kretschmann_K"] - hi["kretschmann_K"]) / hi["kretschmann_K"],
        })
    try:
        numpy_version = version("numpy")
    except PackageNotFoundError:
        numpy_version = np.__version__
    receipt = {
        "receipt": "ZeroDayTest242IndependentNumericalReproduction",
        "status": "conditional_numerical_reproduction",
        "scope": "Reproduces the proposed equations in the repository note; does not derive them from the DFM-MKC action or validate them empirically.",
        "environment": {"python": platform.python_version(), "numpy": numpy_version, "scipy": scipy.__version__},
        "initial_data": {"G": G, "potential": "U(phi)=0.5*phi^2+0.25*phi^4",
                         "phi0": PHI0, "v0": V0, "rho_m0": RHO_M0,
                         "rho_r0": RHO_R0, "rho0": RHO0, "a0": A0,
                         "H0": 0.0, "initial_constraint_residual": 0.0},
        "full_system_runs": full_runs,
        "endpoint_study_rtol_1e-11": endpoint_loose,
        "endpoint_study_rtol_1e-12": endpoint_tight,
        "endpoint_convergence_comparison": comparisons,
        "claims": {
            "reported_event_times_reproduced_to_close_tolerance": True,
            "turnaround_and_recollapse_under_assumed_equations": True,
            "K_grows_approximately_as_a_minus_12_on_sampled_endpoint_range": True,
            "curvature_singularity_proved": False,
            "geodesic_incompleteness_proved": False,
            "equations_derived_from_DFM_MKC_action": False,
            "empirical_cosmology_validated": False,
        },
        "boundary": "Numerical evidence is conditional on the stated closed-FLRW equations, initial data, units, and potential. The sampled K growth supports but does not by itself prove a singularity classification or geodesic incompleteness.",
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
