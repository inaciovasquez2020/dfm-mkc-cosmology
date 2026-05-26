#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, List

import numpy as np

ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
READINESS = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_source_provenance_readiness_2026_05_25.json")
DEFAULT_OUTPUT = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_extraction_candidate.json")

def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()

def sha256_array(arr: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(arr)
    h = hashlib.sha256()
    h.update(str(contiguous.dtype).encode())
    h.update(str(contiguous.shape).encode())
    h.update(contiguous.tobytes())
    return h.hexdigest()

def load_text_table(path: Path) -> np.ndarray:
    try:
        table = np.loadtxt(path, comments="#")
    except Exception as exc:
        raise SystemExit(f"failed to load text table {path}: {exc}")
    if table.ndim == 1:
        table = table.reshape(1, -1)
    return table

def parse_mapping(path: Path) -> List[Dict[str, int]]:
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        rows = data.get("row_mapping")
    else:
        rows = data
    if not isinstance(rows, list):
        raise SystemExit("mapping file must be a list or contain row_mapping list")
    parsed = []
    for item in rows:
        if not isinstance(item, dict):
            raise SystemExit("each mapping row must be an object")
        for key in ["target_index", "source_row", "source_col"]:
            if key not in item:
                raise SystemExit(f"mapping row missing {key}")
        parsed.append({
            "target_index": int(item["target_index"]),
            "source_row": int(item["source_row"]),
            "source_col": int(item["source_col"]),
        })
    return parsed

def build_vector(table: np.ndarray, mapping: List[Dict[str, int]], required_len: int) -> np.ndarray:
    vector = np.full((required_len,), np.nan, dtype=float)
    seen = set()
    for item in mapping:
        target = item["target_index"]
        row = item["source_row"]
        col = item["source_col"]
        if target < 0 or target >= required_len:
            raise SystemExit(f"target_index out of range: {target}")
        if row < 0 or row >= table.shape[0]:
            raise SystemExit(f"source_row out of range: {row}")
        if col < 0 or col >= table.shape[1]:
            raise SystemExit(f"source_col out of range: {col}")
        if target in seen:
            raise SystemExit(f"duplicate target_index: {target}")
        vector[target] = float(table[row, col])
        seen.add(target)
    if len(seen) != required_len:
        raise SystemExit(f"mapping covers {len(seen)} rows, required {required_len}")
    if np.isnan(vector).any():
        raise SystemExit("extracted vector contains NaN")
    return vector

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract an ACT DR6 baseline LCDM vector candidate from an official best-fit spectra text table using an explicit row-order mapping."
    )
    parser.add_argument("--best-fit-file", required=True, help="Official NASA LAMBDA ACT DR6/P-ACT LCDM best-fit spectra text file.")
    parser.add_argument("--mapping", required=True, help="JSON row mapping into the certified ACT DR6 CMB-only row order.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output extraction-candidate JSON.")
    args = parser.parse_args()

    best_fit = Path(args.best_fit_file)
    mapping_path = Path(args.mapping)
    output = Path(args.output)

    if not ORDER.exists():
        raise SystemExit(f"missing ordering certificate: {ORDER}")
    if not READINESS.exists():
        raise SystemExit(f"missing provenance readiness record: {READINESS}")
    if not best_fit.exists():
        raise SystemExit(f"missing best-fit file: {best_fit}")
    if not mapping_path.exists():
        raise SystemExit(f"missing mapping file: {mapping_path}")

    order = json.loads(ORDER.read_text())
    readiness = json.loads(READINESS.read_text())
    required_shape = tuple(order["ordering_rule"]["required_prediction_vector_shape"])
    if len(required_shape) != 1:
        raise SystemExit(f"required prediction vector shape must be 1D, got {required_shape}")

    table = load_text_table(best_fit)
    mapping = parse_mapping(mapping_path)
    vector = build_vector(table, mapping, int(required_shape[0]))

    if tuple(vector.shape) != required_shape:
        raise SystemExit(f"extracted vector shape {vector.shape} does not match required shape {required_shape}")

    best_fit_payload = best_fit.read_bytes()
    mapping_payload = mapping_path.read_bytes()

    record = {
        "id": "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_CANDIDATE",
        "status": "OFFICIAL_BEST_FIT_EXTRACTION_CANDIDATE_ONLY_NOT_BASELINE_VECTOR_PROMOTED",
        "best_fit_file": str(best_fit),
        "best_fit_sha256": sha256_bytes(best_fit_payload),
        "mapping_file": str(mapping_path),
        "mapping_sha256": sha256_bytes(mapping_payload),
        "source_provenance_readiness": str(READINESS),
        "source_provenance_status": readiness["status"],
        "ordering_certificate": str(ORDER),
        "ordering_certificate_id": order["id"],
        "vector_shape": list(vector.shape),
        "vector_dtype": str(vector.dtype),
        "vector_sha256": sha256_array(vector),
        "row_order_binding_rule": "extracted vector entry i is assigned only by explicit mapping target_index i and must correspond to ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE row index i",
        "not_observed_data_vector_basis": "candidate is generated from an official LCDM best-fit spectra source file plus explicit extraction mapping, not from the observed ACT DR6 extracted data_vector artifact",
        "promotion_decision": "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "next_required_validation": "ACT_DR6_BASELINE_LCDM_EXTRACTED_VECTOR_ROW_ORDER_AUDIT",
        "vector_values": vector.tolist(),
        "does_not_prove": [
            "baseline LCDM prediction vector exists",
            "baseline LCDM prediction vector is fully row-audited",
            "baseline LCDM prediction vector is physically correct",
            "DFM-MKC prediction vector exists",
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
