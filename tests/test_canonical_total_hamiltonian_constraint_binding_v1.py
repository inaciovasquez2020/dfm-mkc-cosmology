import sympy as sp

from dfm_mkc_solver import complete_scalar_quadratic_action_v1 as complete
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


def _small_residual(lhs, rhs):
    residual = sp.expand(lhs - rhs)
    if residual != 0:
        residual = sp.cancel(residual)
    if residual != 0:
        residual = sp.simplify(residual)
    return residual


def test_complete_canonical_A_row_equals_total_hamiltonian_constraint():
    assert complete.FIELD_ORDER == total.VARIABLES

    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))
    qpp = {
        name: sp.Symbol(f"{name}_double_prime")
        for name in total.VARIABLES
    }

    row_index = complete.FIELD_ORDER.index("A")
    row = complete.euler_hessian()[row_index]

    canonical_row = sp.Add(
        *(
            operator.coefficient(0) * q[name]
            + operator.coefficient(1) * qp[name]
            + operator.coefficient(2) * qpp[name]
            for name, operator in zip(complete.FIELD_ORDER, row)
        )
    )

    canonical_row = sp.expand(
        canonical_row.subs(
            total.on_shell_reduction()["substitution"],
            simultaneous=True,
        )
    )

    gauge = {
        q["B"]: 0,
        qp["B"]: 0,
        qpp["B"]: 0,
        q["E"]: 0,
        qp["E"]: 0,
        qpp["E"]: 0,
    }
    canonical_row = sp.expand(
        canonical_row.subs(gauge, simultaneous=True)
    )

    metric_kernel = (
        z["k2"] * q["psi"]
        + 3
        * z["H"]
        * (
            qp["psi"]
            + z["H"] * q["A"]
        )
    )

    dark_density = (
        (
            z["alpha"]
            * z["php"]
            * qp["delta_phi"]
            + z["beta"]
            * (
                z["ph"]**2
                * z["thp"]
                * qp["delta_theta"]
                + z["ph"]
                * z["thp"]**2
                * q["delta_phi"]
            )
            - q["A"]
            * (
                z["alpha"] * z["php"]**2
                + z["beta"]
                * z["ph"]**2
                * z["thp"]**2
            )
        )
        / z["a"]**2
        + (
            z["m2"] * z["ph"]
            + z["lam"] * z["ph"]**3
        )
        * q["delta_phi"]
    )

    visible_density = (
        z["mb"] * q["delta_J_b_0"] / z["a"]**3
        + sp.Rational(4, 3)
        * z["kr"]
        * z["Jr"]**sp.Rational(1, 3)
        * q["delta_J_r_0"]
        / z["a"]**4
        + 3
        * z["Jb"]
        * z["mb"]
        * q["psi"]
        / z["a"]**3
        + 4
        * z["kr"]
        * z["Jr"]**sp.Rational(4, 3)
        * q["psi"]
        / z["a"]**4
    )

    expected_row = sp.expand(
        -z["a"]**2
        / (4 * sp.pi * z["G"])
        * (
            metric_kernel
            + 4
            * sp.pi
            * z["G"]
            * z["a"]**2
            * (dark_density + visible_density)
        )
    )

    perturbation_atoms = (
        tuple(q[name] for name in total.VARIABLES)
        + tuple(qp[name] for name in total.VARIABLES)
        + tuple(qpp[name] for name in total.VARIABLES)
    )

    failures = []
    for atom in perturbation_atoms:
        residual = _small_residual(
            canonical_row.coeff(atom),
            expected_row.coeff(atom),
        )
        if residual != 0:
            failures.append((str(atom), residual))

    zero_map = {atom: 0 for atom in perturbation_atoms}
    constant_residual = _small_residual(
        canonical_row.subs(zero_map, simultaneous=True),
        expected_row.subs(zero_map, simultaneous=True),
    )
    if constant_residual != 0:
        failures.append(("constant", constant_residual))

    print(f"COEFFICIENTS_CHECKED := {len(perturbation_atoms) + 1}")
    print(f"NONZERO_COEFFICIENT_RESIDUALS := {len(failures)}")

    assert not failures, "\n".join(
        f"{name}: {residual}"
        for name, residual in failures
    )
