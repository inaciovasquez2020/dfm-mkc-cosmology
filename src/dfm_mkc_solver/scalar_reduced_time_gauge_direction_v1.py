"""Conditional identification of the reduced scalar time-gauge direction."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from . import full_scalar_diffeomorphism_generator_v1 as gauge
from . import scalar_spatial_gauge_quotient_v1 as quotient
from . import scalar_spatial_gauge_quotient_kinetic_v1 as kinetic
from . import total_scalar_lapse_shift_hessian_v1 as total


ACTIVE_FIELDS = kinetic.ACTIVE_FIELDS


@dataclass(frozen=True)
class ScalarReducedTimeGaugeDirectionCertificate:
    active_field_count: int
    kinetic_generator_residuals_zero: bool
    cofactor_parallelism_residuals_zero: bool
    cofactor_nonzero_on_pivot_domain: bool
    generator_nonzero_domain_required: bool
    rank_domain_required: bool
    time_gauge_direction_identified: bool
    identification_conditional: bool
    time_gauge_quotient_applied: bool
    reduced_field_count: int
    configuration_generator_complete: bool
    first_jet_prolongation_explicit: bool
    first_jet_product_rule_residuals_zero: bool
    full_configuration_restriction_residuals_zero: bool
    full_jet_restriction_residuals_zero: bool
    second_time_parameter_jet_absent: bool


def _symbols_by_name(value):
    symbols = {}

    if isinstance(value, sp.Basic):
        for symbol in value.free_symbols:
            symbols.setdefault(str(symbol), symbol)
    elif isinstance(value, dict):
        for item in value.values():
            symbols.update(_symbols_by_name(item))
    elif isinstance(value, (tuple, list)):
        for item in value:
            symbols.update(_symbols_by_name(item))

    return symbols


@lru_cache(maxsize=1)
def reduced_time_gauge_first_jet_prolongation_data():
    """Restrict the full generator and prolong its reduced time direction."""

    field_order = quotient.QUOTIENT_FIELDS
    full_configuration = gauge.scalar_diffeomorphism_generator()
    full_jets = gauge.scalar_diffeomorphism_jet_generator()
    gauge_symbols = gauge._symbols()
    total_symbols = _symbols_by_name(total._symbols())

    if any(field not in full_configuration for field in field_order):
        raise ValueError("reduced field is absent from the full generator")
    if any(f"{field}_prime" not in full_jets for field in field_order):
        raise ValueError("reduced field jet is absent from the full generator")

    generator_symbols = _symbols_by_name((full_configuration, full_jets))
    time_parameters = tuple(
        symbol for name, symbol in generator_symbols.items()
        if name == "T"
    )
    time_parameter_primes = tuple(
        symbol for name, symbol in generator_symbols.items()
        if name == "T_prime"
    )
    if len(time_parameters) != 1 or len(time_parameter_primes) != 1:
        raise ValueError("time-gauge parameter symbols are not unique")

    T = time_parameters[0]
    T_prime = time_parameter_primes[0]
    T_double_prime = gauge_symbols["T_double_prime"]
    spatial_zero = {
        gauge_symbols["L"]: 0,
        gauge_symbols["L_prime"]: 0,
        gauge_symbols["L_double_prime"]: 0,
    }

    def canonicalize(expression):
        substitution = {
            symbol: total_symbols[str(symbol)]
            for symbol in expression.free_symbols
            if str(symbol) in total_symbols
        }
        return sp.expand(expression.xreplace(substitution))

    restricted_configuration = {
        field: canonicalize(
            full_configuration[field].subs(
                spatial_zero,
                simultaneous=True,
            )
        )
        for field in field_order
    }
    restricted_jets = {
        field: canonicalize(
            full_jets[f"{field}_prime"].subs(
                spatial_zero,
                simultaneous=True,
            )
        )
        for field in field_order
    }
    coefficients = {
        field: sp.simplify(
            sp.diff(restricted_configuration[field], T)
        )
        for field in field_order
    }
    configuration_shifts = {
        field: sp.expand(coefficients[field] * T)
        for field in field_order
    }
    coefficient_derivatives = {
        field: total._D_eta(coefficients[field])
        for field in field_order
    }
    first_jet_shifts = {
        field: sp.expand(
            coefficient_derivatives[field] * T
            + coefficients[field] * T_prime
        )
        for field in field_order
    }

    configuration_residuals = {
        field: sp.simplify(
            restricted_configuration[field]
            - configuration_shifts[field]
        )
        for field in field_order
    }
    product_rule_residuals = {
        field: sp.simplify(
            first_jet_shifts[field]
            - coefficient_derivatives[field] * T
            - coefficients[field] * T_prime
        )
        for field in field_order
    }
    full_jet_residuals = {
        field: sp.simplify(
            restricted_jets[field] - first_jet_shifts[field]
        )
        for field in field_order
    }
    second_jet_absence_residuals = {
        field: sp.simplify(
            sp.diff(first_jet_shifts[field], T_double_prime)
        )
        for field in field_order
    }

    return {
        "field_order": field_order,
        "time_parameter": T,
        "time_parameter_prime": T_prime,
        "configuration_coefficients": coefficients,
        "configuration_shifts": configuration_shifts,
        "coefficient_time_derivatives": coefficient_derivatives,
        "first_jet_shifts": first_jet_shifts,
        "full_generator_configuration_shifts":
            restricted_configuration,
        "full_generator_first_jet_shifts": restricted_jets,
        "configuration_restriction_residuals":
            configuration_residuals,
        "first_jet_product_rule_residuals":
            product_rule_residuals,
        "full_jet_restriction_residuals":
            full_jet_residuals,
        "second_time_parameter_jet_absence_residuals":
            second_jet_absence_residuals,
    }


def _sum_of_squares(values):
    return sp.simplify(sum(
        (sp.simplify(value)) ** 2
        for value in values
    ))


@lru_cache(maxsize=1)
def exact_reduced_time_gauge_first_jet_prolongation_certificate():
    """Return the seven exact residuals for the reduced prolongation."""

    data = reduced_time_gauge_first_jet_prolongation_data()
    z = total._symbols()
    coefficients = data["configuration_coefficients"]
    active_vector = sp.Matrix(
        [coefficients[field] for field in ACTIVE_FIELDS]
    )
    expected_active_vector = sp.Matrix(
        [z["H"], -z["php"], -z["thp"]]
    )

    return {
        "active_psi_direction": sp.simplify(
            coefficients["psi"] - z["H"]
        ),
        "active_radial_direction": sp.simplify(
            coefficients["delta_phi"] + z["php"]
        ),
        "active_phase_direction": sp.simplify(
            coefficients["delta_theta"] + z["thp"]
        ),
        "active_vector_reconstruction": _sum_of_squares(
            active_vector - expected_active_vector
        ),
        "configuration_full_generator_restriction": _sum_of_squares(
            data["configuration_restriction_residuals"].values()
        ),
        "first_jet_product_rule": _sum_of_squares(
            data["first_jet_product_rule_residuals"].values()
        ),
        "first_jet_full_generator_restriction": _sum_of_squares(
            data["full_jet_restriction_residuals"].values()
        ),
    }


@lru_cache(maxsize=1)
def reduced_time_gauge_direction_data():
    rank_data = kinetic.quotient_kinetic_rank_data()
    z = total._symbols()

    active_block = rank_data["active_block"]
    cofactor_vector = rank_data["cofactor_null_vector"]

    reduced_time_generator = sp.Matrix(
        [
            z["H"],
            -z["php"],
            -z["thp"],
        ]
    )

    kinetic_generator_residuals = tuple(
        sp.cancel(value)
        for value in (
            active_block * reduced_time_generator
        )
    )

    cofactor_parallelism_residuals = (
        sp.cancel(
            cofactor_vector[0] * reduced_time_generator[1]
            - cofactor_vector[1] * reduced_time_generator[0]
        ),
        sp.cancel(
            cofactor_vector[0] * reduced_time_generator[2]
            - cofactor_vector[2] * reduced_time_generator[0]
        ),
        sp.cancel(
            cofactor_vector[1] * reduced_time_generator[2]
            - cofactor_vector[2] * reduced_time_generator[1]
        ),
    )

    generator_nonzero_domain = sp.Or(
        sp.Ne(z["H"], 0, evaluate=False),
        sp.Ne(z["php"], 0, evaluate=False),
        sp.Ne(z["thp"], 0, evaluate=False),
        evaluate=False,
    )

    identification_domain = sp.And(
        rank_data["rank_domain"],
        generator_nonzero_domain,
        evaluate=False,
    )

    full_generator = sp.zeros(
        len(kinetic.FIELD_ORDER),
        1,
    )

    for field, value in zip(
        ACTIVE_FIELDS,
        reduced_time_generator,
    ):
        full_generator[
            kinetic.FIELD_ORDER.index(field),
            0,
        ] = value

    return {
        "active_fields": ACTIVE_FIELDS,
        "active_block": active_block,
        "reduced_time_generator": reduced_time_generator,
        "full_reduced_time_generator": full_generator,
        "cofactor_vector": cofactor_vector,
        "pivot_minor": rank_data["pivot_minor"],
        "kinetic_generator_residuals":
            kinetic_generator_residuals,
        "cofactor_parallelism_residuals":
            cofactor_parallelism_residuals,
        "rank_domain": rank_data["rank_domain"],
        "generator_nonzero_domain": generator_nonzero_domain,
        "identification_domain": identification_domain,
        "first_jet_prolongation":
            reduced_time_gauge_first_jet_prolongation_data(),
    }


@lru_cache(maxsize=1)
def certificate():
    data = reduced_time_gauge_direction_data()
    prolongation = data["first_jet_prolongation"]

    kinetic_null_exact = all(
        residual == 0
        for residual in data[
            "kinetic_generator_residuals"
        ]
    )

    parallel_exact = all(
        residual == 0
        for residual in data[
            "cofactor_parallelism_residuals"
        ]
    )

    cofactor_nonzero = (
        sp.cancel(
            data["cofactor_vector"][2]
            - data["pivot_minor"]
        ) == 0
    )

    identified = bool(
        kinetic_null_exact
        and parallel_exact
        and cofactor_nonzero
    )

    return ScalarReducedTimeGaugeDirectionCertificate(
        active_field_count=len(ACTIVE_FIELDS),
        kinetic_generator_residuals_zero=kinetic_null_exact,
        cofactor_parallelism_residuals_zero=parallel_exact,
        cofactor_nonzero_on_pivot_domain=cofactor_nonzero,
        generator_nonzero_domain_required=True,
        rank_domain_required=True,
        time_gauge_direction_identified=identified,
        identification_conditional=True,
        time_gauge_quotient_applied=False,
        reduced_field_count=len(prolongation["field_order"]),
        configuration_generator_complete=(
            len(prolongation["configuration_shifts"])
            == len(prolongation["field_order"])
        ),
        first_jet_prolongation_explicit=(
            len(prolongation["first_jet_shifts"])
            == len(prolongation["field_order"])
        ),
        first_jet_product_rule_residuals_zero=all(
            residual == 0
            for residual in prolongation[
                "first_jet_product_rule_residuals"
            ].values()
        ),
        full_configuration_restriction_residuals_zero=all(
            residual == 0
            for residual in prolongation[
                "configuration_restriction_residuals"
            ].values()
        ),
        full_jet_restriction_residuals_zero=all(
            residual == 0
            for residual in prolongation[
                "full_jet_restriction_residuals"
            ].values()
        ),
        second_time_parameter_jet_absent=all(
            residual == 0
            for residual in prolongation[
                "second_time_parameter_jet_absence_residuals"
            ].values()
        ),
    )
