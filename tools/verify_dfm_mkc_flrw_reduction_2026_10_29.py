"""Symbolically verify the homogeneous DFM-MKC FLRW identities.

This checks algebraic consequences of the pinned action's equations; it is not
a numerical solver or an observational validation.
"""
from __future__ import annotations

import sympy as sp


def flrw_residuals() -> dict[str, sp.Expr]:
    alpha, beta, phi, phidot, phiddot, theta_dot, theta_ddot, H, Uprime = sp.symbols(
        "alpha beta phi phidot phiddot theta_dot theta_ddot H Uprime",
        nonzero=True,
    )
    rho_dot = (
        alpha * phidot * phiddot
        + beta * phi * phidot * theta_dot**2
        + beta * phi**2 * theta_dot * theta_ddot
        + Uprime * phidot
    )
    amplitude_rhs = -3 * H * phidot + beta * phi * theta_dot**2 / alpha - Uprime / alpha
    phase_rhs = -3 * H * theta_dot - 2 * phidot * theta_dot / phi
    continuity = sp.factor(
        rho_dot.subs({phiddot: amplitude_rhs, theta_ddot: phase_rhs})
        + 3 * H * (alpha * phidot**2 + beta * phi**2 * theta_dot**2)
    )

    G, rho, pressure, rho_dot_total, Hdot, k, a = sp.symbols(
        "G rho pressure rho_dot_total Hdot k a"
    )
    # Derivative of F = H^2 + k/a^2 - (8*pi*G/3)*rho - Lambda/3.
    constraint_derivative = (
        2 * H * (Hdot - k / a**2)
        - sp.Rational(8, 3) * sp.pi * G * rho_dot_total
    )
    einstein_acceleration = -4 * sp.pi * G * (rho + pressure)
    total_continuity = -3 * H * (rho + pressure)
    constraint_propagation = sp.factor(
        constraint_derivative.subs(
            {Hdot: einstein_acceleration + k / a**2, rho_dot_total: total_continuity}
        )
    )
    return {
        "dark_sector_continuity": sp.simplify(continuity),
        "friedmann_constraint_propagation": sp.simplify(constraint_propagation),
    }


def main() -> int:
    residuals = flrw_residuals()
    for name, residual in residuals.items():
        print(f"{name}: {residual}")
    if any(residual != 0 for residual in residuals.values()):
        return 1
    print("PASS: all symbolic FLRW residuals vanish")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
