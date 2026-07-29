"""Exact conditional BAO distance and profiled-overlap stability certificate."""

import sympy as sp


def exact_bao_distance_profile_stability_certificate():
    """Return the ten exact residuals in the conditional BAO certificate.

    The certificate assumes a uniform Hubble error on the complete redshift
    interval.  D_H and D_M then inherit O(alpha) errors, and positive linear
    interpolation preserves their bounds.  Away from z=0, D_V inherits an
    O(alpha) error.  Consequently, on the finite ``DESI_DR2_BAO_ROWS``
    redshift set, the frozen 13-row raw dimensional BAO vector differs by
    O(alpha): ``DH_over_rs`` rows use D_H, ``DM_over_rs`` rows use D_M
    (including interpolation), and ``DV_over_rs`` rows use the D_V bound.
    These are Mpc distances before division by a sound horizon.

    Applying the fixed Cholesky whitening map for the positive-definite DESI
    covariance and evaluating the positive-r_d profile at the Lambda-CDM
    ``r_drag`` gives an O(alpha**2) candidate covariance objective.  Since
    the profiled objective is nonnegative and cannot exceed that candidate,
    its manifold infimum is conditionally zero only if the exactly prepared,
    admissible alpha>0 solution family exists on all of 0 <= z <= 2.33 for
    arbitrarily small alpha.

    No exact finite-alpha interior overlap is proved.  No compact canonical
    DFM parameter domain is supplied, and no positive certified separation
    claim is authorized.  In particular, this is algebraic propagation only:
    it performs neither numerical integration nor parameter optimization and
    does not assert existence of the prepared solution family.
    """
    c, H_lcdm, H_floor, epsilon_H = sp.symbols(
        "c H_lcdm H_floor epsilon_H", positive=True
    )
    delta_H = sp.symbols("delta_H", nonnegative=True)
    H_dfm = H_lcdm + delta_H
    D_H_lcdm = c / H_lcdm
    D_H_dfm = c / H_dfm
    U_H = c * epsilon_H / H_floor**2
    distance_difference = D_H_lcdm - D_H_dfm
    distance_identity_rhs = c * delta_H / (H_lcdm * H_dfm)
    distance_majorant_rhs = c * (
        (epsilon_H - delta_H) * H_lcdm * H_dfm
        + delta_H * (H_lcdm * H_dfm - H_floor**2)
    ) / (H_floor**2 * H_lcdm * H_dfm)

    w = sp.symbols("w", nonnegative=True)
    e_left, e_right, U_I = sp.symbols(
        "e_left e_right U_I", nonnegative=True
    )
    e_interp = (1 - w) * e_left + w * e_right

    z, M_dfm, R_dfm, M_upper, R_upper, U_M, U_R, X_floor = sp.symbols(
        "z M_dfm R_dfm M_upper R_upper U_M U_R X_floor", positive=True
    )
    delta_M, delta_R = sp.symbols("delta_M delta_R", nonnegative=True)
    M_lcdm = M_dfm + delta_M
    R_lcdm = R_dfm + delta_R
    X_lcdm = z * M_lcdm**2 * R_lcdm
    X_dfm = z * M_dfm**2 * R_dfm
    D_V_lcdm = X_lcdm ** sp.Rational(1, 3)
    D_V_dfm = X_dfm ** sp.Rational(1, 3)
    cube_root_denominator = (
        X_lcdm ** sp.Rational(2, 3)
        + (X_lcdm * X_dfm) ** sp.Rational(1, 3)
        + X_dfm ** sp.Rational(2, 3)
    )
    X_difference = X_lcdm - X_dfm
    X_difference_rhs = z * (
        delta_M * (M_lcdm + M_dfm) * R_lcdm
        + M_dfm**2 * delta_R
    )
    U_X = z * (
        2 * M_upper * R_upper * U_M + M_upper**2 * U_R
    )
    product_majorant_rhs = z * (
        2 * M_upper * R_upper * (U_M - delta_M)
        + delta_M
        * (
            2 * M_upper * R_upper
            - (M_lcdm + M_dfm) * R_lcdm
        )
        + M_upper**2 * (U_R - delta_R)
        + delta_R * (M_upper**2 - M_dfm**2)
    )
    U_V = U_X / (3 * X_floor ** sp.Rational(2, 3))
    volume_difference = D_V_lcdm - D_V_dfm
    volume_majorant_rhs = (
        (U_X - X_difference) * cube_root_denominator
        + X_difference
        * (
            cube_root_denominator
            - 3 * X_floor ** sp.Rational(2, 3)
        )
    ) / (
        3
        * X_floor ** sp.Rational(2, 3)
        * cube_root_denominator
    )

    epsilon, r_drag = sp.symbols("epsilon r_drag", positive=True)
    k = sp.symbols("k0:13", real=True)
    Q_error = sum((epsilon * k_i) ** 2 for k_i in k)
    K_squared = sum(k_i**2 for k_i in k)
    candidate_profile_objective = Q_error / r_drag**2

    simplify_powers = lambda expression: sp.simplify(
        sp.powdenest(expression, force=True)
    )
    return {
        "hubble_distance_identity": sp.simplify(
            distance_difference - distance_identity_rhs
        ),
        "hubble_distance_majorant_remainder": sp.simplify(
            (U_H - distance_difference) - distance_majorant_rhs
        ),
        "comoving_integrand_identity": sp.simplify(
            (c / H_lcdm - c / H_dfm) - distance_identity_rhs
        ),
        "comoving_integrand_majorant_remainder": sp.simplify(
            (U_H - (c / H_lcdm - c / H_dfm))
            - distance_majorant_rhs
        ),
        "linear_interpolation_majorant_identity": sp.simplify(
            (U_I - e_interp)
            - ((1 - w) * (U_I - e_left) + w * (U_I - e_right))
        ),
        "volume_product_difference": sp.expand(
            X_difference - X_difference_rhs
        ),
        "volume_cube_root_identity": simplify_powers(
            volume_difference * cube_root_denominator - X_difference
        ),
        "volume_product_majorant_remainder": sp.expand(
            (U_X - X_difference) - product_majorant_rhs
        ),
        "volume_distance_majorant_remainder": simplify_powers(
            (U_V - volume_difference) - volume_majorant_rhs
        ),
        "thirteen_row_profile_candidate_scaling": sp.expand(
            candidate_profile_objective
            - epsilon**2 * K_squared / r_drag**2
        ),
    }
