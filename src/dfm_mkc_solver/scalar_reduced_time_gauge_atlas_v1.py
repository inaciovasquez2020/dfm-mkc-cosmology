"""Conditional three-chart atlas for the reduced scalar time gauge."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from . import full_scalar_diffeomorphism_generator_v1 as gauge
from . import scalar_spatial_gauge_quotient_v1 as quotient
from . import total_scalar_lapse_shift_hessian_v1 as total


FIELD_ORDER = quotient.QUOTIENT_FIELDS

CHART_PIVOTS = (
    "psi",
    "delta_phi",
    "delta_theta",
)


@dataclass(frozen=True)
class ScalarReducedTimeGaugeAtlasCertificate:
    field_count: int
    chart_count: int
    active_generator_direction_exact: bool
    chart_slices_exact: bool
    chart_maps_orbit_invariant: bool
    transition_maps_exact: bool
    atlas_cover_exact: bool
    global_single_chart_not_assumed: bool
    time_gauge_field_atlas_constructed: bool
    quotient_action_atlas_constructed: bool
    construction_conditional: bool


def _collect_chart_symbols(value, output):
    if isinstance(value, sp.Symbol):
        output.setdefault(str(value), value)
        return

    if isinstance(value, sp.Basic):
        for symbol in value.free_symbols:
            output.setdefault(str(symbol), symbol)
        return

    if isinstance(value, dict):
        for item in value.values():
            _collect_chart_symbols(item, output)
        return

    if isinstance(value, (tuple, list)):
        for item in value:
            _collect_chart_symbols(item, output)


def _time_generator_coefficients():
    generator = gauge.scalar_diffeomorphism_generator()
    z = total._symbols()

    generator_symbols = set().union(
        *(
            expression.free_symbols
            for expression in generator.values()
        )
    )

    time_symbols = tuple(
        symbol
        for symbol in generator_symbols
        if str(symbol) == "T"
    )

    if len(time_symbols) != 1:
        raise ValueError(
            "exact scalar time-gauge parameter was not identified"
        )

    T = time_symbols[0]

    chart_symbols = {}
    _collect_chart_symbols(z, chart_symbols)

    coefficients = {}

    for field in FIELD_ORDER:
        coefficient = sp.cancel(
            sp.diff(generator[field], T)
        )

        symbol_substitution = {
            symbol: chart_symbols[str(symbol)]
            for symbol in coefficient.free_symbols
            if str(symbol) in chart_symbols
        }

        coefficients[field] = sp.cancel(
            coefficient.xreplace(symbol_substitution)
        )

    return coefficients


@lru_cache(maxsize=1)
def reduced_time_gauge_atlas():
    quotient_data = quotient.scalar_spatial_gauge_quotient()

    q = quotient_data["quotient_symbols"]
    coefficients = _time_generator_coefficients()

    chart_domains = {
        pivot: sp.Ne(
            coefficients[pivot],
            0,
            evaluate=False,
        )
        for pivot in CHART_PIVOTS
    }

    atlas_domain = sp.Or(
        *(chart_domains[pivot] for pivot in CHART_PIVOTS),
        evaluate=False,
    )

    chart_shifts = {
        pivot: sp.cancel(
            -q[pivot] / coefficients[pivot]
        )
        for pivot in CHART_PIVOTS
    }

    chart_representatives = {
        pivot: {
            field: sp.cancel(
                q[field]
                + coefficients[field] * chart_shifts[pivot]
            )
            for field in FIELD_ORDER
        }
        for pivot in CHART_PIVOTS
    }

    transition_shifts = {}
    transition_residuals = {}

    for source_pivot in CHART_PIVOTS:
        for target_pivot in CHART_PIVOTS:
            key = (source_pivot, target_pivot)

            transition_shift = sp.cancel(
                -chart_representatives[
                    source_pivot
                ][target_pivot]
                / coefficients[target_pivot]
            )

            transition_shifts[key] = transition_shift

            transition_residuals[key] = {
                field: sp.cancel(
                    chart_representatives[
                        source_pivot
                    ][field]
                    + coefficients[field] * transition_shift
                    - chart_representatives[
                        target_pivot
                    ][field]
                )
                for field in FIELD_ORDER
            }

    orbit_parameter = sp.Symbol(
        "reduced_time_gauge_orbit_parameter"
    )

    orbit_shifted_coordinates = {
        field: sp.Add(
            q[field],
            coefficients[field] * orbit_parameter,
            evaluate=False,
        )
        for field in FIELD_ORDER
    }

    orbit_invariance_residuals = {}

    for pivot in CHART_PIVOTS:
        shifted_chart_parameter = sp.cancel(
            -orbit_shifted_coordinates[pivot]
            / coefficients[pivot]
        )

        orbit_invariance_residuals[pivot] = {
            field: sp.cancel(
                orbit_shifted_coordinates[field]
                + coefficients[field] * shifted_chart_parameter
                - chart_representatives[pivot][field]
            )
            for field in FIELD_ORDER
        }

    return {
        "field_order": FIELD_ORDER,
        "chart_pivots": CHART_PIVOTS,
        "time_generator_coefficients": coefficients,
        "chart_domains": chart_domains,
        "atlas_domain": atlas_domain,
        "chart_shifts": chart_shifts,
        "chart_representatives": chart_representatives,
        "transition_shifts": transition_shifts,
        "transition_residuals": transition_residuals,
        "orbit_parameter": orbit_parameter,
        "orbit_invariance_residuals":
            orbit_invariance_residuals,
    }


@lru_cache(maxsize=1)
def certificate():
    data = reduced_time_gauge_atlas()
    z = total._symbols()

    coefficients = data["time_generator_coefficients"]
    representatives = data["chart_representatives"]

    active_direction_exact = all(
        sp.cancel(actual - expected) == 0
        for actual, expected in (
            (coefficients["psi"], z["H"]),
            (coefficients["delta_phi"], -z["php"]),
            (coefficients["delta_theta"], -z["thp"]),
        )
    )

    slices_exact = all(
        representatives[pivot][pivot] == 0
        for pivot in CHART_PIVOTS
    )

    orbit_invariant = all(
        residual == 0
        for chart_residuals in data[
            "orbit_invariance_residuals"
        ].values()
        for residual in chart_residuals.values()
    )

    transitions_exact = all(
        residual == 0
        for transition_residuals in data[
            "transition_residuals"
        ].values()
        for residual in transition_residuals.values()
    )

    expected_cover = sp.Or(
        sp.Ne(z["H"], 0, evaluate=False),
        sp.Ne(z["php"], 0, evaluate=False),
        sp.Ne(z["thp"], 0, evaluate=False),
        evaluate=False,
    )

    cover_exact = (
        sp.simplify_logic(
            sp.Equivalent(
                data["atlas_domain"],
                expected_cover,
            )
        )
        is sp.true
    )

    constructed = bool(
        len(FIELD_ORDER) == 9
        and len(CHART_PIVOTS) == 3
        and active_direction_exact
        and slices_exact
        and orbit_invariant
        and transitions_exact
        and cover_exact
    )

    return ScalarReducedTimeGaugeAtlasCertificate(
        field_count=len(FIELD_ORDER),
        chart_count=len(CHART_PIVOTS),
        active_generator_direction_exact=active_direction_exact,
        chart_slices_exact=slices_exact,
        chart_maps_orbit_invariant=orbit_invariant,
        transition_maps_exact=transitions_exact,
        atlas_cover_exact=cover_exact,
        global_single_chart_not_assumed=True,
        time_gauge_field_atlas_constructed=constructed,
        quotient_action_atlas_constructed=False,
        construction_conditional=True,
    )
