#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any

import numpy as np
from astropy.io import fits

PAYLOAD = Path(
    "artifacts/public_payloads/act_lite_numeric_like_extracted_2026_05_21/"
    "DR6-ACT-lite-main__act_dr6_cmbonly__data__act_dr6_cmb_sacc.fits"
)

OUT = Path("artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_unfixed_2026_05_21.json")

STATUS = "ACTDR6_NUMERICAL_DATA_UNFIXED_EXTRACTED_FROM_AUTHENTIC_PAYLOAD"

DATA_HDUS = ["data:cl_00", "data:cl_0e", "data:cl_ee"]
COVARIANCE_HDU = "covariance"

BOUNDARY = [
    "numerical data extraction only",
    "uses ACT-lite SACC FITS payload already present locally",
    "data vector extracted from value columns of data:cl_00, data:cl_0e, and data:cl_ee",
    "covariance matrix extracted from covariance image HDU",
    "mask inferred as all-active because no explicit mask HDU is present",
    "does not bind a DFM-MKC likelihood rule",
    "does not execute the likelihood",
    "does not compute residuals",
    "does not supply empirical evidence",
    "does not promote any empirical slot",
]

DOES_NOT_PROVE = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def sha256_jsonable(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def finite_float_list(values: np.ndarray) -> list[float]:
    arr = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(arr)):
        raise ValueError("non-finite value detected")
    return [float(x) for x in arr.tolist()]

def main() -> None:
    if not PAYLOAD.exists():
        raise SystemExit(f"missing payload: {PAYLOAD}")

    data_blocks = []
    vector_parts = []

    with fits.open(PAYLOAD, memmap=False) as hdul:
        hdu_names = [hdu.name for hdu in hdul]

        for name in DATA_HDUS:
            hdu = hdul[name]
            table = hdu.data
            values = finite_float_list(table["value"])
            ells = [int(x) for x in np.asarray(table["ell"]).tolist()]
            window_ind = [int(x) for x in np.asarray(table["window_ind"]).tolist()]
            block = {
                "hdu": name,
                "length": len(values),
                "columns": list(table.columns.names),
                "tracer_0": [str(x) for x in table["tracer_0"].tolist()],
                "tracer_1": [str(x) for x in table["tracer_1"].tolist()],
                "ell": ells,
                "window_ind": window_ind,
                "value": values,
            }
            data_blocks.append(block)
            vector_parts.extend(values)

        covariance = np.asarray(hdul[COVARIANCE_HDU].data, dtype=float)
        if covariance.shape != (len(vector_parts), len(vector_parts)):
            raise ValueError(f"covariance shape {covariance.shape} incompatible with data length {len(vector_parts)}")
        if not np.all(np.isfinite(covariance)):
            raise ValueError("non-finite covariance entry detected")

        mask = [True] * len(vector_parts)

        payload = {
            "path": str(PAYLOAD),
            "size_bytes": PAYLOAD.stat().st_size,
            "sha256": sha256_file(PAYLOAD),
            "hdu_names": hdu_names,
        }

    extracted = {
        "artifact": "dfm_mkc_actdr6_numerical_data_unfixed",
        "date": "2026-05-21",
        "status": STATUS,
        "predecessor": {
            "pull_request": 105,
            "branch": "analysis/dfm-mkc-act-dr6-authentic-payload-validation-run-2026-05-21",
            "status": "ACT_DR6_PAYLOAD_FILE_PRESENCE_INSPECTED_NO_SCHEMA_VALIDATION",
        },
        "payload": payload,
        "data_vector": {
            "length": len(vector_parts),
            "source_hdus": DATA_HDUS,
            "values": vector_parts,
            "sha256": sha256_jsonable(vector_parts),
        },
        "covariance_matrix": {
            "shape": list(covariance.shape),
            "source_hdu": COVARIANCE_HDU,
            "values": covariance.tolist(),
            "sha256": sha256_jsonable(covariance.tolist()),
        },
        "mask": {
            "length": len(mask),
            "source": "inferred_all_active_no_explicit_mask_hdu",
            "values": mask,
            "sha256": sha256_jsonable(mask),
        },
        "data_blocks": data_blocks,
        "remaining_blocker": "DFM-MKC likelihood rule, field equations, and protocol execution remain unsupplied",
        "boundary": BOUNDARY,
        "does_not_prove": DOES_NOT_PROVE,
    }

    canonical = json.dumps(extracted, sort_keys=True, indent=2)
    extracted["artifact_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()

    OUT.write_text(json.dumps(extracted, sort_keys=True, indent=2) + "\n")
    print("DFM-MKC ACTDR6 numerical data unfixed extraction OK.")
    print(f"Status: {STATUS}")
    print(f"Output: {OUT}")
    print(f"Data length: {len(vector_parts)}")
    print(f"Covariance shape: {covariance.shape}")
    print(f"Payload sha256: {payload['sha256']}")

if __name__ == "__main__":
    main()
