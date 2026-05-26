#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from astropy.io import fits


PAYLOAD = Path("data/act_dr6_cmbonly/dr6_data_cmbonly.fits")
OUT = Path("artifacts/dfm_mkc/act_dr6_cmbonly_data_vector_covariance_extraction_2026_05_25.json")


def numeric_array_from_hdu_data(data):
    if data is None:
        return None

    if isinstance(data, np.ndarray) and data.dtype.names is None:
        arr = np.asarray(data)
        if np.issubdtype(arr.dtype, np.number):
            finite = np.isfinite(arr)
            return {
                "shape": list(arr.shape),
                "dtype": str(arr.dtype),
                "size": int(arr.size),
                "finite_count": int(finite.sum()),
                "ndim": int(arr.ndim)
            }

    if hasattr(data, "columns") and getattr(data.columns, "names", None):
        cols = {}
        for name in data.columns.names:
            try:
                arr = np.asarray(data[name])
            except Exception:
                continue
            if np.issubdtype(arr.dtype, np.number):
                cols[name] = {
                    "shape": list(arr.shape),
                    "dtype": str(arr.dtype),
                    "size": int(arr.size),
                    "finite_count": int(np.isfinite(arr).sum()),
                }
        return cols if cols else None

    return None


def main() -> None:
    assert PAYLOAD.exists(), PAYLOAD

    hdu_summaries = []
    numeric_candidates = []

    with fits.open(PAYLOAD) as hdul:
        for idx, hdu in enumerate(hdul):
            data = getattr(hdu, "data", None)
            header = dict(hdu.header)

            entry = {
                "index": idx,
                "name": hdu.name,
                "class": hdu.__class__.__name__,
                "naxis": int(header.get("NAXIS", 0)),
                "shape": list(getattr(data, "shape", []) or []),
                "columns": list(getattr(getattr(data, "columns", None), "names", []) or []),
            }
            hdu_summaries.append(entry)

            numeric = numeric_array_from_hdu_data(data)
            if numeric is not None:
                numeric_candidates.append({
                    "index": idx,
                    "name": hdu.name,
                    "numeric_summary": numeric,
                })

    OUT.write_text(json.dumps({
        "id": "ACT_DR6_CMBONLY_DATA_VECTOR_COVARIANCE_EXTRACTION_2026_05_25",
        "status": "SCHEMA_LEVEL_EXTRACTION_ONLY_NO_EMPIRICAL_COMPARISON",
        "payload_path": str(PAYLOAD),
        "hdu_count": len(hdu_summaries),
        "hdu_summaries": hdu_summaries,
        "numeric_candidate_count": len(numeric_candidates),
        "numeric_candidates": numeric_candidates,
        "data_vector_status": "CANDIDATE_ARRAYS_IDENTIFIED_NOT_PROMOTED",
        "covariance_matrix_status": "CANDIDATE_ARRAYS_IDENTIFIED_NOT_PROMOTED",
        "baseline_lcdm_prediction_vector_status": "NOT_EXTRACTED",
        "dfm_mkc_prediction_vector_status": "NOT_AVAILABLE_NO_DFM_MKC_ACT_SOLVER_BOUND",
        "residual_eigenspace_empirical_run_status": "NOT_RUN",
        "physical_dark_matter_phase_claim_status": "HYPOTHESIS_ONLY",
        "does_not_prove": [
            "ACT DR6 empirical comparison has been run",
            "baseline LCDM prediction vector has been extracted",
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

    print("ACT_DR6_CMBONLY_DATA_VECTOR_COVARIANCE_EXTRACTION_OK")


if __name__ == "__main__":
    main()
