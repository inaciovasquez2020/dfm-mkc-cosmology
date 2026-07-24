"""Complete uneliminated scalar quadratic action and Euler operator.

The quadratic density is differentiated from the four original-action
expansions in :mod:`total_scalar_lapse_shift_hessian_v1`.  ``DiffOp`` stores
``sum_n c[n] D**n`` with coefficients on the left; in particular ``D`` is
never treated as a commuting polynomial.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import comb

import sympy as sp

from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


FIELD_ORDER = (
    "A", "B", "psi", "E", "delta_phi", "delta_theta",
    "delta_J_b_0", "delta_J_b_L", "delta_ell_b",
    "delta_J_r_0", "delta_J_r_L", "delta_ell_r",
)
ACTION_COMPONENTS = (
    "Einstein-Hilbert plus Gibbons-Hawking-York (ADM)",
    "DFM-MKC scalar amplitude/phase",
    "pressureless baryon Schutz-Sorkin",
    "radiation Schutz-Sorkin",
)
SECTOR_KEYS = ("eh_ghy", "dfm", "b", "r")
SECTOR_PROVENANCE = {
    "eh_ghy": "total_scalar_lapse_shift_hessian_v1._sector_quadratic_densities: ADM Einstein-Hilbert+GHY",
    "dfm": "total_scalar_lapse_shift_hessian_v1._sector_quadratic_densities: canonical DFM-MKC action",
    "b": "visible_sector_action_v1 and visible_sector_offshell_scalar_hessian_v1: pressureless Schutz-Sorkin",
    "r": "visible_sector_action_v1 and visible_sector_offshell_scalar_hessian_v1: radiation Schutz-Sorkin",
}


def total_derivative(expr: sp.Expr, times: int = 1) -> sp.Expr:
    """Apply the declared conformal-time total derivative to a coefficient."""
    answer = sp.sympify(expr)
    for _ in range(times):
        answer = total._D_eta(answer)
    return sp.expand(answer)


@dataclass(frozen=True)
class DiffOp:
    """Exact left-coefficient scalar differential operator."""

    coefficients: tuple[sp.Expr, ...]

    def __post_init__(self):
        values = tuple(sp.expand(sp.sympify(x)) for x in self.coefficients)
        while len(values) > 1 and values[-1] == 0:
            values = values[:-1]
        object.__setattr__(self, "coefficients", values or (sp.Integer(0),))

    @staticmethod
    def scalar(value: sp.Expr) -> "DiffOp":
        return DiffOp((value,))

    def coefficient(self, order: int) -> sp.Expr:
        return self.coefficients[order] if order < len(self.coefficients) else sp.Integer(0)

    def __add__(self, other) -> "DiffOp":
        other = other if isinstance(other, DiffOp) else DiffOp.scalar(other)
        size = max(len(self.coefficients), len(other.coefficients))
        return DiffOp(tuple(self.coefficient(i) + other.coefficient(i) for i in range(size)))

    __radd__ = __add__

    def __neg__(self) -> "DiffOp":
        return DiffOp(tuple(-x for x in self.coefficients))

    def __sub__(self, other) -> "DiffOp":
        return self + (-other if isinstance(other, DiffOp) else -DiffOp.scalar(other))

    def __mul__(self, other) -> "DiffOp":
        """Compose operators, using D^m b=sum binomial D^(m-r)b D^r."""
        other = other if isinstance(other, DiffOp) else DiffOp.scalar(other)
        out = [sp.Integer(0)] * (len(self.coefficients) + len(other.coefficients) - 1)
        for m, a in enumerate(self.coefficients):
            for n, b in enumerate(other.coefficients):
                for r in range(m + 1):
                    out[n + r] += a * comb(m, r) * total_derivative(b, m - r)
        return DiffOp(tuple(out))

    def __rmul__(self, other) -> "DiffOp":
        return DiffOp.scalar(other) * self

    def apply(self, function: sp.Expr, eta: sp.Symbol) -> sp.Expr:
        return sp.expand(sum(c * sp.diff(function, eta, n)
                             for n, c in enumerate(self.coefficients)))

    def adjoint(self) -> "DiffOp":
        out = DiffOp.scalar(0)
        for n, a in enumerate(self.coefficients):
            # (a D^n)^dagger=(-D)^n a, expanded with Leibniz.
            out += DiffOp(tuple(
                (-1) ** n * comb(n, r) * total_derivative(a, n - r)
                for r in range(n + 1)
            ))
        return out

    def simplified(self) -> "DiffOp":
        return DiffOp(tuple(sp.simplify(x) for x in self.coefficients))

    def is_zero(self) -> bool:
        return all(sp.simplify(x) == 0 for x in self.coefficients)


@lru_cache(maxsize=1)
def quadratic_action():
    """Return the exact off-shell quadratic density and its sector summands."""
    sectors = total._sector_quadratic_densities()
    return {
        "density": sp.expand(sum(sectors.values(), sp.Integer(0))),
        "sectors": sectors,
        "fields": FIELD_ORDER,
        "field_jets": total._symbols()["qp"],
        "derivative_order": 1,
        "background_shell": False,
    }


def _operator_from_density(density: sp.Expr, left: int, right: int) -> DiffOp:
    z = total._symbols()
    q, qp = z["q"], z["qp"]
    # Linearization of E_i=L_,qi-D L_,qi' with coefficients kept left.
    a00 = sp.diff(density, q[left], q[right])
    a01 = sp.diff(density, q[left], qp[right])
    a10 = sp.diff(density, qp[left], q[right])
    a11 = sp.diff(density, qp[left], qp[right])
    return DiffOp((
        a00 - total_derivative(a10),
        a01 - a10 - total_derivative(a11),
        -a11,
    ))


@lru_cache(maxsize=1)
def euler_hessian():
    """Return the exact 12x12 off-shell Euler/Hessian operator."""
    density = quadratic_action()["density"]
    return tuple(tuple(_operator_from_density(density, i, j)
                       for j in range(12)) for i in range(12))


@lru_cache(maxsize=1)
def sector_hessians():
    return {
        key: tuple(tuple(_operator_from_density(density, i, j)
                         for j in range(12)) for i in range(12))
        for key, density in quadratic_action()["sectors"].items()
    }


def matrix_adjoint(matrix):
    return tuple(tuple(matrix[j][i].adjoint()
                       for j in range(len(matrix))) for i in range(len(matrix)))


def formal_adjoint_residuals():
    matrix, adjoint = euler_hessian(), matrix_adjoint(euler_hessian())
    return tuple(tuple((matrix[i][j] - adjoint[i][j]).simplified()
                       for j in range(12)) for i in range(12))


def block_provenance():
    """List independently detected action summands for every nonzero block."""
    sectors = sector_hessians()
    return {
        (FIELD_ORDER[i], FIELD_ORDER[j]): tuple(
            SECTOR_PROVENANCE[key] for key in SECTOR_KEYS
            if not sectors[key][i][j].is_zero()
        )
        for i in range(12) for j in range(12)
        if not euler_hessian()[i][j].is_zero()
    }


def row_provenance():
    blocks = block_provenance()
    return {
        field: tuple(sorted({source for (row, _), sources in blocks.items()
                             if row == field for source in sources}))
        for field in FIELD_ORDER
    }


def lapse_shift_subblock_residuals():
    """Compare the A/B rows with the independently exposed merged rows."""
    z = total._symbols()
    out = []
    rows = total.build_total_scalar_lapse_shift_hessian()["rows"]
    for i, name in enumerate(("A", "B")):
        for j, field in enumerate(FIELD_ORDER):
            c0, c1 = rows[name][field]
            out.append((euler_hessian()[i][j] - DiffOp((c0, c1))).simplified())
    return tuple(out)


def lapse_shift_on_shell_residuals():
    """Apply the merged, explicitly labelled shell chart to both A/B sides."""
    substitution = total.on_shell_reduction()["substitution"]
    return tuple(
        DiffOp(tuple(sp.factor(c.subs(substitution, simultaneous=True))
                     for c in residual.coefficients))
        for residual in lapse_shift_subblock_residuals()
    )


def visible_sector_residuals():
    """Use the merged module's independent visible-action comparison."""
    return tuple(sp.simplify(x) for x in total.visible_import_residual())


def dark_principal_residuals():
    z = total._symbols()
    matrix = euler_hessian()
    expected = (z["a"]**2*z["alpha"], z["a"]**2*z["beta"]*z["ph"]**2)
    # Euler operators have -kinetic_matrix*D^2 and +k^2*gradient_matrix.
    return tuple(sp.simplify(matrix[i][i].coefficient(2) + value)
                 for i, value in zip((4, 5), expected))


def certificate():
    matrix = euler_hessian()
    qp = total._symbols()["qp"]
    L2 = quadratic_action()["density"]
    return {
        "canonical_field_order": FIELD_ORDER,
        "action_components": ACTION_COMPONENTS,
        "all_euler_rows_present": all(row_provenance().values()),
        "formal_adjoint_residuals_zero": all(
            op.is_zero() for row in formal_adjoint_residuals() for op in row
        ),
        "lapse_shift_residuals_zero": all(op.is_zero() for op in lapse_shift_subblock_residuals()),
        "lapse_shift_on_shell_residuals_zero": all(
            op.is_zero() for op in lapse_shift_on_shell_residuals()
        ),
        "visible_residuals_zero": all(x == 0 for x in visible_sector_residuals()),
        "dark_principal_residuals_zero": all(x == 0 for x in dark_principal_residuals()),
        "no_lapse_shift_time_kinetics": all(
            sp.diff(L2, qp[i], jet) == 0 for i in (0, 1)
            for jet in total._symbols()["q"] + qp
        ),
        "operator_shape": (len(matrix), len(matrix[0])),
        "F_zero_used": False,
        "gauge_fixing_used": False,
        "constraint_elimination_used": False,
    }
