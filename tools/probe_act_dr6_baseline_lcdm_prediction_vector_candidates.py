#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
HARNESS = Path("tools/bind_act_dr6_baseline_lcdm_cobaya_run_output.py")
DEFAULT_OUTPUT = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_result.json")

SEARCH_ROOTS = [
    Path("artifacts/dfm_mkc"),
    Path("chains"),
    Path("runs"),
    Path("data"),
    Path("."),
]

NAME_HINTS = [
    "baseline",
    "lcdm",
    "lambda",
    "theory",
    "prediction",
    "camb",
    "cobaya",
    "act",
    "dr6",
]

VECTOR_KEYS = [
    "baseline_lcdm_prediction_vector",
    "prediction_vector",
    "theory_vector",
    "lcdm_prediction_vector",
    "data_vector",
]

def required_shape() -> Tuple[int, ...]:
    order = json.loads(ORDER.read_text())
    return tuple(order["ordering_rule"]["required_prediction_vector_shape"])

def name_score(path: Path) -> int:
    lower = str(path).lower()
    return sum(1 for hint in NAME_HINTS if hint in lower)

def discover_files() -> List[Path]:
    found = []
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for suffix in ("*.npz", "*.npy", "*.json"):
            found.extend(root.rglob(suffix))
    return sorted(set(found), key=lambda p: (-name_score(p), str(p)))

def inspect_candidate(path: Path, shape: Tuple[int, ...]) -> Dict[str, object]:
    record: Dict[str, object] = {
        "path": str(path),
        "suffix": path.suffix,
        "name_score": name_score(path),
        "matching_vectors": [],
        "rejected_vectors": [],
        "error": None,
    }

    try:
        if path.suffix == ".npy":
            arr = np.asarray(np.load(path))
            item = {"key": "npy_array", "shape": list(arr.shape), "ndim": int(arr.ndim)}
            if arr.ndim == 1 and tuple(arr.shape) == shape:
                record["matching_vectors"].append(item)
            else:
                record["rejected_vectors"].append(item)

        elif path.suffix == ".npz":
            npz = np.load(path)
            for key in sorted(npz.files):
                arr = np.asarray(npz[key])
                item = {"key": key, "shape": list(arr.shape), "ndim": int(arr.ndim)}
                if arr.ndim == 1 and tuple(arr.shape) == shape:
                    record["matching_vectors"].append(item)
                else:
                    record["rejected_vectors"].append(item)

        elif path.suffix == ".json":
            data = json.loads(path.read_text())
            for key in VECTOR_KEYS:
                if key not in data:
                    continue
                arr = np.asarray(data[key])
                item = {"key": key, "shape": list(arr.shape), "ndim": int(arr.ndim)}
                if arr.ndim == 1 and tuple(arr.shape) == shape:
                    record["matching_vectors"].append(item)
                else:
                    record["rejected_vectors"].append(item)
    except Exception as exc:
        record["error"] = repr(exc)

    return record

def bind_first_match(matches: List[Dict[str, object]], output_dir: Path) -> Optional[Dict[str, object]]:
    for match in matches:
        path = Path(str(match["path"]))
        vectors = match.get("matching_vectors", [])
        if not vectors:
            continue
        key = str(vectors[0]["key"])
        output = output_dir / "act_dr6_baseline_lcdm_prediction_vector_binding_candidate_from_probe.json"

        cmd = [
            "python3",
            str(HARNESS),
            "--candidate",
            str(path),
            "--output",
            str(output),
        ]
        if key != "npy_array":
            cmd.extend(["--key", key])

        result = subprocess.run(cmd, text=True, capture_output=True)
        return {
            "candidate": str(path),
            "key": key,
            "output": str(output),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "bound": result.returncode == 0 and output.exists(),
        }

    return None

def main() -> None:
    if not ORDER.exists():
        raise SystemExit(f"missing ordering certificate: {ORDER}")
    if not HARNESS.exists():
        raise SystemExit(f"missing binding harness: {HARNESS}")

    shape = required_shape()
    files = discover_files()
    inspected = [inspect_candidate(path, shape) for path in files]
    matches = [item for item in inspected if item["matching_vectors"]]

    bind_result = bind_first_match(matches, DEFAULT_OUTPUT.parent)

    result = {
        "id": "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE_RESULT",
        "status": "MATCHING_CANDIDATE_FOUND_AND_BOUND" if bind_result and bind_result.get("bound") else "NO_MATCHING_BASELINE_LCDM_VECTOR_CANDIDATE_FOUND",
        "required_prediction_vector_shape": list(shape),
        "files_scanned": len(files),
        "matching_candidate_count": len(matches),
        "matching_candidates": matches,
        "binding_result": bind_result,
        "does_not_prove": [
            "matched candidate is official",
            "matched candidate is physically correct",
            "baseline LCDM prediction vector is validated",
            "ACT DR6 residual eigenspace empirical comparison has been run",
            "DFM-MKC empirical validation",
            "Lambda-CDM failure"
        ]
    }

    DEFAULT_OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", DEFAULT_OUTPUT)
    print(result["status"])

if __name__ == "__main__":
    main()
