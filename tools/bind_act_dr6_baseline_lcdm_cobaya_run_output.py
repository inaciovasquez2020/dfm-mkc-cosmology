#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
from typing import Optional, Tuple

import numpy as np

ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
DEFAULT_OUTPUT = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_binding_candidate.json")

def sha256_array(arr: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(arr)
    h = hashlib.sha256()
    h.update(str(contiguous.dtype).encode())
    h.update(str(contiguous.shape).encode())
    h.update(contiguous.tobytes())
    return h.hexdigest()

def load_vector(path: Path, key: Optional[str]) -> Tuple[np.ndarray, str]:
    if path.suffix == ".npz":
        npz = np.load(path)
        keys = sorted(npz.files)
        if key is None:
            candidates = [k for k in keys if k in {"theory_vector", "prediction_vector", "baseline_lcdm_prediction_vector", "data_vector"}]
            if not candidates:
                raise SystemExit(f"no admissible vector key found in {path}; keys={keys}")
            key = candidates[0]
        if key not in npz.files:
            raise SystemExit(f"key {key!r} not found in {path}; keys={keys}")
        return np.asarray(npz[key]), key

    if path.suffix == ".npy":
        return np.asarray(np.load(path)), "npy_array"

    if path.suffix == ".json":
        data = json.loads(path.read_text())
        if key is None:
            key = "prediction_vector"
        if key not in data:
            raise SystemExit(f"key {key!r} not found in {path}")
        return np.asarray(data[key]), key

    raise SystemExit(f"unsupported candidate format: {path.suffix}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and bind an ACT DR6 baseline LCDM Cobaya/CAMB prediction-vector candidate to the frozen ACT DR6 row order."
    )
    parser.add_argument("--candidate", required=True, help="Candidate .npz, .npy, or .json vector artifact.")
    parser.add_argument("--key", default=None, help="Optional key for .npz or .json candidate.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output binding-candidate JSON path.")
    args = parser.parse_args()

    candidate = Path(args.candidate)
    output = Path(args.output)

    if not ORDER.exists():
        raise SystemExit(f"missing ordering certificate: {ORDER}")
    if not candidate.exists():
        raise SystemExit(f"missing candidate vector artifact: {candidate}")

    order = json.loads(ORDER.read_text())
    required_shape = tuple(order["ordering_rule"]["required_prediction_vector_shape"])

    vector, vector_key = load_vector(candidate, args.key)
    if vector.ndim != 1:
        raise SystemExit(f"candidate vector must be 1D; got {vector.shape}")
    if tuple(vector.shape) != required_shape:
        raise SystemExit(f"candidate vector shape {vector.shape} does not match required shape {required_shape}")

    record = {
        "id": "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_BINDING_CANDIDATE",
        "status": "SHAPE_AND_ORDER_BINDING_CANDIDATE_ONLY_NOT_VALIDATED",
        "candidate_path": str(candidate),
        "candidate_key": vector_key,
        "candidate_shape": list(vector.shape),
        "candidate_dtype": str(vector.dtype),
        "candidate_sha256": sha256_array(vector),
        "ordering_certificate": str(ORDER),
        "ordering_certificate_id": order["id"],
        "row_binding_rule": "candidate entry i is bound to frozen ACT DR6 CMB-only official data-vector row index i",
        "does_not_prove": [
            "baseline LCDM prediction vector is official",
            "baseline LCDM prediction vector is physically correct",
            "ACT DR6 residual eigenspace empirical comparison has been run",
            "DFM-MKC empirical validation",
            "Lambda-CDM failure"
        ]
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n")
    print(f"WROTE {output}")

if __name__ == "__main__":
    main()
