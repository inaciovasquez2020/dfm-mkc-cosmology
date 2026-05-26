#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

PAYLOAD = Path("data/act_dr6_cmbonly/dr6_data_cmbonly.fits")
OUT_NPZ = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_data_covariance_2026_05_25.npz")
OUT_JSON = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_array_extraction_2026_05_25.json")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_with_sacc(path: Path):
    import sacc
    s = sacc.Sacc.load_fits(str(path))
    data_vector = np.asarray(s.mean, dtype=float)
    covariance = np.asarray(s.covariance.covmat, dtype=float)
    return s, data_vector, covariance


def main() -> None:
    assert PAYLOAD.exists(), PAYLOAD

    sacc_obj, data_vector, covariance = load_with_sacc(PAYLOAD)

    assert data_vector.ndim == 1
    assert covariance.ndim == 2
    assert covariance.shape[0] == covariance.shape[1]
    assert covariance.shape[0] == data_vector.shape[0]

    symmetry_error = float(np.max(np.abs(covariance - covariance.T)))
    eigvals = np.linalg.eigvalsh((covariance + covariance.T) / 2.0)
    finite_data = bool(np.isfinite(data_vector).all())
    finite_covariance = bool(np.isfinite(covariance).all())

    OUT_NPZ.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        OUT_NPZ,
        data_vector=data_vector,
        covariance_matrix=covariance,
        covariance_eigenvalues=eigvals,
    )

    OUT_JSON.write_text(json.dumps({
        "id": "ACT_DR6_CMBONLY_OFFICIAL_ARRAY_EXTRACTION_2026_05_25",
        "status": "OFFICIAL_DATA_VECTOR_COVARIANCE_EXTRACTED_NO_MODEL_COMPARISON",
        "payload_path": str(PAYLOAD),
        "payload_sha256": sha256_file(PAYLOAD),
        "array_artifact_path": str(OUT_NPZ),
        "array_artifact_sha256": sha256_file(OUT_NPZ),
        "extraction_backend": "sacc.Sacc.load_fits",
        "data_vector_shape": list(data_vector.shape),
        "covariance_matrix_shape": list(covariance.shape),
        "data_vector_finite": finite_data,
        "covariance_matrix_finite": finite_covariance,
        "covariance_symmetry_max_abs_error": symmetry_error,
        "covariance_min_eigenvalue": float(eigvals.min()),
        "covariance_max_eigenvalue": float(eigvals.max()),
        "covariance_positive_semidefinite_numerical_status": "PASSED" if float(eigvals.min()) >= -1e-8 else "FAILED_OR_REQUIRES_REGULARIZATION",
        "baseline_lcdm_prediction_vector_status": "NOT_AVAILABLE",
        "dfm_mkc_prediction_vector_status": "NOT_AVAILABLE_NO_DFM_MKC_ACT_SOLVER_BOUND",
        "residual_eigenspace_empirical_run_status": "NOT_RUN_REQUIRES_BASELINE_AND_DFM_MKC_PREDICTION_VECTORS",
        "physical_dark_matter_phase_claim_status": "HYPOTHESIS_ONLY",
        "does_not_prove": [
            "baseline LCDM prediction vector exists",
            "DFM-MKC prediction vector exists",
            "residual eigenspace empirical comparison has been run",
            "DFM-MKC empirical validation",
            "Lambda-CDM failure",
            "dark matter resolution",
            "dark energy resolution",
            "dark matter is liquid",
            "dark matter is solid",
            "dark matter phase transition is physically real",
            "ACT validation of DFM-MKC",
            "CMB validation of DFM-MKC",
            "independent empirical replication",
            "gravity closure",
            "Chronos-RR",
            "H4.1/FGL",
            "P vs NP",
            "any Clay problem"
        ]
    }, indent=2, sort_keys=True) + "\n")

    print("ACT_DR6_CMBONLY_OFFICIAL_ARRAY_EXTRACTION_OK")


if __name__ == "__main__":
    main()
