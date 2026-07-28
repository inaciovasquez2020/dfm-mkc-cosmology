"""Conditional identification of the reduced scalar time-gauge direction."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

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
    }


@lru_cache(maxsize=1)
def certificate():
    data = reduced_time_gauge_direction_data()

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
    )
