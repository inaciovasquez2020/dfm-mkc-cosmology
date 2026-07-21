#!/usr/bin/env python3
from pathlib import Path
import json
import math

import numpy as np

from dfm_mkc_solver import charge_reduced_background_v1 as module


artifact_path = Path(
    "artifacts/dfm_mkc/"
    "dfm_cdm_minimal_circular_solution_receipt_2026_07_21.json"
)
doc_path = Path(
    "docs/status/"
    "DFM_CDM_MINIMAL_CIRCULAR_SOLUTION_RECEIPT_2026_07_21.md"
)

data = json.loads(artifact_path.read_text())
doc = doc_path.read_text()

assert data["status"] == (
    "DFM_CDM_MINIMAL_CIRCULAR_SOLUTION_RECEIPT_2026_07_21"
)
assert data["classification"] == (
    "conditional_numerical_background_calibration_solution"
)
assert data["conditional"] is True
assert data["growth_likelihood_gate"] == "blocked"

solves = data["solves"]
assert solves["conditional_six_equation_background_calibration"] is True
assert solves["growth_likelihood"] is False
assert solves["parameter_to_observable_map"] is False
assert solves["observational_validation"] is False

alpha = float(data["alpha"])
beta = float(data["beta"])
target_w_dfm0 = float(data["target_w_dfm0"])

unit_inputs = data["unit_map_inputs"]
unit_map = module.build_dfm_cdm_unit_map(
    H0_km_s_Mpc=float(unit_inputs["H0_km_s_Mpc"]),
    omega_b0=float(unit_inputs["omega_b0"]),
    omega_cdm0=float(unit_inputs["omega_cdm0"]),
    omega_r0=float(unit_inputs["omega_r0"]),
)

config_data = data["solver_config"]
config = module.ChargeReducedSolverConfig(
    N_initial=float(config_data["N_initial"]),
    N_final=float(config_data["N_final"]),
    samples=int(config_data["samples"]),
    rtol=float(config_data["rtol"]),
    atol=float(config_data["atol"]),
)

candidate = np.asarray(data["candidate_vector"], dtype=float)

assert tuple(data["parameter_names"]) == module.SHOOTING_PARAMETER_NAMES
assert tuple(data["augmented_residual_names"]) == (
    module.DFM_CDM_AUGMENTED_RESIDUAL_NAMES
)
assert tuple(data["shooting_residual_names"]) == (
    module.SHOOTING_RESIDUAL_NAMES
)

phi_initial, v_initial, rho_star, m2, lambda_phi, Q_theta = candidate

assert phi_initial > 0.0
assert Q_theta > 0.0
assert v_initial == 0.0
assert rho_star == 0.0
assert lambda_phi == 0.0

expected_m2 = (
    Q_theta**2
    * math.exp(-6.0 * config.N_initial)
    / (beta * phi_initial**4)
)
assert math.isclose(
    m2,
    expected_m2,
    rel_tol=2.0e-15,
    abs_tol=0.0,
)

augmented = module.dfm_cdm_augmented_residual_vector(
    candidate,
    alpha=alpha,
    beta=beta,
    unit_map=unit_map,
    config=config,
    target_w_dfm0=target_w_dfm0,
)

shooting = module.dfm_cdm_shooting_residual_vector(
    candidate,
    alpha=alpha,
    beta=beta,
    unit_map=unit_map,
    config=config,
    target_w_dfm0=target_w_dfm0,
)

np.testing.assert_allclose(
    augmented,
    np.asarray(data["augmented_residual"], dtype=float),
    rtol=0.0,
    atol=5.0e-13,
)
np.testing.assert_allclose(
    shooting,
    np.asarray(data["shooting_residual_with_F_H"], dtype=float),
    rtol=0.0,
    atol=5.0e-13,
)

maximum_residual = float(np.max(np.abs(augmented)))
assert maximum_residual <= 1.0e-8
assert math.isclose(
    maximum_residual,
    float(data["maximum_absolute_augmented_residual"]),
    rel_tol=0.0,
    abs_tol=5.0e-13,
)

full_record = data["full_augmented_jacobian"]
analysis = module.analyze_dfm_cdm_augmented_jacobian(
    candidate,
    alpha=alpha,
    beta=beta,
    unit_map=unit_map,
    config=config,
    target_w_dfm0=target_w_dfm0,
    relative_step=float(full_record["relative_step"]),
)

assert analysis.rank == 6
assert analysis.locally_identifiable is True
assert np.isfinite(analysis.condition_number)
np.testing.assert_allclose(
    analysis.singular_values,
    np.asarray(full_record["singular_values"], dtype=float),
    rtol=2.0e-7,
    atol=1.0e-10,
)

stability = data["full_jacobian_step_stability"]
full_smallest = []
full_margins = []
full_ranks = set()

for relative_step in stability["relative_steps"]:
    step_analysis = module.analyze_dfm_cdm_augmented_jacobian(
        candidate,
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
        target_w_dfm0=target_w_dfm0,
        relative_step=float(relative_step),
    )
    full_ranks.add(step_analysis.rank)
    smallest = float(step_analysis.singular_values[-1])
    full_smallest.append(smallest)
    full_margins.append(
        smallest / step_analysis.rank_tolerance
    )

assert full_ranks == {6}
assert min(full_margins) > 2.5
assert max(full_smallest) / min(full_smallest) < 1.001

root_log_coordinates = np.asarray(
    data["log_coordinates"],
    dtype=float,
)


def closed_vector(log_coordinates):
    log_phi = float(log_coordinates[0])
    log_charge = float(log_coordinates[1])

    phi = math.exp(log_phi)
    charge = math.exp(log_charge)
    mass_squared = math.exp(
        2.0 * log_charge
        - 4.0 * log_phi
        - 6.0 * config.N_initial
        - math.log(beta)
    )

    return np.asarray(
        (phi, 0.0, 0.0, mass_squared, 0.0, charge),
        dtype=float,
    )


def reduced_residual(log_coordinates):
    return module.dfm_cdm_augmented_residual_vector(
        closed_vector(log_coordinates),
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
        target_w_dfm0=target_w_dfm0,
    )[:2]


determinants = []
conditions = []
reduced_smallest = []

for relative_step in stability["relative_steps"]:
    jacobian = np.empty((2, 2), dtype=float)

    for column in range(2):
        step = float(relative_step) * max(
            1.0,
            abs(float(root_log_coordinates[column])),
        )

        plus = root_log_coordinates.copy()
        minus = root_log_coordinates.copy()
        plus[column] += step
        minus[column] -= step

        jacobian[:, column] = (
            reduced_residual(plus)
            - reduced_residual(minus)
        ) / (2.0 * step)

    singular_values = np.linalg.svd(
        jacobian,
        compute_uv=False,
    )
    determinants.append(float(np.linalg.det(jacobian)))
    conditions.append(float(np.linalg.cond(jacobian)))
    reduced_smallest.append(float(singular_values[-1]))

assert all(np.isfinite(conditions))
assert all(value != 0.0 for value in determinants)
assert all(
    np.sign(value) == np.sign(determinants[0])
    for value in determinants
)
assert min(abs(value) for value in determinants) > 0.3
assert max(conditions) < 20.0
assert max(reduced_smallest) / min(reduced_smallest) < 1.001

assert (
    "Status: "
    "`DFM_CDM_MINIMAL_CIRCULAR_SOLUTION_RECEIPT_2026_07_21`"
    in doc
)
assert "Conditional: `true`" in doc
assert "Growth likelihood remains blocked." in doc
assert (
    "It does not construct the growth observable forward model"
    in doc
)
assert (
    "growth_observable_forward_model_and_likelihood_evaluation_"
    "from_the_converged_background"
    in doc
)

print("DFM_CDM_MINIMAL_CIRCULAR_SOLUTION_RECEIPT_OK")
