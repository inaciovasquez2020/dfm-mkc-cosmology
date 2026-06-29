#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class CovarianceOrderedPredictionResidualAdapter:
    """
    Finite-patch residual adapter for dfm-mkc-cosmology.

    This computes a bounded diagnostic trace from a covariance block and a
    witness matrix. It does not evaluate gravity, tensor laws, LCDM refutation,
    DFM-MKC validation, or chi-squared closure.
    """

    block_dim: int = 36
    adapter_id: str = "covariance_ordered_prediction_residual_adapter"
    claim_status: str = "diagnostic_field_only_no_tensor_law"

    def map_external_residuals(
        self,
        cov_matrix: np.ndarray,
        witness_matrix: np.ndarray,
    ) -> dict[str, Any]:
        cov = np.asarray(cov_matrix, dtype=float)
        witness = np.asarray(witness_matrix, dtype=float)

        expected = (self.block_dim, self.block_dim)
        if cov.shape != expected:
            raise ValueError(f"Expected {self.block_dim}x{self.block_dim} covariance inputs.")
        if witness.shape != expected:
            raise ValueError(f"Expected {self.block_dim}x{self.block_dim} witness inputs.")
        if not np.allclose(cov, cov.T):
            raise ValueError("Covariance input must be symmetric.")
        if not np.all(np.isfinite(cov)):
            raise ValueError("Covariance input must be finite.")
        if not np.all(np.isfinite(witness)):
            raise ValueError("Witness input must be finite.")

        _, _, vh = np.linalg.svd(witness, full_matrices=True)
        null_vector = vh[-1, :]
        norm = float(np.linalg.norm(null_vector))
        if norm == 0.0:
            raise ValueError("Witness null vector has zero norm.")
        null_vector = null_vector / norm

        p_null = np.outer(null_vector, null_vector)
        adapted_block = p_null @ cov @ p_null.T
        diagnostic_trace = float(np.trace(adapted_block))

        return {
            "adapter_id": self.adapter_id,
            "finite_patch_trace": diagnostic_trace,
            "claim_status": self.claim_status,
            "block_dim": self.block_dim,
            "boundary": [
                "no_LCDM_refutation_claim",
                "no_DFM_MKC_cosmology_validation_claim",
                "no_strict_w0wa_schema_constraint",
                "no_chi_squared_likelihood_closure",
                "diagnostic_field_only_no_tensor_law"
            ],
        }


def deterministic_covariance(block_dim: int = 36, scale: float = 0.02) -> np.ndarray:
    return np.eye(block_dim, dtype=float) * scale


def deterministic_rank_deficient_witness(block_dim: int = 36) -> np.ndarray:
    witness = np.eye(block_dim, dtype=float)
    witness[-1, :] = witness[-2, :]
    return witness


if __name__ == "__main__":
    adapter = CovarianceOrderedPredictionResidualAdapter()
    result = adapter.map_external_residuals(
        deterministic_covariance(adapter.block_dim),
        deterministic_rank_deficient_witness(adapter.block_dim),
    )
    print(
        f"COVARIANCE_ORDERED_PREDICTION_RESIDUAL_ADAPTER_OK "
        f"trace={result['finite_patch_trace']:.17g}"
    )
